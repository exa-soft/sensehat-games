import turtle
import logging

class SimonTurtle(object):
    """Class for the display of SimonSays with the turtle.
    To use the class, overwrite the hook method  receivedColor(colorNum)
    """

    #constants
    sizeXY = 50
    spaceX = 20
    spaceY = 50
    baseX = -400
    baseYTop = 100
    baseYBtm = baseYTop - (1.5 * sizeXY)
    colors = ['blue', 'green' , 'yellow', 'red']
    font = ('Arial', 12, 'normal')
    align = 'left'  # or 'center' or 'right'


    def __init__(self):
        # global variables
        self.curPos = 0
        self.isTopRow = True
        self.screen = turtle.Screen()
        self.reset()

    def reset(self):
        """reset display to be ready for a new game"""
        self.curPos = 0
        self.isTopRow = True
        turtle.clear()
        turtle.penup()
        turtle.setpos((self.baseX, self.baseYTop + 3 * self.spaceY))
        turtle.write("Neues Rätsel bereit", move=False, align=self.align, font=self.font)
        turtle.setpos((self.baseX, self.baseYTop + 2 * self.spaceY))
        turtle.write("0: blau, 1: grün, 2: gelb, 3: rot", move=False, align=self.align, font=self.font)
        self.screen = turtle.Screen()

    def _clearGameArea(self):
        """clear game area (display and solution - to be ready for the next round)"""
        turtle.setpos((self.baseX, self.baseYBtm))
        turtle.color('white', 'white')
        turtle.pensize(width=1)
        turtle.pendown()
        turtle.begin_fill()
        width = 10 * (self.sizeXY + self.spaceX)
        height = self.sizeXY * 2 + self.spaceY
        turtle.forward(width)
        turtle.left(90)
        turtle.forward(height)
        turtle.left(90)
        turtle.forward(width)
        turtle.left(90)
        turtle.forward(height)
        turtle.left(90)
        turtle.end_fill()
        turtle.penup()

    def _pos2XY(self):
        """calculates x/y-position from posNum and isTopRow"""
        x = self.baseX if self.isTopRow else self.baseX + self.curPos * (self.sizeXY + self.spaceX)
        y = self.baseYTop if self.isTopRow else self.baseYBtm
        return (x, y)

    def _paintColor (self, color, borderColor='black'):
        """paint a square of size sizeXY at the current position, with the given color"""
        turtle.color(borderColor, color)
        turtle.pensize(width=1)
        turtle.pendown()
        turtle.begin_fill()
        for i in range(4):
            turtle.forward(self.sizeXY)
            turtle.left(90)
        turtle.end_fill()
        turtle.penup()

    def _gotoPos (self):
        """moves the turtle to the position defined by posNum and isTopRow"""
        turtle.setpos(self._pos2XY())

    def showColor (self, colorNum):
        """show the given color at the current position"""
        self._paintColor(self.colors[colorNum])

    def _nextPos (self):
        """moves the internal variables and the turtle to the next output position"""
        self.curPos += 1
        self._gotoPos()

    def receivedColor(self, colorNum) :
        """subclasses will implement this method to be notified
        when the user has input a color"""
        logging.info('received color: {}'.format(colorNum))

    def _recvdCol0Go(self):
        self.showColorAndMove(0)
        self.receivedColor(0)

    def _recvdCol1Go(self):
        self.showColorAndMove(1)
        self.receivedColor(1)

    def _recvdCol2Go(self):
        self.showColorAndMove(2)
        self.receivedColor(2)

    def _recvdCol3Go(self):
        self.showColorAndMove(3)
        self.receivedColor(3)

    def showColorAndMove(self, colorNum):
        self.showColor (colorNum)
        self._nextPos()

    def startSaying(self):
        """Display message to the user to be attentive"""
        turtle.setpos((self.baseX + self.sizeXY + self.spaceX, self.baseYTop))
        turtle.color('black')
        turtle.write("Merk dir die Farben!", move=False, align=self.align, font=self.font)
        self._clearGameArea()

        self.isTopRow = True
        self.curPos = 0
        self._gotoPos()
        logging.debug ('screen: {}'.format(self.screen))
        self.screen.onkey(None, "0")
        self.screen.onkey(None, "1")
        self.screen.onkey(None, "2")
        self.screen.onkey(None, "3")

    def startListening(self):
        """Make ready to receive input from the user and display it"""
        # cover last displayed color
        self._paintColor ('white', 'white')
        # message to user
        turtle.setpos((self.baseX, self.baseYBtm - self.spaceY))
        turtle.color('black')
        turtle.write("Du bist dran", move=True, align=self.align, font=self.font)
        self.isTopRow = False
        self.curPos = 0
        self._gotoPos()
        self.screen.onkey(self._recvdCol0Go, "0")
        self.screen.onkey(self._recvdCol1Go, "1")
        self.screen.onkey(self._recvdCol2Go, "2")
        self.screen.onkey(self._recvdCol3Go, "3")
        self.screen.listen()

    def roundSolved(self):
        #turtle.setpos((self.baseX + self.sizeXY + self.spaceX, self.baseYTop))
        turtle.color('black')
        turtle.write("Richtig!", move=False, align=self.align, font=self.font)

    def writeResult(self, ok):
        turtle.setpos((self.baseX, self.baseYBtm - 2 * self.spaceY))
        if ok:
            turtle.color('darkgreen')
            turtle.write('Sehr gut!', font=self.font)
        else:
            turtle.color('red')
            turtle.write('Das war falsch! Spiel abgebrochen', font=self.font)

    def __str__(self):
        return 'SimonTurtle (curPos {sf.curPos}, isTopRow {sf.isTopRow})'.format(sf=self)


if __name__ == "__main__":

    # logging.basicConfig(level=logging.DEBUG,
    #                format='%(asctime)s %(levelname)s %(message)s',
    #                filename='myapp.log',
    #                filemode='w')
    logging.getLogger().setLevel(logging.DEBUG)

    st = SimonTurtle()
    logging.debug('initialized: {}'.format(st))
    st.startSaying()
    st.showColorAndMove(2)
    st.showColorAndMove(3)
    st.showColorAndMove(1)
    st.startListening()

