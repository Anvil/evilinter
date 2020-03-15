from ..lexer import Lexer
from .tokens import *


class SheBangLexer(Lexer):

    def shell(self):
        return self.consume_select(
            lambda char: char not in ' '  + self.EOL, SheBangShell)

    def __iter__(self):
        if not self.compare_ahead('#', '!'):
            return
        self.buffer + 2
        yield SheBang
        yield from self.consume_chars(' ', SheBangShellSeparator)
        yield from self.shell()
        yield from self.consume_separator(SheBangSeparator)
        yield from self.consume_rest_of_line(SheBangParameter)
