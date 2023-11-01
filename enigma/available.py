from collections.abc import Iterable
from enum import StrEnum, unique
from string import ascii_uppercase


def _validate(enum: StrEnum) -> StrEnum:
    unique(enum)

    for e in enum:
        if len(e) != len(set(e)):
            msg = f"{enum}.{e.name} contain more the same letter several times."
            raise ValueError(msg)

        if not all(l in ascii_uppercase for l in e):
            msg = f"{enum}.{e.name} not contain only ASCII uppercase letters."
            raise ValueError(msg)

    return enum


class _Available(StrEnum):
    @classmethod
    def names(cls) -> Iterable[str]:
        for item in cls:
            yield item.name


@_validate
class AvailableRotor(_Available):
    IC = "DMTWSILRUYQNKFEJCAZBPGXOHV"
    IIC = "HQZGPJTMOBLNCIFDYAWVEUSRKX"
    IIIC = "UQNTLSZFMREHDPXKIBVYGJCWOA"
    I = "JGDQOXUSCAMIFRVTPNEWKBLZYH"
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


@_validate
class AvailableReflector(_Available):
    UKW = "QYHOGNECVPUZTFDJAXWMKISRBL"
    ETW = "QWERTZUIOASDFGHJKPYXCVBNML"
    UKWK = "IMETCGFRAYSQBZXWLHKDVUPOJN"
    BETA = "LEYJVCNIXWPBQMDRTAKZGFUHOS"
    GAMMA = "FSOKANUERHMBTIYCWLQPZXVGJD"
    REFA = "EJMZALYXVBWFCRQUONTSPIKHGD"
    REFB = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
    REFC = "FVPJIAOYEDRZXWGCTKUQSBNMHL"
    REFBTHIN = "ENKQAUYWJICOPBLMDXZVFTHRGS"
    REFCTHIN = "RDOBJNTKVEHMLFCWZAXGYIPSUQ"
    REFETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
