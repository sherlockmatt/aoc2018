from helpers import download
import re
import numpy as np
from math import floor


def getData():
    r = download('https://adventofcode.com/2018/day/24/input')
    regex = re.compile(r'^(\d+) units each with (\d+) hit points (?:\((?:(immune|weak) to ((?:\w+,? ?)+))?(?:; (immune|weak) to ((?:\w+,? ?)+))?\) )?with an attack that does (\d+) (\w+) damage at initiative (\d+)$')
    groups = []
    curTeam = None

    for line in r.iter_lines():
        if line == b'Immune System:':
            curTeam = False
        elif line == b'Infection:':
            curTeam = True
        elif line == b'':
            pass
        else:
            units, hp, mod1Type, mod1List, mod2Type, mod2List, dmg, dmgType, init = regex.match(line.decode()).groups()
            mods = {}

            if mod1Type is not None:
                mods = {x: (0 if mod1Type == 'immune' else 2) for x in mod1List.split(', ')}

                # Groups can only have a second mod if they had a first one
                if mod2Type is not None:
                    mods.update({x: (0 if mod2Type == 'immune' else 2) for x in mod2List.split(', ')})

            # Store the groups with an ID
            groups.append((len(groups), curTeam, int(units), int(hp), mods, int(dmg), dmgType, int(init), int(units) * int(dmg)))

    return np.array(groups, dtype={'names': ['id', 'isInfection', 'units', 'hp', 'mods', 'dmg', 'dmgType', 'init', 'power'], 'formats': ['u1', 'bool', 'u4', 'u4', 'O', 'u2', '<U11', 'u1', 'u4']})


def sortByInit(groups):
    return np.flip(np.sort(groups, order=['init']), 0)


def sortByPowerThenInit(groups):
    return np.flip(np.sort(groups, order=['power', 'init']), 0)


def groupsOfOtherTeam(groups, fromGroup):
    return groups[groups['isInfection'] != fromGroup['isInfection']]


def calcDamage(attacker, defender):
    return attacker['units'] * attacker['dmg'] * (defender['mods'][attacker['dmgType']] if attacker['dmgType'] in defender['mods'] else 1)


def simulate(groups):
    # Make sure not to fiddle with the original
    groups = groups.copy()

    numGroups = len(groups)

    immuneGroups = groups['isInfection'] == False
    infectionGroups = groups['isInfection'] == True

    # These don't matter on the first loop, as long as they're >0
    immuneUnits = 1
    infectionUnits = 1

    stalemate = False

    while not stalemate and immuneUnits > 0 and infectionUnits > 0:
        targets = np.array([-1 for _ in range(numGroups)])

        # Choose targets in the correct order
        for group in sortByPowerThenInit(groups):
            # Dead groups don't take part
            if group['units'] > 0:
                maxDamage = 0
                target = -1
                for otherGroup in sortByPowerThenInit(groupsOfOtherTeam(groups, group)):
                    if otherGroup['units'] > 0 and otherGroup['id'] not in targets:
                        dmg = calcDamage(group, otherGroup)
                        if dmg > maxDamage:
                            maxDamage = dmg
                            target = otherGroup['id']

                # Groups that could only deal 0 damage instead do not target anyone
                targets[group['id']] = target if maxDamage > 0 else -1

        # If we get to a point where no-one can deal any damage to anyone else, declare a stalemate
        if np.count_nonzero(targets > -1) == 0:
            stalemate = True
        else:
            # Deal damage in the correct order
            for groupId in sortByInit(groups)['id']:
                group = groups[groupId]
                if group['units'] > 0 and targets[groupId] > -1:
                    target = groups[targets[groupId]]
                    dmg = calcDamage(group, target)
                    # Number of deaths is rounded down, and we can't kill more than are alive right now
                    unitsKilled = min(floor(dmg / target['hp']), target['units'])

                    groups[target['id']]['units'] -= unitsKilled
                    groups[target['id']]['power'] -= unitsKilled * groups[target['id']]['dmg']

        # Update the unit counts after this round
        immuneUnits = np.sum(groups[immuneGroups]['units'], 0)
        infectionUnits = np.sum(groups[infectionGroups]['units'], 0)

    return infectionUnits, immuneUnits


def puzzle1(groups):
    infectionUnits, immuneUnits = simulate(groups)
    print('Answer: {}'.format(max(infectionUnits, immuneUnits)))


def puzzle2(groups):
    # Make sure not to fiddle with the original
    groups = groups.copy()

    immuneGroups = np.argwhere(groups['isInfection'] == False).flatten()

    # Do the first battle without a boost, in case none is needed
    boost = 0
    infectionUnits, immuneUnits = simulate(groups)

    while infectionUnits > 0:
        # Use a gradient-descent-like stepping function to skip a lot of the useless boost values
        # The / 2000 is a bit of a magic number - it controls how close we get before stepping by 1 every time, and was chosen by eye
        # The check makes sure that if we're very close we only step by 1
        delta = floor((infectionUnits - immuneUnits) / 2000) + 1 if immuneUnits == 0 else 1
        boost += delta
        for i in immuneGroups:
            groups[i]['dmg'] += delta
            groups[i]['power'] += delta * groups[i]['units']

        infectionUnits, immuneUnits = simulate(groups)

    print('Answer: {}'.format(immuneUnits))


if __name__ == '__main__':
    inputData = getData()
    puzzle1(inputData)
    puzzle2(inputData)
