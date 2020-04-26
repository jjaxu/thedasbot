from .botcommand import BotCommand
from .start_command import StartCommand
from .help_command import HelpCommand
from .joke_command import JokeCommand
from .fact_command import FactCommand
from .trivia_command import TriviaCommand
from .invalid_command import InvalidCommand
from botquery import BotQuery
from shlex import split as sh_split

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

            # Parses the command at the end of the callback payload by design
            # eg. "Payload_data/trivia" will be parsed as a trivia command
            cmd_name = bot_query.callback_query.callback_data.rsplit('/')[-1].lower()
            if cmd_name in AVAILABLE_COMMANDS:
                return AVAILABLE_COMMANDS[cmd_name](bot_query)
            return InvalidCommand(bot_query)

        args = sh_split(str(bot_query.message))
        
        cmd_arg = args[0].lower() if len(args) > 0 else ""
        cmd_name = cmd_arg[1:] if len(cmd_arg) > 0 else ""

        if cmd_arg.startswith("/") and cmd_name in AVAILABLE_COMMANDS:
            return AVAILABLE_COMMANDS[cmd_name](bot_query, args)
        return InvalidCommand(bot_query, args)
