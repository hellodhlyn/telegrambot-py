import re
from typing import Callable

from telegrambot.context import Context


class Command:
    REGEX_COMMAND = r'^(?P<cmd>/\w+)'
    REGEX_PARAM_TEMPLATE = r'{\s*\w+\s*}'
    REGEX_PARAM_NAME = r'\w+'

    def __init__(self, template: str, func: Callable):
        self.regex = self._parse_template(template)
        self.func = func

    def matched(self, text: str):
        return re.match(self.regex, text) is not None

    def matched_params(self, text: str):
        matched = re.match(self.regex, text)
        if not matched:
            return None

        return matched.groupdict()

    def call(self, text: str, ctx: Context):
        params = self.matched_params(text)
        return self.func(ctx, **params) if params else self.func(ctx)

    @classmethod
    def _parse_template(cls, template: str) -> str:
        regex = template

        param_tpls = re.findall(cls.REGEX_PARAM_TEMPLATE, template)
        for tpl in param_tpls:
            param_name = re.search(cls.REGEX_PARAM_NAME, tpl).group(0)
            param_regex = r"(?P<{}>.+)".format(param_name)
            regex = regex.replace(tpl, param_regex)

        return "^{}$".format(regex)
