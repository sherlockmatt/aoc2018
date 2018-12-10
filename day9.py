from helpers import download
import re


class doublyLinkedListNode:
    def __init__(self, value):
        self.value = value
        self.prevNode = None
        self.nextNode = None

    def next(self, num):
        if num == 1:
            return self.nextNode
        else:
            return self.nextNode.next(num - 1)

    def prev(self, num):
        if num == 1:
            return self.prevNode
        else:
            return self.prevNode.prev(num - 1)


def getData():
    r = download('https://adventofcode.com/2018/day/9/input')
    regex = re.compile(r'^(\d+) players; last marble is worth (\d+) points$')
    return tuple(map(int, regex.match(r.text.strip()).groups()))


def puzzle1(numPlayers, lastMarble):
    # It seems like there should be a linear algebra solution for this, maybe I'll find it later
    curNode = doublyLinkedListNode(0)
    curNode.nextNode = curNode
    curNode.prevNode = curNode
    currentPlayer = 1
    scores = [0 for _ in range(numPlayers)]
    for marble in range(1, lastMarble + 1):
        if marble % 23 > 0:
            # Create a new node, place it in between curNode.next(1) and curNode.next(2)
            newNode = doublyLinkedListNode(marble)
            newNode.nextNode = curNode.next(2)
            newNode.prevNode = curNode.next(1)
            curNode.next(2).prevNode = newNode
            curNode.next(1).nextNode = newNode
            # Set the current node to the newly added marble
            curNode = newNode
        else:
            # Add the marble to the current players score
            scores[currentPlayer - 1] += marble
            # Find the marble to remove and it to the current player's score
            remNode = curNode.prev(7)
            scores[currentPlayer - 1] += remNode.value
            # Bridge the list over the marble to remove
            remNode.prev(1).nextNode = remNode.next(1)
            remNode.next(1).prevNode = remNode.prev(1)
            # Set the current node to the one after the removed marble
            curNode = remNode.next(1)
            del remNode

        # Increment the player cyclicly, this way should be faster than currentPlayer = (currentPlayer + 1) % numPlayers
        if currentPlayer == numPlayers:
            currentPlayer = 1
        else:
            currentPlayer += 1

    print('Answer: {}'.format(max(scores)))


def puzzle2(numPlayers, lastMarble):
    puzzle1(numPlayers, lastMarble * 100)


if __name__ == '__main__':
    inputData = getData()
    puzzle1(*inputData)
    puzzle2(*inputData)
