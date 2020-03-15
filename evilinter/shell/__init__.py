import re

from ..lexer import Lexer
from .tokens import *


class BashLexer(Lexer):

    __word_char = re.compile('[-a-zA-Z0-9+_]').match
   
    def __consume_word(self):
        self.__consume(str.isalnum)

    @staticmethod
    def __not_single_quote(char: str):
        return char != "'"

    def single_quote(self):
        self.forward()
        yield OpeningSingleQuote
        yield from self.consume_select(
            self.__not_single_quote, SingleQuotedString)
        self.forward()
        yield ClosingSingleQuote

    def double_quote(self):
        pass

    def subshell(self):
        pass

    def expansion(self):
        pass

    def comment(self):
        yield from self.consume_rest_of_line(Comment)

    def __iter__(self):
        last_token_position = None
        consumers = {"#": self.comment,
                     "'": self.single_quote,
                     '"': self.double_quote,
                     "(": self.subshell,
                     "$": self.expansion}
        while last_token_position != self.buffer.position:
            last_token_position = self.buffer.position
            try:
                consumer = consumers[self.current]
            except KeyError:
                pass
            else:
                yield from consumer()
