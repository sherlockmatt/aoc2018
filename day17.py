from helpers import download
import re
import numpy as np


def printGrid(grid):
    for line in grid:
        for char in line:
            print(char, end='')
        print()


def expandGrid(grid, shiftX, shiftY, coords):
    # Allow padding in the x direction since water can travel 1 space past each solid surface
    newMinX = min(coords['x']) - 1
    newMaxX = max(coords['x']) + 1
    newMinY = min(coords['y'])
    newMaxY = max(coords['y'])

    # The first time, initialise the as-yet-unknown shiftY to the correct value
    if shiftY == -1:
        shiftY = newMinY

    curMinX = shiftX
    curMaxX = len(grid[0]) + shiftX
    curMinY = shiftY
    curMaxY = len(grid) + shiftY

    # Prepend free space onto each row to expand in the -x direction
    if newMinX < curMinX:
        for k, v in enumerate(grid):
            grid[k] = ['.' for _ in range(newMinX, curMinX)] + v
        shiftX = newMinX

    # Append free space onto each row to expand in the +x direction
    if newMaxX > curMaxX:
        for k, v in enumerate(grid):
            grid[k] = v + ['.' for _ in range(curMaxX, newMaxX + 1)]

    # Prepend rows of free space to the grid to expand in the -y direction
    if newMinY < curMinY:
        grid = [['.' for _ in range(min(curMinX, newMinX), max(curMaxX, newMaxX + 1))] for _ in range(newMinY, curMinY)] + grid
        shiftY = newMinY

    # Append rows of free space to the grid to expand in the +y direction
    if newMaxY > curMaxY:
        grid = grid + [['.' for _ in range(min(curMinX, newMinX), max(curMaxX, newMaxX + 1))] for _ in range(curMaxY, newMaxY + 1)]

    return grid, shiftX, shiftY


def getData():
    r = download('https://adventofcode.com/2018/day/17/input')
    regex = re.compile(r'^([xy])=(\d+), ([xy])=(\d+)..(\d+)$')

    grid = [['.']]
    shiftX = 500
    shiftY = -1

    for line in r.iter_lines():
        k1, v1, k2, v2start, v2end = regex.match(line.decode()).groups()
        # Store two lists of the same length, so that the zip below creates the correct amount of coordinate pairs
        coords = {k1: [int(v1) for _ in range(int(v2start), int(v2end) + 1)], k2: [x for x in range(int(v2start), int(v2end) + 1)]}

        # Expand the grid if necessary
        grid, shiftX, shiftY = expandGrid(grid, shiftX, shiftY, coords)

        # Input all the clay pieces
        for x, y in zip(coords['x'], coords['y']):
            grid[y - shiftY][x - shiftX] = '#'

    return np.array(grid), shiftX


def checkRow(grid, x, y):
    # Walk left and right, checking to see if we're bounded by walls or if there's free space left to flow into
    for ddx in [-1, 1]:
        dx = ddx
        while grid[y][x + dx] == '|':
            dx += ddx
        if grid[y][x + dx] == '.':
            return False

    return True


def solidifyRow(grid, x, y):
    returnSet = set()

    # Handle the current location
    grid[y][x] = '~'
    if grid[y - 1][x] == '|':
        returnSet.add((x, y - 1))

    # Walk left and right changing flowing water to standing water, and tracking input flows
    for ddx in [-1, 1]:
        dx = ddx
        while grid[y][x + dx] == '|':
            grid[y][x + dx] = '~'
            if grid[y - 1][x + dx] == '|':
                returnSet.add((x + dx, y - 1))

            dx += ddx

    return returnSet


def simulate(grid, shiftX):
    # The initial node is under the spring at (500, 0)
    currentLayer = {(500 - shiftX, 0)}

    # Simulate in pseudo-real-time: progress one step from all frontiers at each timestep
    # This isn't the most efficient way, but it looks cool if you watch it
    while len(currentLayer) > 0:
        newLayer = set()

        for x, y in currentLayer:
            # Set this location to "running water"
            grid[y][x] = '|'

            # Check for falling off the bottom of the grid
            if y + 1 < len(grid):
                objBelow = grid[y + 1][x]
                if objBelow in ['#', '~']:
                    # The object below is solid, so check to see if we've filled up the row
                    if checkRow(grid, x, y):
                        # Turn all the flowing water into standing water
                        newNodes = solidifyRow(grid, x, y)
                        # Add nodes that are flowing into the current row to be checked
                        for node in newNodes:
                            newLayer.add(node)
                    else:
                        # We haven't filled up the row, so flow sideways if there's space
                        for dx in [-1, 1]:
                            if grid[y][x + dx] == '.':
                                newLayer.add((x + dx, y))
                else:
                    # There's empty space below, so flow down into it
                    newLayer.add((x, y + 1))

        currentLayer = newLayer

    return grid


def puzzle1(grid):
    numWet = np.count_nonzero(grid == '~')
    numDamp = np.count_nonzero(grid == '|')
    print('Answer: {}'.format(numWet + numDamp))


def puzzle2(grid):
    numWet = np.count_nonzero(grid == '~')
    print('Answer: {}'.format(numWet))


if __name__ == '__main__':
    inputData = getData()
    finalGrid = simulate(*inputData)
    puzzle1(finalGrid)
    puzzle2(finalGrid)
