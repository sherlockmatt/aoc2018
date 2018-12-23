from helpers import download, manhattan
import numpy as np
from queue import PriorityQueue


def getData():
    r = download('https://adventofcode.com/2018/day/22/input')
    lines = r.text.strip().split('\n')
    depth = int(lines[0][7:])
    targetStr = lines[1][8:]
    target = tuple(map(int, targetStr.split(',')))
    return depth, target


def printGrid(grid):
    charMap = ['.', '=', '|']
    for l in grid:
        for p in l:
            print(charMap[p % 3], end='')
        print()


def expandGrid(grid, depth, targetX, targetY, toX, toY):
    curX = grid.shape[1] - 1
    curY = grid.shape[0] - 1
    newGrid = np.array([[0 if x > curX or y > curY else grid[y, x] for x in range(toX + 1)] for y in range(toY + 1)])

    for x in range(curX + 1, toX + 1):
        newGrid[0, x] = (x * 16807 + depth) % 20183

    for y in range(curY + 1, toY + 1):
        newGrid[y, 0] = (y * 48271 + depth) % 20183

    for y in range(1, toY + 1):
        for x in range(curX + 1, toX + 1):
            newGrid[y, x] = (newGrid[y, x - 1] * newGrid[y - 1, x] + depth) % 20183

    for y in range(curY + 1, toY + 1):
        for x in range(1, curX + 1):
            newGrid[y, x] = (newGrid[y, x - 1] * newGrid[y - 1, x] + depth) % 20183

    newGrid[targetY, targetX] = depth % 20183

    return newGrid


def puzzle1(depth, target):
    grid = expandGrid(np.array([[depth % 20183]]), depth, *target, *target)

    riskLevel = 0

    for y, line in enumerate(grid):
        for x, pos in enumerate(line):
            riskLevel += grid[y, x] % 3

    print('Answer: {}'.format(riskLevel))

    return grid


def puzzle2(grid, depth, target):
    tx, ty = target

    maxX = tx + 10
    maxY = ty + 10
    grid = expandGrid(grid, depth, tx, ty, maxX, maxY)

    minTravelTime = np.array([[[0 for _ in range(3)] for _ in range(maxX + 1)] for _ in range(maxY + 1)], dtype=np.uint16)

    # Using a priority queue means a .get() will always pop off the node with the lowest f(n)
    openSet = PriorityQueue()
    # (f(n), x, y, tool); 0 = neither, 1 = torch, 2 = climbing gear
    # This mapping of equipment means that grid[y, x] % 3 can't be used at (x, y)
    openSet.put((tx + ty, 0, 0, 1))

    closedSet = set()

    while not openSet.empty():
        node = openSet.get()
        fn, x, y, curEquipped = node

        if x == tx and y == ty and curEquipped == 1:
            while not openSet.empty():
                # Empty the queue, we're done
                openSet.get()
        else:
            closedSet.add((x, y, curEquipped))

            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                newX = x + dx
                newY = y + dy
                curTime = minTravelTime[y, x, curEquipped]

                if newX >= 0 and newY >= 0 and (newX, newY, curEquipped) not in closedSet:
                    # Check if we want to leave the current calculated grid, if so then expand it a bit more
                    if newX > maxX or newY > maxY:
                        maxX += 10
                        maxY += 10
                        grid = expandGrid(grid, depth, tx, ty, maxX, maxY)
                        newMTT = np.array([[[0 for _ in range(3)] for _ in range(maxX + 1)] for _ in range(maxY + 1)], dtype=np.uint16)
                        newMTT[:maxY - 9, :maxX - 9, :] = minTravelTime[:, :, :]
                        minTravelTime = newMTT

                    thisType = grid[y, x] % 3
                    otherType = grid[newY, newX] % 3
                    newTime = curTime + 1
                    newEquipped = curEquipped

                    # If they're the same type, we can just move there
                    # If they're different, check whether our tool is valid there
                    # If it is we can move, if not we'll have to swap
                    if not (thisType == otherType or otherType != curEquipped):
                        newTime += 7
                        newEquipped = ((thisType + otherType) * 2) % 3

                    # We must always switch to the torch at the target, so force this
                    if newX == tx and newY == ty and newEquipped != 1:
                        newTime += 7
                        newEquipped = 1

                    # A value of 0 means this node hasn't been visited yet
                    if minTravelTime[newY, newX, newEquipped] == 0 or newTime < minTravelTime[newY, newX, newEquipped]:
                        minTravelTime[newY, newX, newEquipped] = newTime
                        # Our f(n) heuristic is g(n) + manhattan distance, since this is an admissable heuristic for this problem
                        openSet.put((newTime + manhattan((newX, newY), (tx, ty)), newX, newY, newEquipped))

    # The target is always reached with the torch in hand
    print('Answer: {}'.format(minTravelTime[ty, tx, 1]))


if __name__ == '__main__':
    inputData = getData()
    p1Output = puzzle1(*inputData)
    puzzle2(p1Output, *inputData)
