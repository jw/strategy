"""Strategy main module."""

import logging

from strategy.board import Board
from strategy.player import Player

log = logging.getLogger(__name__)

if __name__ == "__main__":
    log.warning("Strategy started.")
    board = Board()
    board.create_random_pieces(Player.RED)
    board.create_random_pieces(Player.BLUE)
    log.warning("Created random board.")
