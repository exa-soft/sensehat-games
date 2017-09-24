import logging
from cores.simonsays import SimonSays
#import cores.simonsays as ss

#from output.simonTurtle import SimonTurtle
import output.simonTurtle as siTurtle


# situ.init()

"""
class Cat(Pet):
    def __init__(self, name, hates_dogs):
        Pet.__init__(self, name, "Cat")
        self.hates_dogs = hates_dogs
"""

class SimonOnTurtle(SimonSays):

    def __init__(self, length):
        SimonSays.__init__(self, length)
        print('simonSays length:', self.size)
        self.situ = siTurtle.SimonTurtle()
        print('self.situ:', self.situ)

    def afterRestart(self):
        self.situ.reset()
        print("neue Lösung bereit auf Turtle (Länge: {})".format(self.length))

    def beforeSayingColors(self):
        self.situ.startSaying()

    def beforeHearingColors(self):
        self.situ.startListening()

    def sayColor(self, colorNum):
        self.situ.showColor(colorNum)

    def roundSolved(self):
        self.situ.clearSolutionArea()

    def wrongColor(self):
        self.situ.writeResult(False)

    def gameSolved(self):
        self.situ.writeResult(True)


def test():
    tusi = SimonOnTurtle(2)
    #tusi = ss.SimonSays(4)
    #logging.info ("state: ", tusi.state)
    tusi.restart()


if __name__ == "__main__":
    test()

