from copy import deepcopy
from datetime import datetime
import unittest
from unittest.mock import Mock

from telegram import Bot as BotInterface, Chat, Message, Update
from telegrambot import Bot


_mock_chat = Chat(1, 'PRIVATE')
_mock_message = Message(2, None, datetime.now(), _mock_chat, text='/ping')
_mock_update = Update(update_id=3, message=_mock_message)

_mock_error = RuntimeError('MockError')


class TestBot(unittest.TestCase):
    def setUp(self):
        interface = Mock(spec=BotInterface)
        interface.get_updates = Mock(return_value=[_mock_update])
        interface.send_message = Mock(return_value=_mock_message)

        error_handler = Mock()

        bot = Bot('dummy_token')
        bot._interface = interface

        @bot.command('/ping')
        def ping(ctx):
            return 'pong'

        @bot.command('/invalid')
        def invalid(ctx):
            raise _mock_error

        @bot.error_handler()
        def handle_error(e):
            error_handler(_mock_error)

        self.bot = bot
        self._error_handler = error_handler

    def test_command(self):
        self.assertEqual(len(self.bot._commands), 2)

    def test_poll(self):
        self.bot._execute_command = Mock()

        self.bot._poll()

        self.bot._execute_command.assert_called_once_with(_mock_message)
        self.assertEqual(self.bot._update_offset, 4)

    def test_poll_exception(self):
        self.bot._execute_command = Mock(side_effect=RuntimeError())

        self.bot._poll()
        self.assertEqual(self.bot._update_offset, 4)

    def test_execute_command(self):
        self.bot._execute_command(_mock_message)
        self.bot._interface.send_message \
            .assert_called_once_with(chat_id=_mock_chat.id, text='pong')

    def test_execute_invalid_command(self):
        message = deepcopy(_mock_message)
        message.text = '/pingping'
        with self.assertRaises(RuntimeError):
            self.bot._execute_command(message)

        self.bot._interface.send_message.assert_not_called()

    def test_error_handler(self):
        message = deepcopy(_mock_message)
        message.text = '/invalid'
        update = deepcopy(_mock_update)
        update.message = message

        self.bot._handle_update(update)
        self._error_handler.assert_called_once_with(_mock_error)
