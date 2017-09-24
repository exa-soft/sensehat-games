import turtle
import logging

class SimonTurtle(object):
    """Class for the display of SimonSays with the turtle.
    To use the class, overwrite the hook method  heardColor(colorNum)
    """

    #constants
    baseX = -300
    baseY = 100
    sizeX = 50
    spaceX = 20
    spaceY = 50
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
        self.curPos = 0
        self.isTopRow = True
        turtle.clear()
        turtle.penup()
        turtle.setpos((self.baseX, self.baseY + 3 * self.spaceY))
        turtle.pendown()
        turtle.write("Neues Rätsel bereit", move=False, align=self.align, font=self.font)
        turtle.penup()
        self.screen = turtle.Screen()

    def clearSolutionArea(self):
        turtle.setpos((self.baseX, self.baseY + 0.5 * self.spaceY))
        turtle.pendown()
        turtle.color('black', 'white')
        turtle.pensize(width=1)
        turtle.pendown()
        turtle.begin_fill()
        width = 7 * (self.sizeX + self.spaceX)
        height = self.sizeY
        turtle.forward(width)
        turtle.left(90)
        turtle.forward(height)
        turtle.left(90)
        turtle.forward(width)
        turtle.left(90)
        turtle.forward(height)
        turtle.end_fill()
        turtle.penup()

    def pos2XY(self):
        """calculates x/y-position from posNum and isTopRow"""
        x = self.baseX if self.isTopRow else self.baseX + self.curPos * (self.sizeX + self.spaceX)
        y = (self.baseY + 0.5 * self.spaceY) if self.isTopRow else (self.baseY - self.spaceY)
        return (x, y)

    def paintColor (self, color):
        """paint a square of size sizeX at the current position, with the given color"""
        turtle.color('black', color)
        turtle.pensize(width=1)
        turtle.pendown()
        turtle.begin_fill()
        for i in range(4):
            turtle.forward(self.sizeX)
            turtle.left(90)
        turtle.end_fill()
        turtle.penup()

    def gotoPos (self):
        """moves the turtle to the position defined by posNum and isTopRow"""
        turtle.setpos(self.pos2XY())

    def showColor (self, colorNum):
        """show the given color at the current position"""
        self.paintColor(self.colors[colorNum])

    def nextPos (self):
        """moves the internal variables and the turtle to the next output position"""
        self.curPos += 1
        self.gotoPos()

    def heardColor(self, colorNum) :
        """subclasses will implement this method to be notified
        when the user has input a color"""
        logging.info('received color: {}'.format(colorNum))

    def heardCol0Go(self):
        self.showColorAndMove(0)
        self.heardColor(0)

    def heardCol1Go(self):
        self.showColorAndMove(1)
        self.heardColor(1)

    def heardCol2Go(self):
        self.showColorAndMove(2)
        self.heardColor(2)

    def heardCol3Go(self):
        self.showColorAndMove(3)
        self.heardColor(3)

    def showColorAndMove(self, colorNum):
        self.showColor (colorNum)
        self.nextPos()

    def startSaying(self):
        turtle.setpos((self.baseX, self.baseY + 2 * self.spaceY))
        #turtle.color('black', color)
        turtle.pendown()    # test if necessary
        turtle.write("Achtung", move=False, align=self.align, font=self.font)
        turtle.penup()    # test if necessary
        self.isTopRow = True
        self.curPos = 0
        self.gotoPos()
        logging.debug ('screen: {}'.format(self.screen))
        self.screen.onkey(None, "0")
        self.screen.onkey(None, "1")
        self.screen.onkey(None, "2")
        self.screen.onkey(None, "3")

    def startListening(self):
        turtle.setpos((self.baseX, self.baseY - 2 * self.spaceY))
        #turtle.color('black', color)
        turtle.write("Du bist dran", move=False, align=self.align, font=self.font)
        self.isTopRow = False
        self.curPos = 0
        self.gotoPos()
        #self.screen.onkey(funct, "Up")
        self.screen.onkey(self.heardCol0Go, "0")
        self.screen.onkey(self.heardCol1Go, "1")
        self.screen.onkey(self.heardCol2Go, "2")
        self.screen.onkey(self.heardCol3Go, "3")
        self.screen.listen()

    def writeResult(self, ok):
        turtle.setpos((self.baseX, self.baseY + 2 * self.spaceY))
        if ok:
            turtle.write('Sehr gut!')
        else:
            turtle.write('Das war falsch! Spiel abgebrochen')

    def __str__(self):
        return 'SimonTurtle (curPos {sf.curPos}, isTopRow {sf.isTopRow})'.format(sf=self)


#self.screen.textinput("NIM", "Name of first player:")
# self.screen.onclick(turtle.goto) # Subsequently clicking into the TurtleScreen will
                            # make the turtle move to the clicked point.
#self.screen.onclick(None)


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

