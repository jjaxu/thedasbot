import unittest
import setup

from botquery import BotQuery
from boterror import BotError
from json import dumps

class BotQueryTest(unittest.TestCase):
    def test_private_message(self):
        data = dumps({
            "update_id":1234,
            "message":{
                "message_id":9876,
                "from":{
                    "id":777,
                    "is_bot":False,
                    "first_name":"Alice",
                    "last_name":"Alias",
                    "language_code":"en"
                },
                "chat":{
                    "id":777,
                    "first_name":"Alice",
                    "last_name":"Alias",
                    "type":"private"
                },
                "date":1584803939,
                "text":"/debug",
                "entities":[
                    {
                        "offset":0,
                        "length":6,
                        "type":"bot_command"
                    }
                ]
            }
        })
        query = BotQuery.parse_event(data)

        self.assertTrue(query.is_private, "is_private is wrong!")
        self.assertFalse(query.is_group, "is_group is wrong!")
        self.assertFalse(query.is_edited, "is_edited is wrong!")
        self.assertFalse(query.is_inline_query, "is_inline_query is wrong!")
        self.assertFalse(query.has_callback_query, "has_callback_query is wrong!")
        self.assertEqual(query.chat_id, 777, "Wrong chat ID!")
        self.assertEqual(query.from_id, 777, "Wrong from ID!")
        self.assertEqual(query.user_first_name, "Alice", "Wrong first name!")
        self.assertEqual(query.user_last_name, "Alias", "Wrong last name!")
        self.assertEqual(query.message, "/debug", "Wrong message!")
        self.assertIsNone(query.chat_title, "chat_title is wrong!")
    
    def test_group_message(self):
        data = dumps({
            "update_id":9876,
            "message":{
                "message_id":422,
                "from":{
                    "id":98765,
                    "is_bot":False,
                    "first_name":"Bob",
                    "last_name":"Builder",
                    "language_code":"en"
                },
                "chat":{
                    "id":-420,
                    "title":"My Group",
                    "type":"group",
                    "all_members_are_administrators":True
                },
                "date":1584995118,
                "text":"say hi to my bot!",
                "entities":[
                    {
                        "offset":0,
                        "length":5,
                        "type":"bot_command"
                    }
                ]
            }
        })

        query = BotQuery.parse_event(data)
        self.assertFalse(query.is_private, "is_private is wrong!")
        self.assertTrue(query.is_group, "is_group is wrong!")
        self.assertFalse(query.is_edited, "is_edited is wrong!")
        self.assertFalse(query.is_inline_query, "is_inline_query is wrong!")
        self.assertFalse(query.has_callback_query, "has_callback_query is wrong!")
        self.assertEqual(query.chat_id, -420, "Wrong chat ID!")
        self.assertEqual(query.from_id, 98765, "Wrong from ID!")
        self.assertEqual(query.user_first_name, "Bob", "Wrong first name!")
        self.assertEqual(query.user_last_name, "Builder", "Wrong last name!")
        self.assertEqual(query.message, "say hi to my bot!", "Wrong message!")
        self.assertEqual(query.chat_title, "My Group", "Wrong chat title!")
    
    def test_callback_query_private(self):
        data = dumps({
            "update_id":76,
            "callback_query":{
                "id":"807",
                "from":{
                    "id":13579,
                    "is_bot":False,
                    "first_name":"Mallory",
                    "last_name":"Malicous",
                    "language_code":"en"
                },
                "message":{
                    "message_id":707,
                    "from":{
                        "id":80088008,
                        "is_bot":True,
                        "first_name":"SAD Bot",
                        "username":"thesadbot"
                    },
                    "chat":{
                        "id":13579,
                        "first_name":"Mallory",
                        "last_name":"Malicous",
                        "type":"private"
                    },
                    "date":1585421298,
                    "text":"A, B, C, or D?",
                    "reply_markup":{
                        "inline_keyboard":[
                            [
                                {
                                    "text":"A",
                                    "callback_data":"0"
                                },
                                {
                                    "text":"B",
                                    "callback_data":"0"
                                }
                            ],
                            [
                                {
                                    "text":"C",
                                    "callback_data":"1"
                                },
                                {
                                    "text":"D",
                                    "callback_data":"0"
                                }
                            ]
                        ]
                    }
                },
                "chat_instance":"-4971937584078270380",
                "data":"1"
            }
        })

        query = BotQuery.parse_event(data)
        self.assertTrue(query.has_callback_query, "There should be a callback query!")
        self.assertIsNotNone(query.callback_query, "There should be a callback query property!")

        callback_query = query.callback_query
        self.assertTrue(callback_query.is_private, "is_private is wrong!")
        self.assertFalse(callback_query.is_group, "is_group is wrong!")
        self.assertFalse(callback_query.is_edited, "is_edited is wrong!")
        self.assertFalse(callback_query.is_inline_query, "is_inline_query is wrong!")
        self.assertFalse(callback_query.has_callback_query, "has_callback_query is wrong!")
        self.assertEqual(callback_query.chat_id, 13579, "Wrong chat ID!")
        self.assertEqual(callback_query.from_id, 80088008, "Wrong from ID!")
        self.assertEqual(callback_query.user_first_name, "SAD Bot", "Wrong first name!")
        self.assertIsNone(callback_query.user_last_name, "Last name should be None")
        self.assertEqual(callback_query.message, "A, B, C, or D?", "Wrong message!")
        self.assertIsNone(callback_query.chat_title, "Chat title should be None!")

    def test_callback_query_group(self):
        data = dumps({
            "update_id":12,
            "callback_query":{
                "id":"24680",
                "from":{
                    "id":69420,
                    "is_bot":False,
                    "first_name":"Eve",
                    "last_name":"Evans",
                    "language_code":"en"
                },
                "message":{
                    "message_id":5320,
                    "from":{
                        "id":-42069,
                        "is_bot":True,
                        "first_name":"Bot",
                        "username":"bot"
                    },
                    "chat":{
                        "id":-111999,
                        "title":"Some Group",
                        "type":"group",
                        "all_members_are_administrators":True
                    },
                    "date":1586129908,
                    "text":"MCQ question!",
                    "entities":[
                        {
                        "offset":0,
                        "length":8,
                        "type":"bold"
                        },
                        {
                        "offset":38,
                        "length":10,
                        "type":"bold"
                        },
                        {
                        "offset":59,
                        "length":70,
                        "type":"italic"
                        }
                    ],
                    "reply_markup":{
                        "inline_keyboard":[
                            [
                                {
                                    "text":"A",
                                    "callback_data":"AD"
                                },
                                {
                                    "text":"B",
                                    "callback_data":"BD"
                                }
                            ],
                            [
                                {
                                    "text":"C",
                                    "callback_data":"CD"
                                },
                                {
                                    "text":"D",
                                    "callback_data":"DD"
                                }
                            ]
                        ]
                    }
                },
                "chat_instance":"-8144088342400282673",
                "data":"DD"
            }
        })

        query = BotQuery.parse_event(data)
        self.assertTrue(query.has_callback_query, "There should be a callback query!")
        self.assertIsNotNone(query.callback_query, "There should be a callback query property!")

        callback_query = query.callback_query
        self.assertFalse(callback_query.is_private, "is_private is wrong!")
        self.assertTrue(callback_query.is_group, "is_group is wrong!")
        self.assertFalse(callback_query.is_edited, "is_edited is wrong!")
        self.assertFalse(callback_query.is_inline_query, "is_inline_query is wrong!")
        self.assertFalse(callback_query.has_callback_query, "has_callback_query is wrong!")
        self.assertEqual(callback_query.chat_id, -111999, "Wrong chat ID!")
        self.assertEqual(callback_query.from_id, -42069, "Wrong from ID!")
        self.assertEqual(callback_query.user_first_name, "Bot", "Wrong first name!")
        self.assertIsNone(callback_query.user_last_name, "Last name should be None")
        self.assertEqual(callback_query.message, "MCQ question!")
        self.assertEqual(callback_query.chat_title, "Some Group", "Wrong chat title!")

    def test_edited_message_private(self):
        data = dumps({
            "update_id":442342,
            "edited_message":{
                "message_id":289,
                "from":{
                    "id":168,
                    "is_bot":False,
                    "first_name":"Foo",
                    "last_name":"Bar",
                    "language_code":"en"
                },
                "chat":{
                    "id":168,
                    "first_name":"Foo",
                    "last_name":"Bar",
                    "type":"private"
                },
                "date":1584942586,
                "edit_date":1584942635,
                "text":"EDIT: I stand corrected",
                "entities":[
                    {
                        "offset":0,
                        "length":5,
                        "type":"bot_command"
                    }
                ]
            }
        })
        query = BotQuery.parse_event(data)

        self.assertTrue(query.is_private, "is_private is wrong!")
        self.assertFalse(query.is_group, "is_group is wrong!")
        self.assertTrue(query.is_edited, "is_edited is wrong!")
        self.assertFalse(query.is_inline_query, "is_inline_query is wrong!")
        self.assertFalse(query.has_callback_query, "has_callback_query is wrong!")
        self.assertEqual(query.chat_id, 168, "Wrong chat ID!")
        self.assertEqual(query.from_id, 168, "Wrong from ID!")
        self.assertEqual(query.user_first_name, "Foo", "Wrong first name!")
        self.assertEqual(query.user_last_name, "Bar", "Wrong last name!")
        self.assertEqual(query.message, "EDIT: I stand corrected", "Wrong message!")
        self.assertIsNone(query.chat_title, "chat_title is wrong!")

    def test_inline_query(self):
        data = dumps({
            "update_id":567,
            "inline_query":{
                "id":"90876",
                "from":{
                    "id":-7480,
                    "is_bot":False,
                    "first_name":"Unit",
                    "last_name":"Test",
                    "language_code":"en"
                },
                "query":"cute cat",
                "offset":""
            }
        })
        query = BotQuery.parse_event(data)
        self.assertTrue(query.is_inline_query)
        self.assertEqual(query.inline_query_id, "90876")
        self.assertEqual(query.inline_query_text, "cute cat")

    def test_bad_input(self):
        self.assertRaises(BotError, BotQuery.parse_event, None)
        self.assertRaises(BotError, BotQuery.parse_event, 5)
        self.assertRaises(BotError, BotQuery.parse_event, "{}")
        self.assertRaises(BotError, BotQuery.parse_event, dict(), False)
    