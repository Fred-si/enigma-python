from typing import Any

import pytest


from enigma import EnigmaConfig

from . import encode, get_test_conf


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
