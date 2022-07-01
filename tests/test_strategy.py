"""First test."""
from strategy.game import Board, Empty, Lake


def test_board():
    board = Board()
    assert len(board) == 10 * 10
    assert board[1, 2] == Empty
    assert board[2, 4] == Lake
    assert board[4, 2] == Empty


def test_board_str():
    board = Board()
    assert "[4|2: <lake>]" in str(board)
    assert "[6|6: <empty>]" in str(board)
