"""The Strategy players."""
from enum import Enum, auto


class Player(Enum):
    """The Player can be `RED` or `BLUE`."""

    BLUE = auto()  # blue is on top
    RED = auto()  # red is on bottom
    UNKNOWN = auto()  # only used in the PIECES constant
