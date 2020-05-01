import matplotlib
import requests
import pandas as pd
from pytrends.request import TrendReq
from datetime import date, timedelta

from .botcommand import BotCommand
from boterror import BotError
from botquery import BotQuery
from config import BASE_URL
from constants import SEND_PHOTO_ENDPOINT, PHOTO_KEY, CHAT_ID_KEY, NEW_LINE_CHAR, SPACE, UNDERSCORE

"""
returns the associated response dictionary key w.r.t to a country's name
eg. United States -> united_states
    canada -> Canada
"""
def get_country_key(name: str):
    name_formatted = name.strip().replace(SPACE, UNDERSCORE).lower()
    if name_formatted == 'new_zealand':
        return 'new zealand' # For some reason, New Zealand is the only country without an underscore in the response
    if name_formatted in { 'us', 'usa', 'states', 'america' }:
        return 'united_states'
    return name_formatted

"""
Calculates the day time_delta units away from the given date.
time_delta_str should be in the format '<number><unit>' where number is a positive integer and unit is one of d, w, m or y
"""
def get_initial_date(current_date: date, time_delta_str: str):
    allowed_units_map = {
        'd': 1,
        'w': 7,
        'm': 30,
        'y': 365
    }

    try:
        unit = time_delta_str[-1]
        time = int(time_delta_str[:-1])
        time_difference = None
        
        return current_date - timedelta(days=time * allowed_units_map[unit])
    except:
        raise BotError(f"Invalid argument '{time_delta_str}' for option '{TrendsCommand.TIME_FLAG}'")

"""
Validates the string 'year' is a valid year. 'year' should be in the form of 'YYYY'
"""
def validate_year_str(year_str: str):
    try:
        year = int(year_str)
        if year < 0:
            raise
    except:
        raise BotError(f"Invalid year '{year}'")

"""
Formats a list of items into a newline-separated string with their rankings.
eg. ["Apple", "Banana", "Cherry"] -> 
    1. Apple
    2. Banana
    3. Cherry
"""
def format_list_items(data, key):
    return NEW_LINE_CHAR.join([ f"{i}. {item}" for i, item in enumerate(data[key], start=1) ])

class TrendsCommand(BotCommand):
    KEYWORDS_STR = 'keywords'
    TIME_FLAG = '--time'
    TRENDING_TAG = '--trending'
    TOP_TAG = '--top'
    DEFAULT_TIME_DELTA = '12m'
    DEFAULT_TRENDING_LOCATION = 'united_states'
    FIGURE_NAME = 'figure.png'

    @classmethod
    def get_help_text(cls):
        pass

    def execute(self):
        if self.skip_edited():
            return

        try:
            command_dict = self.parse_flags_and_keywords(self.command_arguments[1:])

            if self.TRENDING_TAG in command_dict:
                self.execute_trending_searches(command_dict.get(self.TRENDING_TAG) or self.DEFAULT_TRENDING_LOCATION)
            elif self.TOP_TAG in command_dict:
                self.execute_top_searches(command_dict.get(self.TOP_TAG) or str(date.today().year - 1))
            else:
                self.execute_compare(command_dict)

        except BotError as err:
            self.handle_normal_query(f"Unable to fetch the trends: {str(err)}")
        except Exception as err:
            print(f"Unchecked exception in TrendsCommand:\n\t{str(err)}")
            import traceback
            traceback.print_exc()
            self.handle_normal_query("Oops! Can't fetch trends right now.")

    def execute_compare(self, command_dict):
        today = date.today()
        keywords = command_dict[self.KEYWORDS_STR]

        if len(keywords) == 0:
            raise BotError("No keywords provided")
        
        time_difference_str = command_dict.get(self.TIME_FLAG) or self.DEFAULT_TIME_DELTA
        
        initial_date = get_initial_date(today, time_difference_str)

        pytrend = TrendReq(hl="en-US", tz=360)
        pytrend.build_payload(
            kw_list=keywords,
            cat=0,
            timeframe=f'{initial_date.isoformat()} {today.isoformat()}',
            gprop='')
        
        data = pytrend.interest_over_time()
        
        if data.empty:
            raise BotError("Not enough data to be shown")
        
        # data.drop(labels=['isPartial'],axis='columns', inplace=True)
        image = data.plot(title = f"Google Trends data ({time_difference_str})")
        image.set_xlabel("Time")
        image.set_ylabel("Interest")
        matplotlib.pyplot.gcf().subplots_adjust(bottom=0.15)

        fig = image.get_figure()
        fig.savefig(self.FIGURE_NAME)

        self.handle_image_query(self.FIGURE_NAME)

    def execute_trending_searches(self, location):
        try:
            pytrend = TrendReq(hl="en-US", tz=360)
            data = pytrend.trending_searches(pn=location) # united_states
            self.handle_normal_query(f"Current trending searches ({location.replace(UNDERSCORE, SPACE).title()}):{NEW_LINE_CHAR}{NEW_LINE_CHAR}{format_list_items(data, 0)}")
        except KeyError:
            raise BotError(f"There's no trending searches in '{location}'")
        except Exception:
            raise BotError(f"Could not get trending searches for '{location}'")

    def execute_top_searches(self, year):
        try:
            validate_year_str(year)
            pytrend = TrendReq(hl="en-US", tz=360)
            data = pytrend.top_charts(year, hl='en-US', tz=300, geo='GLOBAL')
            self.handle_normal_query(f"Top searches of {year}:{NEW_LINE_CHAR}{NEW_LINE_CHAR}{format_list_items(data, 'title')}")
        except BotError:
            raise
        except Exception:
            raise BotError(f"Could not get top searches for '{year}'")


    def handle_image_query(self, img_name):
        with open(img_name, 'rb') as input_file:
            self.response_json = {
                CHAT_ID_KEY: self.query.chat_id
            }
        
            url = f"{BASE_URL}/{SEND_PHOTO_ENDPOINT}"
            res = requests.post(url, data=self.response_json, files = {'photo': input_file})
            if not res.ok:
                print(f"sendPhoto did not complete successfully. Code: {res.status_code}\n\t{res.text}")

    def parse_flags_and_keywords(self, arguments):
        keywords = []
        result = dict()
        i = 0
        while i < len(arguments):
            if arguments[i] == self.TIME_FLAG:
                try:
                    result[self.TIME_FLAG] = arguments[i+1]
                    i += 1
                except:
                    raise BotError(f"No arguments provided for option '{self.TIME_FLAG}'")
            elif arguments[i] == self.TOP_TAG:
                if i == len(arguments) - 1:
                    result[self.TOP_TAG] = None
                else:
                    result[self.TOP_TAG] = arguments[i+1]
                    i += 1
            elif arguments[i] == self.TRENDING_TAG:
                if i == len(arguments) - 1:
                    result[self.TRENDING_TAG] = None
                else:
                    result[self.TRENDING_TAG] = get_country_key(arguments[i+1])
                    i += 1
            else:
                keywords.append(arguments[i])
            i += 1

        result[self.KEYWORDS_STR] = keywords
        return result
        