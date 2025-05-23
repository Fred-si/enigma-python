from __future__ import annotations

from string import ascii_uppercase
from typing import TYPE_CHECKING

from .exception import NotASCIILetterError
from .helper import batched, get_letter_from_index, get_letter_index
from .plug_board import PlugBoard
from .rotor import Reflector, Rotor

if TYPE_CHECKING:
    from collections.abc import Callable

    from .config import EnigmaConfig
    from .encoder import EncoderInterface


class Enigma:
    def __init__(self, config: EnigmaConfig) -> None:
        rotors_config = config.rotors_config
        reflector_config = config.reflector_config
        plugs = config.plugs
        debug = config.debug

        encoders: list[EncoderInterface] = [
            Reflector(reflector_config.encoder, reflector_config.position),
        ]

        for encoder_config in rotors_config:
            encoders.append(
                Rotor(
                    encoder_config.encoder,
                    encoder_config.position,
                    encoders[-1].make_step,
                ),
            )
        encoders.append(PlugBoard(*plugs, turnover=encoders[-1].make_step))

        self._encode = self._chain(
            *(r.encode for r in encoders[::-1]),
            *(r.encode_reverse for r in encoders),
        )
        self._make_step = encoders[-1].make_step
        self._debug = debug

    def encode_message(self, message: str) -> str:
        message = message.replace(" ", "").replace("\n", "")
        encoded = (self.encode_letter(letter) for letter in message)

        return "\n".join(
            " ".join(words)
            for words in batched(
                ("".join(letters) for letters in batched(encoded, 4)),
                4,
            )
        )

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
