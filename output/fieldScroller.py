#from sense_hat import SenseHat
from sense_emu import SenseHat
#import logging
import time
from . import displayUtils
from exceptions import DataError

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


def scrollUp (sense, newScreen, borderColor=(120, 120, 120), speed=.2):
    """Scrolls the display up, such that the new screen appears from
    bottom.
    Speed is the waiting time between steps (drawing border etc.)
    """

    if len(newScreen) != 64:
        raise DataError (newScreen, "screen data must have 64 elements")

    oldDisplay = sense.get_pixels()

    time.sleep(speed)
    _draw_border1 (sense, borderColor)
    # copy the array and add a border:
    newWithBorder = newScreen[:]
    
    _add_border2 (newWithBorder, borderColor)  
    newRows = displayUtils.screen2rows(newWithBorder, True)  # true = from top

    time.sleep(speed)
    _draw_border2 (sense, borderColor)

    time.sleep(speed)
    displayUtils.scroll_vertical (sense, True, newRows)

    time.sleep(speed)
    _undraw_border2 (sense, borderColor, newScreen)

    time.sleep(speed)
    _undraw_border1 (sense, newScreen)
    

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
    

def _border_move_in (sense, color):
    """Adds a border moving in from the edge."""
    _draw_border1 (sense, color)
    time.sleep(0.05)
    _draw_border2 (sense, color)
    time.sleep(0.2)


def  _border_move_out (sense, color, screen):
    """Removes the border by moving it towards the edge."""
    _undraw_border2 (sense, color, screen)
    time.sleep(0.05)
    _undraw_border1 (sense, screen)
    time.sleep(0.2)


def _draw_border1 (sense, color):
    """Draw a border around the display (along the edges).

    Parameters:
        sense -- the SenseHAT object
        color -- the color to use
    """

    for i in range(8):
        sense.set_pixel(0, i, color)
        sense.set_pixel(7, i, color)
    for i in range(1, 7):
        sense.set_pixel(i, 0, color)
        sense.set_pixel(i, 7, color)


def _draw_border2 (sense, color):
    """Draw a border inside the display: the pixels along the  edges
    are deleted (set to black), the second row of pixels is painted
    in the given color.

    Parameters:
        sense -- the SenseHAT object
        color -- the color to use
    """

    # first paint the inner border
    for i in range(1, 7):
        sense.set_pixel(1, i, color)
        sense.set_pixel(6, i, color)
    for i in range(2, 6):
        sense.set_pixel(i, 1, color)
        sense.set_pixel(i, 6, color)

    # then delete the outer border
    for i in range(8):
        sense.set_pixel(0, i, _black)
        sense.set_pixel(7, i, _black)
    for i in range(1, 7):
        sense.set_pixel(i, 0, _black)
        sense.set_pixel(i, 7, _black)


def _get_pixel (screenData, x, y):
    index = y * 8 + x
    return screenData[index]


def _undraw_border1 (sense, screen):
    """Remove the border along the eges and replace it with data from
    screen.

    Parameters:
        sense -- the SenseHAT object
        screen -- the data of the screen to display (format as for SenseHAT)
    """

    # restore the outer border
    for i in range(8):
        pixel = _get_pixel (screen, 0, i)
        sense.set_pixel(0, i, pixel)
        pixel = _get_pixel (screen, 7, i)
        sense.set_pixel(7, i, pixel)
    for i in range(1, 7):
        pixel = _get_pixel (screen, i, 0)
        sense.set_pixel(i, 0, pixel)
        pixel = _get_pixel (screen, i, 7)
        sense.set_pixel(i, 7, pixel)


def _undraw_border2 (sense, borderColor, screen):
    """Move the border from the second row to the row along the eges
    and replace the second row with data from screen.

    Parameters:
        sense -- the SenseHAT object
        screen -- the data of the screen to display (format as for SenseHAT)
    """

    # first paint the outer border
    for i in range(8):
        sense.set_pixel(0, i, borderColor)
        sense.set_pixel(7, i, borderColor)
    for i in range(1, 7):
        sense.set_pixel(i, 0, borderColor)
        sense.set_pixel(i, 7, borderColor)

    # then restore the inner border
    for i in range(1, 7):
        pixel = _get_pixel (screen, 1, i)
        sense.set_pixel(1, i, pixel)
        pixel = _get_pixel (screen, 6, i)
        sense.set_pixel(6, i, pixel)
    for i in range(2, 6):
        pixel = _get_pixel (screen, i, 1)
        sense.set_pixel(i, 1, pixel)
        pixel = _get_pixel (screen, i, 6)
        sense.set_pixel(i, 6, pixel)

