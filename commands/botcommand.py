# This class defines the base class that all commands for the bot must inherit from

class BotCommand(object):
    def __init__(self, command: str):
        super().__init__()
        self.command = command
        self.ignore_edited = True
        self.parse_mode = None
        self.other_params = None

    def skip_edited(self) -> bool:
        return self.query.is_edited and self.ignore_edited

    def execute(self):
        raise NotImplementedError("Method is not implemented, did you forget to override?")
