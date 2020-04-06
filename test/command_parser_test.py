import unittest
import setup

from commands import CommandParser, StartCommand, HelpCommand
from botquery import BotQuery

class CommandParserTest(unittest.TestCase):
    def test_start_command(self):
        query = BotQuery()
        query.message = " /start 123 "
        result = CommandParser.parse_command(query)
        self.assertIsInstance(result, StartCommand)
        self.assertIs(query, result.query)
        self.assertEqual(result.command, "start")

    def test_help_command(self):
        query = BotQuery()
        query.message = " /help me"
        result = CommandParser.parse_command(query)
        self.assertIsInstance(result, HelpCommand)
        self.assertIs(query, result.query)
        self.assertEqual(result.command, "help")

    def test_empty_command(self):
        query = BotQuery()
        query.message = "/"
        result = CommandParser.parse_command(query)
        self.assertIsNone(result)

    def test_none(self):
        query = BotQuery()
        query.message = None
        result = CommandParser.parse_command(query)
        self.assertIsNone(result)

    def test_empty_string(self):
        query = BotQuery()
        query.message = ""
        result = CommandParser.parse_command(query)
        self.assertIsNone(result)

    def test_unrecognized_command(self):
        query = BotQuery()
        query.message = "/badcommand"
        result = CommandParser.parse_command(query)
        self.assertIsNone(result)

    def test_unrecognized_command_substring(self):
        query = BotQuery()
        query.message = "/starts"
        result = CommandParser.parse_command(query)
        self.assertIsNone(result)

    def test_not_a_command(self):
        query = BotQuery()
        query.message = "hello there"
        result = CommandParser.parse_command(query)
        self.assertIsNone(result)
