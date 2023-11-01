import pytest

from itertools import permutations, product
from typing import Any, Iterable

from string import ascii_uppercase

from enigma.available import AvailableReflector
from main import get_random_config


def joined_permutation(iterable: Iterable[Any], r=None, char=" ") -> Iterable[str]:
    for p in permutations(iterable, r=r):
        yield char.join(p)


def get_rotors() -> Iterable[str]:
    yield from joined_permutation(("II1930", "IIIC", "I1930"))


def get_initial_rotor_positions() -> Iterable[str]:
    for p in product(range(3), repeat=3):
        yield " ".join([str(q) for q in p])

    yield "20 23 11"


def get_plug_choices() -> Iterable[str]:
    pairs = list(joined_permutation(ascii_uppercase, r=2, char=""))
    for pair_count in range(10, 11):
        for choices in joined_permutation(pairs, r=pair_count):
            yield choices


def get_plugin_board() -> Iterable[str]:
    yield from ("", "AI", "JK", "AI JK", "AI PU BM", "MN AH JR CQ")


def get_reflectors() -> Iterable[AvailableReflector]:
    forbidden_reflectors = {
        AvailableReflector.BETA,
        AvailableReflector.GAMMA,
        AvailableReflector.ETW,
    }
    for reflector in AvailableReflector:
        if reflector in forbidden_reflectors:
            continue

        yield reflector


def get_test_conf() -> Iterable[tuple[str, str, str, AvailableReflector]]:
    return product(
        get_rotors(),
        get_initial_rotor_positions(),
        get_plugin_board(),
        get_reflectors(),
    )


@pytest.mark.parametrize(
    ("rotor_places", "initial_rotor_positions", "plugin_board", "reflector"),
    get_test_conf(),
)
def test_equality(
    rotor_places: str,
    initial_rotor_positions: str,
    plugin_board: str,
    reflector: AvailableReflector,
) -> None:
    message = "AHAHAHJEVOUSAIBIENNIQUE"

    encoded = encode(
        message,
        rotor_places,
        initial_rotor_positions,
        plugin_board,
        reflector,
    )
    decoded = encode(
        encoded,
        rotor_places,
        initial_rotor_positions,
        plugin_board,
        reflector,
    )

    assert decoded == message


@pytest.mark.parametrize(
    ("rotor_places", "initial_rotor_positions", "plugin_board", "reflector"),
    get_test_conf(),
)
def test_snapshot(
    rotor_places: str,
    initial_rotor_positions: str,
    plugin_board: str,
    reflector: AvailableReflector,
    snapshot,
) -> None:
    message = "AHAHAHJEVOUSAIBIENNIQUE"

    encoded = encode(
        message,
        rotor_places,
        initial_rotor_positions,
        plugin_board,
        reflector,
    )

    assert encoded.strip() == snapshot


@pytest.mark.parametrize("_", range(10_000))
def test_random_equality(_) -> None:
    message = "AHAHAHJEVOUSAIBIENNIQUE"

    config = get_random_config(10)

    encoded = encode(message, **config)
    decoded = encode(encoded, **config)

    assert decoded == message


def encode(
    message: str,
    rotor_places: str,
    initial_rotor_positions: str,
    plugin_board: str,
    reflector: AvailableReflector,
) -> str:
    from main import get_enigma_from_config

    return get_enigma_from_config(
        rotor_places,
        initial_rotor_positions,
        plugin_board,
        reflector.name,
    ).encode_message(message)
