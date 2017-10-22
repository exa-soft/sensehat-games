"""Test for basic game "window" and"window collection" module."""

__author__ = 'Edith Birrer
__version__ = '0.2'


import logging
#import time
#from sense_hat import SenseHat
from sense_emu import SenseHat
from .game import GameWindow, GameWindowGrid
#from exceptions import ArgumentError

def simple_test():
    """only 2 games: top and bottom."""
    
    grid = GameWindowGrid (1, 2)
    logging.debug (grid.games)
    game1 = GameWindow('Top-Above')
    game2 = GameWindow('Bottom-Below')
    
    grid.set_game (0, 0, game1)
    grid.set_game (0, 1, game2)
    grid.start ()


def _test():
    simpleTest()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    simple_test ()

