import pytest

from .available import AvailableRotor
from .encoder import Encoder, Config


class ConfigTest:
    def test_normal(self) -> None:
        expected = {
            0: 9,
            1: 6,
            2: 3,
            3: 16,
            4: 14,
            5: 23,
            6: 20,
            7: 18,
            8: 2,
            9: 0,
            10: 12,
            11: 8,
            12: 5,
            13: 17,
            14: 21,
            15: 19,
            16: 15,
            17: 13,
            18: 4,
            19: 22,
            20: 10,
            21: 1,
            22: 11,
            23: 25,
            24: 24,
            25: 7,
        }
        assert Config(AvailableRotor.I).normal == expected

    def test_reverse(self) -> None:
        expected = {
            0: 9,
            1: 21,
            2: 8,
            3: 2,
            4: 18,
            5: 12,
            6: 1,
            7: 25,
            8: 11,
            9: 0,
            10: 20,
            11: 22,
            12: 10,
            13: 17,
            14: 4,
            15: 16,
            16: 3,
            17: 13,
            18: 7,
            19: 15,
            20: 6,
            21: 14,
            22: 19,
            23: 5,
            24: 24,
            25: 23,
        }
        assert Config(AvailableRotor.I).reverse == expected


class EncoderTest:
    @pytest.mark.parametrize(("normal", "reverse"), Config(AvailableRotor.I))
    def test_encode_with_first_config(self, normal: int, reverse: int) -> None:
        config = AvailableRotor.I
        rotor = Encoder(config)

        assert rotor.encode(normal) == reverse

    @pytest.mark.parametrize(("normal", "reverse"), Config(AvailableRotor.I))
    def test_encode_reverse_with_first_config(
        self, normal: int, reverse: int,
    ) -> None:
        config = AvailableRotor.I
        rotor = Encoder(config)

        assert rotor.encode_reverse(reverse) == normal

    @pytest.mark.parametrize(("normal", "reverse"), Config(AvailableRotor.II))
    def test_encode_with_second_config(self, normal: int, reverse: int) -> None:
        config = AvailableRotor.II
        rotor = Encoder(config)

        assert rotor.encode(normal) == reverse

    @pytest.mark.parametrize(("normal", "reverse"), Config(AvailableRotor.II))
    def test_encode_reverse_with_second_config(
        self, normal: int, reverse: int,
    ) -> None:
        config = AvailableRotor.II
        rotor = Encoder(config)

        assert rotor.encode_reverse(reverse) == normal
