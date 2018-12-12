from helpers import download
import numpy as np
from numba import cuda


@cuda.jit(device=True)
def manhattan(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


@cuda.jit
def distMapKernel(distMap, data):
    numSeeds = distMap.shape[0]
    width = distMap.shape[2]
    height = distMap.shape[1]

    startX, startY, startZ = cuda.grid(3)
    stepX = cuda.gridDim.x * cuda.blockDim.x
    stepY = cuda.gridDim.y * cuda.blockDim.y
    stepZ = cuda.gridDim.z * cuda.blockDim.z

    for seed in range(startZ, numSeeds, stepZ):
        for x in range(startX, width, stepX):
            for y in range(startY, height, stepY):
                distMap[seed][y][x] = manhattan(x, y, data[seed][0], data[seed][1])


def calcSeedMap(distMap, data):
    blockdim = (8, 8, 8)
    griddim = (32, 32, 32)

    deviceMap = cuda.to_device(distMap)
    distMapKernel[griddim, blockdim](deviceMap, data)
    deviceMap.to_host()

    return distMap


@cuda.jit(device=True)
def collapseDistToCell(coord):
    # Implemented manually because numba doesn't support all numpy functions yet
    minVal = np.inf
    minIndex = 0
    multiMin = False
    for i, v in enumerate(coord):
        if v < minVal:
            minVal = v
            minIndex = i
            multiMin = False
        elif v == minVal:
            multiMin = True
    return False if multiMin else minIndex


@cuda.jit
def cellMapKernel(deviceMap, data):
    width = data.shape[2]
    height = data.shape[1]

    startX, startY = cuda.grid(2)
    stepX = cuda.gridDim.x * cuda.blockDim.x
    stepY = cuda.gridDim.y * cuda.blockDim.y

    for x in range(startX, width, stepX):
        for y in range(startY, height, stepY):
            deviceMap[y][x] = collapseDistToCell(data[:, y, x])


def calcCellMap(cellMap, data):
    blockdim = (32, 32)
    griddim = (64, 64)

    deviceMap = cuda.to_device(cellMap)
    cellMapKernel[griddim, blockdim](deviceMap, data)
    deviceMap.to_host()

    # Filter out all the False values before we return it
    return np.ma.masked_invalid(cellMap)


def getData():
    r = download('https://adventofcode.com/2018/day/6/input')

    data = np.array([list(map(int, x.decode().split(', '))) for x in r.iter_lines()])

    # Make the bounds 1 unit larger than the bounding seeds
    lowerbound = np.subtract(np.min(data, 0), [1, 1])
    upperbound = np.add(np.max(data, 0), [1, 1])
    width = upperbound[1] - lowerbound[1]
    height = upperbound[0] - lowerbound[0]

    # Re-index the dataset so that the smallest coordinate is 0
    data = np.subtract(data, [lowerbound] * data.shape[0])
    distMap = np.zeros((data.shape[0], width, height))
    distMap = calcSeedMap(distMap, data)
    return distMap, width, height


def puzzle1(distMap, width, height):
    cellMap = np.zeros((width, height), dtype=np.uint32)
    cellMap = calcCellMap(cellMap, distMap)

    # Because we made the bounds larger, any cells on the border are infinite in size
    infiniteSeeds = np.unique(np.concatenate((cellMap[0, :], cellMap[width - 1, :], cellMap[:, 0], cellMap[:, height - 1])))

    counts = np.delete(np.bincount(cellMap.flatten()), infiniteSeeds)

    print('Answer: {}'.format(counts.max()))


def puzzle2(distMap):
    # Trim off the border we added earlier
    distMap = distMap[:, 1:-1, 1:-1]

    # Sum the distances for each coordinate
    sums = np.sum(distMap, 0)

    print('Answer: {}'.format(np.count_nonzero(sums < 10000)))


if __name__ == '__main__':
    distMap_in, width_in, height_in = getData()
    puzzle1(distMap_in, width_in, height_in)
    puzzle2(distMap_in)
