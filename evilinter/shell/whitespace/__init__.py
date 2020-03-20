from ..typing import TokenYielder, TokenClass
from ..lexer import Lexer
from .tokens import *


class WhiteSpaceLexer(Lexer):

    def consume_spaces(self, cls: TokenClass) -> TokenYielder:
        return self.consume_chars(self.SPACES, cls)

    SPACES = {' ', '\t'}

    def consume_eol(self) -> TokenYielder:
        while self.current == '\n':
            self.forward()
            yield EOL

    def consume_separator(self, include_newline=False) -> TokenYielder:
        while self.current in self.SPACES:
            yield from self.consume_spaces(WhiteSpace)
            if self.compare_ahead('\\', '\n'):
                self.forward(2)
                yield NonInterruptingEOL
            elif include_newline and self.current == '\n':
                yield from self.consume_eol()
            else:
                continue        # Could also be return.
            yield from self.consume_spaces(Indentation)
