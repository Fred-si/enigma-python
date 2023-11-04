from dataclasses import dataclass
from string import ascii_uppercase

import pytest

from .available import AvailableReflector, AvailableRotor
from .enigma import Enigma, AbstractConfig, ReflectorConfig, RotorConfig
from .exception import (
    ConfigurationError,
    InvalidReflectorError,
    InvalidRotorError,
    NotASCIILetterError,
)
from .plug_board import Plug


class AbstractConfigTest:
    @dataclass
    class FakeConfig(AbstractConfig):
        rotor_position: str

    @pytest.mark.parametrize("rotor_position", ["", "a", "AB"])
    def test_init_should_raise_when_position_is_not_single_ascii_uppercase_char(
        self,
        rotor_position: str,
    ) -> None:
        with pytest.raises(ValueError, match="single ascii uppercase letter"):
            self.FakeConfig(rotor_position)


class EnigmaTest:
    def test_init_should_not_raise(self) -> None:
        Enigma(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
        )

    def test_init_should_raise_when_called_without_rotor(self) -> None:
        with pytest.raises(ConfigurationError, match="at least three"):
            Enigma(
                (),
                ReflectorConfig(AvailableReflector.UKW, "A"),
            )

    def test_init_should_raise_when_called_with_one_rotor(self) -> None:
        with pytest.raises(ConfigurationError, match="at least three"):
            Enigma(
                (RotorConfig(AvailableRotor.I, "A"),),
                ReflectorConfig(AvailableReflector.UKW, "A"),
            )

    def test_init_should_raise_when_called_with_two_rotors(self) -> None:
        with pytest.raises(ConfigurationError, match="at least three"):
            Enigma(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
            )

    def test_init_should_raise_when_first_rotor_is_thin(self) -> None:
        with pytest.raises(InvalidRotorError, match="first"):
            Enigma(
                (
                    RotorConfig(AvailableRotor.BETA, "A"),
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
            )

    def test_init_should_raise_when_second_rotor_is_thin(self) -> None:
        with pytest.raises(InvalidRotorError, match="second"):
            Enigma(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.BETA, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
            )

    def test_init_should_raise_when_third_rotor_is_thin(self) -> None:
        with pytest.raises(InvalidRotorError, match="third"):
            Enigma(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                    RotorConfig(AvailableRotor.BETA, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
            )

    def test_init_should_raise_when_fourth_rotor_is_not_thin(self) -> None:
        with pytest.raises(InvalidRotorError, match="fourth"):
            Enigma(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                    RotorConfig(AvailableRotor.III, "A"),
                    RotorConfig(AvailableRotor.IIC, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
            )

    def test_init_should_raise_when_called_with_more_than_four_rotors(
        self,
    ) -> None:
        with pytest.raises(ConfigurationError, match="at most four"):
            Enigma(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                    RotorConfig(AvailableRotor.III, "A"),
                    RotorConfig(AvailableRotor.BETA, "A"),
                    RotorConfig(AvailableRotor.IIC, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
            )

    def test_init_should_raise_when_called_with_four_rotor_and_normal_reflector(
        self,
    ) -> None:
        with pytest.raises(InvalidReflectorError, match="thin"):
            Enigma(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                    RotorConfig(AvailableRotor.III, "A"),
                    RotorConfig(AvailableRotor.BETA, "A"),
                ),
                ReflectorConfig(AvailableReflector.UKW, "A"),
            )

    def test_init_should_raise_when_called_with_three_rotor_and_thin_reflector(
        self,
    ) -> None:
        with pytest.raises(InvalidReflectorError, match="not.*thin"):
            Enigma(
                (
                    RotorConfig(AvailableRotor.I, "A"),
                    RotorConfig(AvailableRotor.II, "A"),
                    RotorConfig(AvailableRotor.III, "A"),
                ),
                ReflectorConfig(AvailableReflector.REFBTHIN, "A"),
            )

    def test_encode_letter_should_step_first_rotor(self) -> None:
        enigma = Enigma(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
        )

        first = enigma.encode_letter("A")
        second = enigma.encode_letter("A")

        assert first != second

    def test_encode_letter_should_encode_letter_after_step(self) -> None:
        config = (
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
        )

        assert Enigma(*config).encode_letter("A") == "I"

    @pytest.mark.parametrize("letter", ascii_uppercase)
    def test_encode_already_encoded_letter_should_return_decoded_letter(
        self,
        letter: str,
    ) -> None:
        config = (
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
        )
        encoded = Enigma(*config).encode_letter(letter)

        # because Enigma step rotors at each letter, we need to create a new
        # instance from the config for decode the letter.
        decoded = Enigma(*config).encode_letter(encoded)

        assert decoded == letter

    def test_encode_should_convert_letter_to_uppercase(self) -> None:
        config = (
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
        )

        assert Enigma(*config).encode_letter("a") == "I"

    @pytest.mark.parametrize("letter", ["", "AB", "É", "!", ",", '"', "'"])
    def test_encode_should_raise_not_ascii_error_when_letter_is_not_an_ascii_letter(
        self,
        letter: str,
    ) -> None:
        config = (
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
        )

        with pytest.raises(NotASCIILetterError):
            Enigma(*config).encode_letter(letter)

    @pytest.mark.parametrize(
        ("message", "expected"),
        [
            ("F", "F"),
            ("FOO", "FOO"),
            ("FOO BAR", "FOOB AR"),
            ("FOOBAR", "FOOB AR"),
            ("AAAAAAAAAAAAAAAA", "AAAA AAAA AAAA AAAA"),
        ],
    )
    def test_mesage_should_grouped_by_four_letter(
        self,
        message: str,
        expected: str,
    ) -> None:
        config = (
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
        )
        encoded = Enigma(*config).encode_message(message)
        decoded = Enigma(*config).encode_message(encoded)

        assert decoded == expected

    @pytest.mark.parametrize(
        ("message", "expected"),
        [
            ("AAAAAAAAAAAAAAAA", "AAAA AAAA AAAA AAAA"),
            ("AAAAAAAAAAAAAAAAA", "AAAA AAAA AAAA AAAA\nA"),
            (
                "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
                "AAAA AAAA AAAA AAAA\nAAAA AAAA AAAA AAAA",
            ),
        ],
    )
    def test_mesage_lines_should_contain_four_letter_groups(
        self,
        message: str,
        expected: str,
    ) -> None:
        config = (
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
        )
        encoded = Enigma(*config).encode_message(message)
        decoded = Enigma(*config).encode_message(encoded)

        assert decoded == expected

    def test_encode_message_should_return_encoded_message(self) -> None:
        config = (
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
        )
        encoded = Enigma(*config).encode_message("FOO BAR")

        assert encoded == "VSLR QF"

    def test_encode_already_encoded_message_should_return_decoded_message(
        self,
    ) -> None:
        config = (
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
        )
        encoded = Enigma(*config).encode_message("FOO BAR")

        # because Enigma step rotors at each letter, we need to create a new
        # instance from the config for decode the letter.
        decoded = Enigma(*config).encode_message(encoded)

        assert decoded == "FOOB AR"

    def test_plug_board_permute_letters(self) -> None:
        config = (
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            Plug("F", "G"),
            Plug("O", "P"),
            Plug("A", "C"),
            Plug("B", "D"),
            Plug("R", "S"),
        )
        encoded = Enigma(*config).encode_message("FOO BAR")

        assert encoded == "PMJL KE"

    def test_encode_already_encoded_message_should_return_decoded_message_again(
        self,
    ) -> None:
        config = (
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            Plug("F", "G"),
            Plug("O", "P"),
            Plug("A", "C"),
            Plug("B", "D"),
            Plug("R", "S"),
        )
        encoded = Enigma(*config).encode_message("FOO BAR")

        # because Enigma step rotors at each letter, we need to create a new
        # instance from the config for decode the letter.
        decoded = Enigma(*config).encode_message(encoded)

        assert decoded == "FOOB AR"
