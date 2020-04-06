from .botcommand import BotCommand
from .start_command import StartCommand
from .help_command import HelpCommand
from .joke_command import JokeCommand

import sys
sys.path.append('..')

from botquery import BotQuery

AVAILABLE_COMMANDS = {
    "start": StartCommand,
    "help": HelpCommand,
    "joke": JokeCommand
}

class CommandParser(object):
    @classmethod
    def parse_command(cls, bot_query: BotQuery) -> BotCommand:
        args = str(bot_query.message).strip().split()
        cmd_name = args[0].lower() if len(args) > 0 else ""

        if cmd_name.startswith("/") and cmd_name[1:] in AVAILABLE_COMMANDS:
            return AVAILABLE_COMMANDS[cmd_name[1:]](bot_query)
        return None
