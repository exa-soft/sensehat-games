#from sense_hat import SenseHat
import logging
import time


def scrollVertical (sense, scrollUp, newRows):
    """Scroll the display of the given SenseHAT vertically up or down
    (defined by scrollUp: True/False) by the number of rows given in
    newRows. newRows must be an array of arrays that are each length 8.
    The new rows will be fed into the display starting at element 0
    from the array. They will be appended at the bottom when scrolling
    up, and at the top when scrolling down).
    """

    scrollRange = range(0, 7) if scrollUp else range(7, 0)
    step = 1 if scrollUp else -1
    appendIndex = 7 if scrollUp else 0

    print('scrollRange {}, step {}, appendIndex {}'.format(scrollRange, step, appendIndex))

    for newRowIndex in range(0, len(newRows)):
        print('scrolling for new row {}: {}'.format(newRowIndex, newRows[newRowIndex]))
        # copy the information from the second-last row to the last row,
        # then from the third-last to the second-last and so on
        for row in scrollRange:
            copyRow (sense, row + step, row)
            print('copied to row {}'.format(row))
        appendRow (sense, appendIndex, newRows[newRowIndex])

"""
        else:
            print('scrolling for new row {}: {}'.format(newRowIndex, newRows[newRowIndex]))
            # copy the information from the second-last row to the last row,
            # then from the third-last to the second-last and so on
            for row in range(7, 0):
                copyRow (sense, row - 1, row)
                print('copied to row {}'.format(row))
            appendRow (sense, 7, newRows[newRowIndex])
            print ('row is {}'.format(row))
"""

def copyRow (sense, fromRow, toRow):
    rowToCopy = sense[fromRow]
    sense.pop(toRow)
    sense.insert(toRow, rowToCopy)
    # if the values can be read and written separately:
    # for i in range(8):
    #    v = sense.get(i, fromRow)
    #    sense.set(i, toRow, v)

def appendRow (sense, toRow, rowData):
    sense.pop(toRow)
    sense.insert(toRow, rowData)
    # if the values can be read and written separately:
    #for i in range(8):
    #    sense.set(i, toRow, rowData[i])

def printSense (sense):
    for i in range(8):
        print(sense[i])

def initSense():
    s = [
        list('aabccbba'),
        list('bbcddcbb'),
        list('bcdeedcb'),
        list('cdeffedc'),
        list('cdeffedc'),
        list('bcdeedcb'),
        list('bbcddcbb'),
        list('abbccbaa')
    ]
    return s

def test():
    print ("in init")
    cnt.state()


if __name__ == "__main__":
    a = initSense()
    #test()
