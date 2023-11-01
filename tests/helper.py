from string import ascii_uppercase


def index(letter: str) -> int:
    assert len(letter) == 1

    return ord(letter) - 65
