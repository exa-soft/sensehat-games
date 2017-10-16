from sense_emu import SenseHat
#from sense_hat import SenseHat
#import logging
import time

    
def scroll_vertical (sense, scrollUp, newRows, speed=.1):
    """Scroll the display of the given SenseHAT vertically up or down
    (defined by scrollUp: True/False) by the number of rows given in
    newRows. newRows must be an array of arrays that are each length 8.
    The new rows will be fed into the display starting at element 0
    from the array. They will be appended at the bottom when scrolling
    up, and at the top when scrolling down).
    Speed is the time the display waits between scrolling steps.
    """

    scrollRange = range(0, 7) if scrollUp else range(7, 0, -1)
    step = 1 if scrollUp else -1
    appendIndex = 7 if scrollUp else 0

    for newRowIndex in range(0, len(newRows)):
        # copy the information from the second-last row to the last row,
        # then from the third-last to the second-last and so on
        for row in scrollRange:
            copy_row (sense, row + step, row)
        append_row (sense, appendIndex, newRows[newRowIndex])
        time.sleep(speed)


def scroll_horizontal (sense, scrollLeft, newCols, speed=.1):
    """Scroll the display of the given SenseHAT horizontally left or right
    (defined by scrollLeft: True/False) by the number of columns given in
    newCols. newCols must be an array of arrays that are each length 8.
    The new cols will be fed into the display starting at element 0
    from the array. They will be appended at the right when scrolling
    left, and at the left when scrolling right).
    Speed is the time the display waits between scrolling steps.
    """

    scrollRange = range(0, 7) if scrollLeft else range(7, 0, -1)
    step = 1 if scrollLeft else -1
    appendIndex = 7 if scrollLeft else 0

    for newColIndex in range(0, len(newCols)):
        # copy the information from the second-last col to the last col,
        # then from the third-last to the second-last and so on
        for col in scrollRange:
            copy_col (sense, col + step, col)
        append_col (sense, appendIndex, newCols[newColIndex])
        time.sleep(speed)


def copy_row (sense, fromRow, toRow):
    """Copy a row from the SenseHAT display to another row.
    fromRow and toRow are row indices (0..7)
    """
    #print('copy row {} to {}'.format(fromRow, toRow))
    for i in range(8):
        sense.set_pixel(i, toRow, sense.get_pixel(i, fromRow))


def copy_col (sense, fromCol, toCol):
    """Copy a column from the SenseHAT display to another column.
    fromCol and toCol are column indices (0..7)
    """
    #print('copy col {} to {}'.format(fromCol, toCol))
    for i in range(8):
        sense.set_pixel(toCol, i, sense.get_pixel(fromCol, i))


def append_row (sense, toRow, newData):
    """Append data from an 8 element array with color values
    to a given row on the SenseHAT display.
    toRow must be a row index (0..7).
    newData must be an 8 element array with color tuples.
    """
    #print('appending newData to row {}'.format(toRow))
    for i in range(8):
        sense.set_pixel(i, toRow, newData[i])


def append_col (sense, toCol, newData):
    """Append data from an 8 element array with color values
    to a given column on the SenseHAT display.
    toCol must be a row index (0..7).
    newData must be an 8 element array with color tuples.
    """
    #print('appending newData to column {}'.format(toCol))
    for i in range(8):
        sense.set_pixel(toCol, i, newData[i])


def screen2rows (data, fromTop):
    """Convert an array with screen data (64 elements)
    to an array of rows (8 elements with 8 elements each).
    fromTop defines if element 0 is topmost or bottommost row.
    """
    rowRange = range(8) if fromTop else range(8, 0)
    return [data[y*8:(y+1)*8] for y in rowRange]


def screen2cols (data, fromLeft):
    """Convert an array with screen data (64 elements)
    to an array of columns (8 elements with 8 elements each).
    fromLeft defines if element 0 is left or rightmost column.
    """
    colRange = range(8) if fromLeft else range(8, 0)
    cols = [None] * 8
    for x in colRange:
        cols[x] = [data[y*8 + x] for y in range(8)]
    return cols


### test code ###########################################

_s = SenseHat()
_s.low_light = False

_n = (0,   0,   0)   # nothing
_a = (255, 255, 0)   # yellow
_b = (255, 153, 0)   # orange
_f = (255, 0,   0)   # red

_testImages = [
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

_scrollData = [
        [_n, _n, _n, _b, _f, _b, _n, _n],
        [_n, _n, _b, _f, _b, _n, _n, _n],
        [_n, _b, _f, _b, _n, _n, _n, _n],
        [_b, _f, _b, _n, _n, _n, _n, _n],
    ]


def _init(i):
    _s.set_pixels(_testImages[i])
   

def _testVertical():
    print ("in _testVertical")

    a = _init(1)
    time.sleep(1)
    for i in range(4):
        scroll_vertical(_s, False, _scrollData)

    time.sleep(2)
    for i in range(4):
        scroll_vertical(_s, True, _scrollData)


def _testHorizontal():
    print ("in _testHorizontal ")

    a = _init(1)
    time.sleep(1)    
    for i in range(4):
        scroll_horizontal(_s, False, _scrollData)

    time.sleep(2)
    for i in range(4):
        scroll_horizontal(_s, True, _scrollData)
    




if __name__ == "__main__":
    #_testVertical()
    _testHorizontal()
