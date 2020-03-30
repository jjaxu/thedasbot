from html import unescape
import requests


def fetchCategories():
    res = requests.get("https://opentdb.com/api_category.php")
    if not res.ok:
        return dict()
    return res.json()

class Trivia(object):
    category_ids = fetchCategories()

    @classmethod
    def getCategoryId(cls, category_name: str) -> int:
        if category_name.lower() == "any":
            return "any"
        for category in cls.category_ids.get("trivia_categories") or []:
            name = category["name"].lower()
            if category_name.lower().strip() in name:
                return int(category["id"])

    def __init__(self, json_response):
        if json_response["response_code"] != 0:
            raise RuntimeError("Bad Trivia Response")

        r = json_response["results"][0]
        print(r)
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
        res = "Category - {}\n".format(self.category.capitalize())
        res += "Difficulty - {}\n\n".format(self.difficulty.capitalize())
        res += self.question + "\n\n"
        for i, ans in enumerate(self.answers):
            res += "{}. {}\n".format(chr(i + offset), ans)
        return res

    def correct_answer_index(self):
        return self.answers.index(self.correct_answer)
