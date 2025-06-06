from string import ascii_uppercase
from unittest.mock import MagicMock

import pytest

from enigma.exception import NotASCIIUppercaseLetterError
from enigma.helper import get_letter_index as index
from enigma.plug_board import Plug, PlugBoard


class PlugTest:
    @pytest.mark.parametrize(
        ("left", "right"),
        [
            ("", ""),
            ("A", ""),
            ("", "A"),
        ],
    )
    def test_plug_init_should_raise_when_values_are_not_single_ascii_letters(
        self,
        left: str,
        right: str,
    ) -> None:
        with pytest.raises(NotASCIIUppercaseLetterError):
            Plug(left, right)


class PlugBoardTest:
    @pytest.mark.parametrize("letter", ascii_uppercase)
    def test_plug_board_should_not_permute_letters_when_init_without_plug(
        self,
        letter: str,
    ) -> None:
        plug_board = PlugBoard(turnover=MagicMock())

        assert plug_board.encode(index(letter)) == index(letter)

    def test_plug_board_should_permute_plugged_letters(self) -> None:
        plug_board = PlugBoard(Plug("A", "I"), turnover=MagicMock())

        assert plug_board.encode(index("A")) == index("I")
        assert plug_board.encode(index("I")) == index("A")

    def test_plug_board_should_permute_plugged_letters_with_two_plugs(
        self,
    ) -> None:
        plug_board = PlugBoard(
            Plug("A", "I"),
            Plug("B", "Z"),
            turnover=MagicMock(),
        )

        assert plug_board.encode(index("A")) == index("I")
        assert plug_board.encode(index("I")) == index("A")
        assert plug_board.encode(index("B")) == index("Z")
        assert plug_board.encode(index("Z")) == index("B")

    @pytest.mark.parametrize(
        "letter",
        set(ascii_uppercase) - {"A", "I", "B", "Z"},
    )
    def test_plug_board_should_not_permute_letters_when_not_plugged(
        self,
        letter: str,
    ) -> None:
        plug_board = PlugBoard(
            Plug("A", "I"),
            Plug("B", "Z"),
            turnover=MagicMock(),
        )

        assert plug_board.encode(index(letter)) == index(letter)

    def test_init_should_raise_when_pass_duplicated_plug(self) -> None:
        with pytest.raises(ValueError, match=".*duplicate.*"):
            PlugBoard(Plug("A", "I"), Plug("I", "A"), turnover=MagicMock())

    def test_init_should_raise_when_pass_more_than_ten_plugs(self) -> None:
        with pytest.raises(ValueError, match=".*10.*11.*"):
            PlugBoard(
                Plug("A", "B"),
                Plug("C", "D"),
                Plug("E", "F"),
                Plug("G", "H"),
                Plug("I", "J"),
                Plug("K", "L"),
                Plug("M", "N"),
                Plug("O", "P"),
                Plug("Q", "R"),
                Plug("S", "T"),
                Plug("U", "V"),
                turnover=MagicMock(),
            )
