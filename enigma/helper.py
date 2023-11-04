from itertools import islice
from string import ascii_uppercase
from typing import TypeVar
from collections.abc import Iterable

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


T = TypeVar("T")


def batched(iterable: Iterable[T], n: int) -> Iterable[tuple[T, ...]]:
    """
    Polyfill of python3.12 itertools.batched.

    https://docs.python.org/3/library/itertools.html#itertools.batched

    >>> list(batched('', 1))
    []

    >>> list(batched('a', 1))
    [('a',)]

    >>> list(batched('ab', 1))
    [('a',), ('b',)]

    >>> list(batched('ab', 2))
    [('a', 'b')]

    >>> list(batched('abc', 2))
    [('a', 'b'), ('c',)]
    """
    if n < 1:
        msg = f"n must be at least one, {n} given"
        raise ValueError(msg)

    it = iter(iterable)

    while batch := tuple(islice(it, n)):
        yield batch
