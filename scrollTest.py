import logging
from output import fieldScroller
#import cores.simonsays as ss
from sense_emu import SenseHat
#from sense_hat import SenseHat
import time


green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
nothing = (0,0,0)

n = nothing
a = yellow
f = red

testImages = [
    [
    n, n, n, n, n, n, n, n, 
    n, n, n, n, n, n, n, n, 
    n, n, n, a, a, n, n, n, 
    n, n, a, a, a, a, n, n, 
    n, n, a, a, a, a, n, n, 
    n, n, n, a, a, n, n, n, 
    n, n, n, n, n, n, n, n, 
    n, n, n, n, n, n, n, n, 
    ],
    [
    f, a, n, n, n, n, n, n, 
    a, f, a, n, n, n, n, n, 
    n, a, f, a, n, n, n, n,
    n, n, a, f, a, n, n, n,
    n, n, n, a, f, a, n, n,
    n, n, n, n, a, f, a, n,
    n, n, n, n, n, a, f, a,
    n, n, n, n, n, n, a, f, 
    ],
]


def testAll():
	
    s = SenseHat()
    s.low_light = False
    s.set_pixels(testImages[0])

    fieldScroller.scrollUp (s, testImages[1], borderColors=(blue, green), speed=.5)

    time.sleep(1)
    fieldScroller.scrollDown (s, testImages[0], (green, blue), speed=.3)

    time.sleep(1)
    fieldScroller.scrollLeft (s, testImages[1], (red, green), speed=.2)

    time.sleep(1)
    fieldScroller.scrollRight (s, testImages[0], (green, red), speed=.1)


if __name__ == "__main__":
    testAll()

