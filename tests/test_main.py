from unittest.mock import patch

import pytest

from strategy.board import Board
from strategy.colour import Colour
from strategy.main import main, turn


def test_main_turn_red(capsys):
    board = Board()
    board.create_random_pieces(Colour.RED)
    with pytest.raises(SystemExit):
        turn(board, Colour.RED)
        captured = capsys.readouterr()
        assert "Red wins the game!" in captured.out


def test_main_turn_blue(capsys):
    board = Board()
    board.create_random_pieces(Colour.BLUE)
    with pytest.raises(SystemExit):
        turn(board, Colour.BLUE)
        captured = capsys.readouterr()
        assert "Blue wins the game!" in captured.out


@patch("strategy.main.turn", side_effect=SystemExit)
def test_main_main(turn, capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Created random board.\n" in captured.out
