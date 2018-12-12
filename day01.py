from functools import reduce
from helpers import download


def getData():
    r = download('https://adventofcode.com/2018/day/1/input')
    return list(map((lambda x: int(x)), r.iter_lines()))


def puzzle1(data):
    print('Answer is: {}'.format(reduce((lambda x, y: x + y), data)))


def puzzle2(data):
    ans = False
    current = 0
    freqs = []

    dataCount = len(data)
    index = 0
    while not ans and index < 1000000:  # We should find it within 1 million checks, riiiight?
        current += data[index % dataCount]
        # This check isn't very performant but I can't be bothered to improve it
        # See puzzle2_faster for the very simple improvement...
        if current in freqs:
            ans = current
        else:
            freqs.append(current)
        index += 1

    print('Answer is: {}, found at index: {}'.format(ans, index))


def puzzle2_faster(data):
    ans = False
    current = 0
    freqs = set()

    dataCount = len(data)
    index = 0
    while not ans and index < 1000000:  # We should find it within 1 million checks, riiiight?
        current += data[index % dataCount]
        # This test is much faster for sets than lists
        if current in freqs:
            ans = current
        else:
            freqs.add(current)
        index += 1

    print('Answer is: {}, found at index: {}'.format(ans, index))


if __name__ == '__main__':
    inputData = getData()
    puzzle1(inputData)
    puzzle2_faster(inputData)
