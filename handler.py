import os
import sys

from commands import CommandParser
from botquery import BotQuery
from boterror import BotError
from config import BASE_URL, ALLOW_EDITED_MESSAGES
from constants import *

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vendored"))

import requests

def trigger(event_raw:dict, context):
    try:
        bot_query = BotQuery.parse_event(event_raw.get("body"))
        if bot_query.is_inline_query:
            handle_inline_query(bot_query)
        elif bot_query.has_callback_query:
            handle_callback_query(bot_query)
        else: # Normal Query
            handle_normal_query(bot_query)
    except BotError as err:
        print("Caught checked exception:\n\t{}".format(err))
    except Exception as err:
        print("Caught unchecked exception:\n\t{}".format(err))
    finally:
        return {"statusCode": 200}


def handle_normal_query(bot_query: BotQuery):
    if bot_query.is_edited and not ALLOW_EDITED_MESSAGES:
        return

    bot_command = CommandParser.parse_command(bot_query)
    data = dict()

    if bot_command is not None: # Valid command
        response = bot_command.execute()

        # No response, don't send anything back
        if response is None:
            return
        if bot_command.parse_mode:
            data["parse_mode"] = bot_command.parse_mode

        if bot_command.other_params:
            data.update(bot_command.other_params)
    else: # Not a valid command
        response = "Sorry! I don't understand. Try /help"

    data["chat_id"] = bot_query.chat_id
    data["text"] = response

    url = "{}/sendMessage".format(BASE_URL)
    res = requests.post(url, json=data)
    if not res.ok:
        print("sendMessage did not complete successfully. Code: {}\n\t{}".format(res.status_code, res.text))


def handle_callback_query(bot_query: BotQuery):
    pass

def handle_inline_query(bot_query: BotQuery):
    pass
