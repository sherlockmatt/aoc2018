from helpers import download
import re


def getData():
    r = download('https://adventofcode.com/2018/day/3/input')
    data = []
    regex = re.compile(r'^#(\d+) @ (\d+),(\d+): (\d+)x(\d+)$')
    # The wording of the problem says the size is "at least 1000x1000"
    # My input is exactly 1000x1000, but let's play it safe and work it out anyway
    max_x = 0
    max_y = 0
    for line in [x.decode() for x in r.iter_lines()]:
        linematch = regex.match(line)
        _, left, top, width, height = map(int, linematch.groups())
        # Process each line into a list of (x,y) tuples that its rectangle covers
        coords = []
        for x in range(left, left + width):
            for y in range(top, top + height):
                coords.append((x, y))
        max_x = max(max_x, left + width)
        max_y = max(max_y, top + height)
        data.append(coords)
    print('Grid size is {}x{}'.format(max_x, max_y))
    return data, (max_x, max_y)


def puzzle1(data, max_x, max_y):
    # Make an array of size (max_x,max_y) full of False
    # Not very memory efficient, but fast for checking particular coords
    seenOnce = [False] * max_y
    for i in range(max_y):
        seenOnce[i] = [False] * max_x
    seenMulti = set()
    count = 0
    for line in data:
        for coord in line:
            x, y = coord
            # If we haven't seen it, see it
            if not seenOnce[x][y]:
                seenOnce[x][y] = True
            # If we've seen it exactly once, increment count
            elif coord not in seenMulti:
                seenMulti.add(coord)
                count += 1

    print('Answer: {}'.format(count))
    return seenMulti


def puzzle2(data, seenMulti):
    dataLength = len(data)
    found = False
    i = 0
    while not found and i < dataLength:
        line = data[i]
        lineLength = len(line)
        overlap = False
        j = 0
        # Don't bother continuing to check once we found an overlap
        while not overlap and j < lineLength:
            # If we've seen this coord at least twice, it must overlap something
            if line[j] in seenMulti:
                overlap = True
            j += 1
        i += 1
        # Deliberately save the index after incrementing because the ID's are 1-indexed
        if not overlap:
            found = i

    print('Answer: {}'.format(found))


if __name__ == '__main__':
    inputData, maxSize = getData()
    p1Output = puzzle1(inputData, *maxSize)
    puzzle2(inputData, p1Output)
