from helpers import download
from math import floor


def getData():
    r = download('https://adventofcode.com/2018/day/14/input')
    return int(r.text.strip())


def tick(scores, indexes):
    total = scores[indexes[0]] + scores[indexes[1]]

    if total >= 10:
        scores.append(floor(total / 10))
    scores.append(total % 10)

    indexes[0] = (indexes[0] + scores[indexes[0]] + 1) % len(scores)
    indexes[1] = (indexes[1] + scores[indexes[1]] + 1) % len(scores)


def puzzle1(data):
    scores = [3, 7]
    indexes = [0, 1]

    while len(scores) < data + 10:
        tick(scores, indexes)

    output = ''
    for i in scores[-10:]:
        output += str(i)

    print('Answer: {}'.format(output))


def compareSlices(haystack, needle):
    if len(haystack) < len(needle):
        return False

    i = 0
    match = False
    while not match and i <= len(haystack) - len(needle):
        j = 0
        match = True
        while match and j < len(needle):
            if haystack[i + j] != needle[j]:
                match = False
            j += 1
        i += 1

    return match


def puzzle2(data):
    scores = [3, 7]
    indexes = [0, 1]
    inputList = list(map(int, str(data)))
    inputLength = len(inputList)
    lastLength = 2

    while not compareSlices(scores[lastLength + 1 - inputLength:], inputList):
        lastLength = len(scores)
        tick(scores, indexes)

    print('Answer: {}'.format(len(scores) - inputLength - 1))


if __name__ == '__main__':
    inputData = getData()
    puzzle1(inputData)
    puzzle2(inputData)
