import logging
from .simonsays import SimonSays
from .simonTurtle import SimonTurtle


# situ.init()

"""
class Cat(Pet):
    def __init__(self, name, hates_dogs):
        Pet.__init__(self, name, "Cat")
        self.hates_dogs = hates_dogs
"""

class SimonOnTurtle(SimonSays, SimonTurtle):

    def __init__(self, length):
        SimonSays.__init__(self, length)
        print('simonSays length:', self.size)
        SimonTurtle.__init__(self)

    def onRestart(self):
        """Reset screen on restart
        (overwritten method from SimonSays)"""
        SimonTurtle.reset(self)
        print("neue Lösung bereit auf Turtle (Länge: {})".format(self.size))

    def beforeSayingColors(self):
        """Message to user that Simon will say something
        (overwritten method from SimonSays)"""
        SimonTurtle.startSaying(self)

    def beforeHearingColors(self):
        """Start to listen to user
        (overwritten method from SimonSays)"""
        SimonTurtle.startListening(self)

    def sayColor(self, colorNum):
        """Display one color "said" by Simon
        (overwritten method from SimonSays)"""
        SimonTurtle.showColor(self, colorNum)

    def roundSolved(self):
        """Finish round
        (overwritten method from SimonSays)"""
        SimonTurtle.roundSolved(self)

    def wrongColor(self):
        """Display error to user on wrong input
        (overwritten method from SimonSays)"""
        SimonTurtle.writeResult(self, False)

    def gameSolved(self):
        """Display message to user that game solved
        (overwritten method from SimonSays)"""
        SimonTurtle.writeResult(self, True)

    def receivedColor(self, colorNum):
        """Notify SimonSays about received color
        (overwritten method from SimonTurtle)"""
        logging.info('received color: {}'.format(colorNum))
        SimonSays.hearColor(self, colorNum)


def _test():
    tusi = SimonOnTurtle(3)
    #tusi = ss.SimonSays(4)
    #logging.info ("state: ", tusi.state)
    tusi.restart()


if __name__ == "__main__":
    pass
    # _test()   # does not work from main because of relative imports.
    # start tst by with calling _test() manually

