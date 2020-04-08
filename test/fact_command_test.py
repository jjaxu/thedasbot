import unittest
import setup

from unittest.mock import patch

from commands import FactCommand
from botquery import BotQuery

class FactCommandTest(unittest.TestCase):
    def test_successful_simple(self):
        query = BotQuery()
        fact_command = FactCommand(query)
        with patch("commands.FactCommand.execute", return_value="your fact"):
            self.assertEqual(fact_command.execute(), "your fact")

    def test_successful_request(self):
        query = BotQuery()
        fact_command = FactCommand(query)
        with patch("commands.fact_command.requests.get") as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json = lambda: [{"headline": "my fact"}]
            self.assertEqual(fact_command.execute(), "my fact")

    def test_fail_not_ok(self):
        query = BotQuery()
        fact_command = FactCommand(query)
        with patch("commands.fact_command.requests.get") as mock_get:
            mock_get.return_value.ok = False
            self.assertEqual(fact_command.execute(), "Oops! Can't fetch fact right now.")

    def test_fail_exception(self):
        query = BotQuery()
        fact_command = FactCommand(query)
        with patch("commands.fact_command.requests.get", side_effect=Exception("Fact server is down")) as mock_get:
            with patch("commands.fact_command.print"):
                self.assertEqual(fact_command.execute(), "Oops! Can't fetch fact right now.")
