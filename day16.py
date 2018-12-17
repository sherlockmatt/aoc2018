from helpers import download
import re

opcodes = {
    'addr': (lambda r, i: [r[i[1]] + r[i[2]] if k == i[3] else v for k, v in enumerate(r)]),
    'addi': (lambda r, i: [r[i[1]] + i[2] if k == i[3] else v for k, v in enumerate(r)]),
    'mulr': (lambda r, i: [r[i[1]] * r[i[2]] if k == i[3] else v for k, v in enumerate(r)]),
    'muli': (lambda r, i: [r[i[1]] * i[2] if k == i[3] else v for k, v in enumerate(r)]),
    'banr': (lambda r, i: [r[i[1]] & r[i[2]] if k == i[3] else v for k, v in enumerate(r)]),
    'bani': (lambda r, i: [r[i[1]] & i[2] if k == i[3] else v for k, v in enumerate(r)]),
    'borr': (lambda r, i: [r[i[1]] | r[i[2]] if k == i[3] else v for k, v in enumerate(r)]),
    'bori': (lambda r, i: [r[i[1]] | i[2] if k == i[3] else v for k, v in enumerate(r)]),
    'setr': (lambda r, i: [r[i[1]] if k == i[3] else v for k, v in enumerate(r)]),
    'seti': (lambda r, i: [i[1] if k == i[3] else v for k, v in enumerate(r)]),
    'gtir': (lambda r, i: [(1 if i[1] > r[i[2]] else 0) if k == i[3] else v for k, v in enumerate(r)]),
    'gtri': (lambda r, i: [(1 if r[i[1]] > i[2] else 0) if k == i[3] else v for k, v in enumerate(r)]),
    'gtrr': (lambda r, i: [(1 if r[i[1]] > r[i[2]] else 0) if k == i[3] else v for k, v in enumerate(r)]),
    'eqir': (lambda r, i: [(1 if i[1] == r[i[2]] else 0) if k == i[3] else v for k, v in enumerate(r)]),
    'eqri': (lambda r, i: [(1 if r[i[1]] == i[2] else 0) if k == i[3] else v for k, v in enumerate(r)]),
    'eqrr': (lambda r, i: [(1 if r[i[1]] == r[i[2]] else 0) if k == i[3] else v for k, v in enumerate(r)])
}


def getData():
    r = download('https://adventofcode.com/2018/day/16/input')
    registerRegex = re.compile(r'^(?:Before:|After: ) \[(\d+), (\d+), (\d+), (\d+)\]$')

    samples = []
    testProgram = []
    lines = r.iter_lines()

    line = lines.__next__().decode()
    while line[:6] == 'Before':
        samples.append([])

        # Example: Before: [2, 1, 1, 0]
        samples[-1].append(list(map(int, registerRegex.match(line).groups())))

        # Example: 10 1 3 1
        line = lines.__next__().decode()
        samples[-1].append(list(map(int, line.split(' '))))

        # Example: After:  [2, 1, 1, 0]
        line = lines.__next__().decode()
        samples[-1].append(list(map(int, registerRegex.match(line).groups())))

        # Consume the blank line
        _ = lines.__next__()
        # Get the next line for the loop to decide on
        line = lines.__next__().decode()

    # There are 3 line breaks separating the two parts of the input, one has been consumed, line holds the second
    # Consume the third, then put the rest of the lines into the output
    _ = lines.__next__()
    for line in lines:
        testProgram.append(list(map(int, line.decode().split(' '))))

    return samples, testProgram


def puzzle1(samples):
    output = 0
    for sample in samples:
        numMatch = 0
        for opcode, instruction in opcodes.items():
            if instruction(sample[0], sample[1]) == sample[2]:
                numMatch += 1

        if numMatch >= 3:
            output += 1

    print('Answer: {}'.format(output))


def finaliseOpcode(potentialOpcodes, opcodeMapping, opcodeNum):
    opcodeMapping[opcodeNum] = potentialOpcodes[opcodeNum][0]
    # Remove the possibility from the other opcodes
    for i, v in enumerate(potentialOpcodes):
        if opcodeMapping[opcodeNum] in v:
            v.remove(opcodeMapping[opcodeNum])

            # We might have ruled out all other options for this opcode, so finalise it if we can
            if len(potentialOpcodes[i]) == 1:
                finaliseOpcode(potentialOpcodes, opcodeMapping, i)


def puzzle2(samples, program):
    potentialOpcodes = [[k for k in opcodes.keys()] for _ in range(len(opcodes))]
    opcodeMapping = [False for _ in range(len(opcodes))]
    index = 0

    # When each opcode is finalised, its list becomes empty, so loop until all lists are empty
    while sum(map(len, potentialOpcodes)) > 0:
        sample = samples[index]
        opcodeNum = sample[1][0]
        # If we haven't figured this opcode out yet
        if len(potentialOpcodes[opcodeNum]) > 0:
            # Check all remaining potential opcodes against this sample
            for opcode in potentialOpcodes[opcodeNum]:
                if opcodes[opcode](sample[0], sample[1]) != sample[2]:
                    potentialOpcodes[opcodeNum].remove(opcode)

                    # We only need to check this when we rule out a potential opcode
                    if len(potentialOpcodes[opcodeNum]) == 1:
                        finaliseOpcode(potentialOpcodes, opcodeMapping, opcodeNum)

        index += 1

        if index == len(samples):
            print('No more samples to consider, analysis failed.')
            return

    registers = [0, 0, 0, 0]

    for instruction in program:
        registers = opcodes[opcodeMapping[instruction[0]]](registers, instruction)

    print('Answer: {}'.format(registers[0]))


if __name__ == '__main__':
    inputSamples, inputTestProgram = getData()
    puzzle1(inputSamples)
    puzzle2(inputSamples, inputTestProgram)
