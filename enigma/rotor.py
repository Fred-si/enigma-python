from abc import ABC, abstractmethod
from collections.abc import Callable

from .available import AvailableRotor, AvailableReflector
from .encoder import Encoder
from .helper import get_letter_index


class AbstractRotor(ABC):
    @property
    @abstractmethod
    def position(self) -> int:
        ...

    @property
    @abstractmethod
    def encoder(self) -> Encoder:
        ...

    @abstractmethod
    def make_step(self) -> None:
        ...

    def encode(self, letter: int) -> int:
        return self.encoder.encode((letter + self.position) % 26)

    def encode_reverse(self, letter: int) -> int:
        return (self.encoder.encode_reverse(letter) - self.position + 26) % 26


class FrozenRotor(AbstractRotor):
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

    def make_step(self) -> None:
        pass


class Reflector(FrozenRotor):
    def encode_reverse(self, letter: int) -> int:
        return letter

    def __repr__(self) -> str:
        return f"Reflector({self.config!r}, {self._position!r})"


class Rotor(AbstractRotor):
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
