import unittest, setup

from unittest.mock import patch, Mock

from commands.joke_command import JokeCommand
from botquery import BotQuery

class JokeCommandTest(unittest.TestCase):
    def test_successful_request(self):
        query = BotQuery()
        joke_command = JokeCommand(query)
        joke_command.handle_normal_query = Mock()

        with patch("commands.joke_command.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.content = b"Dad joke here!"
            joke_command.execute()
            joke_command.handle_normal_query.assert_called_once_with("Dad joke here!")

    def test_fail_not_ok(self):
        query = BotQuery()
        joke_command = JokeCommand(query)
        joke_command.handle_normal_query = Mock()
        with patch("commands.joke_command.requests.get") as mock_get:
            mock_get.return_value.ok = False
            joke_command.execute()
            joke_command.handle_normal_query.assert_called_once_with("Oops! Can't fetch joke right now.")

    def test_fail_throw_exception(self):
        query = BotQuery()
        joke_command = JokeCommand(query)
        joke_command.handle_normal_query = Mock()
        with patch("commands.joke_command.requests.get", side_effect=Exception("Joke server is down")):
            with patch("commands.joke_command.print") as mock_print: # Supressing printing side effects
                joke_command.execute()
                self.assertTrue(mock_print.called)
                joke_command.handle_normal_query.assert_called_once_with("Oops! Can't fetch joke right now.")
