import unittest, setup

from unittest.mock import patch, Mock

from trivia import Trivia
from commands.trivia_command import TriviaCommand
from commands.botcommand import BotCommand
from botquery import BotQuery
from boterror import BotError

class TriviaCommandTest(unittest.TestCase):
    def test_trivia_get_category_dict(self):
        with patch("trivia.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json = lambda: {"cat1": 1, "cat2:": 2}
            self.assertEqual(Trivia.category_dict, dict())

            # Fetch categories
            Trivia.get_category_dict()
            self.assertEqual(Trivia.category_dict, {"cat1": 1, "cat2:": 2})

            # Already fetched
            Trivia.get_category_dict()
            self.assertEqual(Trivia.category_dict, {"cat1": 1, "cat2:": 2})

    def test_trivia_get_category_id_valid(self):
        return_val = {
            "trivia_categories": [
                {
                    "name": "cat1",
                    "id": 1
                },
                {
                    "name": "cat2",
                    "id": 2
                },
                {
                    "name": "cat3",
                    "id": 3
                }
            ]
        }

        with patch("trivia.Trivia.get_category_dict", return_value=return_val) as mock_dict:
            self.assertEqual(Trivia.get_category_id("cat1"), 1)
            self.assertEqual(Trivia.get_category_id("cat2"), 2)
            self.assertEqual(Trivia.get_category_id("cat3"), 3)
            self.assertEqual(Trivia.get_category_id("cAT1  "), 1)
            self.assertEqual(Trivia.get_category_id("  CaT2"), 2)
            self.assertEqual(Trivia.get_category_id("   cAt3   "), 3)

            self.assertEqual(Trivia.get_category_id("Any"), 0)
            self.assertEqual(Trivia.get_category_id(None), 0)
            self.assertEqual(Trivia.get_category_id(""), 0)
            
    def test_trivia_get_category_id_invalid(self):
        return_val = {
            "trivia_categories": [
                {
                    "name": "science",
                    "id": 1
                }
            ]
        }

        with patch("trivia.Trivia.get_category_dict", return_value=return_val) as mock_dict:
            self.assertEqual(Trivia.get_category_id("Science"), 1)
            self.assertRaises(BotError, Trivia.get_category_id, "bad")

    def test_trivia_fetch_question_valid(self):
        question_json = {
            "response_code":0,
            "results":[
                {
                    "category":"cat1",
                    "type":"multiple",
                    "difficulty":"easy",
                    "question":"What is the first letter of the alphabet?",
                    "correct_answer":"A",
                    "incorrect_answers":[
                        "D",
                        "C",
                        "B"
                    ]
                }
            ]
        }

        with patch("trivia.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json = lambda: question_json

            question = Trivia.fetch_question()
            self.assertEqual(question.category, "cat1")
            self.assertEqual(question.type, "multiple")
            self.assertEqual(question.difficulty, "easy")
            self.assertEqual(question.question, "What is the first letter of the alphabet?")
            self.assertEqual(question.correct_answer, "A")
            self.assertListEqual(question.answers, ["A", "B", "C", "D"])

    @patch("trivia.print")
    def test_trivia_fetch_question_invalid_not_ok(self, _):
        question_json = {
            "response_code":1,
            "results":[]
        }

        with patch("trivia.requests.get") as mock_get:
            mock_get.return_value.ok = False
            self.assertRaises(BotError, Trivia.fetch_question)

    @patch("trivia.print")
    def test_trivia_fetch_question_invalid_bad_json(self, _):
        question_json_1 = dict()

        question_json_2 = {
            "response_code":1,
            "results":[]
        }

        question_json_3 = {
            "response_code":0,
        }

        question_json_4 = {
            "response_code":0,
            "results":[]
        }

        with patch("trivia.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json = lambda: question_json_1
            self.assertRaises(BotError, Trivia.fetch_question)
    
        with patch("trivia.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json = lambda: question_json_2
            self.assertRaises(BotError, Trivia.fetch_question)

        with patch("trivia.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json = lambda: question_json_3
            self.assertRaises(BotError, Trivia.fetch_question)

        with patch("trivia.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json = lambda: question_json_4
            self.assertRaises(BotError, Trivia.fetch_question)
  
    def test_trivia_help_text(self):
        query = BotQuery()
        trivia_command = TriviaCommand(query, ["/trivia", "help"])

        with patch("trivia.Trivia.get_help_text", return_value="help text"):
            trivia_command.handle_normal_query = Mock() 
            trivia_command.execute()
            trivia_command.handle_normal_query.assert_called_once_with("help text")

    def test_trivia_fetch_question_success(self):
        query = BotQuery()
        trivia_command = TriviaCommand(query, ["/trivia"])
        trivia_mock = Trivia()
        trivia_mock.formatted_response = lambda: "trivia question"

        with patch("trivia.Trivia.fetch_question", return_value=trivia_mock):
            trivia_command.handle_normal_query = Mock() 
            trivia_command.execute()
            trivia_command.handle_normal_query.assert_called_once_with("trivia question")

    @patch("commands.trivia_command.print")
    def test_trivia_fetch_question_fail(self, _):
        query = BotQuery()
        trivia_command = TriviaCommand(query, ["/trivia"])

        with patch("trivia.Trivia.fetch_question", side_effect=Exception("trivia error")):
            trivia_command.handle_normal_query = Mock() 
            trivia_command.execute()
            trivia_command.handle_normal_query.assert_called_once_with("trivia error")

    def test_trivia_callback_query(self):
        query = BotQuery()
        query.has_callback_query = True

        trivia_command = TriviaCommand(query)
        trivia_command.handle_callback_query = Mock()

        trivia_command.execute()
        trivia_command.handle_callback_query.assert_called_once()

    def test_trivia_callback_query_incorrect(self):
        query = BotQuery()
        query.has_callback_query = True
        query.callback_query = BotQuery()
        query.callback_query.callback_data = "AD/trivia"
        trivia_command = TriviaCommand(query)

        with patch("commands.trivia_command.requests.post") as mock_post:
            trivia_command.execute()
            response_text = mock_post.call_args[1]["json"]["text"]
            self.assertTrue(response_text.endswith("*A* is incorrect! The correct answer is *D*"))

    def test_trivia_callback_query_correct(self):
        query = BotQuery()
        query.has_callback_query = True
        query.callback_query = BotQuery()
        query.callback_query.callback_data = "CC/trivia"
        trivia_command = TriviaCommand(query)

        with patch("commands.trivia_command.requests.post") as mock_post:
            trivia_command.execute()
            response_text = mock_post.call_args[1]["json"]["text"]
            self.assertTrue(response_text.endswith("*C* is correct!"))
