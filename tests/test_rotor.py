from string import ascii_uppercase
from unittest.mock import MagicMock

from enigma.rotor import Rotor, Reflector

from .helper import index


class TestRotor:
    def test_init(self) -> None:
        Rotor("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A", MagicMock())

    def test_encode_at_position_a(self) -> None:
        rotor = Rotor("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A", MagicMock())

        assert rotor.encode(index("A")) == index("J")

    def test_encode_reverse_at_position_a(self) -> None:
        rotor = Rotor("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A", MagicMock())

        assert rotor.encode_reverse(index("J")) == index("A")

    def test_encode_at_position_b(self) -> None:
        rotor = Rotor("JGDQOXUSCAMIFRVTPNEWKBLZYH", "B", MagicMock())

        assert rotor.encode(index("A")) == index("G")

    def test_encode_reverse_at_position_b(self) -> None:
        rotor = Rotor("JGDQOXUSCAMIFRVTPNEWKBLZYH", "B", MagicMock())

        assert rotor.encode_reverse(index("G")) == index("A")

    def test_encode_at_position_c(self) -> None:
        rotor = Rotor("JGDQOXUSCAMIFRVTPNEWKBLZYH", "C", MagicMock())

        assert rotor.encode(index("A")) == index("D")

    def test_encode_reverse_at_position_c(self) -> None:
        rotor = Rotor("JGDQOXUSCAMIFRVTPNEWKBLZYH", "C", MagicMock())

        assert rotor.encode_reverse(index("D")) == index("A")

    def test_encode_should_not_raise_when_position_overflow(self) -> None:
        rotor = Rotor("JGDQOXUSCAMIFRVTPNEWKBLZYH", "B", MagicMock())

        rotor.encode(index("Z"))

    def test_encode_reverse_should_return_right_letter_when_position_overflow(self) -> None:
        rotor = Rotor("JGDQOXUSCAMIFRVTPNEWKBLZYH", "B", MagicMock())

        assert rotor.encode_reverse(rotor.encode(index("Z"))) == index("Z")

    def test_step_should_increment_rotor_position_by_one_when_position_is_a(
        self,
    ) -> None:
        rotor = Rotor("", "A", MagicMock())
        rotor.make_step()

        assert ascii_uppercase[rotor.position] == "B"

    def test_step_should_increment_rotor_position_by_one_when_position_is_b(
        self,
    ) -> None:
        rotor = Rotor("", "B", MagicMock())
        rotor.make_step()

        assert ascii_uppercase[rotor.position] == "C"

    def test_step_should_turnover_when_current_position_is_z(self) -> None:
        rotor = Rotor("", "Z", MagicMock())
        rotor.make_step()

        assert ascii_uppercase[rotor.position] == "A"

    def test_step_should_call_turnover_callback_when_position_is_z(self) -> None:
        callback = MagicMock()
        rotor = Rotor("", "Z", callback)
        rotor.make_step()

        assert callback.called


class TestReflector:
    def test_init(self) -> None:
        Reflector("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A")

    def test_encode_at_position_a(self) -> None:
        reflector = Reflector("JGDQOXUSCAMIFRVTPNEWKBLZYH", "A")

        assert reflector.encode(index("A")) == index("J")

    def test_encode_at_position_b(self) -> None:
        reflector = Reflector("JGDQOXUSCAMIFRVTPNEWKBLZYH", "B")

        assert reflector.encode(index("A")) == index("G")

    def test_encode_at_position_c(self) -> None:
        reflector = Reflector("JGDQOXUSCAMIFRVTPNEWKBLZYH", "C")

        assert reflector.encode(index("A")) == index("D")