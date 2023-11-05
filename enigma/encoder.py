from collections.abc import Iterator
from typing import Protocol

from .available import AvailableRotor, AvailableReflector
from .helper import get_letter_index


class EncoderInterface(Protocol):
    def encode(self, letter: int) -> int:
        ...

    def encode_reverse(self, letter: int) -> int:
        ...

    def make_step(self) -> None:
        ...


class Encoder:
    def __init__(self, config: AvailableRotor | AvailableReflector) -> None:
        self._config = [
            (idx, get_letter_index(letter)) for idx, letter in enumerate(config)
        ]

        self._normal = dict(self._config)
        self._reverse = {encoded: raw for raw, encoded in self._config}

    def __iter__(self) -> Iterator[tuple[int, int]]:
        yield from self._config

    def encode(self, letter: int) -> int:
        return self._encode(self._normal, letter)

    def encode_reverse(self, letter: int) -> int:
        return self._encode(self._reverse, letter)

    def _encode(self, direction: dict[int, int], letter: int) -> int:
        return direction[letter]
