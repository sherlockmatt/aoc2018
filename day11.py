from helpers import download
import numpy as np


# When we generate the 300x300 grid, instead of storing the power value (-5..4) we store the sum of
# all the power values from the current cell to (1, 1), inclusive.
#
# This can be done efficiently because the value of cell (x, y) is:
# [x, y] + [x-1, y] + [x, y-1] - [x-1, y-1]
# which is, respectively, adding the left rectangle, adding the top rectangle,
# then subtracting the bit we counted twice (the top-left square).
#
# Then to calculate the sum of any grid starting at (x, y) with size s is:
# [x+s-1, y+s-1] - [x, y+s-1] - [x+s-1, y] + [x, y]
# which is, respectively, the sum from the end of the square, subtract the left rectangle,
# subtract the top rectangle, then add on the bit we subtracted twice (the top-left square).
#
# This means that to calculate a square of any size costs 4 2D array lookups, 2 subtractions and an addition,
# meaning that the full calculation gets quicker as the square size goes up due to calculating fewer squares.

def getData():
    r = download('https://adventofcode.com/2018/day/11/input')
    serial = int(r.text.strip())

    data = np.zeros((300, 300), dtype=np.int32)

    for y in range(1, 301):
        for x in range(1, 301):
            curPower = (x + 10) * (x + 10) * y + (x + 10) * serial
            # The minimum value occurs at (1, 1), and is 121 + 11 * serial
            # Assuming the serial is positive, the power will always have a hundreds column.
            curCellPower = int(str(curPower)[-3]) - 5

            # Handle the special cases where there aren't values to the left or the top
            # Note when x==1 and y==1 nothing happens, because the sum of that cell is just itself
            if y == 1:
                if x > 1:
                    curCellPower += data[0][x - 2]
            elif x == 1:
                if y > 1:
                    curCellPower += data[y - 2][0]
            else:
                curCellPower += data[y - 1][x - 2] + data[y - 2][x - 1] - data[y - 2][x - 2]
            data[y - 1][x - 1] = curCellPower

    return data


def calcSquares(data, size):
    squares = np.zeros((301 - size, 301 - size), dtype=np.int32)
    for y in range(1, 302 - size):
        for x in range(1, 302 - size):
            startx = x - 2
            starty = y - 2
            endx = x + size - 2
            endy = y + size - 2

            val = data[endy][endx]

            # Handle the special cases where there aren't values to the left or the top
            # Note when x==1 and y==1 nothing happens, because the sum of that cell is just itself
            if y == 1:
                if x > 1:
                    val -= data[size - 1][endx]
            elif x == 1:
                if y > 1:
                    val -= data[endy][size - 1]
            else:
                val += data[starty][startx] - data[endy][startx] - data[starty][endx]
            squares[y - 1][x - 1] = val

    return squares


def puzzle1(data):
    squares = calcSquares(data, 3)

    coordy, coordx = np.unravel_index(squares.argmax(), squares.shape)

    # Correct for human numbers being 1-indexed
    print('Answer: {},{}'.format(coordx + 1, coordy + 1))


def puzzle2(data):
    squares = np.zeros((300, 300, 300), dtype=np.int32)
    for size in range(1, 301):
        # Since the incoming arrays are different sizes, assign them to a region of the correct shape
        squares[0:301 - size, 0:301 - size, size - 1] = calcSquares(data, size)

    coordy, coordx, maxSize = np.unravel_index(squares.argmax(), squares.shape)

    # Correct for human numbers being 1-indexed
    print('Answer: {},{},{}'.format(coordx + 1, coordy + 1, maxSize + 1))


if __name__ == '__main__':
    inputData = getData()
    puzzle1(inputData)
    puzzle2(inputData)
