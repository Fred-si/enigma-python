from collections.abc import Iterable
from random import choice, choices
from string import ascii_uppercase
from typing import TypeVar

from enigma import Enigma, RotorConfig, ReflectorConfig, Plug
from enigma.available import AvailableRotor, AvailableReflector
from enigma.helper import batched, get_letter_from_index
from enigma.plug_board import PlugBoard

T = TypeVar("T")


def get_enigma_from_config(
    rotor_places: str,
    initial_rotor_positions: str,
    plugin_board: str,
    reflector: str,
    *,
    debug: bool = False,
) -> Enigma:
    return Enigma(
        get_rotors(
            rotor_places.split(),
            map(int, initial_rotor_positions.split()),
        ),
        ReflectorConfig(AvailableReflector[reflector], "A"),
        *(Plug(*plug) for plug in plugin_board.split()),
        debug=debug,
    )


def get_rotors(
    rotor_places: Iterable[str],
    initial_rotor_positions: Iterable[int],
) -> Iterable[RotorConfig]:
    rotor_places = iter(rotor_places)
    initial_rotor_positions = iter(initial_rotor_positions)

    while True:
        try:
            yield RotorConfig(
                AvailableRotor[next(rotor_places)],
                get_letter_from_index(next(initial_rotor_positions)),
            )
        except StopIteration:
            return


def get_random_config(plug_count: int) -> dict[str, str]:
    return {
        "rotor_places": " ".join(choices_unique(AvailableRotor.names(), k=3)),
        "initial_rotor_positions": " ".join(map(str, choices(range(25), k=3))),
        "plugin_board": get_random_plugs(plug_count),
        "reflector": choice(list(get_available_reflectors())).name,
    }


def get_random_plugs(plug_count: int) -> str:
    if plug_count > PlugBoard.MAX_PLUG_COUNT:
        raise ValueError

    return " ".join(
        "".join(chunk)
        for chunk in batched(choices_unique(ascii_uppercase, plug_count * 2), 2)
    )


def get_available_reflectors() -> Iterable[AvailableReflector]:
    forbidden_reflectors = {
        AvailableReflector.BETA,
        AvailableReflector.GAMMA,
        AvailableReflector.ETW,
    }

    for reflector in AvailableReflector:
        if reflector not in forbidden_reflectors:
            yield reflector


def choices_unique(iterable: Iterable[T], k: int = 0) -> list[T]:
    lst = list(iterable)
    ret: list[T] = []
    for _ in range(k):
        ret.append(lst.pop(choice(range(len(lst)))))

    return ret


if __name__ == "__main__":
    config = {
        "rotor_places": "II1930 IIIC I1930",
        "initial_rotor_positions": "20 23 11",
        "plugin_board": "MN AH JR CQ",
        "reflector": "UKW",
    }
    message = "AHAHAHJEVOUSAIBIENNIQUE"
    e = get_enigma_from_config(**config, debug=True).encode_message(message)

    if message != get_enigma_from_config(**config).encode_message(e):  # type: ignore[arg-type]
        raise ValueError

    print(config)
    print(" ".join("".join(b) for b in batched(e, 4)))
