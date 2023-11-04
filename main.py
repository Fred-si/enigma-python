from collections.abc import Iterable
from random import choice, choices
from string import ascii_uppercase
from typing import TypeVar

from enigma import Enigma
from enigma.available import AvailableRotor, AvailableReflector
from enigma.helper import batched
from enigma.plug_board import PlugBoard

T = TypeVar("T")


def get_random_config(plug_count: int) -> dict[str, str]:
    reflector = choice(
        [r.name for r in AvailableReflector.get_normal_reflectors()],
    )
    return {
        "rotors": " ".join(get_random_rotors_config()),
        "reflector": f"{reflector}:A",
        "plugin_board": get_random_plugs(plug_count),
    }


def get_random_rotors_config() -> Iterable[str]:
    rotors = iter(
        choices_unique(
            (r.name for r in AvailableRotor.get_normal_rotors()),
            k=3,
        ),
    )
    positions = iter(choices(ascii_uppercase, k=3))

    while True:
        try:
            yield f"{next(rotors)}:{next(positions)}"
        except StopIteration:
            break


def get_random_plugs(plug_count: int) -> str:
    if plug_count > PlugBoard.MAX_PLUG_COUNT:
        raise ValueError

    return " ".join(
        "".join(chunk)
        for chunk in batched(choices_unique(ascii_uppercase, plug_count * 2), 2)
    )


def choices_unique(iterable: Iterable[T], k: int = 0) -> list[T]:
    lst = list(iterable)
    ret: list[T] = []
    for _ in range(k):
        ret.append(lst.pop(choice(range(len(lst)))))

    return ret


if __name__ == "__main__":
    config = {
        "rotors": "II1930:U IIIC:X I1930:L",
        "plugin_board": "MN AH JR CQ",
        "reflector": "UKW:A",
    }
    message = "AHAHAHJEVOUSAIBIENNIQUE"
    e = Enigma.get_from_str_config(**config, debug=True).encode_message(message)

    if message != Enigma.get_from_str_config(**config).encode_message(e):  # type: ignore[arg-type]
        raise ValueError

    print(config)
    print(" ".join("".join(b) for b in batched(e, 4)))
