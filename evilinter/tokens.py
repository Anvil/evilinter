import logging

from .buffer import Position


LOGGER = logging.getLogger(__name__)


class Token():

    def __init__(self, chars, position: Position):
        self.__value = ''.join(chars)
        self.__position = position
        LOGGER.debug(f"Found new token: {self}")

    @property
    def line(self):
        return self.__position.line

    @property
    def char(self):
        return self.__position.char

    @property
    def value(self):
        return self.__value

    def __str__(self):
        return self.value

    def __repr__(self):
        value = self.value.replace('\n', '\\n')
        return f"{self.__class__.__name__}"\
            f"(at {self.line}:{self.char}: '{value}')"


class EOL(Token):
    pass
