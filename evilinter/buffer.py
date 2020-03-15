class Position:

    def __init__(self):
        self.absolute = 0
        self.line = 1
        self.char = 1
        self.mark = 0, 1, 1

    @property
    def start(self):
        return self.line, self.char

    def forward(self, char):
        self.absolute += 1
        if char == '\n':
            self.line += 1
            self.char = 1
        else:
            self.char += 1

    def rewind(self):
        self.absolute, self.line, self.char = self.mark

    def validate(self):
        self.mark = self.absolute, self.line, self.char

    @property
    def slice(self):
        return slice(self.mark[0], self.absolute, None)

    def __add__(self, other):
        for char in other:
            self.forward(char)

    
class Buffer():

    def __init__(self, filename):
        self.__filename = filename
        self.__buffer = list(open(self.__filename).read())
        self.__position = Position()

    @property
    def filename(self):
        return self.__filename

    @property
    def position(self):
        return self.__position

    @property
    def current(self):
        return self.__buffer[self.position.absolute]

    @property
    def token(self):
        return self[self.position.slice]

    def forward(self):
        self.position + self.current

    def __getitem__(self, key):
        return self.__buffer[key]

    def __add__(self, other: int):
        self.position + self[self.position.absolute:other]
