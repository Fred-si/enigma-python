from collections.abc import Iterable
from dataclasses import dataclass
from string import ascii_uppercase
from typing import Callable

from .available import AvailableRotor, AvailableReflector
from .helper import (
    get_letter_from_index,
    get_letter_index,
    is_single_ascii_uppercase_letter,
)
from .plug_board import Plug, PlugBoard
from .rotor import AbstractRotor, FrozenRotor, Reflector, Rotor
from .exception import NotASCIILetterError


@dataclass(frozen=True)
class RotorConfig:
    encoder_config: AvailableRotor | AvailableReflector
    rotor_position: str

    def __post_init__(self) -> None:
        assert is_single_ascii_uppercase_letter(self.rotor_position)

        assert len(self.encoder_config) == len(ascii_uppercase)
        assert len(self.encoder_config) == len(set(self.encoder_config))
        assert all(letter in ascii_uppercase for letter in self.encoder_config)


class Enigma:
    def __init__(
        self,
        rotors_config: Iterable[RotorConfig],
        reflector: RotorConfig,
        *plugs: Plug,
        debug: bool = False,
    ) -> None:
        self.debug = print if debug else lambda *_, **__: None

        plug_board = PlugBoard(*plugs)

        reflector = Reflector(
            reflector.encoder_config,
            reflector.rotor_position,
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

    def encode_message(self, message: str) -> str:
        return " ".join(self.encode_word(word) for word in message.split())

    def encode_word(self, word: str) -> str:
        return "".join((self.encode_letter(letter) for letter in word))

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
                    f"Converted fred {previous_letter} -> {get_letter_from_index(letter)}"
                )
                previous_letter = get_letter_from_index(letter)

            return letter

        return ret
