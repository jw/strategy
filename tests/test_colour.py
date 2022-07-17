from strategy.colour import Colour


def test_colour():
    c = Colour.RED
    assert f"{c}" == "red"
    assert f"{c!r}" == "<Colour.RED: 2>"
