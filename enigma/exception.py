from typing import Any


class NotASCIILetterError(ValueError):
    def __init__(self, value: Any) -> None:
        super().__init__(f'"{value}" is not an ASCII letter.')


class NotASCIIUppercaseLetterError(ValueError):
    def __init__(self, value: Any) -> None:
        super().__init__(f'"{value}" is not an ASCII uppercase letter.')
