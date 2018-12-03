from helpers import download


def getData():
    r = download('https://adventofcode.com/2018/day/2/input')
    return list(r.iter_lines())


def puzzle1(data):
    print('Answer: {}'.format(''))


def puzzle2(data):
    print('Answer: {}'.format(''))


if __name__ == '__main__':
    inputData = getData()
    puzzle1(inputData)
    puzzle2(inputData)
