#from sense_hat import SenseHat
from sense_emu import SenseHat
#import logging
import time


s = SenseHat()
s.low_light = False

green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
nothing = (0,0,0)

n = nothing
a = yellow
b = (255, 153, 0)
c = (255, 51, 0)
d = (255, 35, 0)
e = (255, 15, 0)
f = red
g = (102, 0, 0)
h = (51, 0, 0)

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

def init(i):
    s.set_pixels(testImages[i])

def scroll_vertical (sense, scrollUp, newRows):
    """Scroll the display of the given SenseHAT vertically up or down
    (defined by scrollUp: True/False) by the number of rows given in
    newRows. newRows must be an array of arrays that are each length 8.
    The new rows will be fed into the display starting at element 0
    from the array. They will be appended at the bottom when scrolling
    up, and at the top when scrolling down).
    """

    scrollRange = range(0, 7) if scrollUp else range(7, 0, -1)
    step = 1 if scrollUp else -1
    appendIndex = 7 if scrollUp else 0

    for newRowIndex in range(0, len(newRows)):
        # copy the information from the second-last row to the last row,
        # then from the third-last to the second-last and so on
        for row in scrollRange:
            #time.sleep(0.1)
            _copyRow (sense, row + step, row)
        #time.sleep(0.03)
        _appendRow (sense, appendIndex, newRows[newRowIndex])
        time.sleep(0.1)

def _copyRow (sense, fromRow, toRow):
    # if the values can be read and written separately:
    print('copy row {} to {}'.format(fromRow, toRow))
    for i in range(8):
        v = sense.get_pixel(i, fromRow)
        sense.set_pixel(i, toRow, v)

def _appendRow (sense, toRow, newData):
    print('appending newData to row {}'.format(toRow))
    #print('newData is {}'.format(newData))
    for i in range(8):
        color = newData[i]
        sense.set_pixel(i, toRow, color)

def test():
    print ("in init")


if __name__ == "__main__":
    a = init(1)
    time.sleep(1)
    data = [
        [n, n, n, b, f, b, n, n],
        [n, n, b, f, b, n, n, n],
        [n, b, f, b, n, n, n, n],
        [b, f, b, n, n, n, n, n],
    ]
    for i in range(4):
        scroll_vertical(s, False, data)

    time.sleep(2)
    for i in range(4):
        scroll_vertical(s, True, data)
