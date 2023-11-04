from dataclasses import dataclass
from string import ascii_uppercase

import pytest

from .available import AvailableReflector, AvailableRotor
from .enigma import Enigma, AbstractConfig, ReflectorConfig, RotorConfig
from .exception import NotASCIILetterError
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
    def test_init(self) -> None:
        Enigma(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
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

        assert Enigma(*config).encode_letter("A") == "M"

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

        assert Enigma(*config).encode_letter("a") == "M"

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

    def test_encode_word_should_return_encoded_word(self) -> None:
        config = (
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
        )
        encoded = Enigma(*config).encode_word("FOOBAR")

        assert encoded == "IQRDCU"

    def test_encode_already_encoded_word_should_return_decoded_word(
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
        encoded = Enigma(*config).encode_word("FOOBAR")

        # because Enigma step rotors at each letter, we need to create a new
        # instance from the config for decode the letter.
        decoded = Enigma(*config).encode_word(encoded)

        assert decoded == "FOOBAR"

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

        assert encoded == "IQR DCU"

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

        assert decoded == "FOO BAR"

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

        assert encoded == "ERN DCW"

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

        assert decoded == "FOO BAR"
