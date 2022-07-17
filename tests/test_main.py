from unittest.mock import patch

import pytest

from strategy.board import Board
from strategy.colour import Colour
from strategy.main import main, show_moves, turn


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


def test_main_show_moves(capsys):
    moves = [
        (Colour.RED, (6, 7), (5, 7)),
        (Colour.RED, (5, 7), (3, 7)),
        (Colour.RED, (2, 7), (3, 7)),
        (Colour.RED, (3, 7), (4, 7)),
    ]
    show_moves(moves)
    captured = capsys.readouterr()
    assert captured.out == (
        "     red: x=6, y=7 -> x=5, y=7\n"
        "     red: x=5, y=7 -> x=3, y=7\n"
        "     red: x=2, y=7 -> x=3, y=7\n"
        "     red: x=3, y=7 -> x=4, y=7\n"
    )


@patch("strategy.main.turn", side_effect=SystemExit)
def test_main_main(turn, capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "Created random board.\n" in captured.out
