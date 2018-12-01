from functools import reduce
from helpers import download


def getData():
    r = download('https://adventofcode.com/2018/day/1/input')
    return list(map((lambda x: int(x)), r.iter_lines()))


def puzzle1():
    print('Answer is: {}'.format(reduce((lambda x, y: x + y), getData())))


def puzzle2():
    ans = False
    current = 0
    deltas = getData()
    freqs = []

    numdeltas = len(deltas)
    index = 0
    while not ans and index < 1000000:  # We should find it within 1 million checks, riiiight?
        current += deltas[index % numdeltas]
        # This check isn't very performant but I can't be bothered to improve it
        if current in freqs:
            ans = current
        else:
            freqs.append(current)
        index += 1

    print('Answer is: {}, found at index: {}'.format(ans, index))


def puzzle2_faster():
    ans = False
    current = 0
    deltas = getData()
    freqs = set()

    numdeltas = len(deltas)
    index = 0
    while not ans and index < 1000000:  # We should find it within 1 million checks, riiiight?
        current += deltas[index % numdeltas]
        # This test is much faster for sets than lists
        if current in freqs:
            ans = current
        else:
            freqs.add(current)
        index += 1

    print('Answer is: {}, found at index: {}'.format(ans, index))


if __name__ == '__main__':
    puzzle1()
    puzzle2_faster()
