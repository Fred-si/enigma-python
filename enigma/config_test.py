from dataclasses import dataclass

import pytest

from enigma.available import AvailableReflector, AvailableRotor
from enigma.config import (
    AbstractRotorConfig,
    ConfigurationError,
    EnigmaConfig,
    InvalidReflectorError,
    InvalidRotorError,
    ReflectorConfig,
    RotorConfig,
)


class AbstractPositionalConfigTest:
    @dataclass
    class FakeConfig(AbstractRotorConfig):
        position: str

    @pytest.mark.parametrize("rotor_position", ["", "a", "AB"])
    def test_init_should_raise_when_position_is_not_single_ascii_uppercase_char(
        self,
        rotor_position: str,
    ) -> None:
        with pytest.raises(ValueError, match="single ascii uppercase letter"):
            self.FakeConfig(rotor_position)


class EnigmaConfigTest:
    def test_init_should_not_raise(self) -> None:
        EnigmaConfig(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            [],
        )

    def test_init_should_raise_when_called_without_rotor(self) -> None:
        with pytest.raises(ConfigurationError, match="at least three"):
            EnigmaConfig(
                (),
                ReflectorConfig(AvailableReflector.UKW, "A"),
                [],
            )

    def test_init_should_raise_when_called_with_one_rotor(self) -> None:
        with pytest.raises(ConfigurationError, match="at least three"):
            EnigmaConfig(
                (RotorConfig(AvailableRotor.I, "A"),),
                ReflectorConfig(AvailableReflector.UKW, "A"),
                [],
            )

    def test_init_should_raise_when_called_with_two_rotors(self) -> None:
        with pytest.raises(ConfigurationError, match="at least three"):
            EnigmaConfig(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
                [],
            )

    def test_init_should_raise_when_first_rotor_is_thin(self) -> None:
        with pytest.raises(InvalidRotorError, match="first"):
            EnigmaConfig(
                (
                    RotorConfig(AvailableRotor.BETA, "A"),
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
                [],
            )

    def test_init_should_raise_when_second_rotor_is_thin(self) -> None:
        with pytest.raises(InvalidRotorError, match="second"):
            EnigmaConfig(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.BETA, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
                [],
            )

    def test_init_should_raise_when_third_rotor_is_thin(self) -> None:
        with pytest.raises(InvalidRotorError, match="third"):
            EnigmaConfig(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                    RotorConfig(AvailableRotor.BETA, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
                [],
            )

    def test_init_should_raise_when_fourth_rotor_is_not_thin(self) -> None:
        with pytest.raises(InvalidRotorError, match="fourth"):
            EnigmaConfig(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                    RotorConfig(AvailableRotor.III, "A"),
                    RotorConfig(AvailableRotor.IIC, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
                [],
            )

    def test_init_should_raise_when_called_with_more_than_four_rotors(
        self,
    ) -> None:
        with pytest.raises(ConfigurationError, match="at most four"):
            EnigmaConfig(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                    RotorConfig(AvailableRotor.III, "A"),
                    RotorConfig(AvailableRotor.BETA, "A"),
                    RotorConfig(AvailableRotor.IIC, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
                [],
            )

    def test_init_should_raise_when_called_with_four_rotor_and_normal_reflector(
        self,
    ) -> None:
        with pytest.raises(InvalidReflectorError, match="thin"):
            EnigmaConfig(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                    RotorConfig(AvailableRotor.III, "A"),
                    RotorConfig(AvailableRotor.BETA, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
                [],
            )

    def test_init_should_raise_when_called_with_three_rotor_and_thin_reflector(
        self,
    ) -> None:
        with pytest.raises(InvalidReflectorError, match="not.*thin"):
            EnigmaConfig(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                    RotorConfig(AvailableRotor.III, "A"),
                ),
                ReflectorConfig(AvailableReflector.REFBTHIN, "A"),
                [],
            )
