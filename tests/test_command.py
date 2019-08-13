import unittest

from telegrambot import Command


class TestCommand(unittest.TestCase):
    def test_parse_template(self):
        cases = [
            ('/ping { name } { test }', r'^/ping (?P<name>.+) (?P<test>.+)$'),
            ('/ping {name} {  test  }', r'^/ping (?P<name>.+) (?P<test>.+)$'),
            ('/ping {name } { test}', r'^/ping (?P<name>.+) (?P<test>.+)$'),
        ]

        for tpl, expected in cases:
            self.assertEqual(Command._parse_template(tpl), expected)

    def test_matched(self):
        command = Command('/ping {a} {b}', lambda __: None)
        cases = [
            ('/ping hello world', True),
            ('/ping 한글 테스트', True),
            ('/ping 123 456', True),
            ('/ping hello', False),
            ('/ping', False),
        ]

        for text, expected in cases:
            self.assertEqual(command.matched(text), expected)

    def test_matched_params(self):
        command = Command('/ping {name}', lambda __: None)
        cases = [
            ('/ping world', {'name': 'world'}),
            ('/ping', None),
        ]

        for text, expected in cases:
            self.assertEqual(command.matched_params(text), expected)

    def text_call(self):
        def _command(ctx, name):
            return "Hello, {}!".format(name)

        command = Command('/ping {name}', _command)
        cases = [
            ('/ping world', 'Hello, world!'),
            ('/ping', None),
        ]

        for text, expected in cases:
            self.assertEqual(command.call(text, None), expected)
