from collections.abc import Iterable
from itertools import chain, permutations, product

from enigma import AvailableReflector, Enigma, EnigmaConfig


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
