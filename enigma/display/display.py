from time import sleep
from typing import Final

from .box import Align, Box
from .curses_adapter import CursesAdapter, FKey, CtrlKey
from .symbol import Symbol

KEYBOARD = (
    "QWERTZUIO",
    "ASDFGHJK",
    "PYXCVBNML",
)

KEYS = [
    " ".join((f"{Symbol.VERTICAL_BAR}{k}{Symbol.VERTICAL_BAR}" for k in line))
    for line in KEYBOARD
]

BOX = Box(
    lines=KEYS,
    align=Align.CENTER,
    line_spacing=1,
    border=True,
    padding=1,
)


class Display:
    quit_keys: Final = {CtrlKey.Q, FKey.F10}
    refresh_keys: Final = {CtrlKey.R}

    def __init__(self) -> None:
        self._curses = CursesAdapter()

    def loop(self) -> None:
        self._curses.print(0, 0, "Hello world!")
        for idx, line in enumerate(BOX.lines):
            self._curses.print(5, 5 + idx, line)

        try:
            while True:
                self._process_keyboard_inputs()
                sleep(0.1)

        except KeyboardInterrupt:
            return

        except Exit:
            return

    def _repaint(self) -> None:
        raise NotImplementedError

    def _print(self, key: str) -> None:
        self._curses.print(5, 5, key)

    def _process_keyboard_inputs(self) -> None:
        for key in self._curses.get_keys():
            key = key.strip()
            if key in self.quit_keys:
                raise Exit

            if key in self.refresh_keys:
                self._repaint()

            try:
                self._print(f"{key}: {ord(key)}")
            except TypeError:
                self._print(key)


class Exit(Exception):
    pass
