import turtle
#to use it:
#from output import simon-out-turtle as situ
# situ.init()

#constants
baseX = -300
baseY = 100
sizeX = 50
spaceX = 20
spaceY = 50
colors = ['blue', 'green' , 'yellow', 'red']
font = ('Arial', 12, 'normal')
align = 'left'  # or 'center' or 'right'

# global variables
curPos = 0
isTopRow = True
screen = None

def init():
    global screen
    screen = turtle.Screen()
    reset()

def reset():
    global curPos
    curPos = 0
    isTopRow = True
    turtle.clear()
    turtle.penup()
    turtle.setpos((baseX, baseY + 3 * spaceY))
    turtle.pendown()
    turtle.write("Neues Rätsel bereit", move=False, align=align, font=font)
    turtle.penup()

def pos2XY():
    """calculates x/y-position from posNum and isTopRow"""
    x = baseX if isTopRow else baseX + curPos * (sizeX + spaceX)
    y = (baseY + 0.5 * spaceY) if isTopRow else (baseY - spaceY)
    return (x, y)

def paintColor (color):
    """paint a square of size sizeX at the current position, with the given color"""
    turtle.color('black', color)
    turtle.pensize(width=1)
    turtle.pendown()
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(sizeX)
        turtle.left(90)
    turtle.end_fill()
    turtle.penup()

def gotoPos ():
    """moves the turtle to the position defined by posNum and isTopRow"""
    turtle.setpos(pos2XY())

def showColor (colNum):
    """show the given color at the current position"""
    paintColor(colors[colNum])

def nextPos ():
    """moves the internal variables and the turtle to the next output position"""
    global curPos
    curPos += 1
    gotoPos()

def showCol0Go():
    showColorAndMove(0)

def showCol1Go():
    showColorAndMove(1)

def showCol2Go():
    showColorAndMove(2)

def showCol3Go():
    showColorAndMove(3)

def showColorAndMove(colNum):
    showColor (colNum)
    nextPos()

def startSaying():
    turtle.setpos((baseX, baseY + 2 * spaceY))
    #turtle.color('black', color)
    turtle.pendown()    # test if necessary
    turtle.write("Achtung", move=False, align=align, font=font)
    turtle.penup()    # test if necessary
    global isTopRow
    global curPos
    isTopRow = True
    curPos = 0
    gotoPos()
    #screen.onkey(None, "0")
    #screen.onkey(None, "1")
    #screen.onkey(None, "2")
    #screen.onkey(None, "3")

def startListening():
    turtle.setpos((baseX, baseY - 2 * spaceY))
    #turtle.color('black', color)
    turtle.write("Du bist dran", move=False, align=align, font=font)
    global isTopRow
    global curPos
    isTopRow = False
    curPos = 0
    gotoPos()
    #screen.onkey(funct, "Up")
    screen.onkey(showCol0Go, "0")
    screen.onkey(showCol1Go, "1")
    screen.onkey(showCol2Go, "2")
    screen.onkey(showCol3Go, "3")
    screen.listen()

#screen.textinput("NIM", "Name of first player:")
# screen.onclick(turtle.goto) # Subsequently clicking into the TurtleScreen will
                            # make the turtle move to the clicked point.
#screen.onclick(None)


if __name__ == "__main__":
    init()
    startSaying()
    showCol2Go()
    showCol3Go()
    showCol1Go()
    startListening()


