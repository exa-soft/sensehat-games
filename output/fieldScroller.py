#from sense_hat import SenseHat
from sense_emu import SenseHat
#import logging
import time
from . import displayUtils
from .exceptions import DataError

"""The fieldScroller will take the current SenseHAT display and a
second 8x8 fields (as array of 64 elements) and implement a scroll
movement from the current display to the new one. The direction for
the scroll movement can be selected (up, down, left, right).
To mark the scroll operations, all screens are first displayed with
a border which shrinks a bit, then the scroll is done to the new screen,
which is displayed with a shrinked border first, then that border is
expanded and disappears.
"""

_black = (0, 0, 0)
defaultBorderColor = (120, 120, 120)
defaultBorderColors = (defaultBorderColor, defaultBorderColor)
defaultSpeed = .2


def scrollUp (senseHat, newScreen, borderColors=defaultBorderColors, speed=defaultSpeed):
    """Scrolls the display up, such that the new screen appears 
    from bottom.
    
    - borderColors are the colors of the borders pointed around the 
      screens during scrolling: first element is around old screen (the 
      one that is scrolled away), second element around new screen. 
      
    - speed is the waiting time between steps (drawing border etc.)
    """
    # True: scroll vertically. second boolean: direction (scroll up?)
    _scroll (senseHat, newScreen, borderColors, speed, True, True)
    


def scrollDown (senseHat, newScreen, borderColors=defaultBorderColors, speed=defaultSpeed):
    """Scrolls the display down, such that the new screen appears 
    from top.
    
    - screen is the data for the new screen (an array with 64 color tuples).
    
    - borderColors are the colors of the borders pointed around the 
      screens during scrolling: first element is around old screen (the 
      one that is scrolled away), second element around new screen. 
      
    - speed is the waiting time between steps (drawing border etc.)
    """
    # True: scroll vertically. second boolean: direction (scroll up?)
    _scroll (senseHat, newScreen, borderColors, speed, True, False)


def scrollLeft (senseHat, newScreen, borderColors=defaultBorderColors, speed=defaultSpeed):
    """Scrolls the display left, such that the new screen appears 
    from right.
    
    - borderColors are the colors of the borders pointed around the 
      screens during scrolling: first element is around old screen (the 
      one that is scrolled away), second element around new screen. 
      
    - speed is the waiting time between steps (drawing border etc.)
    """
    # False: scroll horizontally. second boolean: direction (scroll left?)
    _scroll (senseHat, newScreen, borderColors, speed, False, True)


def scrollRight (senseHat, newScreen, borderColors=defaultBorderColors, speed=defaultSpeed):
    """Scrolls the display right, such that the new screen appears 
    from left.
    
    - borderColors are the colors of the borders pointed around the 
      screens during scrolling: first element is around old screen (the 
      one that is scrolled away), second element around new screen. 
      
    - speed is the waiting time between steps (drawing border etc.)
    """
    _scroll (senseHat, newScreen, borderColors, speed, False, False)



def _scroll (senseHat, newScreen, borderColors, speed, vertical, upOrLeft):

    if len(newScreen) != 64:
        raise DataError (newScreen, "screen data must have 64 elements")

    if len(borderColors) != 2:
        raise DataError (borderColors, "borderColors must have exactly 2 elements (colors)")

    bColors = (borderColors, borderColors) if len(borderColors) == 1 else borderColors[0:2]
    #oldDisplay = senseHat.get_pixels()

    # draw a border along the edge
    time.sleep(speed)
    _draw_border1 (senseHat, bColors[0])
    
    # (in memory) copy the new screen data and add a border
    newWithBorder = newScreen[:]
    _add_border2 (newWithBorder, bColors[1])  

    # move the border away from the edge to the second row/col
    time.sleep(speed)
    _draw_border2 (senseHat, bColors[0])

    # scroll from the current display to the one now in memory
    time.sleep(speed)
    if vertical:
        newRows = displayUtils.screen2rows(newWithBorder, upOrLeft)
        displayUtils.scroll_vertical (senseHat, upOrLeft, newRows)
    else:
        newCols = displayUtils.screen2rows(newWithBorder, upOrLeft)
        displayUtils.scroll_horizontal (senseHat, upOrLeft, newCols)

    # move the border from the second row/col towards the edge
    time.sleep(speed)
    _undraw_border2 (senseHat, bColors[1], newScreen)
    
    # remove the border from the edge
    time.sleep(speed)
    _undraw_border1 (senseHat, newScreen)


def _add_border2 (screenData, borderColor):
    """Add a border as in _draw_border2, but do not add it on screen, 
    but to the data in screenData instead"""
        
    # clear the outer border
    for i in range(8):
        screenData[i] = _black       # 0*8 + i
        screenData[56 + i] = _black  # 7*8 + i
    for i in range(1, 7):
        screenData[i*8] = _black
        screenData[i*8 + 7] = _black

    # data for the inner border    
    for i in range(1, 7):
        screenData[8 + i] = borderColor    # 1*8 + i
        screenData[48 + i] = borderColor   # 6*8 + i
    for i in range(2, 6):
        screenData[i*8 + 1] = borderColor
        screenData[i*8 + 6] = borderColor
    

def _border_move_in (senseHat, color):
    """Adds a border moving in from the edge."""
    _draw_border1 (senseHat, color)
    time.sleep(0.05)
    _draw_border2 (senseHat, color)
    time.sleep(0.2)


def  _border_move_out (senseHat, color, screen):
    """Removes the border by moving it towards the edge."""
    _undraw_border2 (senseHat, color, screen)
    time.sleep(0.05)
    _undraw_border1 (senseHat, screen)
    time.sleep(0.2)


def _draw_border1 (senseHat, color):
    """Draw a border around the display (along the edges).

    Parameters:
        senseHat -- the SenseHAT object
        color -- the color to use
    """

    for i in range(8):
        senseHat.set_pixel(0, i, color)
        senseHat.set_pixel(7, i, color)
    for i in range(1, 7):
        senseHat.set_pixel(i, 0, color)
        senseHat.set_pixel(i, 7, color)


def _draw_border2 (senseHat, color):
    """Draw a border inside the display: the pixels along the  edges
    are deleted (set to black), the second row of pixels is painted
    in the given color.

    Parameters:
        senseHat -- the SenseHAT object
        color -- the color to use
    """

    # first paint the inner border
    for i in range(1, 7):
        senseHat.set_pixel(1, i, color)
        senseHat.set_pixel(6, i, color)
    for i in range(2, 6):
        senseHat.set_pixel(i, 1, color)
        senseHat.set_pixel(i, 6, color)

    # then delete the outer border
    for i in range(8):
        senseHat.set_pixel(0, i, _black)
        senseHat.set_pixel(7, i, _black)
    for i in range(1, 7):
        senseHat.set_pixel(i, 0, _black)
        senseHat.set_pixel(i, 7, _black)


def _get_pixel (screenData, x, y):
    index = y * 8 + x
    return screenData[index]


def _undraw_border1 (senseHat, screen):
    """Remove the border along the eges and replace it with data from
    screen.

    Parameters:
        senseHat -- the SenseHAT object
        screen -- the data of the screen to display (format as for SenseHAT)
    """

    # restore the outer border
    for i in range(8):
        pixel = _get_pixel (screen, 0, i)
        senseHat.set_pixel(0, i, pixel)
        pixel = _get_pixel (screen, 7, i)
        senseHat.set_pixel(7, i, pixel)
    for i in range(1, 7):
        pixel = _get_pixel (screen, i, 0)
        senseHat.set_pixel(i, 0, pixel)
        pixel = _get_pixel (screen, i, 7)
        senseHat.set_pixel(i, 7, pixel)


def _undraw_border2 (senseHat, borderColor, screen):
    """Move the border from the second row to the row along the eges
    and replace the second row with data from screen.

    Parameters:
        senseHat -- the SenseHAT object
        screen -- the data of the screen to display (format as for SenseHAT)
    """

    # first paint the outer border
    for i in range(8):
        senseHat.set_pixel(0, i, borderColor)
        senseHat.set_pixel(7, i, borderColor)
    for i in range(1, 7):
        senseHat.set_pixel(i, 0, borderColor)
        senseHat.set_pixel(i, 7, borderColor)

    # then restore the inner border
    for i in range(1, 7):
        pixel = _get_pixel (screen, 1, i)
        senseHat.set_pixel(1, i, pixel)
        pixel = _get_pixel (screen, 6, i)
        senseHat.set_pixel(6, i, pixel)
    for i in range(2, 6):
        pixel = _get_pixel (screen, i, 1)
        senseHat.set_pixel(i, 1, pixel)
        pixel = _get_pixel (screen, i, 6)
        senseHat.set_pixel(i, 6, pixel)


_green = (0, 255, 0)
_blue = (0, 0, 255)
_red = (255, 0, 0)

_n = (0, 0, 0)   # nothing
_a = (255, 255, 0)   # yellow
_f = _red

testImages = [
    [
    _n, _n, _n, _n, _n, _n, _n, _n, 
    _n, _n, _n, _n, _n, _n, _n, _n, 
    _n, _n, _n, _a, _a, _n, _n, _n, 
    _n, _n, _a, _a, _a, _a, _n, _n, 
    _n, _n, _a, _a, _a, _a, _n, _n, 
    _n, _n, _n, _a, _a, _n, _n, _n, 
    _n, _n, _n, _n, _n, _n, _n, _n, 
    _n, _n, _n, _n, _n, _n, _n, _n, 
    ],
    [
    _f, _a, _n, _n, _n, _n, _n, _n, 
    _a, _f, _a, _n, _n, _n, _n, _n, 
    _n, _a, _f, _a, _n, _n, _n, _n,
    _n, _n, _a, _f, _a, _n, _n, _n,
    _n, _n, _n, _a, _f, _a, _n, _n,
    _n, _n, _n, _n, _a, _f, _a, _n,
    _n, _n, _n, _n, _n, _a, _f, _a,
    _n, _n, _n, _n, _n, _n, _a, _f, 
    ],
]


def _testAll():
    """Call for testing and watch on SenseHAT 
    (real or emulator, depending on import)"""

    s = SenseHat()
    s.low_light = False
    s.set_pixels(testImages[0])

    scrollUp (s, testImages[1], borderColors=(_blue, _green), speed=.5)

    time.sleep(1)
    scrollDown (s, testImages[0], (_green, _blue), speed=.3)

    time.sleep(1)
    scrollLeft (s, testImages[1], (_red, _green), speed=.2)

    time.sleep(1)
    scrollRight (s, testImages[0], (_green, _red), speed=.3)


if __name__ == "__main__":
    pass
    #_testAll()    # does not work because of relative imports


