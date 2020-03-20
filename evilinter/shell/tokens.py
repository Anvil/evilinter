from ..tokens import Token


class Comment(Token):
    pass


class OpeningSingleQuote(Token):
    pass


class ClosingSingleQuote(Token):
    pass


class SingleQuotedString(Token):
    pass


class OpeningDoubleQuote(Token):
    pass


class ClosingDoubleQuote(Token):
    pass


class DoubleQuotedString(Token):
    pass


class OpeningDoubleBracket(Token):
    pass


class ClosingDoubleBracket(Token):
    pass


class ConditionnalUnaryOperator(Token):
    pass


class UnaryStringOperator(ConditionnalUnaryOperator):
    pass


class UnaryFileOperator(ConditionnalUnaryOperator):
    pass


class UnaryFDOperator(ConditionnalUnaryOperator):
    pass


class ConditionnalBinaryOperator(Token):
    pass


class BinaryFileOperator(ConditionnalBinaryOperator):
    pass


class BinaryIntegerOperator(ConditionnalBinaryOperator):
    pass


class BinaryStringOperator(ConditionnalBinaryOperator):
    pass


class OpeningParenthesis(Token):
    pass


class ClosingParenthesis(Token):
    pass


class Parameter(Token):
    pass


class Number(Token):
    pass


class FileDescriptor(Number):
    pass


class OutputRedirectionToFD(Token):
    pass


class OutputRedirectionToFile(Token):
    pass


class EscapedChar(Token):
    pass


class CommandStatusInvertion(Token):
    pass
