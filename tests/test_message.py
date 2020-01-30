import time
import unittest
from datetime import datetime
from unittest.mock import Mock

from telegram import Bot as BotInterface, Message, Chat

from telegrambot.message import TextMessage

_mock_chat = Chat(1, 'PRIVATE')
_mock_message = Message(2, None, datetime.now(), _mock_chat, text='/ping')


class TestTextMessage(unittest.TestCase):
    def setUp(self):
        interface = Mock(spec=BotInterface)
        interface.send_message = Mock(return_value=_mock_message)

        self.interface = interface

    def test_send_message(self):
        msg = TextMessage('pong')
        msg.send(self.interface, _mock_chat.id)
        self.interface.send_message \
            .assert_called_once_with(chat_id=_mock_chat.id, text='pong')

    def test_send_message_with_delay(self):
        msg = TextMessage('pong', delay=1)
        msg.send(self.interface, _mock_chat.id)
        self.interface.send_message.assert_not_called()

        time.sleep(1.1)
        self.interface.send_message \
            .assert_called_once_with(chat_id=_mock_chat.id, text='pong')
