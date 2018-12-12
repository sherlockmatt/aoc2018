from helpers import download
import numpy as np
from numba import njit, prange

padding = [False, False, False, False]


def getData():
    r = download('https://adventofcode.com/2018/day/12/input')
    iterlines = r.iter_lines()

    # Prepend and append some padding to allow the 5-wide window tests
    initialState = padding + [x == b'#'[0] for x in iterlines.__next__()[15:]] + padding
    # Skip the empty line in the input
    _ = iterlines.__next__()

    rules = []
    for line in iterlines:
        # Only store the rules which grow plants
        if line[9] == b'#'[0]:
            rule = 0
            for x in line[0:5]:
                rule = rule << 1
                rule += x == b'#'[0]
            rules.append(rule)

    return np.array(initialState, dtype=np.bool), np.array(rules, dtype=np.uint8)


@njit(parallel=True)
def calcNewState(currentState, newState, rules):
    # Calculate all available windows of 5 pots in parallel
    for i in prange(2, len(currentState) - 3):
        window = 0
        for x in currentState[i - 2:i + 3]:
            window = window << 1
            window += x

        # If the window matches any of the rules, grow a plant, if none match don't grow one
        newState[i] = np.equal(rules, window).any()


def calculateTotalPotValue(initialState, rules, generations):
    # Array index 0 is actually pot number -4 at the start, thanks to the padding
    shift = -4
    lastShift = shift
    currentState = initialState.copy()
    gen = 0
    converged = False
    while not converged and gen < generations:
        # Start the new state with some padding
        newState = np.array([False for _ in range(len(currentState))], dtype=np.bool)
        calcNewState(currentState, newState, rules)

        # Calculate how much to trim the array (remove False values on the ends)
        start = 0
        while not newState[start]:
            start += 1
        end = len(newState) - 1
        while not newState[end]:
            end -= 1

        # Execute the trim and add padding on both ends
        newState = np.array(np.append(padding, np.append(newState[start:end + 1], padding)), dtype=np.bool)

        # Adjust the shift for the trimming and padding
        shift += start - 4

        # Check for convergence i.e. the same pattern we saw last generation
        if len(currentState) == len(newState) and np.array_equal(currentState, newState):
            converged = True
            # Simulate the array "moving" for the remainder of the generations, at the current speed
            shift += (generations - gen - 1) * (shift - lastShift)

        currentState = newState
        lastShift = shift
        gen += 1

    print('Answer: {}'.format(sum([i + shift for i, v in enumerate(currentState) if v])))


def puzzle1(initialState, rules):
    calculateTotalPotValue(initialState, rules, 20)


def puzzle2(initialState, rules):
    calculateTotalPotValue(initialState, rules, 50000000000)


if __name__ == '__main__':
    inputData = getData()
    puzzle1(*inputData)
    puzzle2(*inputData)
