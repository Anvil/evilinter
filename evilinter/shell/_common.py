import re

from ..typing import TokenYielder
from ..lexer import Lexer
from .tokens import *


class _CommonLexer(Lexer):

    SPECIAL_VARS = set("$*#@!-0123456789")

    variable_first_char = re.compile(r'[a-zA-Z_]').fullmatch
    variable_char = re.compile(r'[a-zA-Z0-9_]').fullmatch

    def expansion(self) -> TokenYielder:
        self.forward()
        if self.current == "(":
            # Arithmetic or command expansion
            pass
        elif self.current == "[":
            # Obsolete arithmetic
            pass
        elif self.current == "'":
            # string expansion
            pass
        elif self.current == '"':
            # l10n
            pass
        if self.current == "{":
            # ${foo}
            pass
        if self.current in self.SPECIAL_VARS:
            # Bash specials vars, omitting $_
            pass
        else:
            yield from self.parameter_name()

    def backquote(self):
        raise NotImplementedError()

    def __double_quote_content(self) -> TokenYielder:
        while self.current != '"':
            yield from self.consume_select(
                lambda char: char not in '"\\$`', DoubleQuotedString)
            if self.current == "$":
                yield from self.expansion()
            elif self.current == "`":
                yield from self.backquote()
            elif self.current == "\\":
                self.forward(2)
                yield EscapedChar

    def double_quote(self) -> TokenYielder:
        # Assume current is '"'
        self.forward()
        yield OpeningDoubleQuote
        yield from self.__double_quote_content()
        self.forward()
        yield ClosingDoubleQuote
