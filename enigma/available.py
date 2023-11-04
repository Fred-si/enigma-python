from collections.abc import Iterable
from enum import StrEnum, unique
from string import ascii_uppercase


def _validate(enum: type[StrEnum]) -> type[StrEnum]:
    unique(enum)

    for e in enum:
        if len(e) != len(ascii_uppercase):
            msg = (
                f"{enum}.{e.name} contain {len(e)}"
                f" letters instead of {len(ascii_uppercase)}"
            )
            raise ValueError(msg)

        if len(e) != len(set(e)):
            msg = f"{enum}.{e.name} contain same letter several times."
            raise ValueError(msg)

        if not all(letter in ascii_uppercase for letter in e):
            msg = f"{enum}.{e.name} not contain only ASCII uppercase letters."
            raise ValueError(msg)

    return enum


@_validate
class AvailableRotor(StrEnum):
    IC = "DMTWSILRUYQNKFEJCAZBPGXOHV"
    IIC = "HQZGPJTMOBLNCIFDYAWVEUSRKX"
    IIIC = "UQNTLSZFMREHDPXKIBVYGJCWOA"
    I = "JGDQOXUSCAMIFRVTPNEWKBLZYH"  # noqa: E741 (Ambiguous variable name: `I`)
    II = "NTZPSFBOKMWRCJDIVLAEYUXHGQ"
    III = "JVIUBHTCDYAKEQZPOSGXNRMWFL"
    IK = "PEZUOHXSCVFMTBGLRINQJWAYDK"
    IIK = "ZOUESYDKFWPCIQXHMVBLGNJRAT"
    IIIK = "EHRVXGAOBQUSIMZFLYNWKTPDJC"
    I1930 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
    II1930 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
    III1930 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
    IV1938 = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
    V1938 = "VZBRGITYUPSDNHLXAWMJQOFECK"
    VI1939 = "JPGVOUMFYQBENHZRDKASXLICTW"
    VII1939 = "NZJHGRCXMYSWBOUFAIVLPEKQDT"
    VIII1939 = "FKQHTLXOCBJSPDZRAMEWNIUYGV"

    # Thin rotors
    BETA = "LEYJVCNIXWPBQMDRTAKZGFUHOS"
    GAMMA = "FSOKANUERHMBTIYCWLQPZXVGJD"

    @classmethod
    def get_thin_rotors(cls) -> set["AvailableRotor"]:
        return {
            cls.BETA,
            cls.GAMMA,
        }

    @classmethod
    def get_normal_rotors(cls) -> set["AvailableRotor"]:
        thin_rotors = cls.get_thin_rotors()

        return {r for r in cls if r not in thin_rotors}


@_validate
class AvailableReflector(StrEnum):
    UKW = "QYHOGNECVPUZTFDJAXWMKISRBL"
    UKWK = "IMETCGFRAYSQBZXWLHKDVUPOJN"
    REFA = "EJMZALYXVBWFCRQUONTSPIKHGD"
    REFB = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    REFC = "FVPJIAOYEDRZXWGCTKUQSBNMHL"

    # Thin reflectors
    REFBTHIN = "ENKQAUYWJICOPBLMDXZVFTHRGS"
    REFCTHIN = "RDOBJNTKVEHMLFCWZAXGYIPSUQ"

    @classmethod
    def get_thin_reflectors(cls) -> Iterable["AvailableReflector"]:
        return {
            cls.REFBTHIN,
            cls.REFCTHIN,
        }

    @classmethod
    def get_normal_reflectors(cls) -> set["AvailableReflector"]:
        thin_reflectors = cls.get_thin_reflectors()

        return {r for r in cls if r not in thin_reflectors}
