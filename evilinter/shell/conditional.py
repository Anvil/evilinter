from typing import Iterator, Tuple

from ..typing import TokenYielder, TokenClass

from ._common import _CommonLexer
from .tokens import *


class DoubleBracketConditionnalLexer(_CommonLexer):

    def consume_separator(self, include_newline=True):
        return self.consume_separator(include_newline)

    def parameter_name(self) -> TokenYielder:
        if self.variable_first_char(self.current):
            self.forward()
            yield from self.consume_select(self.variable_char, Parameter)
        # Else regular string: $% for instance is '$%'

    def word(self):
        if self.current == '"':
            yield from self.double_quote()
            yield from self.word()
            return
        if self.current == "$":
            yield from self.expansion()

    def __any_simple_word(self, *words: Tuple[str]) -> bool:
        return any(self.compare_word_ahead(*list(operator))
                   for operator in words)

    def end_of_binary_operator_expression(self):
        # Assume current == -
        self.forward()
        if self.__any_simple_word("eq", "ne", "lt", "le", "gt", "ge"):
            self.forward(2)
            yield BinaryIntegerOperator
            yield from self.consume_separator()
            yield from self.consume_select(str.isdigit, Number)
            yield from self.consume_separator()
            return
        if self.__any_simple_word("ef", "nt", "ot"):
            self.forward(2)
            yield BinaryFileOperator
        elif self.compare_word_ahead("<>="):
            self.forward()
            yield BinaryStringOperator
        elif self.compare_word_ahead("=", "=~"):
            self.foward(2)
            yield BinaryStringOperator

    def binary_operator_expression(self):
        yield from self.word()
        yield from self.consume_separator()
        yield from self.end_of_binary_operator_expression()

    def parenthesis(self):
        self.forward()
        yield OpeningParenthesis
        yield from self.expression()
        yield ClosingParenthesis

    def __unary_expression(self, cls: TokenClass) -> TokenYielder:
        self.forward(2)
        yield cls
        yield from self.consume_separator()
        # Basically "one word" XXX: need refactoring with shell module.

    def expression(self) -> TokenYielder:
        if self.compare_word_ahead("!"):
            self.forward()
            yield NegationOperator
            yield from self.consume_separator()
            # Bash allows something like [[ ! ! ! ! ! .... ]] to be valid.
            yield from self.expression()
        elif self.current == "(" and not self.compare_ahead("(", offset=1):
            yield self.parenthesis()
        if self.compare_word_ahead("-", "nz"):
            yield from self.__unary_expression(UnaryStringOperator)
        elif self.compare_word_ahead("-", "bcdefghkprsuwxGLNOS"):
            yield from self.__unary_expression(UnaryFileOperator)
        elif self.compare_word_ahead("-", "t"):
            yield from self.__unary_expression(UnaryFDOperator)
        # Any other dash-word (-word) in this context will be
        # considered as a regular string.
        # FIXME: Possibly [[ foo ]]
        yield from self.binary_operator_expression()

    def __iter__(self) -> TokenYielder:
        self.forward(2)
        yield OpeningDoubleBracket
        yield from self.consume_separator()
        yield from self.expression()
        if self.compare_word_ahead("]", "]"):
            self.forward(2)
            yield ClosingDoubleBracket
