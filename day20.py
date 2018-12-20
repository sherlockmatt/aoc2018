from helpers import download
from collections import deque

opposite = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E',
    'root': ''
}


class room:
    def __init__(self, letter, parent, lastBranch, distance):
        self.letter = letter
        self.parent = parent
        self.children = []
        self.lastBranch = lastBranch
        self.distance = distance


def printRooms(rootRoom):
    toPrint = deque([rootRoom])

    while len(toPrint) > 0:
        node = toPrint.pop()
        toPrint.extend(reversed(node.children))
        print(' |' * node.distance + '-' + node.letter)


def getData():
    r = download('https://adventofcode.com/2018/day/20/input')
    rootRoom = room('root', None, None, 0)

    line = r.text.strip()

    currentRoom = rootRoom
    curLastBranch = rootRoom
    index = 1  # Skip the ^ at the start
    maxDist = 0
    numLong = 0
    while line[index] != '$':
        char = line[index]
        if char == '(':
            if line[index + 1] == opposite[currentRoom.letter]:
                # There seem to be some triple-backtracks just to throw you off, i.e. SESWWWWN(SEEEENSWWWWN|)
                # Since this is completely pointless, this is a low-effort fix (just skip the whole group)
                while line[index] != ')':
                    index += 1
            else:
                curLastBranch = currentRoom
        elif char == '|':
            # In the special case that the next group is empty, i.e. xxx|)xxx, we'll go back to lastBranch on the ) anyway, so don't do it here
            if line[index + 1] != ')':
                currentRoom = currentRoom.lastBranch
        elif char == ')':
            currentRoom = currentRoom.lastBranch
            curLastBranch = currentRoom.lastBranch
        else:
            if char == opposite[currentRoom.letter]:
                # Ignore backtracking, but keep the current room up to date
                # Don't go to the parent if it's also the lastBranch, the end of the group will do that for us
                if currentRoom.parent != curLastBranch:
                    currentRoom = currentRoom.parent
            else:
                newRoom = room(char, currentRoom, curLastBranch, currentRoom.distance + 1)
                currentRoom.children.append(newRoom)
                currentRoom = newRoom

                # Keep track of the two metrics we need
                maxDist = max(maxDist, currentRoom.distance)
                if currentRoom.distance >= 1000:
                    numLong += 1

        index += 1

    return maxDist, numLong


def puzzle1(ans):
    print('Answer: {}'.format(ans))


def puzzle2(ans):
    print('Answer: {}'.format(ans))


if __name__ == '__main__':
    ans1, ans2 = getData()
    puzzle1(ans1)
    puzzle2(ans2)
