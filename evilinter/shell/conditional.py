from typing import Iterator

from ..typing import TokenYielder, TokenClass

from ..lexer import Lexer
from ..tokens import Token
from .tokens import *


class DoubleBracketConditionnalLexer(Lexer):

    def unary_operator(self):
        pass

    def binary_operator(self):
        pass

    def parenthesis(self):
        self.forward()
        yield OpeningParenthesis
        yield from self.expression()
        yield ClosingParenthesis

    def __unary_expression(self, cls: TokenClass) -> TokenYielder:
        self.forward(2)
        yield cls
        yield from self.consume_ifs(WhiteSpace)
        # Basically "one word" XXX: need refactoring with shell module.

    def expression(self) -> TokenYielder:
        if self.compare_word_ahead("!"):
            self.forward()
            yield NegationOperator
            yield from self.consume_ifs()
            # Bash allows something like [[ ! ! ! ! ! .... ]] to be valid.
            yield from self.expression()
        elif self.current == "(" and not self.compare_ahead("(", offset=1):
            yield self.parenthesis()
        if self.compare_word_ahead("-", "nz"):
            yield from self.__unary_expression(UnaryStringOperator)
        elif self.compare_word_ahead("-", "bcdefghkprsuwx"):
            yield from self.__unary_expression(UnaryFileOperator)
        elif self.compare_word_ahead("-", "t"):
            yield from self.__unary_expression(UnaryFDOperator)
        yield from self.binary_operator()

    def __iter__(self):
        self.forward(2)
        yield OpeningDoubleBracket
        yield from self.consume_ifs(WhiteSpace)
        yield from self.expression()
        # Need a test
        # self.forward(2)
        # yield ClosingDoubleBracket
