from telegram import Bot as BotInterface
from telegram.utils.request import Request

from telegrambot.context import Context

_POLLING_TIMEOUT = 30


class Bot:
    def __init__(self, token: str):
        request = Request(read_timeout=_POLLING_TIMEOUT + 5)
        self._interface = BotInterface(token, request=request)

        self._commands = {}
        self._update_offset = 0

    def command(self, command):
        """
        A decorator to register a command.
        Usage example:

            @bot.command('/ping')
            def ping(ctx):
                return 'pong'
        """

        def decorator(f):
            self._commands[command] = f
            return f

        return decorator

    def start(self):
        """
        Start getting updates.
        """
        while True:
            updates = self._interface.get_updates(timeout=_POLLING_TIMEOUT,
                                                  offset=self._update_offset)
            for update in updates:
                try:
                    self._execute_command(update.message)
                except Exception:
                    # TODO - call error handler
                    pass

                self._update_offset = update.update_id + 1

    def _execute_command(self, message):
        texts = message.text.split(' ')
        context = Context(texts[0], texts[1:], message)

        command = context.command
        func = self._commands.get(command, None)
        if not func:
            raise RuntimeError("No such command: {}".format(command))

        res = func(context)
        self._interface.send_message(
            chat_id=context.message.chat.id,
            text=res,
        )
