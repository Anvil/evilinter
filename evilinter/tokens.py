import logging

from .buffer import Position


LOGGER = logging.getLogger(__name__)


class Token():

    def __init__(self, chars, position: Position):
        self._str = ''.join(chars)
        self._line, self._char = self.position.start
        LOGGER.debug(f"Found new token: '{self._str}' "
                     f"at line {line}, char {pos}")

    def __str__(self):
        return self._str

    def __repr__(self):
        return f"{self.__class__.__name__}"\
            f"(at {self._line}:{self._pos}: '{self._str}')"


class EOL(Token):
    pass
