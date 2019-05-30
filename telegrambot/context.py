from telegram import Message


class Context:
    def __init__(self, command: str, subcommands: list, message: Message):
        self.command = command
        self.subcommands = subcommands
        self.message = message
