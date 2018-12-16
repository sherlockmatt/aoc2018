from helpers import download
import numpy as np
from collections import deque


def getData():
    return download('https://adventofcode.com/2018/day/15/input')


def processData(data, elfAtk=3):
    actors = []
    field = []

    for y, line in enumerate(data.text.strip().split('\n')):
        field.append([])
        for x, char in enumerate(line):
            if char == '#':
                field[-1].append(-2)
            elif char == '.':
                field[-1].append(-1)
            else:
                actors.append((len(actors), x, y, char == 'E', 200, elfAtk if char == 'E' else 3))
                field[-1].append(len(actors) - 1)

    actors = np.array(actors, dtype={'names': ['id', 'x', 'y', 'isElf', 'hp', 'atk'], 'formats': ['uint16', 'uint8', 'uint8', 'bool', 'uint8', 'uint8']})

    return np.array(field), actors


def neighbours(x, y):
    for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
        yield x + dx, y + dy


def printField(field, actors):
    output = ''
    for line in field:
        fieldSeg = ''
        healthSeg = ''
        for obj in line:
            if obj == -2:
                fieldSeg += '#'
            elif obj == -1:
                fieldSeg += '.'
            else:
                icon = 'E' if actors[obj]['isElf'] else 'G'
                fieldSeg += icon
                healthSeg += ' {}({})'.format(icon, actors[obj]['hp'])
        output += '{}  {}\n'.format(fieldSeg, healthSeg)

    print(output.strip())


def move(field, actors, actorIndex):
    actor = actors[actorIndex]
    startNodes = []

    # Check the immediate neighbours first
    finished = False
    for check in neighbours(actor['x'], actor['y']):
        obj = field[check[1], check[0]]
        if obj >= 0 and actors[obj]['isElf'] != actor['isElf']:
            finished = True
        elif obj == -1:
            # Initialise the queue with all the neighbours of the actor, if the space is empty
            # Store these nodes with themselves as "parent", so that later we can see which node the answer stemmed from
            startNodes.append((check[0], check[1], check[0], check[1]))

    newLayer = deque(startNodes)
    targetNodes = []
    seen = set([(actor['x'], actor['y'])] + [(x[0], x[1]) for x in startNodes])

    layer = 0
    while not finished and len(newLayer) > 0:
        layer += 1
        curLayer = newLayer
        newLayer = deque()
        # Consume the entire current layer
        while len(curLayer) > 0:
            node = curLayer.popleft()
            x, y, parentX, parentY = node
            for check in neighbours(x, y):
                if not finished and check not in seen:
                    checkX, checkY = check
                    obj = field[checkY, checkX]
                    if obj == -1:  # is an empty space
                        newLayer.append((checkX, checkY, parentX, parentY))
                        seen.add((checkX, checkY))
                    elif obj >= 0 and actors[obj]['isElf'] != actor['isElf']:  # is an actor of the opposite type
                        # Add this node to the target list
                        targetNodes.append((x, y, parentX, parentY))

        # Check through the target nodes to decide the move, if any are available
        if len(targetNodes) > 0:
            targetNodes = np.array(targetNodes, dtype={'names': ['x', 'y', 'parentX', 'parentY'], 'formats': ['uint8' for _ in range(4)]})

            if len(targetNodes) > 1:
                # Resolve the ties by sorted based on target node reading order, then based on move node reading order
                targetNodes.sort(order=['y', 'x', 'parentY', 'parentX'])

            _, _, parentX, parentY = targetNodes[0]

            # Execute the move
            field[parentY, parentX] = actorIndex
            field[actor['y'], actor['x']] = -1
            actor['x'] = parentX
            actor['y'] = parentY

            finished = True


def attack(field, actors, actorIndex):
    actor = actors[actorIndex]
    minHp = None
    minHpId = None
    deathId = None

    # Find an attack target: the enemy with the lowest health
    for other in neighbours(actor['x'], actor['y']):
        otherX, otherY = other
        obj = field[otherY, otherX]
        if obj >= 0 and actors[obj]['isElf'] != actor['isElf']:
            otherHp = actors[obj]['hp']
            if not minHp or otherHp < minHp:
                minHp = otherHp
                minHpId = obj

    if minHpId is not None:  # If we found a target
        # Check if the target would die or not
        if actors[minHpId]['hp'] <= actor['atk']:
            actors = die(field, actors, minHpId)
            deathId = minHpId
        else:
            # Execute the attack
            actors[minHpId]['hp'] -= actor['atk']

    return actors, deathId


def die(field, actors, actorIndex):
    field[actors[actorIndex]['y'], actors[actorIndex]['x']] = -1
    actors = np.delete(actors, actorIndex)
    for actor in actors[actorIndex:]:
        actor['id'] -= 1
        field[actor['y'], actor['x']] -= 1

    return actors


def puzzle1Finish(actors):
    finished = not 0 < np.sum(actors[:]['isElf']) < len(actors)

    return finished, True


def puzzle2Finish(actors, startNumElves):
    numElves = np.sum(actors[:]['isElf'])
    elfDead = numElves != startNumElves
    finished = elfDead or numElves == len(actors)

    return finished, not elfDead


def simulate(field, actors, finishFunc, *finishFuncArgs):
    step = 0
    finished = False
    success = False
    while not finished:
        step += 1
        numDeaths = 0
        actorMap = [x for x in range(len(actors))]
        for actor in np.sort(actors, 0, order=['y', 'x']):
            actorId = actorMap[actor['id']]

            if not finished and actorId is not None:  # Skip actors who have died
                # Check if the combat is over
                finished, success = finishFunc(actors, *finishFuncArgs)
                if finished:
                    if success:
                        # Answer uses the full steps completed, so subtract 1
                        print('Answer: {}'.format((step - 1) * np.sum(actors[:]['hp'], 0)))
                else:
                    move(field, actors, actorId)
                    # This has to be an assignment because np.delete cannot be done in place, so we have to return it up the stack
                    actors, deathId = attack(field, actors, actorId)

                    # If an actor died, update the mapping
                    if deathId is not None:
                        actorMap[deathId + numDeaths] = None
                        for i in range(deathId + numDeaths + 1, len(actorMap)):
                            if actorMap[i] is not None:
                                actorMap[i] -= 1
                        numDeaths += 1

    return success


def puzzle1(data):
    simulate(*processData(data, 3), puzzle1Finish)


def puzzle2(data):
    elfAtk = 3
    finished = False

    while not finished:
        elfAtk += 1
        field, actors = processData(data, elfAtk)
        startNumElves = np.sum(actors[:]['isElf'])

        finished = simulate(field, actors, puzzle2Finish, startNumElves)


if __name__ == '__main__':
    inputData = getData()
    puzzle1(inputData)
    puzzle2(inputData)
