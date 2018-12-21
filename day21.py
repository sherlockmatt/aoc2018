from helpers import download
from day16 import opcodes


def getData():
    r = download('https://adventofcode.com/2018/day/21/input')
    iterator = r.iter_lines()
    iprLine = iterator.__next__().decode().split(' ')
    instructions = [[int(y) if i > 0 else y for i, y in enumerate(x.decode().split(' '))] for x in iterator]
    return int(iprLine[1]), instructions


def simulate(ipr, instructions, bound):
    registers = [0, 0, 0, 0, 0, 0]
    prevSeen = set()
    lastSeen = None
    answer = False
    while not answer and registers[ipr] < len(instructions):
        instruction = instructions[registers[ipr]]

        if instruction[0] == 'gtrr':
            # There's a loop in the program that does a ">> 8" operation very slowly, so skip all the hard work when we detect it
            modReg = instructions[registers[ipr] - 2][1]
            registers[modReg] = registers[instruction[2]] >> 8

        registers = opcodes[instruction[0]](registers, instruction)
        registers[ipr] += 1

        if instruction[0] == 'eqrr' and min(instruction[1:3]) == 0:
            # The only way the program terminates is if an "eqrr 0 x ipr" instruction returns true
            # Therefore we can simply return the only value that can terminate the program at this time: whatever is in register x
            otherReg = registers[max(instruction[1:3])]
            if bound == 'lower':
                answer = otherReg
            elif bound == 'upper':
                # To get the upper bound is a little harder: wait for register x to loop, then return the last value of the loop
                if otherReg in prevSeen:
                    answer = lastSeen
                else:
                    prevSeen.add(otherReg)
                    lastSeen = otherReg

    return answer


def puzzle1(ipr, instructions):
    print('Answer: {}'.format(simulate(ipr, instructions, 'lower')))


def puzzle2(ipr, instructions):
    print('Answer: {}'.format(simulate(ipr, instructions, 'upper')))


if __name__ == '__main__':
    inputData = getData()
    puzzle1(*inputData)
    puzzle2(*inputData)
