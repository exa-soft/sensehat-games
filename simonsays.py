# state machine module

import logging
from transitions import Machine
from random import Random


class SimonSays(object):
    """Class for a round of SimonSays on a vocabulary of four possible values (0, 1, 2, 3)"""

    def randomSolution(self, size):
        r = Random()
        r.seed()
        sol = []
        for i in range(size):
            sol.append(r.randint(0, 3))
        return sol

    def __init__(self, length):
        """init a SimonSays game with the given maximal length"""
        self.size = length
        self.restart()

    def restart(self):
        """restart the game (with a new solution)"""
        self.solution = self.randomSolution(self.size)
        logging.info ("solution is: ", self.solution)
        self.curLen = 0
        self.nextRound()


    def nextRound(self):
        self.curLen += 1
        self.initMachine (self.curLen)
        self.say()

    def beforeSayingColors(self):
        """ maybe do something before saying the 'colors'"""
        print("Pass auf! Hier kommt's:")
        # TODO we want to plug-in our own method for displaying the "colors"

    def sayColor (self, color):
        """display one color - this method should be given / plugged in by the class using SimonSays"""
        print('- ', color)
        # TODO we want to plug-in our own method for displaying the "colors"

    def say(self):
        """simon says the 'sentence' of the current length"""
        self.beforeSayingColors()
        for i in range(self.curLen):
            self.sayColor(self.solution[i])

    def hearColor(self, color):
        """simon hears the other player say a color (0..3)"""
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

    def solved(self):
        self.roundSolved()
        if self.curLen < self.size:
            self.nextRound()
        else:
            self.gameSolved()

    def gameSolved(self):
        """the game has been solved up to the maximal length"""
        print("------- >>> du bist super! <<<-------")
        # TODO we want to plug-in our own method for what to do when game is solved


    def initMachine(self, size):
        """init state-machine: states correct0, correct1, etc. up to size"""
        self.states = ["correct" + str(i) for i in range(size+1)]
        logging.debug("states are: ", self.states)
        self.machine = Machine(model=self, states=self.states, initial='correct0', ignore_invalid_triggers=True)
        # ignoring invalid triggers will just return False if state transition not possible -> then we can report error in game
        for i in range(size):
            self.machine.add_transition('gotColor' + str(self.solution[i]), source='correct'+str(i), dest='correct'+str(i+1))
            logging.debug('added transition {0} from state "{1}" to state "{2}"'
                .format('gotColor' + str(self.solution[i]), 'correct'+str(i), 'correct'+str(i+1)))

        lastState = self.machine.get_state('correct' + str(size))
        lastState.add_callback('enter', self.solved)
        logging.debug('statemachine initialized')


simon = SimonSays(5)

# Initialize
def init():
    logging.info ("state: ", simon.state)


if __name__ == "__main__":
    #import sys
    #fib(int(sys.argv[1]))
    init()
