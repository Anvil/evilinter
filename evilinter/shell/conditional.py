from ..lexer import Lexer
from .tokens import *


class DoubleBracketConditionnalLexer(Lexer):

    def __iter__(self):
        self.buffer + 2
        yield OpeningDoubleBracket
        yield from self.consume_ifs(WhiteSpace)
        yield ClosingDoubleBracket

