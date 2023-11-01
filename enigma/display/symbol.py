from enum import StrEnum


class Symbol(StrEnum):
    VERTICAL_BAR = "│"
    HORIZONTAL_BAR = "─"
    TOP_LEFT_CORNER = "┌"
    TOP_RIGHT_CORNER = "┐"
    TOP_T = "┬"
    BOTTOM_LEFT_CORNER = "└"
    BOTTOM_RIGHT_CORNER = "┘"
    BOTTOM_T = "┴"
    LEFT_T = "├"
    RIGHT_T = "┤"
    CROSS = "┼"
