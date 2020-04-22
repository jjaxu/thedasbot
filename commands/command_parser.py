from .botcommand import BotCommand
from .start_command import StartCommand
from .help_command import HelpCommand
from .joke_command import JokeCommand
from .fact_command import FactCommand
from .trivia_command import TriviaCommand
from .invalid_command import InvalidCommand
from botquery import BotQuery

# This indicates the acceptable commands
AVAILABLE_COMMANDS = {
    "start": StartCommand,
    "help": HelpCommand,
    "joke": JokeCommand,
    "fact": FactCommand,
    "trivia": TriviaCommand
}

class CommandParser:
    
    @classmethod
    def parse_command(cls, bot_query: BotQuery) -> BotCommand:
        if bot_query.has_callback_query:
            cmd_name = bot_query.callback_query.callback_data.rsplit('/')[-1].lower()
            return AVAILABLE_COMMANDS[cmd_name](bot_query) if cmd_name in AVAILABLE_COMMANDS else InvalidCommand(bot_query)

        args = str(bot_query.message).strip().split()
        cmd_name = args[0].lower() if len(args) > 0 else ""

        if cmd_name.startswith("/") and cmd_name[1:] in AVAILABLE_COMMANDS:
            return AVAILABLE_COMMANDS[cmd_name[1:]](bot_query, args)
        return InvalidCommand(bot_query, args)
