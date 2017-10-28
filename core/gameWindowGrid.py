"""This module contains the "window collection", which is an imaginary 
rectangle of several "GameWindows", each with its game, so the user can 
move from one to another by using the joystick. The whole can be used 
to implement games like "Keep talking and nobody explodes".

Usage:

1. Change width and height of the grid, if necessary.
2. Init each place of the grid with a game (with set_game()).  
3. Call start().  

"""

__author__ = 'Edith Birrer'
__version__ = '0.2'

import logging
import time
#from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from sense_emu import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause
from ..output import fieldScroller
from .exceptions import ArgumentError
from .game import GameWindow


sense = SenseHat()

   
width = 3   
"""width: width of the games grid, defaults to 3"""

height = 2
"""height: height of the games grid"""


posX = 0
"""X-position of the current game in the grid."""

posY = 0
"""Y-position of the current game in the grid."""

scrollSpeed = 0.2
"""Speed of scrolling. Number is wait time between steps (higher means
slower).
"""

_games = [[None for x in range(width)] for y in range(height)]

    
def set_game(x, y, game):
    """Set a game to a position (x, y) in the game grid."""
    if x >= width:
        raise ArgumentError(x, "x must be 0 < x <= width")
    if y >= height:
        raise ArgumentError(y, "y must be 0 < y <= height")
    _games[x][y] = game


def start():
    """Start the overall game (this starts the curent game).
    
    Start: after all the games have been initialized, call this
    method to start the first game (the one at position posX, posY). 
    """
    nextGame = get_game(posX, posY)
    nextGame.resume_game()
    play()

    
def play():
    """The main game loop.
     
    It will listen for and handle joystick events (only up/down and 
    left/right) and then call play_1step() of the current game.
    """
    logging.info('not yet implemented! ')

#        while True:
        #for event in​ sense.stick.get_events():
#print( event.direction )
#print( event.action )
 


def get_game(x, y):
    """ Return the game at the position x, y."""
    if x >= width:
        raise ArgumentError(x, "x must be 0 < x <= width")
    if y >= height:
        raise ArgumentError(y, "y must be 0 < y <= height")

    return _games[x][y]


def go_up():
    """Move to the game above the current one, if possible.
    
    If possible, moves the current position up and returns True.  
    Returns False if the current position is already in the topmost row.
    """
    logging.info('go_up requested from current pos {}/{}'
        .format(posX, posY))
    global posX, posY    
    thisGame = get_game(posX, posY)
    oldCol = thisGame.get_border_color()
    
    if posY == 0:
        logging.info('go_up: no game above')
        fieldScroller.try_scroll_up(oldCol, scrollSpeed)
        
    else:
        thisGame.leave_game()
        posY -= 1
        nextGame = get_game(posX, posY)
        logging.info('go_up: next game (at pos {}/{}): {}'
            .format(posX, posY, nextGame.gameId))
        data = nextGame.get_screen()
        newCol = nextGame.get_border_color()
        fieldScroller.scroll_up(data, [oldCol, newCol], scrollSpeed)
        nextGame.resume_game()


def go_down():
    """Move to the game below the current one, if possible.
    
    If possible, moves the current position down and returns True.  
    Returns False if the current position is already in the last row.
    """
    logging.info('go_down requested from current pos {}/{}'
        .format(posX, posY))
    global posX, posY
    thisGame = get_game(posX, posY) 
    oldCol = thisGame.get_border_color()
    
    if posY == height-1:
        logging.info('go_down: no game below')
        fieldScroller.try_scroll_down(oldCol, scrollSpeed)
        
    else:
        thisGame.leave_game()
        posY += 1
        nextGame = get_game(posX, posY)
        logging.info('go_down: next game (at pos {}/{}): {}'
            .format(posX, posY, nextGame.gameId))
        data = nextGame.get_screen()
        newCol = nextGame.get_border_color()
        fieldScroller.scroll_down(data, [oldCol, newCol], scrollSpeed)
        nextGame.resume_game()


#TODO go_left, go_right  


def __str__():
    return 'GameWindowGrid with {}x{} games, position {}/{}'.format(width, height, posX, posY)


x = 3
y = 3


def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))


def pushed_up(event):
    global y
    if event.action != ACTION_RELEASED:
        y = clamp(y - 1)


def pushed_down(event):
    global y
    if event.action != ACTION_RELEASED:
        y = clamp(y + 1)


def pushed_left(event):
    global x
    if event.action != ACTION_RELEASED:
        x = clamp(x - 1)


def pushed_right(event):
    global x
    if event.action != ACTION_RELEASED:
        x = clamp(x + 1)


def refresh():
    sense.clear()
    sense.set_pixel(x, y, 255, 255, 255)


def _test2():
    sense.stick.direction_up = pushed_up
    sense.stick.direction_down = pushed_down
    sense.stick.direction_left = pushed_left
    sense.stick.direction_right = pushed_right
    sense.stick.direction_any = refresh
    refresh()
    #pause()
    _count()


__counter = 0
"""Counter for displaying numbers, only used for testing."""


def _count():
    while True:        
        sense.show_letter(str(__counter))
        global counter
        __counter += 1
        if __counter == 10:
            __counter = 0
        time.sleep(2)
        


def _test2Games_noJoystick():
    sense.clear()

    global width
    width = 1
    game1 = GameWindow("A")
    game2 = GameWindow("B")
    print(__str__())
    set_game(0, 0, game1)
    set_game(0, 1, game2)
    x = 0
    for y in range(2):
        g = get_game(x, y)
        print('game at {}/{}: {}'.format(x, y, g))
        
    start()
    print('game1 running')
    time.sleep(1)
    print('go down...')
    go_down()
    time.sleep(2)
    print('go down...')
    go_down()
    time.sleep(2)
    print('go up...')
    go_up()
    time.sleep(2)
    print('go up...')
    go_up()
    time.sleep(2)


def _testX():
    
    sense.clear()

    global width
    width = 2
    game1 = GameWindow("A")
    game2 = GameWindow("B")
    game3 = GameWindow("C")
    game4 = GameWindow("D")
    print(__str__())    
    set_game(0, 0, game1)
    set_game(1, 0, game2)
    set_game(0, 1, game3)
    set_game(1, 1, game4)
    for x in range(2):
        for y in range(2):
            g = get_game(x, y)
            print('game at {}/{}: {}'.format(x, y, g))


    #while True:
        #for event in sense.stick.get_events():
            ## Check if the joystick was pressed
            #if event.action == "pressed":
                ## Check which direction
                #if event.direction == "up":
                    #sense.show_letter("U")      # Up arrow
                #elif event.direction == "down":
                    #sense.show_letter("D")      # Down arrow
                #elif event.direction == "left": 
                    #sense.show_letter("L")      # Left arrow
                #elif event.direction == "right":
                    #sense.show_letter("R")      # Right arrow
                #elif event.direction == "middle":
                    #sense.show_letter("M")      # Enter key

                ## Wait a while and then clear the screen
                #time.sleep(0.5)
                #sense.clear()
            #else:
                #print("other event")


def _test():
    _test2Games_noJoystick()
    #pass
    

if __name__ == "__main__":
    #logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger().setLevel(logging.INFO)
    _test()

