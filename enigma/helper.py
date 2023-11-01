from string import ascii_uppercase

from enigma.exception import NotASCIIUppercaseLetterError

_ascii_uppercase = set(ascii_uppercase)


def is_single_ascii_uppercase_letter(letter: str) -> bool:
    return len(letter) == 1 and letter in _ascii_uppercase


def get_letter_index(letter: str) -> int:
    if not is_single_ascii_uppercase_letter(letter):
        raise NotASCIIUppercaseLetterError(letter)

    return ord(letter) - 65


def get_letter_from_index(index: int) -> str:
    return ascii_uppercase[index]
