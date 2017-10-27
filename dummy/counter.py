"""Dummy "game": a counter in a GameWindow."""

__author__ = 'Edith Birrer'
__version__ = '0.2'

#from sense_hat import SenseHat
from sense_emu import SenseHat
import logging
import time
import threading
from threading import Timer
from ..core.game import GameWindow
from ..core.exceptions import ArgumentError
#from ..output import fieldScroller


"""
threading.active_count()
Return the number of Thread objects currently alive. The returned count is equal to the length of the list returned by enumerate().

threading.current_thread()
Return the current Thread object, corresponding to the caller’s thread of control. If the caller’s thread of control was not created through the threading module, a dummy thread object with limited functionality is returned.

threading.get_ident()
"""

class CounterDummyGame(GameWindow):
    """A "game" that counts from 0 to the maximal number (max. 9) 
    while it is active. Used for testing the switch between GameWindows
    in a GameWindowGrid.
    """
 
    def init_game(self):
        """Init game: name ID start with a digit."""
        num = int(self.gameId[0])
        if num < 0 or num > 10:
            return ArgumentError(num, 'gameId must start with one digit')
        self.maxNum = num
        self.curNum = 0
        self.solved = False
        logging.debug('init_game, max is {}, isRunning is {}'.format(self.maxNum, self.isRunning))

    def get_name(self):
        """ Return the name of the game"""
        return self.name
        
    def get_border_color(self):
        """ Color for the border (used when scrolling), can serve to 
        easier identify the game.
        """
        n = 24 * (self.maxNum + 1)
        m = 180
        numCol = max(n, m)
        return [numCol, numCol, m]

    def start_game(self):
        """Start the game. Will be called when resume_game() is 
        called for the first time.
        """
        self._display_number()

    def continue_game(self):
        """Continue the game. Will be called when resume_game() is 
        called not for the first time, but the game is not yet solved.
        """
        self._display_number()

    def _display_number(self):
        self.sense.show_letter(str(self.curNum), text_colour=self.get_border_color(), back_colour=[0, 0, 0])
        
    def play(self):
        """This "game" counts from 0 up to its maximal number."""
        self._display_number()
        if self.curNum < self.maxNum:
            logging.debug('curNum {} < maxNum {}, will set timer for next number'.format(self.curNum, self.maxNum))
            self.print_threads()
            self._waitBeforeCount(2.0)
            logging.info('timer started (play)')
        logging.info('play finished')
       
    def _count_one(self):
        if self.isRunning:
            logging.info('count_one(): game is running (cur {}, max {})'.format(self.curNum, self.maxNum))
            self.curNum += 1
            self._display_number()
            if self.curNum < self.maxNum:
                logging.info('{} < {}, will set timer (i am thread {} {})'
                    .format(self.curNum, self.maxNum, threading.get_ident(), threading.current_thread().name))
                self.print_threads()
                self._waitBeforeCount(2.0)
            else:
                logging.info('curNum {} = maxNum {}'.format(self.curNum, self.maxNum))
                self.print_threads()
        else:
            logging.info('_count_one(): game is not running (cur {}, max {})'.format(self.curNum, self.maxNum))
            self.print_threads()

    def _waitBeforeCount(self, sec):
        self.t = Timer (sec, self._count_one)
        self.t.start()
        
    def pause_game(self):
        """Hook to implement operations before leaving the game."""
        self.t.cancel()
                
    def is_solved(self):
        """Return true if solved: i.e. if maxNum has been reached"""
        return self.curNum == self.maxNum

    def print_threads(self):
        logging.info('i am thread {} {}'
            .format(threading.get_ident(), threading.current_thread().name))
        tList = threading.enumerate()
        for e in tList:
            logging.info('- thread {}, alive {}'.format(e, e.is_alive()))
               

def _test():
    
    sense = SenseHat()
    sense.low_light = False

    logging.info('I am thread {} {})'
        .format(threading.get_ident(), threading.current_thread().name))

    global gm
    gm = CounterDummyGame('7game')
    gm.resume_game()
    time.sleep(4.5)

    gm.leave_game()
    
    pixlist = [(120, 160, 80) for i in range(64)]
    sense.set_pixels(pixlist)
    time.sleep(3)
    
    gm.resume_game()
    #time.sleep(2)
    #gm.resume_game()    
    #time.sleep(2)
   

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    _test()

