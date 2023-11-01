import pytest

from itertools import permutations, product, islice
from typing import Any, Iterable, TypeVar

from string import ascii_uppercase

def joined_permutation(iterable: Iterable[Any], r=None, char=' ') -> Iterable[str]:
    for p in permutations(iterable, r=r):
        yield char.join(p)

def get_rotor_choices() -> Iterable[str]:
    yield from joined_permutation("012")

def get_rotor_pos() -> Iterable[str]:
    for p in product(range(3), repeat=3):
        yield ' '.join([str(q) for q in p])

def get_plug_choices() -> Iterable[str]:
    pairs = list(joined_permutation(ascii_uppercase, r=2, char=""))
    for pair_count in range(10, 11):
        for choices in joined_permutation(pairs, r=pair_count):
            yield choices
def get_test_conf() -> Iterable[tuple[str, str, str]]:
    return product(
        get_rotor_choices(), ("","AI", "JK", "AI JK", "AI PU BM"), get_rotor_pos()
    )

@pytest.mark.skip
@pytest.mark.parametrize(
    ("rotor_choice", "plugin_board", "rotor_pos"),
    get_test_conf(),
)
def test_kirino(rotor_choice: str, plugin_board: str, rotor_pos: str, snapshot) -> None:
    message = "aaaaaah".upper()

    encoded = encode_kirino(message, rotor_choice, plugin_board, rotor_pos)

    assert encoded.strip() == snapshot

    decoded = encode_kirino(encoded, rotor_choice, plugin_board, rotor_pos)
    assert decoded == message


@pytest.mark.parametrize(
    ("rotor_choice", "plugin_board", "rotor_pos"),
    get_test_conf(),
)
def test_fred(rotor_choice: str, plugin_board: str, rotor_pos: str, snapshot) -> None:
    message = "aaaaaah".upper()

    encoded = encode_fred(message, rotor_choice, plugin_board, rotor_pos)

    assert encoded.strip() == snapshot

    decoded = encode_fred(encoded, rotor_choice, plugin_board, rotor_pos)
    assert decoded == message

@pytest.mark.skip
@pytest.mark.parametrize(
    ("rotor_choice", "plugin_board", "rotor_pos"),
    [('4 9 10', 'ZL RC WN JP KF IO HV ED GX MT', '20 23 11')],
    # get_test_conf(),
)
def test_versus(rotor_choice: str, plugin_board: str, rotor_pos: str) -> None:
    message = "AHAHAHJEVOUSAIBIENNIQUE"
    fred = encode_fred(message, rotor_choice, plugin_board, rotor_pos)
    kirino = encode_kirino(message, rotor_choice, plugin_board, rotor_pos)

    assert fred == kirino


def encode_kirino(
    message: str,
    rotor_choice: str,
    plugin_board: str,
    rotor_pos: str,
) -> str:
    from kirino import Enigma

    enigma = Enigma()
    enigma.set_initial_rotor_place(rotor_choice)
    enigma.set_plugin_board(plugin_board)
    enigma.set_initial_rotor_position(rotor_pos)

    return enigma.output_message(message)


def encode_fred(
    message: str,
    rotor_choice: str,
    plugin_board: str,
    rotor_pos: str,
) -> str:
    from fred import get_enigma_from_config

    return get_enigma_from_config(rotor_choice, rotor_pos, plugin_board).encode_message(message)
