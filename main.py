from collections.abc import Iterable
from random import choice, choices
from string import ascii_uppercase
from typing import Any, Collection, TypeVar

from enigma import Enigma, RotorConfig, Plug
from enigma.available import AvailableRotor, AvailableReflector
from enigma.helper import get_letter_from_index

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
        RotorConfig(AvailableReflector[reflector], "A"),
        *(Plug(*plug) for plug in plugin_board.split()),
        debug=debug,
    )


def get_rotors(
    rotor_places: Iterable[AvailableRotor],
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
        "reflector": choice(list(get_available_reflectors())),
    }


def get_random_plugs(plug_count: int) -> str:
    if plug_count > 10:
        raise ValueError

    return " ".join(
        "".join(chunk)
        for chunk in chunks(choices_unique(ascii_uppercase, plug_count * 2), 2)
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


def choices_unique(iterable: Iterable[T], k=0) -> list[T]:
    iterable = list(iterable)
    ret: list[str] = []
    for _ in range(k):
        ret.append(iterable.pop(choice(range(len(iterable)))))

    return ret


def chunks(lst: Collection[T], n: int) -> Iterable[Collection[T]]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


if __name__ == "__main__":
    config = {
        "rotor_places": "II1930 IIIC I1930",
        "initial_rotor_positions": "20 23 11",
        "plugin_board": "MN AH JR CQ",
        "reflector": "UKW",
    }
    message = "AHAHAHJEVOUSAIBIENNIQUE"
    e = get_enigma_from_config(**config, debug=True).encode_message(message)

    if message != get_enigma_from_config(**config).encode_message(e):
        raise ValueError
    print(config)
    print(" ".join(chunks(e, 4)))
