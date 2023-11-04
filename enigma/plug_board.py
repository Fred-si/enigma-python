from dataclasses import dataclass

from enigma.exception import NotASCIIUppercaseLetterError
from enigma.helper import get_letter_index, is_single_ascii_uppercase_letter


@dataclass(frozen=True)
class Plug:
    left: str
    right: str

    def __post_init__(self) -> None:
        if not is_single_ascii_uppercase_letter(self.left):
            raise NotASCIIUppercaseLetterError(self.left)

        if not is_single_ascii_uppercase_letter(self.right):
            raise NotASCIIUppercaseLetterError(self.right)


class PlugBoard:
    def __init__(self, *plugs: Plug) -> None:
        if len(plugs) > 10:
            msg = f"PlugBoard can't contain more than 10 plug, {len(plugs)} given"
            raise ValueError(msg)

        self._plugs: dict[int, int] = {}
        for plug in plugs:
            left = get_letter_index(plug.left)
            right = get_letter_index(plug.right)

            if left in self._plugs or right in self._plugs:
                msg = f'"{plug}" is duplicated'
                raise ValueError(msg)

            self._plugs[left] = right
            self._plugs[right] = left

    def permute(self, letter: int) -> int:
        if not self._plugs:
            return letter

        letter = self._plugs.get(letter, letter)

        return letter
