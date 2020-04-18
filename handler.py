import setup

from commands.command_parser import CommandParser
from botquery import BotQuery
from boterror import BotError

import requests

def trigger(event_raw:dict, context):
    try:
        bot_query = BotQuery.parse_event(event_raw.get("body"))
        bot_command = CommandParser.parse_command(bot_query)
        bot_command.execute()
    except BotError as err:
        print(f"Caught checked exception:\n\t{err}")
    except Exception as err:
        print(f"Caught unchecked exception:\n\t{err}")
    finally:
        return {"statusCode": 200}
