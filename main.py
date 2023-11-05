from typing import TypeVar

from enigma import Enigma, EnigmaConfig

T = TypeVar("T")


if __name__ == "__main__":
    message = "AHAHAHJEVOUSAIBIENNIQUE"
    config = EnigmaConfig.parse(
        rotors="II1930:U IIIC:X I1930:L",
        plugin_board="MN AH JR CQ",
        reflector="UKW:A",
    )
    encoded = Enigma(config).encode_message(message)
    decoded = Enigma(config).encode_message(encoded)

    if message != decoded.replace(" ", "").replace("\n", ""):
        raise ValueError

    print(encoded)
