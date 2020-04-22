from html import unescape
from boterror import BotError

import requests

TRIVIA_BASE_URL = "https://opentdb.com"
TRIVIA_BASE_ERROR_MESSAGE = "Failed to fetch trivia question!"
RESPONSE_CODE_STR = "response_code"
RESULTS_STR = "results"

class Trivia:
    category_dict = dict()
    difficulty_list = ["easy", "medium", "hard"]

    @classmethod
    def get_category_dict(cls):
        if not cls.category_dict:
            try:
                res = requests.get(f"{TRIVIA_BASE_URL}/api_category.php")
                if res.ok:
                    cls.category_dict = res.json()
            except Exception as err:
                print(f"Failed to fetch trivia categories\n\t{str(err)}")
        return cls.category_dict

    @classmethod
    def get_help_text(cls) -> str:
        category_list = [("\* " + item["name"]) for item in (cls.get_category_dict().get("trivia_categories", []))]
        difficulty_list = [("\* " + item.capitalize()) for item in cls.difficulty_list]
        nl = '\n'
        return f"Usage: */trivia [category] [difficulty]*\n\n*Categories:*\n{nl.join(category_list)}\n\n*Difficulties:*\n{nl.join(difficulty_list)}"

    @classmethod
    def get_category_id(cls, category_name: str) -> int:
        if not category_name or category_name.lower() == "any":
            return 0
        
        category_lower = category_name.lower()

        for category in cls.get_category_dict().get("trivia_categories", []):
            name = category["name"].lower()
            if category_name.lower().strip() in name:
                return int(category["id"])
        raise BotError(f"{TRIVIA_BASE_ERROR_MESSAGE} No category associated with '{category_name}'")
    
    @classmethod
    def get_difficulty(cls, difficulty: str) -> str:
        if not difficulty or difficulty.lower() == "any": return None
        difficulty_lower = difficulty.lower()
        if difficulty_lower not in cls.difficulty_list:
            raise BotError(f"{TRIVIA_BASE_ERROR_MESSAGE} No difficulty associated with '{difficulty}'")
        return difficulty_lower

    @classmethod
    def fetch_question(cls, category=None, difficulty=None):
        category_id = cls.get_category_id(category)
        difficulty = cls.get_difficulty(difficulty)

        params = {
            "amount": 1,
            "type": "multiple"
        }

        if category_id != 0:
            params["category"] = category_id
        
        if difficulty:
            params["difficulty"] = difficulty
        
        try:
            response = requests.get(f"{TRIVIA_BASE_URL}/api.php", params=params)
            if not response.ok:
                print("Trivia API call did not give an ok (200) response")
                raise BotError(f"{TRIVIA_BASE_ERROR_MESSAGE}")
            
            json_response = response.json()
            if RESPONSE_CODE_STR not in json_response or json_response[RESPONSE_CODE_STR] != 0 or \
                RESULTS_STR not in json_response or len(json_response[RESULTS_STR]) == 0:
                print("Invalid trivia json response, parsing aborted")
                raise BotError(f"{TRIVIA_BASE_ERROR_MESSAGE}")
            
            response = json_response[RESULTS_STR][0]

            result = Trivia()
            result.category = unescape(response["category"])
            result.type = unescape(response["type"])
            result.difficulty = unescape(response["difficulty"])
            result.question = unescape(response["question"])
            result.correct_answer = unescape(response["correct_answer"])
            result.answers = list(map(lambda item: unescape(item), response["incorrect_answers"]))
            result.answers.append(result.correct_answer)
            result.answers.sort()

            return result

        except Exception as err:
            print(f"Trivia fetchQuestion error\n\t{str(err)}")
            raise BotError(err)
    
    def __init__(self):
        self.category = None
        self.type = None
        self.difficulty = None
        self.question = None
        self.correct_answer = None
        self.answers = None

    def formatted_response(self):
        offset = 65
        res = f"*Category* - {self.category}\n"
        res += f"*Difficulty* - {self.difficulty.capitalize()}\n\n"
        res += f"_{self.question}_\n\n"
        for i, ans in enumerate(self.answers):
            res += f"{chr(i + offset)}. {ans}\n"
        return res

    def correct_answer_index(self):
        return self.answers.index(self.correct_answer)
