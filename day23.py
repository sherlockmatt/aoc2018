from helpers import download, manhattan
import re
import numpy as np


def getData():
    r = download('https://adventofcode.com/2018/day/23/input')
    regex = re.compile(r'^pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)$')
    data = np.array(list(map(lambda x: tuple(map(int, regex.match(x.decode()).groups())), r.iter_lines())), dtype={'names': ['x', 'y', 'z', 'r'], 'formats': [np.int32, np.int32, np.int32, np.uint32]})
    return data


def puzzle1(data):
    # Get the strongest nanobot
    tx, ty, tz, tr = np.sort(data, order=['r'])[-1]

    # Count the number of nanobots in its range
    count = 0
    for x, y, z, _ in data:
        if manhattan((tx, ty, tz), (x, y, z)) <= tr:
            count += 1

    print('Answer: {}'.format(count))


def puzzle2(data):
    # The input data is a dense L1-sphere with a bunch of outliers
    # It's much easier to process if these outliers are gone, so we identify them here
    # For each nanobot, count the number of other nanobots whose range overlaps with ours
    counts = np.array([0 for _ in range(data.shape[0])])
    for i, node in enumerate(data):
        x1, y1, z1, r1 = node
        # Don't compare against ourself
        for x2, y2, z2, r2 in np.append(data[:i], data[i + 1:]):
            dist = manhattan((x1, y1, z1), (x2, y2, z2))
            totalRadius = r1 + r2
            if dist <= totalRadius:
                counts[i] += 1

    # Remove the outliers, and just leave the core L1-sphere of nanobots
    # 0.95 is a magic number, but for this input overlapping with 95% of other bots is a good test
    # Ideally this would be improved.
    newData = np.delete(data, np.argwhere(counts < data.shape[0] * 0.95).flatten())

    # Use 3 orthogonal pairs of planes to constrain the single overlap point into a cube
    # Each plane pair takes the form (minimum value, maximum value)
    planes = [[None for _ in range(2)] for _ in range(3)]
    for x, y, z, r in newData:
        for i, v in enumerate([(1, 1, -1), (1, -1, 1), (-1, 1, 1)]):
            modX, modY, modZ = v
            mid = modX * x + modY * y + modZ * z
            low = mid - r
            high = mid + r

            if planes[i][0] is None:
                planes[i][0] = low
            else:
                planes[i][0] = max(low, planes[i][0])

            if planes[i][1] is None:
                planes[i][1] = high
            else:
                planes[i][1] = min(high, planes[i][1])

    # The three planes we used give us:
    # a <=  x + y - z <= A
    # b <=  x - y + z <= B
    # c <= -x + y + z <= C
    # Which we can resolve to:
    # a + b <= 2x <= A + B
    # a + c <= 2y <= A + C
    # b + c <= 2z <= B + C
    # Since we know we are only looking for one point, these must all have only one value, so we get:
    x = int((planes[0][0] + planes[1][0]) / 2)  # x = (a + b) / 2
    y = int((planes[0][0] + planes[2][0]) / 2)  # y = (a + c) / 2
    z = int((planes[1][0] + planes[2][0]) / 2)  # z = (b + c) / 2

    print('Answer: {}'.format(manhattan((0, 0, 0), (x, y, z))))


if __name__ == '__main__':
    inputData = getData()
    puzzle1(inputData)
    puzzle2(inputData)
