from helpers import download
import numpy as np

turnLeft = np.array([[0, 1], [-1, 0]])
turnRight = np.array([[0, -1], [1, 0]])
turnStraight = np.array([[1, 0], [0, 1]])

turnOrder = np.array([
    turnLeft,
    turnStraight,
    turnRight
])


def getData():
    r = download('https://adventofcode.com/2018/day/13/input')
    track = []
    carts = []

    for y, line in enumerate(r.iter_lines()):
        track.append([])
        for x, char in enumerate(line.decode()):
            if char in ['^', 'v']:
                track[-1].append('|')
                carts.append((x, y, 0, 1 if char == '^' else -1, 0))
            elif char in ['>', '<']:
                track[-1].append('-')
                carts.append((x, y, 1 if char == '>' else -1, 0, 0))
            else:
                track[-1].append(char)

    carts = np.array(carts, dtype={'names': ['x', 'y', 'dirx', 'diry', 'rot'], 'formats': [np.int16 for _ in range(5)]})

    return np.array(track), carts


def printTrackAndCarts(track, carts):
    for y, line in enumerate(track):
        output = ''
        for x, pos in enumerate(line):
            i = indexOfCartAtPos((x, y), carts)
            if i > -1:
                cart = carts[i]
                if cart['dirx'] == 1 and cart['diry'] == 0:
                    output += '>'
                elif cart['dirx'] == 0 and cart['diry'] == -1:
                    output += 'v'
                elif cart['dirx'] == -1 and cart['diry'] == 0:
                    output += '<'
                elif cart['dirx'] == 0 and cart['diry'] == 1:
                    output += '^'
                else:
                    output += '?'
            else:
                output += track[y][x]
        print(output)


def indexOfCartAtPos(pos, carts):
    for i, cart in enumerate(carts):
        if pos[0] == cart[0] and pos[1] == cart[1]:
            return i
    return -1


def simulateCarts(track_in, carts_in, stopOnFirstCrash):
    track = track_in.copy()
    carts = carts_in.copy()
    tick = 0
    shouldStop = False
    output = None

    while not shouldStop and tick < 20000:  # Safety net
        carts.sort(0, order=['y', 'x'])
        crashed = []

        # Execute all the moves in order
        for i, cart in enumerate(carts):
            x1 = cart['x']
            y1 = cart['y']
            x2 = x1 + cart['dirx']
            y2 = y1 - cart['diry']

            # Check for a crash
            j = indexOfCartAtPos((x2, y2), carts)
            if j > -1:
                if not stopOnFirstCrash:
                    # Add these indexes to the list of crashed carts
                    crashed.append(i)
                    crashed.append(j)
                else:
                    shouldStop = True
                    if not output:
                        output = (x2, y2)
            else:
                # Move the cart
                cart['x'] = x2
                cart['y'] = y2

                # Rotate the cart
                trackPiece = track[y2, x2]
                if trackPiece not in ['-', '|']:
                    if trackPiece == '/':
                        rotation = turnRight if cart['dirx'] == 0 else turnLeft
                    elif trackPiece == '\\':
                        rotation = turnRight if cart['diry'] == 0 else turnLeft
                    else:  # This must be an intersection
                        rotation = turnOrder[cart['rot']]
                        cart['rot'] = (cart['rot'] + 1) % turnOrder.shape[0]

                    newDir = np.matmul([cart['dirx'], cart['diry']], rotation)
                    cart['dirx'] = newDir[0]
                    cart['diry'] = newDir[1]

        # If required, clean up crashed carts
        if not stopOnFirstCrash:
            carts = np.delete(carts, crashed, 0)
            # Check to see whether there's only one cart left
            if carts.shape[0] == 1:
                shouldStop = True
                output = (carts[0]['x'], carts[0]['y'])

        tick += 1

    if not shouldStop:
        print('Answer: No crash after {} ticks'.format(tick))
    else:
        print('Answer: {},{}'.format(*output))


def puzzle1(track, carts):
    simulateCarts(track, carts, True)


def puzzle2(track, carts):
    simulateCarts(track, carts, False)


if __name__ == '__main__':
    inputData = getData()
    puzzle1(*inputData)
    puzzle2(*inputData)
