from helpers import download
import re


class light:
    def __init__(self, x, y, velx, vely):
        self.x = x
        self.y = y
        self.velx = velx
        self.vely = vely


def getData():
    r = download('https://adventofcode.com/2018/day/10/input')
    regex = re.compile(r'^position=< ?(-?\d+),  ?(-?\d+)> velocity=< ?(-?\d+),  ?(-?\d+)>$')
    return [light(*tuple(map(int, regex.match(x.decode()).groups()))) for x in r.iter_lines()]


def tick(data, direction):
    # Initiliase the bounds to data[0] position, since the comparisons require a starting value
    minx = data[0].x + direction * data[0].velx
    maxx = data[0].x + direction * data[0].velx
    miny = data[0].y + direction * data[0].vely
    maxy = data[0].y + direction * data[0].vely
    for i in data:
        i.x += direction * i.velx
        i.y += direction * i.vely
        minx = min(minx, i.x)
        maxx = max(maxx, i.x)
        miny = min(miny, i.y)
        maxy = max(maxy, i.y)

    return minx, maxx, miny, maxy


def puzzle1(data):
    # Use the tick function with direction 0 to calculate the size without changing anything
    minx, maxx, miny, maxy = tick(data, 0)
    width = maxx - minx
    height = maxy - miny
    # For the first frame, bodge the previous size to always be bigger since it doesn't matter
    prevwidth = width + 1
    prevheight = height + 1

    time = 0
    while width <= prevwidth and height <= prevheight:
        # Tick all the lights, until the first frame where the image has increased in size
        minx, maxx, miny, maxy = tick(data, 1)
        time += 1
        prevwidth = width
        prevheight = height
        width = maxx - minx
        height = maxy - miny

    # We've found the first frame after the solution, so go back one
    minx, maxx, miny, maxy = tick(data, -1)

    # Build output matrix
    output = [['░' for _ in range(minx, maxx + 1)] for _ in range(miny, maxy + 1)]
    for k in data:
        output[k.y - miny][k.x - minx] = '█'

    # Convert output matrix to a string for printing
    outputStr = '\n'.join([''.join(x) for x in output])

    print('Answer: \n{}'.format(outputStr))

    return time - 1


def puzzle2(time):
    print('Answer: {}'.format(time))


if __name__ == '__main__':
    inputData = getData()
    p1Output = puzzle1(inputData)
    puzzle2(p1Output)
