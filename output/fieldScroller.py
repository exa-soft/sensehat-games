"""The fieldScroller will take the current SenseHAT display and a
second 8x8 fields (as array of 64 elements) and implement a scroll
movement from the current display to the new one. The direction for
the scroll movement can be selected (up, down, left, right).
To mark the scroll operations, all screens are first displayed with
a border which shrinks a bit, then the scroll is done to the new screen,
which is displayed with a shrinked border first, then that border is
expanded and disappears.
There is also a possiblity to show that a scroll movement in the 
selected direction is not possible (like if there is no neughbour 
screen on this side). In this case, the operation starts as usual with 
a border that shrinks a bit, but then, the edge of the side where no 
new window is available will be coloured (and no scroll operation 
occurs), then the border expands and disappears as usual. These 
operations are called tryScroll...().
"""

__author__ = 'Edith Birrer'
__version__ = '0.3'


#import logging
import time
#from sense_hat import SenseHat
from sense_emu import SenseHat
from . import displayUtils
from .exceptions import DataError

__version__ = '0.2'
__author__ = 'Edith Birrer'

_black = (0, 0, 0)
_sense = SenseHat()

defaultBorderColor = (120, 120, 120)
defaultBorderColors = (defaultBorderColor, defaultBorderColor)
defaultSpeed = .2


def scroll_up(newScreen, borderColors=defaultBorderColors, 
              speed=defaultSpeed):
    """Scroll to the next screen below.
    
    Scrolls the display up, such that the new screen appears 
    from bottom.

    - newScreen: data for the new screen (a list of 64 color tuples).
    
    - borderColors: colors of the borders pointed around the screens 
      during scrolling: first element is around old screen (the one 
      that is scrolled away), second element around new screen. 
      
    - speed is the waiting time between steps (drawing border etc.)
    """
    # True: scroll vertically. 2nd boolean: direction (scroll up?)
    _scroll(newScreen, borderColors, speed, True, True)
    

def scroll_down(newScreen, borderColors=defaultBorderColors, 
                speed=defaultSpeed):
    """Scroll to the next screen above.
    
    Scrolls the display down, such that the new screen appears 
    from top.
    
    Parameters: see scroll_up().
    """
    # True: scroll vertic., 2nd boolean: direction (scroll up?)
    _scroll(newScreen, borderColors, speed, True, False)


def scroll_left(newScreen, borderColors=defaultBorderColors, 
                speed=defaultSpeed):
    """Scroll to the next screen to the right.
    
    Scrolls the display left, such that the new screen appears 
    from right.
    
    Parameters: see scroll_up().
    """
    # False: scroll horiz., 2nd boolean: direction (scroll left?)
    _scroll(newScreen, borderColors, speed, False, True)


def scroll_right(newScreen, borderColors=defaultBorderColors, 
                 speed=defaultSpeed):
    """Scroll to the next screen to the left.
    
    Scrolls the display right, such that the new screen appears 
    from left.
    
    Parameters: see scroll_up().
    """
    # False: scroll horiz., 2nd boolean: direction (scroll left?)
    _scroll(newScreen, borderColors, speed, False, False)


def _scroll(newScreen, borderColors, speed, vertical, upOrLeft):
    """Scroll: display a border that shrinks from the edge, then scroll
    into the selected direction (moving in the new screen with a 
    border), then extend the border again. 
    """
    if len(newScreen) != 64:
        raise DataError(newScreen, 
            "screen data must have 64 elements")
    if len(borderColors) != 2:
        raise DataError(borderColors, 
            "borderColors must have exactly 2 elements (colors)")

    # add a border moving in from the edge to the second row/col
    time.sleep(speed)
    _border_move_in(borderColors[0], speed)

    # (in memory) copy the new screen data and add a border
    newWithBorder = newScreen[:]
    _add_border2(newWithBorder, borderColors[1])  

    # scroll from the current display to the one now in memory
    time.sleep(speed)
    if vertical:
        newRows = displayUtils.screen2rows(newWithBorder, upOrLeft)
        displayUtils.scroll_vertical(_sense, upOrLeft, newRows)
    else:
        newCols = displayUtils.screen2rows(newWithBorder, upOrLeft)
        displayUtils.scroll_horizontal(_sense, upOrLeft, newCols)

    # move the border towards the edge and then remove it
    time.sleep(speed)
    _border_move_out(borderColors[1], speed, newScreen)
    
    
def try_scroll_up(borderColor=defaultBorderColor, speed=defaultSpeed):
    """Try to scroll to the next screen below.

    Shows that scrolling the display up is not possible (there is 
    no neighbour screen at the bottom).

    - borderColor: colors of the border pointed around the screen 
      during scrolling. 
      
    - speed is the waiting time between steps (drawing border etc.)
    """
    # True: scroll vertically. 2nd boolean: direction (scroll up?)
    _try_scroll(borderColor, speed, True, True)
    

def try_scroll_down(borderColor=defaultBorderColor, speed=defaultSpeed):
    """Try to scroll to the next screen above.
    
    Shows that scrolling the display down is not possible (there is 
    no neighbour screen at the top).
    
    Parameters: see try_scroll_up().
    """
    # True: scroll vertically, 2nd boolean: direction (scroll up?)
    _try_scroll(borderColor, speed, True, False)


def try_scroll_left(borderColor=defaultBorderColor, speed=defaultSpeed):
    """Try to scroll to the next screen to the right.

    Shows that scrolling the display left is not possible (there is 
    no neighbour screen to the right).
    
    Parameters: see try_scroll_up().
    """
    # False: scroll horizontally, 2nd boolean: direction (scroll left?)
    _try_scroll(borderColor, speed, False, True)


def try_scroll_right(borderColor=defaultBorderColor, speed=defaultSpeed):
    """Try to scroll to the next screen to the left.

    Shows that scrolling the display right is not possible (there is 
    no neighbour screen to the left).
    
    Parameters: see try_scroll_up().
    """
    # False: scroll horiz., 2nd boolean: direction (scroll left?)
    _try_scroll(borderColor, speed, False, False)
    

def _try_scroll(borderColor, speed, vertical, upOrLeft):
    """Like _scroll, but instead of moving to the next window, the edge
    of the direction is coloured (as a visual marker that in this 
    direction, scrolling is not possible). 
    """    
    
    # store the screen
    oldScreen = _sense.get_pixels()
    
    # add a border moving in from the edge to the second row/col
    time.sleep(speed)
    _border_move_in(borderColor, speed)

    # colour the edge of the selected tryScroll-direction
    time.sleep(speed)
    if vertical:
        _show_edge_row(borderColor, upOrLeft, speed)
    else:
        _show_edge_column(borderColor, upOrLeft, speed)

    # move the border towards the edge and then remove it
    time.sleep(speed)
    _border_move_out(borderColor, speed, oldScreen)
    
    
def _show_edge_row(borderColor, upOrLeft, speed):
    """Color the first or last row and then remove color again."""
    y = 7 if upOrLeft else 0
    for x in range(8):
        _sense.set_pixel(x, y, borderColor)
    time.sleep(max(.5, 2*speed))
    for x in range(8):
        _sense.set_pixel(x, y, _black)
        

def _show_edge_column(borderColor, upOrLeft, speed):
    """Color the left or right column and then remove color again."""
    x = 7 if upOrLeft else 0
    for y in range(8):
        _sense.set_pixel(x, y, borderColor)
    time.sleep(max(.5, 2*speed))
    for y in range(8):
        _sense.set_pixel(x, y, _black)
        

def _add_border2(screenData, borderColor):
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
    

def _border_move_in(color, speed):
    """Adds a border moving in from the edge."""
    
    _draw_border1(color)
    time.sleep(speed)
    _draw_border2(color)


def  _border_move_out(color, speed, screen):
    """Removes the border by moving it towards the edge."""
    
    _undraw_border2(color, screen)
    time.sleep(speed)
    _undraw_border1(screen)


def _draw_border1(color):
    """Draw a border around the display (along the edges).

    Parameters:
        senseHat -- the SenseHAT object
        color -- the color to use
    """

    for i in range(8):
        _sense.set_pixel(0, i, color)
        _sense.set_pixel(7, i, color)
    for i in range(1, 7):
        _sense.set_pixel(i, 0, color)
        _sense.set_pixel(i, 7, color)


def _draw_border2(color):
    """Draw a border inside the display: the pixels along the  edges
    are deleted (set to black), the second row of pixels is painted
    in the given color.

    Parameters:
        senseHat -- the SenseHAT object
        color -- the color to use
    """

    # first paint the inner border
    for i in range(1, 7):
        _sense.set_pixel(1, i, color)
        _sense.set_pixel(6, i, color)
    for i in range(2, 6):
        _sense.set_pixel(i, 1, color)
        _sense.set_pixel(i, 6, color)

    # then delete the outer border
    for i in range(8):
        _sense.set_pixel(0, i, _black)
        _sense.set_pixel(7, i, _black)
    for i in range(1, 7):
        _sense.set_pixel(i, 0, _black)
        _sense.set_pixel(i, 7, _black)


def _get_pixel(screenData, x, y):
    index = y * 8 + x
    return screenData[index]


def _undraw_border1(screen):
    """Remove the border along the eges and replace it with data from
    screen.

    Parameters:
        senseHat -- the SenseHAT object
        screen -- the data of the screen to display (format as for SenseHAT)
    """

    # restore the outer border
    for i in range(8):
        pixel = _get_pixel(screen, 0, i)
        _sense.set_pixel(0, i, pixel)
        pixel = _get_pixel(screen, 7, i)
        _sense.set_pixel(7, i, pixel)
    for i in range(1, 7):
        pixel = _get_pixel(screen, i, 0)
        _sense.set_pixel(i, 0, pixel)
        pixel = _get_pixel(screen, i, 7)
        _sense.set_pixel(i, 7, pixel)


def _undraw_border2(borderColor, screen):
    """Move the border from the second row to the row along the eges
    and replace the second row with data from screen.

    Parameters:
        senseHat -- the SenseHAT object
        screen -- the data of the screen to display (format as for SenseHAT)
    """

    # first paint the outer border
    for i in range(8):
        _sense.set_pixel(0, i, borderColor)
        _sense.set_pixel(7, i, borderColor)
    for i in range(1, 7):
        _sense.set_pixel(i, 0, borderColor)
        _sense.set_pixel(i, 7, borderColor)

    # then restore the inner border
    for i in range(1, 7):
        pixel = _get_pixel(screen, 1, i)
        _sense.set_pixel(1, i, pixel)
        pixel = _get_pixel(screen, 6, i)
        _sense.set_pixel(6, i, pixel)
    for i in range(2, 6):
        pixel = _get_pixel(screen, i, 1)
        _sense.set_pixel(i, 1, pixel)
        pixel = _get_pixel(screen, i, 6)
        _sense.set_pixel(i, 6, pixel)


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


def _test():
    """Call for testing and watch on SenseHAT 
    (real or emulator, depending on import)"""

    _sense.low_light = False
    _sense.clear()
    _sense.set_pixels(testImages[0])

    scroll_up(testImages[1], borderColors=(_blue, _green), speed=.5)
    time.sleep(1)
    try_scroll_up(borderColor=_green, speed=.5)
    time.sleep(1)
    
    scroll_down(testImages[0], (_green, _blue), .3)
    time.sleep(1)
    try_scroll_down(_blue, .3)
    time.sleep(1)
    
    scroll_left(testImages[1], (_red, _green), speed=.2)
    time.sleep(1)
    try_scroll_left(_green, speed=.2)
    time.sleep(1)
    
    scroll_right(testImages[0], (_green, _red), speed=.3)
    time.sleep(1)
    try_scroll_right(_red, speed=.3)
    time.sleep(1)


if __name__ == "__main__":
    pass
    #_testAll()    # does not work because of relative imports


