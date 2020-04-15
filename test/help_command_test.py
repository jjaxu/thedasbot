import unittest, setup

from unittest.mock import Mock
from commands.help_command import HelpCommand
from botquery import BotQuery

class HelpCommandTest(unittest.TestCase):
    def test_private_chat(self):
        query = BotQuery()
        query.is_private = True
        query.user_first_name = "Lambda"
        help_command = HelpCommand(query)
        self.assertIs(help_command.query, query)
        
        help_command.handle_normal_query = Mock()
        help_command.execute()
        help_command.handle_normal_query.assert_called_once_with("You have invoked the help command!")

    def test_group_chat(self):
        query = BotQuery()
        query.is_group = True
        query.user_first_name = "Foobar"
        query.chat_title = "Anonymous"
        help_command = HelpCommand(query)
        self.assertIs(help_command.query, query)

        help_command.handle_normal_query = Mock()
        help_command.execute()
        help_command.handle_normal_query.assert_called_once_with("You have invoked the help command!")

    def test_edited_message_disallow(self):
        query = BotQuery()
        query.is_edited = True
        help_command = HelpCommand(query)
        self.assertTrue(help_command.skip_edited())

        help_command.handle_normal_query = Mock()
        help_command.execute()
        self.assertFalse(help_command.handle_normal_query.called)

    def test_edited_message_allow(self):
        query = BotQuery()
        query.is_edited = True
        help_command = HelpCommand(query)
        help_command.ignore_edited = False
        self.assertFalse(help_command.skip_edited())

        help_command.handle_normal_query = Mock()
        help_command.execute()
        help_command.handle_normal_query.assert_called_once_with("You have invoked the help command!")
