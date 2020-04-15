import unittest, setup

from unittest.mock import Mock
from commands.invalid_command import InvalidCommand
from botquery import BotQuery

class InvalidCommandTest(unittest.TestCase):
    def test_non_edited(self):
        invalid_command = InvalidCommand(BotQuery())
        invalid_command.handle_normal_query = Mock()
        invalid_command.execute()
        invalid_command.handle_normal_query.assert_called_once_with("Sorry! I don't understand. Try /help")

    def test_edited_message_disallow(self):
        query = BotQuery()
        query.is_edited = True
        invalid_command = InvalidCommand(query)
        self.assertTrue(invalid_command.skip_edited())

        invalid_command.handle_normal_query = Mock()
        invalid_command.execute()
        self.assertFalse(invalid_command.handle_normal_query.called)

    def test_edited_message_allow(self):
        query = BotQuery()
        query.is_edited = True
        invalid_command = InvalidCommand(query)
        invalid_command.ignore_edited = False
        self.assertFalse(invalid_command.skip_edited())

        invalid_command.handle_normal_query = Mock()
        invalid_command.execute()
        invalid_command.handle_normal_query.assert_called_once_with("Sorry! I don't understand. Try /help")
