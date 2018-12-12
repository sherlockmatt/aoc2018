from helpers import download
import numpy as np


def getData():
    r = download('https://adventofcode.com/2018/day/12/input')
    iterlines = r.iter_lines()

    # Prepend and append some padding to allow the 5-wide window tests
    initialState = [False, False, False, False] + [x == b'#'[0] for x in iterlines.__next__()[15:]] + [False, False, False, False]
    # Skip the empty line in the input
    _ = iterlines.__next__()

    rules = []
    for line in iterlines:
        rule = [x == b'#'[0] for x in line[0:5]]
        result = line[9] == b'#'[0]
        rules.append((rule, result))

    return initialState, np.array(rules)


def calculateTotalPotValue(initialState, rules, generations):
    # Array index 0 is actually pot number -4 at the start, thanks to the padding
    shift = -4
    currentState = np.array(initialState)
    gen = 0
    converged = False
    while not converged and gen < generations:
        # Start the new state with some padding
        newState = [False, False]

        # Calculate all available windows of 5 pots
        for i in range(2, len(currentState) - 3):
            matched = False
            j = -1
            # Check for a rule which matches
            while not matched and j < len(rules) - 1:
                j += 1
                # If any of the positions are different from the rule, it's not a match
                matched = not np.bitwise_xor(currentState[i - 2:i + 3], rules[j][0]).any()
            newState.append(rules[j][1] if matched else False)

        # Expand the padding if required
        prependVal = [False for x in newState[2:4] if x]
        appendVal = [False for x in newState[-2:] if x]
        newState = prependVal + newState + appendVal + [False, False]

        # If our padding grew into the negatives, update the index shift
        shift -= len(prependVal)

        # Check for convergence (i.e. the same pattern moving right one pot)
        if len(prependVal) == 0 and len(appendVal) > 0 and np.equal(currentState, newState[1:]).all():
            converged = True
            shift += generations - gen - 1

        currentState = np.array(newState)
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
