import pytest

from itertools import chain, permutations, product
from typing import Any
from collections.abc import Iterable

from enigma import Enigma, EnigmaConfig
from enigma.available import AvailableReflector


def get_rotors_config(
    rotor_places: Iterable[str],
    initial_rotor_positions: Iterable[str],
) -> Iterable[str]:
    rotor_places = iter(rotor_places)
    initial_rotor_positions = iter(initial_rotor_positions)

    while True:
        try:
            yield ":".join((next(rotor_places), next(initial_rotor_positions)))
        except StopIteration:
            return


def get_rotors() -> Iterable[str]:
    for r in permutations(("II1930", "IIIC", "I1930")):
        for p in chain(product("ABC", repeat=3), ("UXL",)):
            yield " ".join(get_rotors_config(r, p))


def get_plugin_board() -> Iterable[str]:
    yield from ("", "AI", "JK", "AI JK", "AI PU BM", "MN AH JR CQ")


def get_reflectors() -> Iterable[str]:
    for reflector in AvailableReflector.get_normal_reflectors():
        yield f"{reflector.name}:A"


def get_test_conf() -> Iterable[tuple[str, str, str]]:
    return product(
        get_rotors(),
        get_reflectors(),
        get_plugin_board(),
    )


@pytest.mark.parametrize(
    ("rotors", "reflector", "plugin_board"),
    get_test_conf(),
)
def test_equality(rotors: str, reflector: str, plugin_board: str) -> None:
    message = "AHAHAHJEVOUSAIBIENNIQUE"

    encoded = encode(
        message,
        rotors,
        reflector,
        plugin_board,
    )
    decoded = encode(
        encoded,
        rotors,
        reflector,
        plugin_board,
    )

    assert decoded == "AHAH AHJE VOUS AIBI\nENNI QUE"


@pytest.mark.parametrize(
    ("rotors", "reflector", "plugin_board"),
    get_test_conf(),
)
def test_snapshot(
    rotors: str,
    reflector: str,
    plugin_board: str,
    snapshot: Any,
) -> None:
    message = "AHAHAHJEVOUSAIBIENNIQUE"

    encoded = encode(
        message,
        rotors,
        reflector,
        plugin_board,
    )

    assert encoded.strip() == snapshot


@pytest.mark.parametrize(
    "config",
    (EnigmaConfig.generate_random_config(10).as_dict() for _ in range(100)),
)
def test_random_equality(config: dict[str, str]) -> None:
    message = "AHAHAHJEVOUSAIBIENNIQUE"

    encoded = encode(message, **config)
    decoded = encode(encoded, **config)

    assert decoded == "AHAH AHJE VOUS AIBI\nENNI QUE"


def test_equality_with_thin_rotor() -> None:
    message = "AHAHAHJEVOUSAIBIENNIQUE"
    config = {
        "rotors": "II1930:U IIIC:X I1930:L BETA:A",
        "plugin_board": "MN AH JR CQ",
        "reflector": "REFBTHIN:A",
    }

    encoded = encode(message, **config)
    decoded = encode(encoded, **config)

    assert decoded == "AHAH AHJE VOUS AIBI\nENNI QUE"


def encode(
    message: str,
    rotors: str,
    reflector: str,
    plugin_board: str,
) -> str:
    config = EnigmaConfig.parse(
        rotors,
        reflector,
        plugin_board,
    )
    return Enigma(config).encode_message(message)
