from html import unescape
from boterror import BotError

import requests

TRIVIA_BASE_URL = "https://opentdb.com/"
TRIVIA_BASE_ERROR_MESSAGE = "Failed to fetch trivia question!"

def fetchCategories():
    res = requests.get(TRIVIA_BASE_URL + "api_category.php")
    if not res.ok:
        return dict()
    return res.json()

class Trivia:
    category_dict = fetchCategories()
    difficulty_list = ["easy", "medium", "hard"]

    @classmethod
    def getHelpText(cls) -> str:
        category_list = [("\* " + item["name"]) for item in (cls.category_dict.get("trivia_categories") or [])]
        difficulty_list = [("\* " + item.capitalize()) for item in cls.difficulty_list]
        return "Usage: */trivia [category] [difficulty]*\n\n*Categories:*\n{}\n\n*Difficulties:*\n{}".format("\n".join(category_list), "\n".join(difficulty_list))

    @classmethod
    def getCategoryId(cls, category_name: str) -> int:
        if not category_name or category_name.lower() == "any": return 0
        category_lower = category_name.lower()
        if category_lower == "help":
            raise BotError(cls.getHelpText())

        for category in cls.category_dict.get("trivia_categories") or []:
            name = category["name"].lower()
            if category_name.lower().strip() in name:
                return int(category["id"])
        raise BotError("{} No category associated with '{}'".format(TRIVIA_BASE_ERROR_MESSAGE, category_name))
    
    @classmethod
    def getDifficulty(cls, difficulty: str) -> str:
        if not difficulty or difficulty.lower() == "any": return None
        difficulty = difficulty.lower()
        if difficulty not in cls.difficulty_list:
            raise BotError("{} No difficulty associated with '{}'".format(TRIVIA_BASE_ERROR_MESSAGE, difficulty))
        return difficulty

    def __init__(self, category, difficulty):
        category_id = self.getCategoryId(category)
        difficulty = self.getDifficulty(difficulty)

        params = {
            "amount": 1,
            "type": "multiple"
        }

        if category_id != 0:
            params["category"] = category_id
        
        if difficulty:
            params["difficulty"] = difficulty
        
        r = requests.get("https://opentdb.com/api.php", params=params)
        if not r.ok:
            raise BotError(TRIVIA_BASE_ERROR_MESSAGE)
        
        json_response = r.json()
        if json_response["response_code"] != 0:
            raise BotError(TRIVIA_BASE_ERROR_MESSAGE)

        r = json_response["results"][0]
        self.category = unescape(r["category"])
        self.type = unescape(r["type"])
        self.difficulty = unescape(r["difficulty"])
        self.question = unescape(r["question"])
        self.correct_answer = unescape(r["correct_answer"])
        self.answers = list(map(lambda item: unescape(item), r["incorrect_answers"]))
        self.answers.append(self.correct_answer)
        self.answers.sort()

    def question(self):
        return self.question

    def answers(self):
        return self.answers

    def formatted_response(self):
        offset = 65
        res = "*Category* - {}\n".format(self.category)
        res += "*Difficulty* - {}\n\n".format(self.difficulty.capitalize())
        res += "_{}_\n\n".format(self.question)
        for i, ans in enumerate(self.answers):
            res += "{}. {}\n".format(chr(i + offset), ans)
        return res

    def correct_answer_index(self):
        return self.answers.index(self.correct_answer)
