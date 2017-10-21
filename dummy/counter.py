"""Dummy "game": a counter in a GameWindow."""

#from sense_hat import SenseHat
from sense_emu import SenseHat
import logging
import time
from ..core.game import GameWindow
from ..core.exceptions import ArgumentError
#from ..output import fieldScroller


class CounterDummyGame (GameWindow):
    """A "game" that counts from 0 to the maximal number (max. 9) 
    while it is active. Used for testing the switch between GameWindows
    in a GameWindowGrid.
    """

 
    def init_game (self):
        """Init game: name must start with a digit."""
        num = int(self.name[0])
        if num < 0 or num > 10:
            return ArgumentError(num, 'name must start with a digit')
        self.maxNum = num
        self.curNum = 0
        self.solved = False
        logging.debug('init_game, max is {}'.format(self.maxNum))


    def get_name (self):
        """ Return the name of the game"""
        return self.name
        

    def get_border_color (self):
        """ Color for the border (used when scrolling), can serve to 
        easier identify the game"""
        numCol = 24 * (self.maxNum + 1)
        return [numCol, numCol, numCol]


    def start_game (self):
        """Start the game. Will be called when resume_game() is 
        called for the first time."""
        self._display_number()


    def continue_game (self):
        """Continue the game. Will be called when resume_game() is 
        called not for the first time, but the game is not yet solved."""
        self._display_number()

        
    def _display_number (self):
        self.sense.show_letter(str(self.curNum), text_colour=self.get_border_color(), back_colour=[0, 0, 0])
        
        
    def play (self):
        """This "game" counts from 0 up to its maximal number."""
        while True:
            self._display_number ()
            time.sleep(2)
            if self.curNum < self.maxNum:
                self.curNum += 1
            

    def is_solved (self):
        """Return true if solved: i.e. if maxNum has been reached"""
        return self.curNum == self.maxNum
               

def _test ():

    game = CounterDummyGame ('7game')
    game.resume_game ()
    time.sleep(2)
    game.resume_game ()
    time.sleep(2)
    game.resume_game ()
    
    sense = SenseHat()
    pixlist = [(120, 160, 80) for i in range(64)]
    print ('pixlist is {}'.format(pixlist))
    sense.set_pixels (pixlist)
    time.sleep(2)
    game.resume_game ()
    time.sleep(2)
   

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    _test ()

