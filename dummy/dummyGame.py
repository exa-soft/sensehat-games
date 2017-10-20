# dummy game in a "window"

#from sense_hat import SenseHat
from sense_emu import SenseHat
import logging
import time
from ..core.game import GameWindow
from ..core.exceptions import ArgumentError
#from ..output import fieldScroller


class DummyGame (GameWindow):
    """a "game" that only displays its first letter 
    and then its name.
    """

 
    def _init_game (self):
        """Init game"""
        self.letter = self.name[0]
        self.solved = False
        logging.debug('_init_game, name is {}'.format(self.name))


    def get_name (self):
        """ Return the name of the game"""
        return self.name
        

    def get_border_color (self):
        """ Color for the border (used when scrolling), can serve to 
        easier identify the game"""
        return (204, 204, 120)


    def _start_game (self):
        """Start the game. Will be called when resume_game() is 
        called for the first time."""
        msg = "the first letter of my name '{}' is '{}'!".format(self.name, self.letter)
        self.sense.show_message(msg, scroll_speed=0.05, text_colour=[255, 255, 0], back_colour=[0, 0, 0])
        

    def _continue_game (self):
        """Continue the game. Will be called when resume_game() is 
        called not for the first time, but the game is not yet solved."""
        msg = "the first letter of my name {} !".format(self.name)
        #self.sense.show_message(msg, scroll_speed=0.05, text_colour=[255, 255, 0], back_colour=[0, 0, 0])
        self.sense.show_letter(self.letter, text_colour=[255, 255, 0], back_colour=[0, 0, 0])
        self.solved = True


    def is_solved (self):
        """Return true if the game is solved"""
        return self.solved
        # should be overwritten by subclasses 
               

def _test ():
    _testResume ()
    
def _testResume ():        
    game = DummyGame ('testgame')
    game.resume_game ()
    time.sleep(2)
    game.resume_game ()
    time.sleep(2)
    game.resume_game ()
    
def _testLeave (): 
    g2 = DummyGame ('more')
    g2.resume_game ()
    time.sleep(1)
    g2.resume_game ()
    time.sleep(1)
    print ('before leave')
    g2.leave_game ()
    time.sleep(1)
    
    sense = SenseHat()
    pixlist = [(120, 160, 80) for i in range(64)]
    print ('pixlist is {}'.format(pixlist))
    sense.set_pixels (pixlist)
    time.sleep(2)
    scr = g2.get_screen ()  
    print ('screen (len{}) is {}'.format(len(scr), scr))
    g2.resume_game ()
    time.sleep(2)
    print ('restoring screen')
    sense.set_pixels (scr)
   

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    _test ()

