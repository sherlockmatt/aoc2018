from helpers import download
from functools import reduce
import numpy as np


def getData():
    r = download('https://adventofcode.com/2018/day/5/input')
    # Deliberately return the byte encoding
    return np.array([x[0] for x in r.iter_content() if x is not b'\n'])


def puzzle1(data):
    index = 0
    assert (data.ndim == 1)
    assert (data.shape[0] > 0)
    while index + 1 < data.shape[0]:
        if abs(data[index] - data[index + 1]) == 32:
            # If the neighbouring characters match, delete the pair
            data = np.delete(data, [index, index + 1])
            # Step back one to check if the previous character matches its new neighbour
            index = max(0, index - 1)
        else:
            index += 1
    return data


def puzzle2(data):
    # For each character a-z, remove all instances of it, run puzzle1() again to react the new string, then take the shortest result
    print('Answer: {}'.format(reduce(min, [puzzle1(np.delete(data, np.append(np.argwhere(data == a), np.argwhere(data == a + 32)))).shape[0] for a in range(b'A'[0], b'Z'[0] + 1)])))


if __name__ == '__main__':
    inputData = getData()
    p1Output = puzzle1(inputData)
    print('Answer: {}'.format(p1Output.shape[0]))
    puzzle2(p1Output)
