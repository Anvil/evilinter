import os
import sys
import logging

from . import SHLexer


def main():
    root_logger = logging.getLogger()
    # root_logger.setLevel(logging.INFO)
    root_logger.addHandler(logging.StreamHandler(sys.stdout))
    ARGSPARSE = "/usr/bin/argsparse.sh"
    for i in SHLexer(ARGSPARSE):
        print(repr(i))


if __name__ == "__main__":
    main()
