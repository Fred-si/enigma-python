from string import ascii_uppercase

import pytest
from enigma import Enigma, RotorConfig
from enigma.exception import NotASCIILetterError
from enigma.plug_board import Plug


class TestRotorConfig:
    @pytest.mark.parametrize("rotor_position", ["", "a", "AB"])
    def test_init_should_raise_when_position_is_not_single_ascii_uppercase_char(
        self,
        rotor_position: str,
    ) -> None:
        with pytest.raises(AssertionError):
            RotorConfig(ascii_uppercase, rotor_position)

    def test_init_should_raise_when_encoder_config_have_less_than_26_char(self) -> None:
        with pytest.raises(AssertionError):
            RotorConfig("BCDEFGHIJKLMNOPQRSTUVWXYZ", "A")

    def test_init_should_raise_when_encoder_config_have_repeated_char(self) -> None:
        with pytest.raises(AssertionError):
            RotorConfig("AABCDEFGHIJKLMNOPQRSTUVWXY", "A")

    def test_init_should_raise_when_encoder_config_contain_not_ascii_uppercase_char(
        self,
    ) -> None:
        with pytest.raises(AssertionError):
            RotorConfig("aBCDEFGHIJKLMNOPQRSTUVWXYZ", "A")


class TestEnigma:
    def test_init(self) -> None:
        Enigma(
            (
                RotorConfig("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A"),
                RotorConfig("NTZPSFBOKMWRCJDIVLAEYUXHGQ", "A"),
                RotorConfig("JVIUBHTCDYAKEQZPOSGXNRMWFL", "A"),
            ),
            RotorConfig("QYHOGNECVPUZTFDJAXWMKISRBL", "A"),
        )

    def test_encode_letter_should_step_first_rotor(self) -> None:
        enigma_a = Enigma(
            (
                RotorConfig("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A"),
                RotorConfig("NTZPSFBOKMWRCJDIVLAEYUXHGQ", "A"),
                RotorConfig("JVIUBHTCDYAKEQZPOSGXNRMWFL", "A"),
            ),
            RotorConfig("QYHOGNECVPUZTFDJAXWMKISRBL", "A"),
        )

        enigma_b = Enigma(
            (
                RotorConfig("JGDQOXUSCAMIFRVTPNEWKBLZYH", "B"),
                RotorConfig("NTZPSFBOKMWRCJDIVLAEYUXHGQ", "A"),
                RotorConfig("JVIUBHTCDYAKEQZPOSGXNRMWFL", "A"),
            ),
            RotorConfig("QYHOGNECVPUZTFDJAXWMKISRBL", "A"),
        )

        first = enigma_a.encode_letter("A")
        second = enigma_a.encode_letter("A")

        assert first != second

    def test_encode_letter_should_encode_letter_after_step(self) -> None:
        config = (
            (
                RotorConfig("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A"),
                RotorConfig("NTZPSFBOKMWRCJDIVLAEYUXHGQ", "A"),
                RotorConfig("JVIUBHTCDYAKEQZPOSGXNRMWFL", "A"),
            ),
            RotorConfig("QYHOGNECVPUZTFDJAXWMKISRBL", "A"),
        )

        assert Enigma(*config).encode_letter("A") == "I"

    @pytest.mark.parametrize("letter", ascii_uppercase)
    def test_encode_already_encoded_letter_should_return_decoded_letter(
        self,
        letter,
    ) -> None:
        config = (
            (
                RotorConfig("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A"),
                RotorConfig("NTZPSFBOKMWRCJDIVLAEYUXHGQ", "A"),
                RotorConfig("JVIUBHTCDYAKEQZPOSGXNRMWFL", "A"),
            ),
            RotorConfig("QYHOGNECVPUZTFDJAXWMKISRBL", "A"),
        )
        encoded = Enigma(*config).encode_letter(letter)

        # because Enigma step rotors at each letter, we need to create a new
        # instance from the config for decode the letter.
        decoded = Enigma(*config).encode_letter(encoded)

        assert decoded == letter

    def test_encode_should_convert_letter_to_uppercase(self) -> None:
        config = (
            (
                RotorConfig("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A"),
                RotorConfig("NTZPSFBOKMWRCJDIVLAEYUXHGQ", "A"),
                RotorConfig("JVIUBHTCDYAKEQZPOSGXNRMWFL", "A"),
            ),
            RotorConfig("QYHOGNECVPUZTFDJAXWMKISRBL", "A"),
        )
        assert Enigma(*config).encode_letter("a") == "I"

    @pytest.mark.parametrize("letter", ["", "AB", "É", "!", ",", '"', "'"])
    def test_encode_should_raise_not_ascii_error_when_letter_is_not_an_ascii_letter(
        self,
        letter: str,
    ) -> None:
        config = (
            (
                RotorConfig("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A"),
                RotorConfig("NTZPSFBOKMWRCJDIVLAEYUXHGQ", "A"),
                RotorConfig("JVIUBHTCDYAKEQZPOSGXNRMWFL", "A"),
            ),
            RotorConfig("QYHOGNECVPUZTFDJAXWMKISRBL", "A"),
        )
        with pytest.raises(NotASCIILetterError):
            Enigma(*config).encode_letter(letter)

    def test_encode_word_should_return_encoded_word(self) -> None:
        config = (
            (
                RotorConfig("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A"),
                RotorConfig("NTZPSFBOKMWRCJDIVLAEYUXHGQ", "A"),
                RotorConfig("JVIUBHTCDYAKEQZPOSGXNRMWFL", "A"),
            ),
            RotorConfig("QYHOGNECVPUZTFDJAXWMKISRBL", "A"),
        )
        encoded = Enigma(*config).encode_word("FOOBAR")

        assert encoded == "VSLRQF"

    def test_encode_already_encoded_word_should_return_decoded_word(self) -> None:
        config = (
            (
                RotorConfig("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A"),
                RotorConfig("NTZPSFBOKMWRCJDIVLAEYUXHGQ", "A"),
                RotorConfig("JVIUBHTCDYAKEQZPOSGXNRMWFL", "A"),
            ),
            RotorConfig("QYHOGNECVPUZTFDJAXWMKISRBL", "A"),
        )
        encoded = Enigma(*config).encode_word("FOOBAR")

        # because Enigma step rotors at each letter, we need to create a new
        # instance from the config for decode the letter.
        decoded = Enigma(*config).encode_word(encoded)

        assert decoded == "FOOBAR"

    def test_encode_message_should_return_encoded_message(self) -> None:
        config = (
            (
                RotorConfig("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A"),
                RotorConfig("NTZPSFBOKMWRCJDIVLAEYUXHGQ", "A"),
                RotorConfig("JVIUBHTCDYAKEQZPOSGXNRMWFL", "A"),
            ),
            RotorConfig("QYHOGNECVPUZTFDJAXWMKISRBL", "A"),
        )
        encoded = Enigma(*config).encode_message("FOO BAR")

        assert encoded == "VSL RQF"

    def test_encode_already_encoded_message_should_return_decoded_message(self) -> None:
        config = (
            (
                RotorConfig("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A"),
                RotorConfig("NTZPSFBOKMWRCJDIVLAEYUXHGQ", "A"),
                RotorConfig("JVIUBHTCDYAKEQZPOSGXNRMWFL", "A"),
            ),
            RotorConfig("QYHOGNECVPUZTFDJAXWMKISRBL", "A"),
        )
        encoded = Enigma(*config).encode_message("FOO BAR")

        # because Enigma step rotors at each letter, we need to create a new
        # instance from the config for decode the letter.
        decoded = Enigma(*config).encode_message(encoded)

        assert decoded == "FOO BAR"

    def test_plug_board_permute_letters(self) -> None:
        config = (
            (
                RotorConfig("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A"),
                RotorConfig("NTZPSFBOKMWRCJDIVLAEYUXHGQ", "A"),
                RotorConfig("JVIUBHTCDYAKEQZPOSGXNRMWFL", "A"),
            ),
            RotorConfig("QYHOGNECVPUZTFDJAXWMKISRBL", "A"),
            Plug("F", "G"),
            Plug("O", "P"),
            Plug("A", "C"),
            Plug("B", "D"),
            Plug("R", "S"),
        )
        encoded = Enigma(*config).encode_message("FOO BAR")

        assert encoded == "PMJ LKE"

    def test_encode_already_encoded_message_should_return_decoded_message_again(
        self,
    ) -> None:
        config = (
            (
                RotorConfig("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A"),
                RotorConfig("NTZPSFBOKMWRCJDIVLAEYUXHGQ", "A"),
                RotorConfig("JVIUBHTCDYAKEQZPOSGXNRMWFL", "A"),
            ),
            RotorConfig("QYHOGNECVPUZTFDJAXWMKISRBL", "A"),
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
