import requests
try:
    import matplotlib
except Exception as err:
    import traceback
    print(f"Failed to import matplotlib!\n\n\t{str(err)}")
    traceback.print_exc()
try:
    from pytrends.request import TrendReq
except Exception as err:
    import traceback
    print(f"Failed to import pytrends!\n\n\t{str(err)}")
    traceback.print_exc()

from datetime import date, timedelta

from .botcommand import BotCommand
from boterror import BotError
from botquery import BotQuery
from config import BASE_URL
from constants import SEND_PHOTO_ENDPOINT, PHOTO_KEY, CHAT_ID_KEY, NEW_LINE_CHAR, SPACE, UNDERSCORE, PARSE_MODE_KEY, UNDERSCORE, SPACE, EN_US_LOCALE, TIMEZONE_OFFSET_MINUTES

"""
Returns the associated response dictionary key w.r.t to a country's name
eg. United States -> united_states
    Canada -> canada
"""
def get_country_key(name: str):
    name_formatted = name.strip().replace(SPACE, UNDERSCORE).lower()
    if name_formatted == 'new_zealand':
        return 'new zealand' # For some reason, New Zealand is the only country without an underscore in the response
    if name_formatted in { 'us', 'usa', 'states', 'america' }: # For user convenience
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
        
        return current_date - timedelta(days=time * allowed_units_map[unit])
    except:
        raise BotError(f"Invalid argument '{time_delta_str}' for option '{TrendsCommand.TIME_FLAG}'")

"""
Validates the string 'year' is a valid year.
"""
def validate_year_str(year_str: str):
    if not year_str.isnumeric() or int(year_str) <= 0:
        raise BotError(f"Invalid year '{year_str}'")

"""
Formats a list of items into a newline-separated string with their rankings.
eg. ["Apple", "Banana", "Cherry"] -> 
    1. Apple
    2. Banana
    3. Cherry
"""
def format_list_items(data, key):
    return NEW_LINE_CHAR.join([ f"{i}. {item}" for i, item in enumerate(data[key], start=1) ])

"""
Gets the TrendsReq object from the pytrends library to start fetching trends data
"""
def get_trends_req():
    return TrendReq(hl=EN_US_LOCALE, tz=TIMEZONE_OFFSET_MINUTES)


class TrendsCommand(BotCommand):
    KEYWORDS_STR = 'keywords'
    GRAPH_FLAG = 'graph'
    HELP_FLAG = 'help'
    TIME_FLAG = '--time'
    TIME_FLAG_SHORT = '-t'
    TRENDING_FLAG = 'trending'
    TOP_FLAG = 'top'
    DEFAULT_TIME_DELTA = '12m'
    DEFAULT_TRENDING_LOCATION = 'united_states'
    TEMP_FIGURE_PATH = '/tmp/figure.png'

    @classmethod
    def get_help_text(cls):
        usage_text_graph = "1. Graphing mode - Graphs trends on a plot. `time` is in the format `<number><unit>`, where `unit` can be one of `d`, `w`, `m`, or `y` (default `12m`).\n/trends graph \[ -t <time> ] <keywords>"

        usage_text_top = "2. Top trends mode - Gets the top searches for a given year (default previous year)\n/trends top \[year]"
        
        usage_text_trending = "3. Trending mode - Gets the current trending searches (default US)\n/trends trending \[country]"

        return f"*Google Trends command help*\n\n{usage_text_graph}\n\n{usage_text_top}\n\n{usage_text_trending}"

    def execute(self):
        if self.skip_edited():
            return

        try:
            command_dict = self.parse_flags_and_keywords(self.command_arguments[1:])
            if self.HELP_FLAG in command_dict:
                self.handle_normal_query(self.get_help_text())
            elif self.TRENDING_FLAG in command_dict:
                self.execute_trending_searches(command_dict.get(self.TRENDING_FLAG) or self.DEFAULT_TRENDING_LOCATION)
            elif self.TOP_FLAG in command_dict:
                self.execute_top_searches(command_dict.get(self.TOP_FLAG) or str(date.today().year - 1))
            else:
                self.execute_graph(command_dict.get(self.GRAPH_FLAG))

        except BotError as err:
            self.handle_normal_query(f"Unable to fetch the trends: {str(err)}")
        except Exception as err:
            print(f"Unchecked exception in TrendsCommand:\n\t{str(err)}")
            self.handle_normal_query("Oops! Can't fetch trends right now.")

    def execute_graph(self, graph_data_dict):
        today = date.today()
        keywords = graph_data_dict[self.KEYWORDS_STR]

        if len(keywords) == 0:
            raise BotError("No keywords provided for graphing")
        
        time_difference_str = graph_data_dict.get(self.TIME_FLAG) or self.DEFAULT_TIME_DELTA
        
        initial_date = get_initial_date(today, time_difference_str)

        pytrend = get_trends_req()
        pytrend.build_payload(
            kw_list=keywords,
            cat=0,
            timeframe=f'{initial_date.isoformat()} {today.isoformat()}',
            gprop='')
        
        data = pytrend.interest_over_time()
        
        if data.empty:
            raise BotError("Not enough data to be shown")
        
        image = data.plot(title = f"Google Trends data ({time_difference_str})")
        image.set_xlabel("Time")
        image.set_ylabel("Interest")
        matplotlib.pyplot.gcf().subplots_adjust(bottom=0.15)

        fig = image.get_figure()
        fig.savefig(self.TEMP_FIGURE_PATH)

        self.handle_image_query(self.TEMP_FIGURE_PATH)

    def execute_trending_searches(self, location):
        try:
            pytrend = get_trends_req()
            data = pytrend.trending_searches(pn=location)
            self.handle_normal_query(f"Current trending searches ({location.replace(UNDERSCORE, SPACE).title()}):{NEW_LINE_CHAR}{NEW_LINE_CHAR}{format_list_items(data, 0)}")
        except KeyError:
            location = location.replace(UNDERSCORE, SPACE)
            raise BotError(f"There's no trending searches in '{location}'")
        except Exception:
            location = location.replace(UNDERSCORE, SPACE)
            raise BotError(f"Could not get trending searches for '{location}'")

    def execute_top_searches(self, year):
        try:
            validate_year_str(year)
            pytrend = get_trends_req()
            data = pytrend.top_charts(year, hl=EN_US_LOCALE, tz=TIMEZONE_OFFSET_MINUTES, geo='GLOBAL')
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
                print(f"the {SEND_PHOTO_ENDPOINT} response was not ok. Code: {res.status_code}\n\t{res.text}")

    def parse_flags_and_keywords(self, arguments):
        arg_len = len(arguments)
        if arg_len == 0:
            raise BotError("No mode provided. Use '/trends help' for more info")

        mode = arguments[0].lower()
        result = dict()

        if mode == self.GRAPH_FLAG: 
            result[self.GRAPH_FLAG] = dict()
            keywords = []
            i = 1
            while i < len(arguments):
                arg = arguments[i].lower()
                if arg == self.TIME_FLAG or arg == self.TIME_FLAG_SHORT:
                    try:
                        result[self.GRAPH_FLAG][self.TIME_FLAG] = arguments[i+1]
                        i += 1
                    except:
                        raise BotError(f"No argument provided for option '{arguments[i]}'")
                else:
                    keywords.append(arguments[i])
                i += 1
            result[self.GRAPH_FLAG][self.KEYWORDS_STR] = keywords
        elif mode == self.TOP_FLAG:
            result[self.TOP_FLAG] = arguments[1] if arg_len > 1 else None
        elif mode == self.TRENDING_FLAG:
            result[self.TRENDING_FLAG] = get_country_key(arguments[1]) if arg_len > 1 else None
        elif mode == self.HELP_FLAG:
            result[self.HELP_FLAG] = None
        else:
            raise BotError(f"Unknown mode '{arguments[0]}'")
        return result

    def format_response_json(self):
        self.response_json[PARSE_MODE_KEY] = "Markdown"
