from helpers import download
from day16 import opcodes
from math import sqrt, floor


def getData():
    r = download('https://adventofcode.com/2018/day/19/input')
    iterator = r.iter_lines()
    iprLine = iterator.__next__().decode().split(' ')
    instructions = [[int(y) if i > 0 else y for i, y in enumerate(x.decode().split(' '))] for x in iterator]
    return int(iprLine[1]), instructions


def divisors(n):
    sqrtn = sqrt(n)

    yield 1
    yield n

    for i in range(2, floor(sqrtn) + 1):
        if n % i == 0:
            yield i
            if i != sqrtn:
                yield int(n / i)


def simulate(ipr, instructions, registers):
    answer = False
    while not answer and registers[ipr] < len(instructions):
        instruction = instructions[registers[ipr]]
        registers = opcodes[instruction[0]](registers, instruction)

        registers[ipr] += 1

        if instruction[3] == 0:
            # The provided program calculates a target number, the sums the divisors of that target number
            # This value is what gets stored in register 0, so shortcut the program and calculate it ourselves
            # We wait until something is written into register 0 - that means the program has started summing, i.e. the target number is ready
            # We don't know which register it's in, but it's the biggest value so we can work it out
            answer = sum(divisors(sorted(registers)[-1]))

    return answer


def puzzle1(ipr, instructions):
    print('Answer: {}'.format(simulate(ipr, instructions, [0, 0, 0, 0, 0, 0])))


def puzzle2(ipr, instructions):
    print('Answer: {}'.format(simulate(ipr, instructions, [1, 0, 0, 0, 0, 0])))


if __name__ == '__main__':
    inputData = getData()
    puzzle1(*inputData)
    puzzle2(*inputData)
