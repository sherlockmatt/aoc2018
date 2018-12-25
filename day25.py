from helpers import download, manhattan
import numpy as np


def getData():
    r = download('https://adventofcode.com/2018/day/25/input')
    return np.array([[int(y) for y in x.decode().split(',')] for x in r.iter_lines()])


def puzzle1(data):
    constellations = np.array([-1 for _ in range(len(data))])
    nextConst = 0

    for i, star in enumerate(data):
        nearby = []
        # No need to check stars we've previously done
        for j, otherStar in enumerate(data[i:]):
            if manhattan(star, otherStar) <= 3:
                # Because j starts from 0, add the "start" index
                nearby.append(i + j)

        if len(nearby) > 0:
            constToModify = np.unique(constellations[nearby])

            for j in nearby:
                constellations[j] = nextConst

            for j, const in enumerate(constellations):
                if const != -1 and const in constToModify:
                    constellations[j] = nextConst

            nextConst += 1

    print('Answer: {}'.format(np.unique(constellations).shape[0]))


def puzzle2():
    print('Answer: {}'.format('We saved Christmas!'))


if __name__ == '__main__':
    inputData = getData()
    puzzle1(inputData)
    puzzle2()
