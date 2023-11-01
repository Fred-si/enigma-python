import curses
from enum import StrEnum
from typing import Any, Generator, Iterable


class FKey(StrEnum):
    F1 = "KEY_F(1)"
    F2 = "KEY_F(2)"
    F3 = "KEY_F(3)"
    F4 = "KEY_F(4)"
    F5 = "KEY_F(5)"
    F6 = "KEY_F(6)"
    F7 = "KEY_F(7)"
    F8 = "KEY_F(8)"
    F9 = "KEY_F(9)"
    F10 = "KEY_F(10)"
    F11 = "KEY_F(11)"
    F12 = "KEY_F(12)"


class CtrlKey(StrEnum):
    A = chr(1)
    B = chr(2)
    D = chr(4)
    E = chr(5)
    F = chr(6)
    G = chr(7)
    H = chr(8)

    N = chr(14)
    O = chr(15)
    P = chr(16)

    Q = chr(17)
    R = chr(18)
    S = chr(19)

    U = chr(21)
    V = chr(22)
    W = chr(23)
    X = chr(24)
    Y = chr(25)


class SingletonMeta(type):
    _instances: dict[type, Any] = {}

    def __call__(cls, *args: list[Any], **kwargs: dict[str, Any]) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance

        return cls._instances[cls]


class CursesAdapter(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._screen = curses.initscr()
        self._screen.keypad(True)  # noqa: FBT003

        # Make the call to getkey() non-blocking
        self._screen.nodelay(True)  # noqa: FBT003

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)  # Hide cursor

    def get_keys(self) -> Generator[str, None, None]:
        """Get keyboard inputs from last function call and return them."""
        try:
            while True:
                yield self.convert_key(self._screen.getkey())

        except curses.error:  # getkey() raise if no input
            pass

    def convert_key(self, key) -> FKey | CtrlKey | None:
        self.print(12, 5, "convert_key")
        for idx, enum in enumerate((FKey, CtrlKey)):
            try:
                return enum(key)
            except ValueError:
                pass

        return key

    def print(self, x: int, y: int, lines: str | Iterable[str]) -> None:
        if isinstance(lines, str):
            lines = [lines]

        for idx, line in enumerate(lines):
            self._screen.move(y + idx, x)
            self._screen.clrtoeol()

            self._print_string(line)

    def _print_string(self, string: Any) -> None:
        self._screen.addstr(str(string))

    def exit_(self) -> None:
        curses.nocbreak()
        curses.echo()
        self._screen.keypad(False)  # noqa: FBT003
        curses.endwin()
        curses.endwin()
