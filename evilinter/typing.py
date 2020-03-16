from typing import Type, NewType, Iterator

from .tokens import Token

TokenClass = NewType('TokenClass', Type[Token])

TokenYielder = NewType('TokenYielder', Iterator[TokenClass])
