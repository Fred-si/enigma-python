from collections.abc import Container
from typing import Any

from enigma.available import AvailableRotor


class NotASCIILetterError(ValueError):
    def __init__(self, value: Any) -> None:
        super().__init__(f'"{value}" is not an ASCII letter.')


class NotASCIIUppercaseLetterError(ValueError):
    def __init__(self, value: Any) -> None:
        super().__init__(f'"{value}" is not an ASCII uppercase letter.')


class ConfigurationError(Exception):
    pass


class InvalidRotorError(TypeError):
    def __init__(
        self,
        rotor_position: str,
        expected: Container[Any],
        actual: AvailableRotor,
    ) -> None:
        msg = (
            f"{rotor_position} rotor must be in {expected}. {actual} given"
        )
        super().__init__(msg)


class InvalidReflectorError(TypeError):
    pass
