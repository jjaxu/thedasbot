import requests

from constants import PARSE_MODE_KEY, EDIT_MESSAGE_ENDPOINT, ASCII_ALPHABET_OFFSET
from config import BASE_URL
from .botcommand import BotCommand
from boterror import BotError
from botquery import BotQuery
from trivia import Trivia, TRIVIA_BASE_ERROR_MESSAGE

class TriviaCommand(BotCommand):
    def __init__(self, query, command_arguments=None):
        super().__init__(query, command_arguments)
        self.trivia = None

    def execute(self):
        if self.query.has_callback_query: # user answered a previous question
            self.execute_question_answered()
        else: # user requests a new question
            self.execute_get_new_question()

    def execute_get_new_question(self):
        category = None
        difficulty = None

        if len(self.command_arguments) > 1:
            category = self.command_arguments[1]
            if category.lower() == "help":
                self.handle_normal_query(Trivia.get_help_text())
                return
                
            if len(self.command_arguments) > 2:
                difficulty = self.command_arguments[2]

        try:
            self.trivia = Trivia.fetch_question(category, difficulty)
        except BotError as bot_err:
            print(f"TriviaCommand Error (Checked):\n\t{bot_err}")
            self.handle_normal_query(str(bot_err))
        except Exception as err:
            print(f"TriviaCommand Error (Unchecked):\n\t{err}")
            self.handle_normal_query(TRIVIA_BASE_ERROR_MESSAGE)
        else:
            self.handle_normal_query(self.trivia.formatted_response())

    def execute_question_answered(self):
        self.handle_callback_query()

    def format_response_json(self):
        self.response_json[PARSE_MODE_KEY] = "Markdown"

        if not self.trivia:
            return

        # Find the letter of the correct answer from its index. 0 -> A, 1 -> B, 2 -> C and 3 -> D
        correct_ans = chr(self.trivia.correct_answer_index() + ASCII_ALPHABET_OFFSET)

        # Formats the payload of the multiple choice buttons as "<chosen_answer><correct_answer>/trivia" so it can be processed when the user clicks it
        buttons = [
            { 
                "text": char,
                "callback_data": f"{char}{correct_ans}/trivia" 
            }
            for char in ["A", "B", "C", "D"]
        ]

        self.response_json["reply_markup"] = {
            "inline_keyboard": [
                [
                    buttons[0],
                    buttons[1]
                ],
                [
                    buttons[2],
                    buttons[3]
                ]
            ]
        }

    def handle_callback_query(self):
        try:
            given_answer = self.query.callback_query.callback_data[0]
            correct_answer = self.query.callback_query.callback_data[1]
            if given_answer == correct_answer:
                result_text = f"*{given_answer}* is correct!"
            else:
                result_text = f"*{given_answer}* is incorrect! The correct answer is *{correct_answer}*"
        except Exception as err:
            print(f"Error occured while handling trivia callback\n\t{err}")
            return

        url = f"{BASE_URL}/{EDIT_MESSAGE_ENDPOINT}"
        response_json = {
            "chat_id": self.query.callback_query.chat_id,
            "message_id": self.query.callback_query.message_id,
            "text": f"{self.query.callback_query.message}\n\n{result_text}",
            "reply_markup": {
                "inline_keyboard": [],
            },
            "parse_mode": "Markdown"
        }

        response = requests.post(url, json=response_json)
        if not response.ok:
            print(f"Error occured while sending trivia results back\n\t{response.text}")
