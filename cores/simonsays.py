# state machine module

import logging
from transitions import Machine
from random import Random


class SimonSays(object):
    """Class for a round of SimonSays on a vocabulary of four possible values (0, 1, 2, 3)
    To play a game:
    - init the object with the length of the final solution, e.g. simon = SimonSays(5)
    - call simon.restart() to start the game (this will start 'saying')
    - listen to user input and give it (as a number from 0..3) to simon using  simon.hearColor(the number)
    See also example in  test().
    Subclasses should overwrite:
    - onRestart()
    - beforeSayingColors()
    - beforeHearingColors()
    - sayColor(solor)
    - roundSolved()
    - wrongColor()
    - gameSolved()
    """


    def __init__(self, length):
        """init a SimonSays game with the given maximal length"""
        self.size = length
        self._reset()

    def _randomSolution(self, size):
        r = Random()
        r.seed()
        sol = []
        for i in range(size):
            sol.append(r.randint(0, 3))
        return sol

    def _reset(self):
        """reset internal variables (new solution)"""
        logging.debug('restart')
        self.solution = self._randomSolution(self.size)
        logging.info ("solution is: {}".format(self.solution))
        self.curLen = 0

    def restart(self):
        """start or restart the game (with a new solution)"""
        self._reset()
        self.onRestart()
        self._nextRound()

    def onRestart(self):
        """ maybe do something when a new game is started"""
        print("neue Lösung bereit (Länge: {})".format(self.size))
        # TODO we want to plug-in our own method for displaying the "colors"

    def _nextRound(self):
        """start the next round ('saying' something which is 1 longer than before)"""
        logging.debug('nextRound')
        self.curLen += 1
        self._initMachine (self.curLen)
        self._say()

    def beforeSayingColors(self):
        """ maybe do something before saying the 'colors'"""
        print("Pass auf! Hier kommt's:")
        # TODO we want to plug-in our own method for displaying the "colors"

    def beforeHearingColors(self):
        """ maybe do something to start 'listening' to the 'colors'"""
        print("Jetzt bist du dran")
        # TODO we want to plug-in our own method for starting to listen


    def sayColor (self, color):
        """display one color - this method should be given / plugged in by the class using SimonSays"""
        print('- ', color)
        # TODO we want to plug-in our own method for displaying the "colors"

    def _say(self):
        """simon says the 'sentence' of the current length"""
        logging.debug('say')
        self.beforeSayingColors()
        for i in range(self.curLen):
            self.sayColor(self.solution[i])
        self.beforeHearingColors()

    def hearColor(self, color):
        """simon hears the other player say a color (0..3)"""
        logging.debug('hear color: {}'.format(color))
        print("hearing color ", color)
        res = self.trigger('gotColor' + str(color))
        if not res:
            self.wrongColor()
        return res

    def roundSolved(self):
        print("------ richtig --------")
        # TODO we want to plug-in our own method for displaying "roundSolved"

    def wrongColor(self):
        print("-----!!! falsch !!!-----------")
        # TODO we want to plug-in our own method for displaying "wrong"

    def _solved(self):
        logging.debug('solved')
        self.roundSolved()
        if self.curLen < self.size:
            self._nextRound()
        else:
            self.gameSolved()

    def gameSolved(self):
        """the game has been solved up to the maximal length"""
        print("------- >>> du bist super! <<<-------")
        # TODO we want to plug-in our own method for what to do when game is solved


    def _initMachine(self, size):
        """init state-machine: states correct0, correct1, etc. up to size"""
        logging.debug('initMachine, size: {}'.format(size))
        self.states = ["correct" + str(i) for i in range(size+1)]
        logging.debug('states are: {}'.format(self.states))
        self.machine = Machine(model=self, states=self.states, initial='correct0', ignore_invalid_triggers=True)
        # ignoring invalid triggers will just return False if state transition not possible -> then we can report error in game
        for i in range(size):
            self.machine.add_transition('gotColor' + str(self.solution[i]), source='correct'+str(i), dest='correct'+str(i+1))
            logging.debug('added transition {0} from state "{1}" to state "{2}"'
                .format('gotColor' + str(self.solution[i]), 'correct'+str(i), 'correct'+str(i+1)))

        lastState = self.machine.get_state('correct' + str(size))
        lastState.add_callback('enter', self._solved)
        logging.debug('statemachine initialized')

    def __str__(self):
        return 'SimonSays (final length {sf.size}, current length {sf.curLen}, solution {sf.solution})'.format(sf=self)


def test(testlen):

    simon = SimonSays(testlen)
    print('[testout]', simon)
    for i in range(simon.size):
        print('[testout] solution', i, ':', simon.solution[i])

    simon.restart()

    for curTestLen in range(testlen):
        # we know the solution... - say numbers up to current length
        for i in range(simon.curLen):
            simon.hearColor(simon.solution[i])
            print('[testout] state: ', simon.state)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    test(3)

