from functools import reduce
import operator
import itertools
import matplotlib.pyplot as plt

xs = [(-17, 9, -5), (-1, 7, 13), (-19, 12, 5), (-6, -6, -4)]
testx = [(-1, 0, 2), (2, -10, -7), (4, -8, 8), (3, 5, -1)]
vs = [(0,0,0),(0,0,0),(0,0,0),(0,0,0)]


def velocity_comp(vs):
    if vs[0] > vs[1]:
        return +1
    if vs[0] < vs[1]:
        return -1
    else:
        return 0

def calc_v(positions):
    others = [positions[:positions.index(pos)] + positions[positions.index(pos)+1:]for pos in positions]
    for i in range(len(positions)):
        curr = positions[i]
        tot = (0,0,0)
        for other in others[i]:
            tot = tuple(map(operator.add, tuple(map(velocity_comp, zip(other, curr))), tot))
        yield tot

def apply_grav(v, x):
    for i in range(len(v)):
        new_x = tuple(map(operator.add, v[i], x[i]))
        yield new_x

def pot_energy(x):
    return sum(map(abs, x))

def kin_energy(v):
    return sum(map(abs, v))

def tot_energy(pot, kin):
    return pot * kin

init_state = {'x': xs.copy(), 'v': vs.copy(), 'pot': [0,0,0,0], 'kin': [0,0,0,0], 'tot': 0}
steps = [init_state]

num_steps = 10000

def add_triplet(a,b):
    return tuple(map(sum, zip(a,b)))

for i in range(1,num_steps+1):
    v_delta = list(calc_v(steps[i-1]['x']))
    new_v = steps[i-1]['v'].copy()
    for j in range(len(v_delta)):
        new_v[j] = add_triplet(new_v[j], v_delta[j])
    new_x = list(apply_grav(new_v, steps[i-1]['x']))
    new_pot = list(map(pot_energy, new_x))
    new_kin = list(map(kin_energy,new_v))

    new_tot = sum([a[0] * a[1] for a in list(zip(new_pot, new_kin))])
    steps.append({'x':new_x.copy(), 'v': new_v.copy(), 'pot': new_pot.copy(), 'kin': new_kin.copy(), 'tot': new_tot})

tots = [sum(x['x'][0]) for x in steps]
t = list(range(0, num_steps+1))
plt.plot(t, tots)
plt.show()