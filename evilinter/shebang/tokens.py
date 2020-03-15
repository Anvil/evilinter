from ..tokens import Token


class SheBang(Token):
    pass

class SheBangShellSeparator(Token):
    pass

class SheBangShell(Token):
    pass

class SheBangSeparator(Token):
    pass

class SheBangParameter(Token):
    pass


__all__ = ["SheBang", "SheBangShellSeparator", "SheBangShell",
           "SheBangSeparator", "SheBangParameter"]
