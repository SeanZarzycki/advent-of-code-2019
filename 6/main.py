import itertools
from iteration_utilities import deepflatten

orbits = {}
bidirect_orbits = {}

data_filename = 'input.txt'
with open(data_filename) as f:
    lines = f.readlines()

for line in lines:
    line = line.rstrip('\n')
    pair = line.split(')')
    if pair[1] in orbits:
        orbits[pair[1]].append(pair[0])
    else:
        orbits[pair[1]] = [pair[0]]
    if pair[0] not in orbits:
        orbits[pair[0]] = []

    if pair[1] in bidirect_orbits:
        bidirect_orbits[pair[1]].append(pair[0])
    else:
        bidirect_orbits[pair[1]] = [pair[0]]

    if pair[0] in bidirect_orbits:
        bidirect_orbits[pair[0]].append(pair[1])
    else:
        bidirect_orbits[pair[0]] = [pair[1]]


def traverse_part1(start, count):
    if len(orbits[start]) == 0:
        return count
    return sum([traverse_part1(x, count+1) for x in orbits[start]])

visited = []
def traverse_part2(start, count):
    visited.append(start)
    if start in bidirect_orbits['SAN']:
        return count-1
    return [traverse_part2(x, count + 1) for x in bidirect_orbits[start] if x not in visited]

#part1 = sum([traverse_part1(o, 0) for o in orbits])
#print(part1)
l = traverse_part2('YOU', 0)
print(l)
part2 = list(deepflatten(l))
print(part2)