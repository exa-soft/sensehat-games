from sense_hat import SenseHat
#import logging
import time
from pixelUtils import *
from ../exeption import DataError

"""The fieldScroller will take the current SenseHAT display and a
second 8x8 fields (as array of 64 elements) and implement a scroll
movement from the current display to the new one. The direction for
the scroll movement can be selected (up, down, left, right).
To mark the screen change operations, all screens are first displayed
with a border which shrinks a bit, then the scroll is done to the new
screen, which is displayed with a shrinked border first, then that
border is expanded and disappears.
There are also functions to display that there is no next screen. They
display the same shrinking border, but then mark the edge of the
missing next screen with a colored bar, then expand the border again,
without scrolling.

This library also exposes functions that convert a SenseHAT screen
(64-element array) to an array of rows or of columns.
"""

def black = (0, 0, 0)
def default_borderColor = (120, 120, 120)


def goto_screen_below (sense, newScreen, borderColor = default_borderColor):
    """Scrolls the display up, the new screen appears from below.
    """
    _goto_screen_vertical (sense, newScreen, borderColor, False)   # False = go down


def goto_screen_above (sense, newScreen, borderColor = default_borderColor):
    """Scrolls the display down, the new screen appears from top.
    """
    _goto_screen_vertical (sense, newScreen, borderColor, True)   # True = go up


def goto_screen_left (sense, newScreen, borderColor = default_borderColor):
    """Scrolls the display right, the new screen appears from the left.
    """
    _goto_screen_horizontal (sense, newScreen, borderColor, False)   # False = go left


def goto_screen_right (sense, newScreen, borderColor = default_borderColor):
    """Scrolls the display left, the new screen appears from right.
    """
    _goto_screen_horizontal (sense, newScreen, borderColor, True)   # True = go right


dev _goto_screen (sense, newScreen, borderColor, isVertical, isUpOrRight):
    """Scrolls the display vertically or horizontally (depending on
    isVertical), where isUpOrRight defines the direction.
    """

    if len(newScreen) != 64:
        raise DataError (newScreen, "screen data must have 64 elements")

    oldDisplay = sense.get_pixels()


    # set the outer border to the existing screen
    time.sleep(1)
    _draw_border1 (sense, borderColor)

    # copy the newScreen array and add a border (in memory)
    newWithBorder = _add_border2 (newScreen[:], borderColor)

    newLines = screen_to_rows (newWithBorder, isUpOrRight) if isVertical else screen_to_cols (newWithBorder, isUpOrRight)

    # set the inner border to the existing screen (remove the outer)
    time.sleep(1)
    _draw_border2 (sense, borderColor)

    # scroll from existing screen to the one now in memory with border
    time.sleep(1)
    if isVertical:
        scroll_vertical (sense, isUpOrRight, newLines)
    else:
        scroll_horizontal (sense, isUpOrRight, newLines)

    # replace inner border with pixels from original new screen and paint outer border
    _undraw_border2 (sense, borderColor, newScreen)

    # replace outer with pixels from original new screen
    time.sleep(1)
    _undraw_border1 (sense, borderColor, newScreen)




def screen_to_rows (screen):
    return [screen[i*8 : i*8 + 7] for i in range(8)]


def _add_border2 (screenData, color = default_borderColor):
    for i in range(1, 7):
        screenData[1, i] = color
        screenData[6, i] = color
    for i in range(2, 6):
        screenData[i, 1] = color
        screenData[i, 6] = color



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

def test_screen2Rows ():
    testArray = [
    '0', '1', '2', '3', '4', '5', '6', '7',
    '0', '1', '2', '3', '4', '5', '6', '7',
    '0', '1', '2', '3', '4', '5', '6', '7',
    '0', '1', '2', '3', '4', '5', '6', '7',
    '0', '1', '2', '3', '4', '5', '6', '7',
    '0', '1', '2', '3', '4', '5', '6', '7',
    '0', '1', '2', '3', '4', '5', '6', '7',
    '0', '1', '2', '3', '4', '5', '6', '7',
    ]
    rows = screen_to_rows (testArray)
    assert len(rows) == 8
    for i in range(8):
        print('row {} is: {}'.format(i, rows[i])


if __name__ == "__main__":

    s = SenseHat()
    s.low_light = True

    s.set_pixels (testImages[1])
    test_drawUndrawBorders (s, testImages[1])
    test_addRemoveBorders (s, testImages[1])
    test_screen2Rows ()
