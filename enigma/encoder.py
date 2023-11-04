from collections.abc import Iterator


from .available import AvailableRotor, AvailableReflector
from .helper import get_letter_index


class Config:
    def __init__(self, config: AvailableRotor | AvailableReflector) -> None:
        self.config = [
            (idx, get_letter_index(letter)) for idx, letter in enumerate(config)
        ]

        self.normal = dict(self.config)
        self.reverse = {encoded: raw for raw, encoded in self.config}

    def __iter__(self) -> Iterator[tuple[int, int]]:
        yield from self.config


class AbstractEncoder:
    def __init__(self, config: AvailableRotor | AvailableReflector) -> None:
        self._config = Config(config)

    def encode(self, letter: int) -> int:
        return self._encode(self._config.normal, letter)

    def _encode(self, direction: dict[int, int], letter: int) -> int:
        return direction[letter]


class ReflectorEncoder(AbstractEncoder):
    pass


class Encoder(AbstractEncoder):
    def encode_reverse(self, letter: int) -> int:
        return self._encode(self._config.reverse, letter)
