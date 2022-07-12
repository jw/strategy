"""The Strategy players."""
from enum import Enum, auto


class Colour(Enum):
    """The colour can be `RED` or `BLUE`."""

    BLUE = auto()  # blue is on top
    RED = auto()  # red is on bottom
