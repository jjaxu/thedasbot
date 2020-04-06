import unittest
import setup

from commands import HelpCommand
from botquery import BotQuery

class HelpCommandTest(unittest.TestCase):
    def test_private_chat(self):
        query = BotQuery()
        query.is_private = True
        query.user_first_name = "Lambda"
        help_command = HelpCommand(query)
        self.assertIs(help_command.query, query)
        self.assertEqual(help_command.command, "help")
        self.assertEqual(help_command.execute(),  "You have invoked the help command!")

    def test_group_chat(self):
        query = BotQuery()
        query.is_group = True
        query.user_first_name = "Foobar"
        query.chat_title = "Anonymous"
        help_command = HelpCommand(query)
        self.assertIs(help_command.query, query)
        self.assertEqual(help_command.command, "help")
        self.assertEqual(help_command.execute(), "You have invoked the help command!")

    def test_edited_message_disallow(self):
        query = BotQuery()
        query.is_edited = True
        self.assertIsNone(HelpCommand(query).execute())

    def test_edited_message_allow(self):
        query = BotQuery()
        query.is_edited = True
        help_command = HelpCommand(query)
        help_command.ignore_edited = False
        self.assertEqual(help_command.command, "help")
        self.assertEqual(help_command.execute(), "You have invoked the help command!")
