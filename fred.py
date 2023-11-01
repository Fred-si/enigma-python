from collections.abc import Iterable
from enum import StrEnum
from random import choice, choices
from string import ascii_uppercase
from typing import Any, Collection, TypeVar

from enigma import Enigma, RotorConfig, Plug
from enigma.available import AvailableRotor as AvailableRotor, AvailableReflector as AvailableReflector
from enigma.helper import get_letter_from_index

from kirino import Enigma as Kirino

T = TypeVar("T")


def get_enigma_from_config(
    rotor_places: str = "II1930 IIIC I1930",
    initial_rotor_positions: str = "5 22 17",
    plugin_board: str = "AB BC DE FG HI JK LM NO PQ RS",
    reflector: AvailableReflector = AvailableReflector.UKW.name,
    *,
    debug: bool = False
) -> Enigma:
    return Enigma(
        *get_rotors(
            rotor_places.split(), to_int(initial_rotor_positions.split())
        ),
        RotorConfig(AvailableReflector[reflector], "A"),
        *get_plugs(plugin_board.split()),
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


def get_plugs(plugin_board: Iterable[str]) -> Iterable[Plug]:
    for plug in plugin_board:
        yield Plug(*plug)


def to_int(iterable: Iterable[Any]) -> Iterable[int]:
    return (int(i) for i in iterable)


def get_random_config(plug_count: int) -> dict[str, str]:
    return {
        "rotor_places": " ".join(
            map(str, choices_unique(range(len(Kirino.available_rotor)), k=3))
        ),
        "initial_rotor_positions": " ".join(map(str, choices(range(25), k=3))),
        "plugin_board": get_random_plugs(plug_count),
    }


def get_random_plugs(plug_count: int) -> str:
    if plug_count > 10:
        raise ValueError

    return " ".join(
        "".join(chunk)
        for chunk in chunks(choices_unique(ascii_uppercase, plug_count * 2), 2)
    )


def choices_unique(iterable: Iterable[T], k=0) -> list[T]:
    iterable = list(iterable)
    ret: list[str] = []
    for _ in range(k):
        ret.append(iterable.pop(choice(range(len(iterable)))))

    return ret


def chunks(lst: Collection[Any], n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


if __name__ == "__main__":
    # config = get_random_config(10)
    config = {
        'rotor_places': 'II1930 IIIC I1930',
        'initial_rotor_positions': '14 6 24',
        'plugin_board': 'MN AH JR CQ',
        'reflector': 'BETA',
    }
    message = "AHAHAHJEVOUSAIBIENNIQUE"
    e = get_enigma_from_config(**config, debug=True).encode_message(message)

    if message != get_enigma_from_config(**config).encode_message(e):
        raise ValueError
    print(config)
    print(" ".join(chunks(e, 4)))
