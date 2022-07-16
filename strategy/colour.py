"""The Strategy players."""
from enum import Enum, auto


class Colour(Enum):
    """The colour can be `RED` or `BLUE`."""

    BLUE = auto()  # blue is on top
    RED = auto()  # red is on bottom

    def __str__(self) -> str:
        """Beautify the name."""
        return self.name.lower()
