from helpers import download
import numpy as np
from numpy.core import defchararray as npc
from functools import reduce


def getData():
    r = download('https://adventofcode.com/2018/day/2/input')
    return list(r.iter_lines())


def puzzle1(data):
    twos = 0
    threes = 0
    for line in data:
        counts = [0 for _ in range(b'a'[0], b'z'[0] + 1)]
        for char in line:
            counts[char - b'a'[0]] += 1
        if 2 in counts:
            twos += 1
        if 3 in counts:
            threes += 1

    print('Answer: {}'.format(twos * threes))


def puzzle2(data):
    # Process the data into a list of strings
    data = list(map((lambda x: x.decode()), data))
    dataLength = len(data)
    # Assume all the strings are the same length
    # Pretty safe assumption, the test is pointless if they aren't
    strLength = len(data[0])
    ans = False
    # Start at one since we can't compare the first string to anything else
    current = 1
    while not ans and current < dataLength:
        # Test current string against all previous strings
        test = 0
        while not ans and test < current:
            i = 0
            diff = 0
            outstr = ''
            # Count the differences, and build the answer at the same time
            while diff < 2 and i < strLength:
                if data[current][i] == data[test][i]:
                    outstr += data[current][i]
                else:
                    diff += 1
                i += 1
            if diff == 1:
                ans = outstr
            test += 1
        current += 1

    print('Answer: {}'.format(ans))


def puzzle2_oneline(d):
    return [np.delete(x, np.nonzero(npc.not_equal(x, y))) for x in d for y in d if np.count_nonzero(npc.not_equal(x, y)) == 1][0]


if __name__ == '__main__':
    inputData = getData()
    puzzle1(inputData)
    puzzle2(inputData)
    print('Answer: {}'.format(reduce((lambda x, y: x + y), puzzle2_oneline(list(map((lambda x: [y for y in x.decode()]), inputData))))))
