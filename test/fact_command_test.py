import unittest, setup

from unittest.mock import patch, Mock

from commands.fact_command import FactCommand
from botquery import BotQuery

class FactCommandTest(unittest.TestCase):
    def test_successful_request(self):
        query = BotQuery()
        fact_command = FactCommand(query)
        fact_command.handle_normal_query = Mock()
        with patch("commands.fact_command.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json = lambda: [{"headline": "my fact", "primaryImage": "my_url"}]
            fact_command.execute()
            fact_command.handle_normal_query.assert_called_once_with(
                '<a href="my_url">&#x200b;</a>my fact'
            )

    def test_fail_not_ok(self):
        query = BotQuery()
        fact_command = FactCommand(query)
        fact_command.handle_normal_query = Mock()
        with patch("commands.fact_command.requests.get") as mock_get:
            with patch("commands.fact_command.print") as mock_print:
                mock_get.return_value.ok = False
                fact_command.execute()
                fact_command.handle_normal_query.assert_called_once_with("Oops! Can't fetch fact right now.")
                self.assertFalse(mock_print.called)

    def test_fail_exception(self):
        query = BotQuery()
        fact_command = FactCommand(query)
        fact_command.handle_normal_query = Mock()
        with patch("commands.fact_command.requests.get", side_effect=Exception("Fact server is down")) as mock_get:
            with patch("commands.fact_command.print") as mock_print:
                fact_command.execute()
                self.assertTrue(mock_print.called)
                fact_command.handle_normal_query.assert_called_once_with("Oops! Can't fetch fact right now.")
