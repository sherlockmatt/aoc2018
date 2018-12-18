from helpers import download
import numpy as np
from collections import deque


def printGrid(grid):
    for line in grid:
        for char in line:
            print(char, end='')
        print()


def neighbours(grid, x, y):
    # Start with all eight neighbours, then remove any outside the grid
    retSet = {(x - 1, y - 1), (x - 1, y), (x - 1, y + 1), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x + 1, y), (x + 1, y + 1)}

    if x == 0:
        retSet -= {(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)}
    elif x == len(grid[0]) - 1:
        retSet -= {(x + 1, y - 1), (x + 1, y), (x + 1, y + 1)}

    if y == 0:
        retSet -= {(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)}
    elif y == len(grid) - 1:
        retSet -= {(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)}

    return retSet


def getData():
    r = download('https://adventofcode.com/2018/day/18/input')
    return np.array([list(x.decode()) for x in r.iter_lines()])


def simulate(grid, maxSteps):
    # Only store the last 50, too many would ruin both memory- and time-performance
    recentlySeen = deque(maxlen=50)
    repeating = False
    step = 0
    while not repeating and step < maxSteps:
        step += 1
        newGrid = np.array([['.' for _ in y] for y in grid])
        for y, line in enumerate(grid):
            for x, char in enumerate(line):
                neighbourValues = np.array([grid[ny, nx] for nx, ny in neighbours(grid, x, y)])
                if char == '.':
                    newGrid[y, x] = '|' if np.count_nonzero(neighbourValues == '|') >= 3 else '.'
                elif char == '|':
                    newGrid[y, x] = '#' if np.count_nonzero(neighbourValues == '#') >= 3 else '|'
                elif char == '#':
                    newGrid[y, x] = '#' if np.count_nonzero(neighbourValues == '#') >= 1 and np.count_nonzero(neighbourValues == '|') >= 1 else '.'

        grid = newGrid

        # Check for a repeating pattern
        i = 0
        while not repeating and i < len(recentlySeen):
            if np.array_equal(recentlySeen[0], grid):
                loopLength = len(recentlySeen) - i
                loopStart = step - loopLength

                # Calculate how far through the repeating loop the final grid appears
                offset = (maxSteps - loopStart) % loopLength

                # Use the offset to store what would be seen at step `maxSteps` in `grid`, this causes the output to print correctly
                grid = recentlySeen[offset]

                repeating = True

            recentlySeen.rotate(-1)
            i += 1

        recentlySeen.append(grid)

    print('Answer: {}'.format(np.count_nonzero(grid == '#') * np.count_nonzero(grid == '|')))


def puzzle1(grid):
    simulate(grid, 10)


def puzzle2(grid):
    simulate(grid, 1000000000)


if __name__ == '__main__':
    inputData = getData()
    puzzle1(inputData)
    puzzle2(inputData)
