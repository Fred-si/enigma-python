from string import ascii_uppercase

import pytest

from .exception import NotASCIIUppercaseLetterError
from .helper import is_single_ascii_uppercase_letter, get_letter_index


class IsSingleASCIIUppercaseLetterTest:
    @pytest.mark.parametrize("letter", ascii_uppercase)
    def test_with_ascii_uppercase_letter_should_return_true(
        self, letter
    ) -> None:
        assert is_single_ascii_uppercase_letter(letter)

    def test_with_empty_string_should_return_false(self) -> None:
        assert not is_single_ascii_uppercase_letter("")

    def test_with_two_char_should_return_false(self) -> None:
        assert not is_single_ascii_uppercase_letter("AB")

    def test_with_non_ascii_uppercase_letter_should_return_false(self) -> None:
        assert not is_single_ascii_uppercase_letter("a")


class GetLetterIndexTest:
    @pytest.mark.parametrize(
        ("expected_index", "letter"), enumerate(ascii_uppercase)
    )
    def test_should_return_letter_index(
        self,
        letter: str,
        expected_index: int,
    ) -> None:
        assert get_letter_index(letter) == expected_index

    @pytest.mark.parametrize("letter", ["", "a", "AB"])
    def test_function_should_raise_when_called_without_single_ascii_uppercase_letter(
        self, letter: str
    ) -> None:
        with pytest.raises(NotASCIIUppercaseLetterError):
            get_letter_index(letter)
