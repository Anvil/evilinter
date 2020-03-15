from typing import Sequence

class Position:

    def __init__(self):
        self.absolute = 0
        self.line = 1
        self.char = 1

    def set(self, other: '__class__'):
        self.absolute = other.absolute
        self.line = other.line
        self.char = other.char

    def forward(self, char):
        self.absolute += 1
        if char == '\n':
            self.line += 1
            self.char = 1
        else:
            self.char += 1

    def __add__(self, other: Sequence[str]):
        for char in other:
            self.forward(char)

    def __str__(self) -> str:
        return f"{self.line}:{self.char}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.absolute}, {self})"


class Buffer():

    def __init__(self, filename):
        self.__filename = filename
        self.__buffer = list(open(self.__filename).read())
        self.__position = Position()
        self.__start = Position()

    @property
    def filename(self):
        return self.__filename

    @property
    def position(self):
        return self.__position

    @property
    def current(self):
        return self.__buffer[self.position.absolute]

    def forward(self):
        return self.position.forward(self.current)

    def validate(self):
        self.__start.set(self.__position)

    def rewind(self):
        self.__position.set(self.__start)

    @property
    def token(self):
        return self[self.__start.absolute:self.__position.absolute]

    def __getitem__(self, key):
        return self.__buffer[key]

    def __add__(self, other: int):
        self.position + self[self.position.absolute:self.position.absolute + other]
