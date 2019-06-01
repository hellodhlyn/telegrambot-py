from telegram import Bot as BotInterface
from telegram.utils.request import Request

from telegrambot.context import Context

_POLLING_TIMEOUT = 30


class Bot:
    def __init__(self, token: str):
        self.token = token

        self._commands = {}
        self._update_offset = 0
        self._error_handler = None

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

    def error_handler(self):
        """
        A decorator to handle raised exception.
        Usage example:

            @bot.error_handler()
            def handle_error(err):
                print(err)
        """

        def decorator(f):
            if self._error_handler is not None:
                raise RuntimeError('error handler can\'t be more than one')
            self._error_handler = f
            return f

        return decorator

    def start(self):
        """
        Start getting updates.
        """

        request = Request(read_timeout=_POLLING_TIMEOUT + 5)
        self._interface = BotInterface(self.token, request=request)

        while True:
            self._poll()

    def _poll(self):
        updates = self._interface.get_updates(timeout=_POLLING_TIMEOUT,
                                              offset=self._update_offset)
        for update in updates:
            self._handle_update(update)
            self._update_offset = update.update_id + 1

    def _handle_update(self, update):
        try:
            self._execute_command(update.message)
        except Exception as e:
            if self._error_handler is not None:
                self._error_handler(e)

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
