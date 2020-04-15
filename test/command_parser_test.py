import unittest, setup

from commands.start_command import StartCommand
from commands.help_command import HelpCommand
from commands.joke_command import JokeCommand
from commands.fact_command import FactCommand
from commands.trivia_command import TriviaCommand
from commands.invalid_command import InvalidCommand
from commands.command_parser import CommandParser

from botquery import BotQuery

class CommandParserTest(unittest.TestCase):
    def test_start_command(self):
        query = BotQuery()
        query.message = " /start 123 "
        result = CommandParser.parse_command(query)
        self.assertIsInstance(result, StartCommand)
        self.assertIs(query, result.query)

    def test_help_command(self):
        query = BotQuery()
        query.message = " /help me"
        result = CommandParser.parse_command(query)
        self.assertIsInstance(result, HelpCommand)
        self.assertIs(query, result.query)
    
    def test_joke_command(self):
        query = BotQuery()
        query.message = "/JOke 1234"
        result = CommandParser.parse_command(query)
        self.assertIsInstance(result, JokeCommand)
        self.assertIs(query, result.query)

    def test_fact_command(self):
        query = BotQuery()
        query.message = " /FACT     "
        result = CommandParser.parse_command(query)
        self.assertIsInstance(result, FactCommand)
        self.assertIs(query, result.query)

    def test_trivia_command(self):
        query = BotQuery()
        query.message = " /trivia     "
        result = CommandParser.parse_command(query)
        self.assertIsInstance(result, TriviaCommand)
        self.assertIs(query, result.query)

    def test_empty_command(self):
        query = BotQuery()
        query.message = "/"
        result = CommandParser.parse_command(query)
        self.assertIsInstance(result, InvalidCommand)

    def test_none(self):
        query = BotQuery()
        query.message = None
        result = CommandParser.parse_command(query)
        self.assertIsInstance(result, InvalidCommand)

    def test_empty_string(self):
        query = BotQuery()
        query.message = ""
        result = CommandParser.parse_command(query)
        self.assertIsInstance(result, InvalidCommand)

    def test_unrecognized_command(self):
        query = BotQuery()
        query.message = "/badcommand"
        result = CommandParser.parse_command(query)
        self.assertIsInstance(result, InvalidCommand)

    def test_unrecognized_command_substring(self):
        query = BotQuery()
        query.message = "/starts"
        result = CommandParser.parse_command(query)
        self.assertIsInstance(result, InvalidCommand)

    def test_not_a_command(self):
        query = BotQuery()
        query.message = "hello there"
        result = CommandParser.parse_command(query)
        self.assertIsInstance(result, InvalidCommand)
