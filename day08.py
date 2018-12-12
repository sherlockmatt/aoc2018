from helpers import download


class node:
    def __init__(self, parent, numchildren, nummeta):
        self.parent = parent
        self.numchildren = numchildren
        self.nummeta = nummeta
        self.children = []
        self.meta = []

    def value(self):
        value = 0
        if self.numchildren == 0:
            value = sum(self.meta)
        else:
            for i in self.meta:
                if 0 < i <= len(self.children):
                    value += self.children[i - 1].value()

        return value


def getData():
    r = download('https://adventofcode.com/2018/day/8/input')
    data = list(map(int, r.text.strip().split(' ')))

    total = 0
    rootNode = node(None, data[0], data[1])
    curNode = rootNode
    # We've already consumed the first two indexes
    i = 2
    while i < len(data):
        if curNode.numchildren > len(curNode.children):
            # Start a new child
            newNode = node(curNode, data[i], data[i + 1])
            curNode.children.append(newNode)
            curNode = newNode
            i += 2
        else:
            # We've finished this nodes children, consume its metadata
            curNode.meta = data[i:i + curNode.nummeta]
            total += sum(curNode.meta)
            i += curNode.nummeta
            # This node is finished, move up to its parent
            curNode = curNode.parent

    return rootNode, total


def puzzle1(total):
    # It's more efficient to keep track of the total as we parse the input, but it doesn't fit this puzzle1/puzzle2 format
    print('Answer: {}'.format(total))


def puzzle2(rootNode):
    print('Answer: {}'.format(rootNode.value()))


if __name__ == '__main__':
    inputRootNode, inputTotal = getData()
    puzzle1(inputTotal)
    puzzle2(inputRootNode)
