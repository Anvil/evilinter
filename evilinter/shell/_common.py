import re

from ..lexer import Lexer


class _CommonLexer(Lexer):

    SPECIAL_VARS = set("$*#@!-0123456789")

    variable_first_char = re.compile(r'[a-zA-Z_]').fullmatch
    variable_char = re.compile(r'[a-zA-Z0-9_]').fullmatch

    
