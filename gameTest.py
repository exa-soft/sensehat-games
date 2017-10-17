# basic game "window" and"window collection" module

#from sense_hat import SenseHat
from sense_emu import SenseHat
from cores.game import GameWindow, GameWindowGrid
import logging
#import time
#from exceptions import ArgumentError

def simple_test():
    """only 2 games* top and bottom"""
    
    grid = GameWindowGrid (1, 2)
    game1 = GameWindow('Top-Above')
    game2 = GameWindow('Bottom-Below')
    
    grid.set_game (0, 0, game1)
    grid.set_game (0, 1, game2)
    grid.start ()



if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    simple_test ()

