import pytest

from itertools import permutations, product
from typing import Any
from collections.abc import Iterable

from string import ascii_uppercase

from enigma.available import AvailableReflector
from main import get_random_config


def joined_permutation(
    iterable: Iterable[Any],
    r: int | None = None,
    char: str = " ",
) -> Iterable[str]:
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
        yield from joined_permutation(pairs, r=pair_count)


def get_plugin_board() -> Iterable[str]:
    yield from ("", "AI", "JK", "AI JK", "AI PU BM", "MN AH JR CQ")


def get_reflectors() -> Iterable[AvailableReflector]:
    thin_reflectors = set(AvailableReflector.get_thin_reflectors())
    for reflector in AvailableReflector:
        if reflector not in thin_reflectors:
            yield reflector


def get_test_conf() -> Iterable[tuple[str, str, str, str]]:
    return product(
        get_rotors(),
        get_initial_rotor_positions(),
        get_plugin_board(),
        (r.name for r in get_reflectors()),
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

    assert decoded == "AHAH AHJE VOUS AIBI\nENNI QUE"


@pytest.mark.parametrize(
    ("rotor_places", "initial_rotor_positions", "plugin_board", "reflector"),
    get_test_conf(),
)
def test_snapshot(
    rotor_places: str,
    initial_rotor_positions: str,
    plugin_board: str,
    reflector: AvailableReflector,
    snapshot: Any,
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


@pytest.mark.parametrize(
    "config",
    (get_random_config(10) for _ in range(1_000)),
)
def test_random_equality(config: dict[str, str]) -> None:
    message = "AHAHAHJEVOUSAIBIENNIQUE"

    encoded = encode(message, **config)
    decoded = encode(encoded, **config)

    assert decoded == "AHAH AHJE VOUS AIBI\nENNI QUE"


def test_equality_with_thin_rotor() -> None:
    message = "AHAHAHJEVOUSAIBIENNIQUE"
    config = {
        "rotor_places": "II1930 IIIC I1930 BETA",
        "initial_rotor_positions": "20 23 11 0",
        "plugin_board": "MN AH JR CQ",
        "reflector": "REFBTHIN",
    }

    encoded = encode(message, **config)
    decoded = encode(encoded, **config)

    assert decoded == "AHAH AHJE VOUS AIBI\nENNI QUE"


def encode(
    message: str,
    rotor_places: str,
    initial_rotor_positions: str,
    plugin_board: str,
    reflector: str,
) -> str:
    from main import get_enigma_from_config

    return get_enigma_from_config(
        rotor_places,
        initial_rotor_positions,
        plugin_board,
        reflector,
    ).encode_message(message)
