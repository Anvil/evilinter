import re

from ..typing import TokenYielder
from ._common import _CommonLexer
from .tokens import *
from .conditional import DoubleBracketConditionnalLexer


class BashLexer(_CommonLexer):

    word_char = re.compile(r'[-a-zA-Z0-9_/]').fullmatch

    variable_char = re.compile(r'[a-zA-Z0-9_]').fullmatch

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

    def subshell(self):
        pass

    def expansion(self):
        self.forward()
        yield from self.consume_select(self.variable_char, Parameter)

    def bracket(self):
        if self.compare_word_ahead("[", "["):
            return DoubleBracketConditionnalLexer(self.buffer)

    def curly_bracket(self):
        pass

    def comment(self):
        return self.consume_rest_of_line(Comment)

    def word(self) -> TokenYielder:
        return self.consume_select(self.word_char, Token)

    def redirection(self) -> TokenYielder:
        if self.current == ">":
            self.forward()
            if self.current == "&":
                self.forward()
                yield OutputRedirectionToFD
                yield from self.consume_select(str.isdigit, FileDescriptor)
            elif self.current == ">":
                raise NotImplementedError()
            elif self.current == ">":
                yield OutputRedirectionToFile
                yield from self.consume_separator(WhiteSpace)
                yield from self.word()
        else:
            raise NotImplementedError()

    def bang(self) -> TokenYielder:
        self.forward()
        if self.current in self.SPACE_SEPARATOR:
            yield CommandStatusInvertion
            return

    KEYWORDS = {"if", "for", "while", "until", "function", "case",
                "declare", "typeset", "export", "wait", "set", "unset"}

    def __iter__(self) -> TokenYielder:
        consumers = {"#": self.comment,
                     "'": self.single_quote,
                     '"': self.double_quote,
                     "(": self.subshell,
                     "$": self.expansion,
                     "{": self.curly_bracket,
                     "[": self.bracket,
                     "\n": self.consume_eol,
                     ">": self.redirection,
                     "<": self.redirection,
                     "!": self.bang}

        last_token_position = None
        while last_token_position != self.buffer.position:
            last_token_position = self.buffer.position.copy()
            try:
                consumer = consumers[self.current]
            except KeyError:
                yield from self.consume_separator(WhiteSpace)
                if self.word_char(self.current):
                    yield from self.word()
            else:
                try:
                    yield from consumer()
                except TypeError:
                    pass
        print("Incomplete parsing:")
        print(self.buffer)
