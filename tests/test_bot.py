from copy import deepcopy
from datetime import datetime
import os
import unittest
from unittest.mock import Mock

from telegram import Bot as BotInterface, Chat, Message, Update
from telegrambot import Bot


_mock_chat = Chat(1, 'PRIVATE')
_mock_message = Message(2, None, datetime.now(), _mock_chat, text='/ping')
_mock_update = Update(update_id=3, message=_mock_message)


class TestBot(unittest.TestCase):
    def setUp(self):
        _interface = Mock(spec=BotInterface)
        _interface.get_updates = Mock(return_value=[_mock_update])
        _interface.send_message = Mock(return_value=_mock_message)

        bot = Bot(os.environ['TEST_BOT_TOKEN'])
        bot._interface = _interface

        @bot.command('/ping')
        def ping(ctx):
            return 'pong'

        self.bot = bot

    def test_command(self):
        self.assertIn('/ping', self.bot._commands.keys())

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
