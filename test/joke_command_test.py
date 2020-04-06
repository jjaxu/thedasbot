import unittest
import setup

from unittest.mock import patch

from commands import JokeCommand
from botquery import BotQuery

class HelpCommandTest(unittest.TestCase):
    def test_successful_simple(self):
        query = BotQuery()
        joke_command = JokeCommand(query)
        with patch("commands.JokeCommand.execute", return_value="Your joke") as mock_execute:
            self.assertEqual(joke_command.execute(), "Your joke")

    def test_successful_request(self):
        query = BotQuery()
        joke_command = JokeCommand(query)
        with patch("commands.joke_command.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.content = b"Dad joke here!"
            self.assertEqual(joke_command.execute(), "Dad joke here!")


    def test_fail_not_ok(self):
        query = BotQuery()
        joke_command = JokeCommand(query)
        with patch("commands.joke_command.requests.get") as mock_get:
            mock_get.return_value.ok = False
            self.assertEqual(joke_command.execute(), "Oops! Can't fetch joke right now.")


    def test_fail_throw_exception(self):
        query = BotQuery()
        joke_command = JokeCommand(query)
        with patch("commands.joke_command.requests.get", side_effect=Exception("Joke server is down")):
            with patch("commands.joke_command.print"): # Supressing printing side effects
                self.assertEqual(joke_command.execute(), "Oops! Can't fetch joke right now.")
