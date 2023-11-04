from abc import ABC
from collections.abc import Iterable
from dataclasses import dataclass
from string import ascii_uppercase
from collections.abc import Callable

from .available import AvailableRotor, AvailableReflector
from .helper import (
    get_letter_from_index,
    get_letter_index,
    is_single_ascii_uppercase_letter,
)
from .plug_board import Plug, PlugBoard
from .rotor import AbstractRotor, FrozenRotor, Reflector, Rotor
from .exception import NotASCIILetterError


class AbstractConfig(ABC):
    rotor_position: str

    def __post_init__(self) -> None:
        if not is_single_ascii_uppercase_letter(self.rotor_position):
            msg = (
                f"rotor_position must be a single ascii uppercase letter."
                f" '{self.rotor_position}' given"
            )
            raise ValueError(msg)


@dataclass(frozen=True)
class RotorConfig(AbstractConfig):
    encoder_config: AvailableRotor
    rotor_position: str


@dataclass(frozen=True)
class ReflectorConfig(AbstractConfig):
    encoder_config: AvailableReflector
    rotor_position: str


class Enigma:
    def __init__(
        self,
        rotors_config: Iterable[RotorConfig],
        reflector_config: ReflectorConfig,
        *plugs: Plug,
        debug: bool = False,
    ) -> None:
        plug_board = PlugBoard(*plugs)

        reflector = Reflector(
            reflector_config.encoder_config,
            reflector_config.rotor_position,
        )
        rotors: list[AbstractRotor] = [
            reflector,
            FrozenRotor(AvailableReflector.ETW, "A"),
        ]
        for rotor in rotors_config:
            rotors.append(
                Rotor(
                    rotor.encoder_config,
                    rotor.rotor_position,
                    rotors[0].make_step,
                ),
            )

        self._encode = self._chain(
            plug_board.permute,
            *(r.encode for r in rotors[::-1]),
            *(r.encode_reverse for r in rotors),
            plug_board.permute,
        )
        self._make_step = rotors[-1].make_step
        self._debug = debug

    def encode_message(self, message: str) -> str:
        return " ".join(self.encode_word(word) for word in message.split())

    def encode_word(self, word: str) -> str:
        return "".join(self.encode_letter(letter) for letter in word)

    def encode_letter(self, letter: str) -> str:
        self._make_step()

        letter = letter.upper()
        self.debug(f"Encode {letter}:")

        if len(letter) != 1 or letter not in ascii_uppercase:
            raise NotASCIILetterError(letter)

        encoded = ascii_uppercase[self._encode(get_letter_index(letter))]

        self.debug(f"Encoded: {letter} -> {encoded}")

        return encoded

    def _chain(self, *encoders: Callable[[int], int]) -> Callable[[int], int]:
        def ret(letter: int) -> int:
            previous_letter = get_letter_from_index(letter)
            for encoder in encoders:
                letter = encoder(letter)
                self.debug(
                    f"Converted fred"
                    f" {previous_letter} -> {get_letter_from_index(letter)}",
                )
                previous_letter = get_letter_from_index(letter)

            return letter

        return ret

    def debug(self, message: str) -> None:
        if self._debug:
            print(message)
