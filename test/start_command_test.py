import unittest
import setup

from commands import StartCommand
from botquery import BotQuery

class StartCommandTest(unittest.TestCase):
    def test_private_chat(self):
        query = BotQuery()
        query.is_private = True
        query.user_first_name = "Lambda"
        start_command = StartCommand(query)
        self.assertIs(start_command.query, query)
        self.assertEqual(start_command.command, "start")
        self.assertEqual(start_command.execute(), "Hello Lambda! Welcome to the DAS bot!")

    def test_group_chat(self):
        query = BotQuery()
        query.is_group = True
        query.user_first_name = "Foobar"
        query.chat_title = "Anonymous"
        start_command = StartCommand(query)
        self.assertIs(start_command.query, query)
        self.assertEqual(start_command.command, "start")
        self.assertEqual(start_command.execute(), "Hello Anonymous! I am the DAS Bot, Foobar has summoned me here!")

    def test_edited_message_disallow(self):
        query = BotQuery()
        query.is_edited = True
        self.assertIsNone(StartCommand(query).execute())

    def test_edited_message_allow(self):
        query = BotQuery()
        query.is_edited = True
        start_command = StartCommand(query)
        start_command.ignore_edited = False
        self.assertIsNotNone(start_command.execute())
