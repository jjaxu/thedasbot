from .botcommand import BotCommand
from boterror import BotError
from botquery import BotQuery

class HelpCommand(BotCommand):
    def execute(self):
        if self.skip_edited():
            return
        help_text = """The DAS Bot help
        
        Available commands:
        /help -- Pulls up this help text
        /joke - Tells a random dad joke
        /fact - Fetches a random fun fact
        /trivia [category] [difficulty] - MC Trivia ("/trivia help" for details)
        /trends <mode> [parameters] - Google Trends ("/trends help" for details)"""

        self.handle_normal_query(help_text)
