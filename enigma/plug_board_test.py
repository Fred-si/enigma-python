from string import ascii_uppercase

import pytest

from .exception import NotASCIIUppercaseLetterError
from .helper import get_letter_index as index
from .plug_board import Plug, PlugBoard


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
        self, left, right
    ) -> None:
        with pytest.raises(NotASCIIUppercaseLetterError):
            Plug(left, right)


class PlugBoardTest:
    @pytest.mark.parametrize("letter", ascii_uppercase)
    def test_plug_board_should_not_permute_letters_when_init_without_plug(
        self,
        letter,
    ) -> None:
        plug_board = PlugBoard()

        assert plug_board.permute(index(letter)) == index(letter)

    def test_plug_board_should_permute_plug_letters(self) -> None:
        plug_board = PlugBoard(Plug("A", "I"))

        assert plug_board.permute(index("A")) == index("I")
        assert plug_board.permute(index("I")) == index("A")

    @pytest.mark.parametrize("letter", set(ascii_uppercase) - {"A", "I"})
    def test_plug_board_should_not_permute_letters_when_not_plug_letters(
        self,
        letter,
    ) -> None:
        plug_board = PlugBoard(Plug("A", "I"))

        assert plug_board.permute(index(letter)) == index(letter)

    def test_plug_board_should_permute_plug_letters_with_two_plugs(
        self,
    ) -> None:
        plug_board = PlugBoard(Plug("A", "I"), Plug("B", "Z"))

        assert plug_board.permute(index("A")) == index("I")
        assert plug_board.permute(index("I")) == index("A")
        assert plug_board.permute(index("B")) == index("Z")
        assert plug_board.permute(index("Z")) == index("B")

    @pytest.mark.parametrize(
        "letter", set(ascii_uppercase) - {"A", "I", "B", "Z"}
    )
    def test_plug_board_should_not_permute_letters_when_not_plug_letters(
        self,
        letter,
    ) -> None:
        plug_board = PlugBoard(Plug("A", "I"), Plug("B", "Z"))

        assert plug_board.permute(index(letter)) == index(letter)

    def test_init_should_raise_when_pass_duplicated_plug(self) -> None:
        with pytest.raises(ValueError, match=".*duplicate.*"):
            PlugBoard(Plug("A", "I"), Plug("I", "A"))

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
            )
