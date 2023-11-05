from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass
from random import choices
from secrets import choice
from string import ascii_uppercase
from typing import Any, Final, Self, TypedDict
from collections.abc import Iterable
from collections.abc import Container

from .available import AvailableReflector, AvailableRotor
from .helper import batched, choices_unique, is_single_ascii_uppercase_letter
from .plug_board import Plug, PlugBoard

name_position_separator: Final = ":"


class AbstractRotorConfig(ABC):
    encoder: AvailableRotor | AvailableReflector
    position: str

    def __post_init__(self) -> None:
        if not is_single_ascii_uppercase_letter(self.position):
            msg = (
                f"rotor_position must be a single ascii uppercase letter."
                f" '{self.position}' given"
            )
            raise ValueError(msg)

    def __str__(self) -> str:
        name = self.encoder.name
        position = self.position

        return f"{name}{name_position_separator}{position}"


@dataclass(frozen=True)
class RotorConfig(AbstractRotorConfig):
    encoder: AvailableRotor
    position: str


@dataclass(frozen=True)
class ReflectorConfig(AbstractRotorConfig):
    encoder: AvailableReflector
    position: str


class StrConfig(TypedDict):
    rotors: str
    reflector: str
    plugin_board: str


@dataclass(frozen=True)
class EnigmaConfig:
    rotors_config: Sequence[RotorConfig]
    reflector_config: ReflectorConfig
    plugs: Sequence[Plug]
    debug: bool = False

    MIN_ROTOR_COUNT: Final = 3
    MAX_ROTOR_COUNT: Final = 4

    def __post_init__(self) -> None:
        rotors = self.rotors_config
        reflector = self.reflector_config

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

    def as_dict(self) -> StrConfig:
        return {
            "rotors": " ".join(str(r) for r in self.rotors_config),
            "reflector": str(self.reflector_config),
            "plugin_board": " ".join(f"{p.left}{p.right}" for p in self.plugs),
        }

    @classmethod
    def parse(
        cls,
        rotors: str,
        reflector: str,
        plugin_board: str,
        *,
        debug: bool = False,
    ) -> Self:
        return cls(
            [cls._get_rotor_config(r) for r in rotors.split()],
            cls._get_reflector_config(reflector),
            [Plug(*p) for p in plugin_board.split()],
            debug=debug,
        )

    @classmethod
    def _get_rotor_config(cls, config: str) -> RotorConfig:
        rotor, position = config.split(name_position_separator)

        return RotorConfig(AvailableRotor[rotor], position)

    @classmethod
    def _get_reflector_config(cls, config: str) -> ReflectorConfig:
        reflector, position = config.split(name_position_separator)

        return ReflectorConfig(AvailableReflector[reflector], position)

    @classmethod
    def generate_random_config(cls, plug_count: int = 0) -> Self:
        reflector = choice(tuple(AvailableReflector.get_normal_reflectors()))
        return cls(
            rotors_config=tuple(cls._generate_random_rotors_config()),
            reflector_config=ReflectorConfig(reflector, "A"),
            plugs=tuple(cls._generate_random_plugs(plug_count)),
        )

    @classmethod
    def _generate_random_rotors_config(cls) -> Iterable[RotorConfig]:
        rotors = iter(
            choices_unique(
                tuple(AvailableRotor.get_normal_rotors()),
                k=3,
            ),
        )
        positions = iter(choices(ascii_uppercase, k=3))

        while True:
            try:
                yield RotorConfig(next(rotors), next(positions))
            except StopIteration:
                break

    @classmethod
    def _generate_random_plugs(cls, plug_count: int) -> Iterable[Plug]:
        if plug_count > PlugBoard.MAX_PLUG_COUNT:
            raise ValueError

        plugs_config = batched(
            choices_unique(ascii_uppercase, plug_count * 2),
            2,
        )

        for plug in plugs_config:
            yield Plug(*plug)


class ConfigurationError(Exception):
    pass


class InvalidRotorError(ConfigurationError):
    def __init__(
        self,
        rotor_position: str,
        expected: Container[Any],
        actual: AvailableRotor,
    ) -> None:
        msg = f"{rotor_position} rotor must be in {expected}. {actual} given"
        super().__init__(msg)


class InvalidReflectorError(ConfigurationError):
    pass
