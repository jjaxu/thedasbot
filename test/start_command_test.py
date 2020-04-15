import unittest, setup

from unittest.mock import Mock
from commands.start_command import StartCommand
from botquery import BotQuery

class StartCommandTest(unittest.TestCase):
    def test_private_chat(self):
        query = BotQuery()
        query.is_private = True
        query.user_first_name = "Lambda"
        start_command = StartCommand(query)
        self.assertIs(start_command.query, query)

        start_command.handle_normal_query = Mock()
        start_command.execute()
        start_command.handle_normal_query.assert_called_once_with("Hello Lambda! Welcome to the DAS bot!")

    def test_group_chat(self):
        query = BotQuery()
        query.is_group = True
        query.user_first_name = "Foobar"
        query.chat_title = "Anonymous"
        start_command = StartCommand(query)
        self.assertIs(start_command.query, query)

        start_command.handle_normal_query = Mock()
        start_command.execute()
        start_command.handle_normal_query.assert_called_once_with("Hello Anonymous! I am the DAS Bot, Foobar has summoned me here!")

    def test_edited_message_disallow(self):
        query = BotQuery()
        query.is_edited = True
        start_command = StartCommand(query)
        
        self.assertTrue(start_command.skip_edited())
        start_command.handle_normal_query = Mock()
        start_command.execute()
        self.assertFalse(start_command.handle_normal_query.called)

    def test_edited_message_allow(self):
        query = BotQuery()
        query.is_edited = True
        start_command = StartCommand(query)
        start_command.ignore_edited = False
        
        self.assertFalse(start_command.skip_edited())
        start_command.handle_normal_query = Mock()
        start_command.execute()
        start_command.handle_normal_query.assert_called_once_with("Greetings from the DAS bot!")
