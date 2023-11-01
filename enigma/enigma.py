from dataclasses import dataclass
from string import ascii_uppercase
from typing import Callable

from .available import AvailableRotor as AvailableRotor, AvailableReflector as AvailableReflector
from .helper import (
    get_letter_from_index,
    get_letter_index,
    is_single_ascii_uppercase_letter,
)
from .plug_board import Plug, PlugBoard
from .rotor import Reflector, Rotor
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
        first_rotor: RotorConfig,
        second_rotor: RotorConfig,
        third_rotor: RotorConfig,
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

        rotors: list[Rotor] = []
        rotors.insert(
            0,
            Rotor(
                first_rotor.encoder_config,
                first_rotor.rotor_position,
                reflector.make_step,
            ),
        )
        rotors.insert(
            0,
            Rotor(
                second_rotor.encoder_config,
                second_rotor.rotor_position,
                rotors[0].make_step,
            ),
        )
        rotors.insert(
            0,
            Rotor(
                third_rotor.encoder_config,
                third_rotor.rotor_position,
                rotors[0].make_step,
            ),
        )
        self._encode = self._chain(
            plug_board.permute,
            rotors[0].encode,
            rotors[1].encode,
            rotors[2].encode,
            reflector.encode,
            rotors[2].encode_reverse,
            rotors[1].encode_reverse,
            rotors[0].encode_reverse,
            plug_board.permute,
        )
        self._make_step = rotors[0].make_step

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
                self.debug(f"Converted fred {previous_letter} -> {get_letter_from_index(letter)}")
                previous_letter = get_letter_from_index(letter)

            return letter

        return ret
