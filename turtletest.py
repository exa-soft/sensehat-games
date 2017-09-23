import turtle

defaultPos = (0, 0)

turtle.setpos(defaultPos)
screen = turtle.Screen()

def quadrat(size, pos=None, color=None):
    turtle.penup()
    if not pos == None: 
        turtle.setpos(pos)
    if not color == None:
        turtle.color('black', color)
    turtle.pensize(width=1)
    turtle.pendown()
    turtle.begin_fill()
    for i in range(4):
        turtle.forward(size)
        turtle.left(90)
    turtle.end_fill()
    turtle.penup()

def test():
    turtle.pensize(width=5)
    turtle.pendown()
    turtle.color('red', 'yellow')
    turtle.begin_fill()
    while True:
        turtle.forward(200)
        turtle.left(90)
        if abs(turtle.pos()) < 1:
            break
    turtle.end_fill()
    turtle.penup()

def f():
    turtle.pendown()
    turtle.forward(70)
    turtle.left(60)
    turtle.penup()

def quadrat0():
    quadrat (50, color='blue')
    
def quadrat1():
    quadrat (50, color='green')

def quadrat2():
    quadrat (50, color='yellow')
    
def quadrat3():
    quadrat (50, color='red')
    
#f()
#quadrat (50, (100,100), 'yellow')
#quadrat (20, (200,200), 'red')
#turtle.goto((200, 400))
#quadrat (20, color='blue')
quadrat (30, (300,350))
quadrat (40, (-200, -100), 'white')

#screen.textinput("NIM", "Name of first player:")

screen.listen()
screen.onkey(f, "Up")
screen.onkey(quadrat0, "0")
screen.onkey(quadrat1, "1")
screen.onkey(quadrat2, "2")
screen.onkey(quadrat3, "3")

screen.onclick(turtle.goto) # Subsequently clicking into the TurtleScreen will
                            # make the turtle move to the clicked point.
#screen.onclick(None)
