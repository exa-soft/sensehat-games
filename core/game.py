"""This module contains the core of this collection of SenseHAT games: 
a "window" (containing one game that runs on the SenseHAT screen) and a 
"window collection", which is an imaginary rectangle of several 
"windows", each with its game, so the user can move from one to another 
by using the joystick. The whole can be used to implement games like
"Keep talking and nobody explodes"."""

__author__ = 'Edith Birrer
__version__ = '0.2'


import logging
import time
#from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from sense_emu import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from . import exceptions

    
class GameWindow(object):
    """Base class for games working on a SenseHAT screen.
    
    This is the base class to implement games that are played in a 
    "window" of one SenseHAT screen and can be combined with other such
    games.
    
    Subclasses must overwrite:
    - init_game()
    - get_name()
    - start_game()
    - play()
    - is_solved()
    
    Optionally, subclasses can overwrite:
    - pause_game()
    - continue_game()
    - get_screen()
    - get_border_color()
    
    Note that a game in GameWindow cannot use the joystick events 
    up/down/left/right, because they are already used to "scroll" from 
    one GameWindow ot its neighbours. However, a game in GameWindow can 
    use the middle button of the joystick. 
    """

    def __init__(self, gameId):
        """Init the game window class.
        
        - gameId: an ID of the game window (no check is made if unique).
        """
        self.gameId = gameId
        self.isStarted = False
        self.savedScreen = None
        self.sense = SenseHat()
        self.init_game()
 
    def init_game(self):
        """Init game. 
        
        Initialize the game logic.   
        Subclasses should overwrite this method.
        """
        logging.debug('init_game')
        # should be overwritten by subclasses 

    def get_name(self):
        """ Returns the name of the game.
        
        Return the name of the game.  This may make usage of the game
        ID or just return the general name of this game.  
        Subclasses should overwrite this method.
        """
        return "(no name set - overwrite method 'get_name')"
        # should be overwritten by subclasses 

    def get_screen(self):
        """Returns the stored screen. 
        
        Get the screen for restoring the game (a 64-element array of 
        color tuples).  The default implementation returns the screen 
        stored in leave_game(), and a black screen for the very first 
        call of this game window.  For other displays on restore, 
        subclasses can overwrite this method.
        """
        return self.savedScreen if self.savedScreen is not None 
            else ([0, 0, 0] * 64)
        # can be overwritten by subclasses 

    def get_border_color(self):
        """Color for the border.  
        
        Color for the border (used when scrolling), can serve to 
        easier identify the game.  
        Subclasses should overwrite this method.
        """
        return [120, 120, 120]
        # should be overwritten by subclasses 

    def resume_game(self):
        """Starts or continues playing the game.
        
        Starts or continues playing the game (after calling 
        get_screen and scrolling to the game window): If it has not yet 
        been started, start_game() is called. Otherwise, if it is 
        not yet solved, continue_game() is called. 
        Otherwise, nothing happens.
        """
        if self.is_solved():
            logging.info('resume_game {}: already solved'
                .format(self.gameId))
            return None
        elif self.isStarted:
            logging.info('resume_game {}: continue game'
                .format(self.gameId))
            self.continue_game()
        else:
            logging.info('resume_game {}: start game'
                .format(self.gameId))
            self.isStarted = True
            self.start_game()
        logging.info('resume_game {}: calling play()'
            .format(self.gameId))
        self.play()
        return None

    def start_game(self):
        """Start the game (for the first time).
        
        Start the game.  Will be called when resume_game() is 
        called for the first time. 
        Subclasses should overwrite this method.
        """
        pass
        # should be overwritten by subclasses 

    def continue_game(self):
        """Continue the game: restore after pausing.  
         
        Continue the game. Will be called when resume_game() is 
        called not for the first time, but the game is not yet solved.
        Subclassed can do things that are necessary when resuming a 
        game from the hidden status. (Restoring the screen has already
        been done as part of the scrolling back to the game.)
        """
        pass
        # can be overwritten by subclasses 

    def pause_game(self):
        """Hook to implement operations before leaving the game.
        
        If necessary, the subclass can do here some saving or 
        cleanup before leaving the game. Will be called in leave_game(). 
        However, saving and restoring the current screen is already 
        taken care of (will be done in leave_game() and get_screen(), 
        as part of the scrolling operation).
        """
        pass
        # can be overwritten by subclasses 

    def leave_game(self):
        """Leave the game (will save screen and call pause_game()).
        
        Before leaving the game, the screen will be saved. 
        Subclasses should overwrite pause_game() if they need to do
        some saving or cleanup before leaving the game."""
        logging.debug('leave game')
        self._save_screen()
        self.pause_game()
        
    def _save_screen(self):
        """Save the screen before leaving the game."""
        self.savedScreen = self.sense.get_pixels()
        logging.debug('saved screen (len: {}): {}'.format(len(self.savedScreen), self.savedScreen))

    def is_solved(self):
        """Return true if the game is solved.
        
        Subclasses should overwrite this method.
        """
        return False
        # should be overwritten by subclasses 
        
    def play(self):
        """Play the game: main game loop. 
        
        Here the game will run, i.e. check for user input and react 
        on it. 
        Subclasses must overwrite this method.
        """        
        logging.info('no game implemented! Overwrite play()')
        
    def fail(self):
        """Displays that the game is lost.
        
        Displays an "explosion" on the screen - can be called by 
        subclasses when the game is lost.
        """
        logging.debug('failed!')
        # TODO display explosion
        self.sense.show_letter("X")

    def __str__(self):
        return 'Game "{sf.name}", border color {sf.borderColor}'.format(sf=self)



def _test():

    sense = SenseHat()
    sense.clear()

    game1 = GameWindow("A")
    game2 = GameWindow("B")
    game3 = GameWindow("C")
    game4 = GameWindow("D")
    grid = GameWindowGrid(2, 2)
    print("Have {}".format(grid))
    
    grid.set_game(0, 0, game1)
    grid.set_game(1, 0, game2)
    grid.set_game(0, 1, game3)
    grid.set_game(1, 1, game4)
    print("Have {}".format(grid))
    
    while True:
        for event in sense.stick.get_events():
            # Check if the joystick was pressed
            if event.action == "pressed":
                # Check which direction
                if event.direction == "up":
                    sense.show_letter("U")      # Up arrow
                elif event.direction == "down":
                    sense.show_letter("D")      # Down arrow
                elif event.direction == "left": 
                    sense.show_letter("L")      # Left arrow
                elif event.direction == "right":
                    sense.show_letter("R")      # Right arrow
                elif event.direction == "middle":
                    sense.show_letter("M")      # Enter key

                # Wait a while and then clear the screen
                time.sleep(0.5)
                sense.clear()
            else:
                print("other event")
    

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    _test()

