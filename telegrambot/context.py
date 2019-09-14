from telegram import Message


class Context:
    def __init__(self, message: Message):
        self.message = message
