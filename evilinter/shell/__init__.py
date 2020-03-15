from ..lexer import Lexer


class BashLexer(Lexer):

    __word_char = re.compile('[-a-zA-Z0-9+_]').match

    def __consume(self, func):
        token = []
        while func(self.current):
            token.append(self.current)
            self.forward()
        if token:
            yield token
   
    def __consume_space(self, blanks=SPACE):
        return self.__consume(lambda char: char in blanks)

    def __consume_shebang_shell(self):
        return self.__consume(lambda char: char not in {' '} | self.EOL)

    def __char(self, char):
        if self.current == char:
            self.forward()
            yield char

    def __consume_rest_of_line(self):
        yield from self.__consume(lambda char: char not in self.EOL)

    def __consume_comment(self):
        if self.current == '#':
            yield from self.__consume_rest_of_line()

    def __consume_word(self):
        self.__consume(str.isalnum)

    def __consume_instruction(self):
        yield from self.__consume_words()
        yield from self.__consume_comment()

    def __iter__(self):
        while True:
            if 
            yield from self.__consume_instruction()
            yield from self.__consume_comment()
            yield from self.__eol()
            assert current != self._current, ''.join(self._buffer[current:100])
