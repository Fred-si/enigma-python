from collections.abc import Iterable
from enum import Enum, StrEnum, auto
from typing import Sequence

from enigma.display.symbol import Symbol


class Align(StrEnum):
    LEFT = "<"
    CENTER = "^"
    RIGHT = ">"


class Box:
    def __init__(
        self,
        lines: Sequence[str],
        *,
        align: Align = Align.LEFT,
        line_spacing: int = 0,
        border: bool = False,
        padding: int = 0,
    ) -> None:
        self._lines = lines
        self._align = align
        self._line_spacing = line_spacing
        self._border = border
        self._padding = padding

    @property
    def width(self) -> int:
        return max(len(line) for line in self._lines)

    @property
    def lines(self) -> Iterable[str]:
        if self._border:
            yield self.top_border
        if self._padding:
            yield self.format_line("")

        for idx, line in enumerate(self._lines):
            if idx != 0:
                for _ in range(self._line_spacing):
                    yield self.format_line("")
            yield self.format_line(line)

        if self._padding:
            yield self.format_line("")
        if self._border:
            yield self.bottom_border

    def format_line(self, line: str) -> str:
        format_ = f"{{border}}{{padding}}{{line: {self._align}{self.width}}}{{padding}}{{border}}"

        return format_.format(
            line=line,
            border=Symbol.VERTICAL_BAR * self._border,
            padding=" " * self._padding,
        )

    @property
    def top_border(self) -> str:
        return self.horizontal_border.format(
            left_corner=Symbol.TOP_LEFT_CORNER,
            right_corner=Symbol.TOP_RIGHT_CORNER,
        )

    @property
    def bottom_border(self) -> str:
        return self.horizontal_border.format(
            left_corner=Symbol.BOTTOM_LEFT_CORNER,
            right_corner=Symbol.BOTTOM_RIGHT_CORNER,
        )

    @property
    def horizontal_border(self) -> str:
        return f"{{left_corner}}{Symbol.HORIZONTAL_BAR*(self.width+self._padding*2)}{{right_corner}}"
