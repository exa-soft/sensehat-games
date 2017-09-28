from sense_hat import SenseHat
#import logging
import time
from pixelUtils import *
from ../exeption import DataError

"""The fieldScroller will take the current SenseHAT display and a
second 8x8 fields (as array of 64 elements) and implement a scroll
movement from the current display to the new one. The direction for
the scroll movement can be selected (up, down, left, right).
To mark the scroll operations, all screens are first displayed with
a border which shrinks a bit, then the scroll is done to the new screen,
which is displayed with a shrinked border first, then that border is
expanded and disappears.
"""

def black = (0, 0, 0)


def scrollUp (sense, newScreen, borderColor=(120, 120, 120)):
    """Scrolls the display up, such that the new screen appears from
    bottom.
    """

    if len(newScreen) != 64:
        raise DataError (newScreen, "screen data must have 64 elements")

    oldDisplay = sense.get_pixels()

    time.sleep(1)
    _draw_border1 (sense, borderColor)
    #newWithBorder = _add_border2 (newScreen[:])  # copy the array and add a border
    #newRows = screen_to_rows(newWithBorder, True)  # true = from top

    time.sleep(1)
    _draw_border2 (sense, borderColor)

    #time.sleep(1)
    #scroll_vertical (sense, True, newRows)

    _undraw_border2 (sense, borderColor, newScreen)

    time.sleep(1)
    _undraw_border1 (sense, borderColor, newScreen)


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
        sense.set_pixel(0, i, black)
        sense.set_pixel(7, i, black)
    for i in range(1, 7):
        sense.set_pixel(i, 0, black)
        sense.set_pixel(i, 7, black)


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



    """
    for arg in sys.argv[1:]:
    try:
        f = open(arg, 'r')
    except IOError:
        print('cannot open', arg)
    else:
        print(arg, 'has', len(f.readlines()), 'lines')
        f.close()
    """

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


def test_drawUndrawBorders(s, imageData):
    color = (255, 56, 0)

    time.sleep(1)
    _draw_border1 (s, color)
    time.sleep(1)
    _draw_border2 (s, color)

    time.sleep(1)
    _undraw_border2 (s, color, imageData)
    time.sleep(1)
    _undraw_border1 (s, imageData)


def test_addRemoveBorders(s, imageData):
    color = (56, 255, 0)

    time.sleep(1)
    _border_move_in (s, color)
    time.sleep(1)
    _border_move_out (s, color, imageData)



if __name__ == "__main__":

    s = SenseHat()
    s.low_light = True

    s.set_pixels(testImages[1])
    test_drawUndrawBorders (s, testImages[1])
    test_addRemoveBorders (s, testImages[1])
