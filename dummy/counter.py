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
from ..core import gameWindowGrid as grid
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
    
    def __init__(self, gameId, color):
        """Init a counter with id and color."""
        GameWindow.__init__(self, gameId)
        self.color = color
 
    def init_game(self):
        """Init game: name ID start with a digit."""
        num = int(self.gameId[0])
        if num < 0 or num > 10:
            return ArgumentError(num, 'gameId must start with one digit')
        self.maxNum = num
        self.curNum = 0
        self.solved = False
        logging.debug('init_game, max is {}, isRunning is {}'
            .format(self.maxNum, self.isRunning))

    def get_name(self):
        """ Return the name of the game"""
        return self.name
        
    def get_border_color(self):
        """ Color for the border (used when scrolling), can serve to 
        easier identify the game.
        """
        return self.color

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
            #self.print_threads()
            self._waitBeforeCount(2.0)
        logging.info('play finished')
       
    def _count_one(self):
        if self.isRunning:
            logging.debug('count_one(): game is running (cur {}, max {})'
                .format(self.curNum, self.maxNum))
            self.curNum += 1
            self._display_number()
            if self.curNum < self.maxNum:
                self._waitBeforeCount(2.0)
        else:
            logging.debug('_count_one(): game is not running (cur {}, max {})'.format(self.curNum, self.maxNum))

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
        logging.debug('i am thread {} {}'
            .format(threading.get_ident(), threading.current_thread().name))
        tList = threading.enumerate()
        for e in tList:
            logging.debug('- thread {}, alive {}'.format(e, e.is_alive()))
               

def _test1Game():
    sense = SenseHat()
    sense.low_light = False

    global gm
    gm = CounterDummyGame('7game', [120, 180, 200])
    gm.resume_game()
    time.sleep(4.5)

    gm.leave_game()
    pixlist = [(120, 160, 80) for i in range(64)]
    sense.set_pixels(pixlist)
    time.sleep(3)
    
    gm.resume_game()


def _test2Games():
    g1 = CounterDummyGame('7game', [120, 180, 200])
    g2 = CounterDummyGame('5game', [200, 180, 120])

    for i in range(5):
        print('round {}, game 1'.format(i))
        g1.resume_game()
        time.sleep(4.5)
        g1.leave_game()
        print('round {}, game 2'.format(i))
        g2.resume_game()   
        time.sleep(3.3)
        g2.leave_game()


def _test2Games_inGrid():
    
    sense = SenseHat()
    sense.clear()
    g1 = CounterDummyGame('7game', [120, 180, 200])
    g2 = CounterDummyGame('5game', [200, 180, 120])
   
    grid.width = 1
    grid.height = 2
    grid.set_game(0, 0, g1)
    grid.set_game(0, 1, g2)
    x = 0
    for y in range(2):
        g = grid.get_game(x, y)
        print('game at {}/{}: {}'.format(x, y, g))
           
    grid.start()
    print('running')
    time.sleep(2)
    print('go down...')
    grid.go_down()
    time.sleep(2)
    print('go down...')
    grid.go_down()
    time.sleep(2)
    print('go up...')
    grid.go_up()
    time.sleep(2)
    print('go up...')
    grid.go_up()
    time.sleep(2)


def _test():
    #_test1Game()
    #_test2Games()
    _test2Games_inGrid()
    

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    _test()

