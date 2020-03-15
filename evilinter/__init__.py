import functools
import logging

from .tokens import Token
from .buffer import Buffer, Position
from .shebang import SheBangLexer
from .shell import BashLexer


LOGGER = logging.getLogger(__name__)


class SHLexer:

    def __init__(self, filename: str):
        self.__buffer = Buffer(filename)

    @property
    def position(self) -> Position:
        return self.__buffer.position

    @property
    def token(self):
        return self.__buffer.token

    def __iter__(self):
        for lexer in (SheBangLexer, BashLexer):
            for cls in lexer(self.__buffer):
                yield cls(''.join(self.token), self.position)
                self.__buffer.validate()
