from .botcommand import BotCommand
from boterror import BotError
from botquery import BotQuery

class StartCommand(BotCommand):
    def execute(self):
        if self.skip_edited():
            return

        if self.query.is_private:
            result = f"Hello {self.query.user_first_name}! Welcome to the DAS bot!"
        elif self.query.is_group:
            result = f"Hello {self.query.chat_title}! I am the DAS Bot, {self.query.user_first_name} has summoned me here!"
        else:
            result = "Greetings from the DAS bot!"

        self.handle_normal_query(result)
