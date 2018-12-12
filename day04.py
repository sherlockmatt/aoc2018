from helpers import download
import re
import numpy as np


def getData():
    r = download('https://adventofcode.com/2018/day/4/input')
    # Make an array for the year 1518 (which is not a leap year)
    initialData = [None] * 12
    for i, v in enumerate([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]):
        initialData[i] = [None] * v
    regex = re.compile(r'^\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (?:(w)akes up|(f)alls asleep|Guard #(\d+) begins shift)$')
    guardSeen = []
    guardMap = []
    guardMaxDays = 0
    for line in [x.decode() for x in r.iter_lines()]:
        linematch = regex.match(line)
        # Two of the last 3 groups (w,f,g) will return None since they weren't matched
        _, m, d, H, M, w, f, g = [(x if not x or x in ['w', 'f'] else int(x)) for x in linematch.groups()]
        # Handle a special case where guards start just before midnight
        if H == 23:
            # Roll over a month if we're on the last day, else add a day
            if d > len(initialData[m]):
                m += 1
                d = 1
            else:
                d += 1

        # Days and months are 1-indexed, so decrement one now to get the index
        m -= 1
        d -= 1

        # Initialise this entry in the array if it hasn't been seen yet
        if not initialData[m][d]:
            initialData[m][d] = {'g': 0, 'w': [], 'f': []}

        if w or f:  # This line is a wake or fall asleep action
            action = w if w else f
            # Store the minutes at which this action happened on this day in reverse order -
            initialData[m][d][action] = sorted(initialData[m][d][action][:] + [M], reverse=True)
        else:  # Then this is a guard shift start
            # If we haven't seen this guard before, add them to the guardMap
            # Maintaining a map like this rather than indexing on the raw id compacts the dataset a lot
            # For the input I had, this reduces it from (3468, 19, 60) to only (22, 19, 60)
            if g not in guardMap:
                guardMapIndex = len(guardMap)
                guardMap.append(g)
            else:
                guardMapIndex = guardMap.index(g)

            # Set the guardMap index for this date
            initialData[m][d]['g'] = guardMapIndex

            # Keep track of the number of times we've seen each guard
            if guardMapIndex < len(guardSeen):
                guardSeen[guardMapIndex] += 1
            else:
                guardSeen.append(1)

            # Keep track of the most days we've seen any particular guard
            guardMaxDays = max(guardMaxDays, guardSeen[guardMapIndex])

    # Build the template for the numpy array, in shape (guard count, guardMaxDays, 60)
    # Add one to guardMaxId to avoid 0-index issues
    template = [None] * len(guardMap)
    for i in range(len(guardMap)):
        template[i] = [None] * guardMaxDays
        for j in range(guardMaxDays):
            template[i][j] = [False] * 60
    data = np.array(template)
    # Loop over the intial data again to convert it into something a little more useful
    for month in initialData:
        for day in month:
            # We don't have data for some days
            if day:
                g = day['g']
                # We use the seen counter to track where we insert this day's data
                # Decrement comes first because of 0-indexing
                guardSeen[g] -= 1
                while len(day['f']) > 0:
                    # Pop the earliest pair of falling/waking off the end of the lists
                    # This works because we sorted in reverse order before
                    f = day['f'].pop()
                    w = day['w'].pop()
                    # Set each minute in the interval to True for this (guard id, seen count) pair
                    data[g][guardSeen[g]][f:w] = [True for _ in range(f, w)]

    return data, guardMap


def puzzle1(data, guardMap):
    # Sum the minutes asleep for each day, then sum those for each guard
    sleepiestGuard = np.argmax(np.sum(np.sum(data, axis=2), axis=1))
    # Sum over each minute for that guard (minute is axis 0 now since we "removed" guardId axis)
    sleepyMinute = np.argmax(np.sum(data[sleepiestGuard], axis=0))
    # Recover the real guard id from the map
    print('Answer: {}'.format(guardMap[sleepiestGuard] * sleepyMinute))


def puzzle2(data, guardMap):
    # Sum over the day axis, pick the highest out of the whole lot, then decompose the id and minute from that
    gid, minute = np.unravel_index(np.argmax(np.sum(data, axis=1)), (data.shape[0], data.shape[2]))
    # Recover the real guard id from the map
    print('Answer: {}'.format(guardMap[gid] * minute))


if __name__ == '__main__':
    inputData, inputGuardMap = getData()
    puzzle1(inputData, inputGuardMap)
    puzzle2(inputData, inputGuardMap)
