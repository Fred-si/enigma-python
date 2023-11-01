from abc import ABC, abstractmethod
from typing import Callable, Iterable

from .available import AvailableRotor, AvailableReflector
from .encoder import Encoder
from .helper import get_letter_index


class BaseRotor(ABC):
    @property
    @abstractmethod
    def position(self) -> int:
        ...

    @property
    @abstractmethod
    def encoder(self) -> Encoder:
        ...

    def encode(self, letter: int) -> int:
        return self.encoder.encode((letter + self.position) % 26)

    def make_step(self) -> None:
        pass


class Reflector(BaseRotor):
    def __init__(
        self,
        config: AvailableReflector,
        position: str,
    ) -> None:
        self.config = config

        self._encoder = Encoder(config)
        self._position = get_letter_index(position)

    @property
    def position(self) -> int:
        return self._position

    @property
    def encoder(self) -> Encoder:
        return self._encoder

    def __repr__(self) -> str:
        return f"Reflector({repr(self.config)}, {repr(self._position)})"


class Rotor(BaseRotor):
    def __init__(
        self,
        config: AvailableRotor,
        initial_position: str,
        turnover: Callable[[], None],
    ) -> None:
        self.config = config

        self._initial_position = initial_position
        self._encoder = Encoder(config)
        self._position = get_letter_index(initial_position)
        self._turnover = turnover

    def encode_reverse(self, letter: int) -> int:
        return (self._encoder.encode_reverse(letter) - self._position + 26) % 26

    def make_step(self) -> None:
        self._position = (self._position + 1) % 26

        if self._position == 0:
            self._turnover()

    @property
    def position(self) -> int:
        return self._position

    @property
    def encoder(self) -> Encoder:
        return self._encoder

    def __repr__(self) -> str:
        return (
            f"Rotor("
            f"{self.config}"
            f", {self._initial_position}"
            f", {self._turnover}"
            f")"
        )
