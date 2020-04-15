from .botcommand import BotCommand
from boterror import BotError
from botquery import BotQuery

class InvalidCommand(BotCommand):
    def execute(self):
        if self.skip_edited():
            return

        self.handle_normal_query("Sorry! I don't understand. Try /help")
