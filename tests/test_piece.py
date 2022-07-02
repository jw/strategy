import pytest

from strategy.exceptions import InvalidOperationError
from strategy.pieces import BOMB, FLAG, MARSHAL, MINER, PIECES, SCOUT, SPY, Piece


def test_pieces():
    assert len(PIECES) == 40


def test_attack():
    assert Piece(MARSHAL, 10).attack(Piece(FLAG, 0)) is True
    assert Piece(MINER, 6).attack(Piece(BOMB, 11)) is True
    assert Piece(SCOUT, 2).attack(Piece(MARSHAL, 10)) is False
    assert Piece(MARSHAL, 10).attack(Piece(BOMB, 11)) is False
    assert Piece(SPY, 1).attack(Piece(BOMB, 11)) is False
    assert Piece(SPY, 1).attack(Piece(MARSHAL, 10)) is True
    assert Piece(SPY, 1).attack(Piece(SPY, 1)) is None
    assert Piece(MARSHAL, 10).attack(Piece(MARSHAL, 10)) is None

    with pytest.raises(InvalidOperationError):
        Piece(BOMB, 0).attack(Piece(MINER, 10))
    with pytest.raises(InvalidOperationError):
        Piece(FLAG, 0).attack(Piece(BOMB, 10))


def test_can_attack():
    assert not Piece(FLAG, 0).can_attack()
    assert not Piece(BOMB, 0).can_attack()
    assert Piece(MINER, 0).can_attack()
