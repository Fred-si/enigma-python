from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass
from string import ascii_uppercase
from collections.abc import Callable
from typing import Final

from .available import AvailableRotor, AvailableReflector
from .helper import (
    batched,
    get_letter_from_index,
    get_letter_index,
    is_single_ascii_uppercase_letter,
)
from .plug_board import Plug, PlugBoard
from .rotor import AbstractRotor, Reflector, Rotor
from .exception import (
    ConfigurationError,
    InvalidReflectorError,
    InvalidRotorError,
    NotASCIILetterError,
)


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
    encoder: AvailableRotor
    rotor_position: str


@dataclass(frozen=True)
class ReflectorConfig(AbstractConfig):
    encoder: AvailableReflector
    rotor_position: str


class Enigma:
    MIN_ROTOR_COUNT: Final = 3
    MAX_ROTOR_COUNT: Final = 4

    def __init__(
        self,
        rotors_config: Sequence[RotorConfig],
        reflector_config: ReflectorConfig,
        *plugs: Plug,
        debug: bool = False,
    ) -> None:
        self.validate_rotors_configuration(rotors_config, reflector_config)
        plug_board = PlugBoard(*plugs)

        reflector = Reflector(
            reflector_config.encoder,
            reflector_config.rotor_position,
        )
        rotors: list[AbstractRotor] = [reflector]
        for encoder_config in rotors_config:
            rotors.append(
                Rotor(
                    encoder_config.encoder,
                    encoder_config.rotor_position,
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

    def validate_rotors_configuration(
        self,
        rotors: Sequence[RotorConfig],
        reflector: ReflectorConfig,
    ) -> None:
        if (rotor_count := len(rotors)) < self.MIN_ROTOR_COUNT:
            msg = f"Enigma need at least three rotors, {rotor_count} given"
            raise ConfigurationError(msg)

        if len(rotors) > self.MAX_ROTOR_COUNT:
            msg = f"Enigma need at most four rotors, {rotor_count} given"
            raise ConfigurationError(msg)

        thin_rotors = set(AvailableRotor.get_thin_rotors())
        for idx, config in enumerate(rotors[:3]):
            if config.encoder in thin_rotors:
                raise InvalidRotorError(
                    ("first", "second", "third")[idx],
                    set(AvailableRotor) - thin_rotors,
                    config.encoder,
                )

        thin_reflectors = set(AvailableReflector.get_thin_reflectors())
        if len(rotors) == self.MAX_ROTOR_COUNT:
            rotor = rotors[3].encoder
            if rotor not in AvailableRotor.get_thin_rotors():
                rotor_position = "fourth"
                raise InvalidRotorError(
                    rotor_position,
                    thin_rotors,
                    rotor,
                )

            if reflector.encoder not in thin_reflectors:
                msg = (
                    "Reflector must be a thin reflector when four rotors given."
                )
                raise InvalidReflectorError(msg)

        elif reflector.encoder in thin_reflectors:
            msg = "Reflector must not be a thin reflector when three rotors given."
            raise InvalidReflectorError(msg)

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

    @classmethod
    def get_from_str_config(
        cls,
        rotors: str,
        reflector: str,
        plugin_board: str,
        *,
        debug: bool = False,
    ) -> "Enigma":
        return cls(
            [cls._get_rotor_config(r) for r in rotors.split()],
            cls._get_reflector_config(reflector),
            *(Plug(*p) for p in plugin_board.split()),
            debug=debug,
        )

    @classmethod
    def _get_rotor_config(cls, config: str) -> RotorConfig:
        rotor, position = config.split(":")

        return RotorConfig(AvailableRotor[rotor], position)

    @classmethod
    def _get_reflector_config(cls, config: str) -> ReflectorConfig:
        reflector, position = config.split(":")

        return ReflectorConfig(AvailableReflector[reflector], position)
