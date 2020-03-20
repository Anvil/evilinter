from ...tokens import Token


class WhiteSpace(Token):
    pass


class EOL(Token):
    pass


class NonInterruptingEOL(EOL):
    pass
