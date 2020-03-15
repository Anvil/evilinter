from typing import Type, Callable
from .buffer import Buffer, Position

from . import tokens


class Lexer:

    EOL = '\n'
    SPACE_SEPARATOR = ' \t'

    def __init__(self, buffer: Buffer):
        self.__buffer = buffer

    @property
    def buffer(self) -> Buffer:
        return self.__buffer

    @property
    def position(self) -> Position:
        return self.__buffer.position

    @property
    def current(self) -> str:
        return self.__buffer.current

    @property
    def token(self) -> str:
        return self.__buffer.token

    @property
    def forward(self):
        return self.__buffer.forward

    def consume_select(self, func: Callable, cls: Type):
        while func(self.current):
            self.forward()
        if self.token:
            yield cls

    def consume_chars(self, chars: str, cls: Type):
        return self.consume_select(lambda char: char in chars, cls)

    def consume_separator(self, cls: Type):
        return self.consume_chars(self.SPACE_SEPARATOR, cls)

    def consume_eol(self):
        return self.consume_chars(self.EOL, tokens.EOL)

    def consume_rest_of_line(self, cls: Type):
        yield from self.consume_select(lambda char: char not in self.EOL, cls)
        yield from self.consume_eol()
