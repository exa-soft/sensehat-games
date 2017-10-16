# basic game "window" and"window collection" module

#from sense_hat import SenseHat
from sense_emu import SenseHat
import logging
import time
from exceptions import ArgumentError
from output import fieldScroller


class GameWindow (object):
    """Base class for a game that is in a "window" (one SenseHAT screen).
    Subclasses should overwrite:
    - _init_game()
    - get_name()
    - get_border_color()
    - is_solved()
    """


    def __init__ (self, name):
        """Init the game window.
        
        - senseHat: sense
        - name: the name of the window (maybe displayed on start 
          or help request)
        """
        self.name = name
        self.sense = SenseHat()
        self._init_game()

 
    def _init_game (self):
        """Init game"""
        logging.debug('_init_game')
        # should be overwritten by subclasses 


    def get_name (self):
        """ Return the name of the game"""
        return "(no name set - overwrite method 'get_name')"
        # should be overwritten by subclasses 


    def get_screen (self):
        """ Return the data for the (current) display of the game."""
        return (96, 96, 96) * 64
        # should be overwritten by subclasses 
        

    def get_border_color (self):
        """ Color for the border (used when scrolling), can serve to 
        easier identify the game"""
        return (120, 120, 120)
        # should be overwritten by subclasses 


    def is_solved (self):
        """Return true if the game is solved"""
        return False
        # should be overwritten by subclasses 
        

    def fail (self):
        """Displays an "explosion" on the screen - can be called by 
        subclasses when the game is lost."""
        logging.debug('failed!')
        # TODO display explosion
        self.sense.show_letter ("X")


    def __str__(self):
        return 'Game "{sf.name}", border color {sf.borderColor}'.format(sf=self)



class GameWindowGrid (object):
    """Base class for a grid of GameWindows, ordered in a rectangle
    of the given width and height.
    """

    def __init__ (self, width, height):
        """Init the GameWindowCGrid. Each place of the grid must
        then be initialized with a game.
        
        - width: width of the games grid
        - height: height of the games grid
        """
        # TODO change constructor to take 2-dim-array of GameWindow?
        
        self.sense = SenseHat()
        self.w = width
        self.h = height
        self.games = [[None for x in range(self.w)] for y in range(self.h)]
        self.posX = 0
        self.posY = 0
        
        
    def set_game (self, x, y, game):
        """Set a game to a position in the game Init game"""
        if x >= self.w:
            raise ArgumentError (x, "x must be 0 < x <= width")
        if y >= self.h:
            raise ArgumentError (y, "y must be 0 < y <= height")

        self.games[x][y] = game


    def get_game (self, x, y):
        """ Return the game at the position x, y"""
        if x >= self.width:
            raise ArgumentError (x, "x must be 0 < x <= width")
        if y >= self.height:
            raise ArgumentError (y, "y must be 0 < y <= height")

        return self.games[x][y]


    def go_up (self):
        """Moves the current position up and returns True.
        Returns False if the current position is already in the topmost row.
        """
        if self.posY == 0:
            return False
        else:
            self.position.y -= 1
            nextGame = get_game (self.posX, self.posY)
            data = nextGame.get_data ()
            color = nextGame.get_border_color ()
            fieldScroller.scrollUp (self.sense, data, color)


    def go_down (self):
        """Moves the current position down and returns True.
        Returns False if the current position is already in the last row.
        """
        if self.posY == self.height - 1:
            return False
        else:
            self.posY += 1
            nextGame = get_game (self.posX, self.posY)
            data = nextGame.get_data ()
            color = nextGame.get_border_color ()
            fieldScroller.scrollDown (self.sense, data, color)

    #TODO go_left, go_right            


    def __str__(self):
        return 'GameWindowGrid with {sf.w}x{sf.h} games, position {sf.posX}/{sf.posY}'.format(sf=self)



def _test ():

    sense = SenseHat ()
    sense.clear()

    game1 = GameWindow ("A")
    game2 = GameWindow ("B")
    game3 = GameWindow ("C")
    game4 = GameWindow ("D")
    grid = GameWindowGrid (2, 2)
    print ("Have {}".format(grid))
    
    grid.set_game (0, 0, game1)
    grid.set_game (1, 0, game2)
    grid.set_game (0, 1, game3)
    grid.set_game (1, 1, game4)
    print ("Have {}".format(grid))
    
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


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    _test ()

