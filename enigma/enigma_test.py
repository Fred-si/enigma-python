from string import ascii_uppercase

import pytest

from .available import AvailableReflector, AvailableRotor
from .enigma import Enigma
from .config import EnigmaConfig, ReflectorConfig, RotorConfig
from .exception import NotASCIILetterError
from .plug_board import Plug


class EnigmaTest:
    def test_encode_letter_should_step_first_rotor(self) -> None:
        config = EnigmaConfig(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            [],
        )
        enigma = Enigma(config)
        first = enigma.encode_letter("A")
        second = enigma.encode_letter("A")

        assert first != second

    def test_encode_letter_should_encode_letter_after_step(self) -> None:
        config = EnigmaConfig(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            [],
        )

        assert Enigma(config).encode_letter("A") == "I"

    @pytest.mark.parametrize("letter", ascii_uppercase)
    def test_encode_already_encoded_letter_should_return_decoded_letter(
        self,
        letter: str,
    ) -> None:
        config = EnigmaConfig(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            [],
        )
        encoded = Enigma(config).encode_letter(letter)

        # because Enigma step rotors at each letter, we need to create a new
        # instance from the config for decode the letter.
        decoded = Enigma(config).encode_letter(encoded)

        assert decoded == letter

    def test_encode_should_convert_letter_to_uppercase(self) -> None:
        config = EnigmaConfig(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            [],
        )

        assert Enigma(config).encode_letter("a") == "I"

    @pytest.mark.parametrize("letter", ["", "AB", "É", "!", ",", '"', "'"])
    def test_encode_should_raise_not_ascii_error_when_letter_is_not_an_ascii_letter(
        self,
        letter: str,
    ) -> None:
        config = EnigmaConfig(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            [],
        )

        with pytest.raises(NotASCIILetterError):
            Enigma(config).encode_letter(letter)

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
        config = EnigmaConfig(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            [],
        )
        encoded = Enigma(config).encode_message(message)
        decoded = Enigma(config).encode_message(encoded)

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
        config = EnigmaConfig(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            [],
        )
        encoded = Enigma(config).encode_message(message)
        decoded = Enigma(config).encode_message(encoded)

        assert decoded == expected

    def test_encode_message_should_return_encoded_message(self) -> None:
        config = EnigmaConfig(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            [],
        )
        encoded = Enigma(config).encode_message("FOO BAR")

        assert encoded == "VSLR QF"

    def test_encode_already_encoded_message_should_return_decoded_message(
        self,
    ) -> None:
        config = EnigmaConfig(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            [],
        )
        encoded = Enigma(config).encode_message("FOO BAR")

        # because Enigma step rotors at each letter, we need to create a new
        # instance from the config for decode the letter.
        decoded = Enigma(config).encode_message(encoded)

        assert decoded == "FOOB AR"

    def test_plug_board_permute_letters(self) -> None:
        config = EnigmaConfig(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            (
                Plug("F", "G"),
                Plug("O", "P"),
                Plug("A", "C"),
                Plug("B", "D"),
                Plug("R", "S"),
            ),
        )
        encoded = Enigma(config).encode_message("FOO BAR")

        assert encoded == "PMJL KE"

    def test_encode_already_encoded_message_should_return_decoded_message_again(
        self,
    ) -> None:
        config = EnigmaConfig(
            (
                RotorConfig(AvailableRotor.I, "A"),
                RotorConfig(AvailableRotor.II, "A"),
                RotorConfig(AvailableRotor.III, "A"),
            ),
            ReflectorConfig(AvailableReflector.UKW, "A"),
            (
                Plug("F", "G"),
                Plug("O", "P"),
                Plug("A", "C"),
                Plug("B", "D"),
                Plug("R", "S"),
            ),
        )
        encoded = Enigma(config).encode_message("FOO BAR")

        # because Enigma step rotors at each letter, we need to create a new
        # instance from the config for decode the letter.
        decoded = Enigma(config).encode_message(encoded)

        assert decoded == "FOOB AR"
