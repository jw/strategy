"""The Strategy exceptions."""


class InvalidOperationError(Exception):
    """Invalid operation."""

    pass


class InvalidDimensionsError(Exception):
    """Invalid dimension."""

    pass


class NoPieceError(Exception):
    """Invalid piece."""

    pass


class InvalidCoordinateError(Exception):
    """Invalid coordinate given."""

    pass


class InvalidDestinationError(Exception):
    """Invalid destination given."""

    pass
