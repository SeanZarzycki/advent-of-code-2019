import operator

import sys
import itertools 
import goless
import time

with open('11/input.txt') as f:
    data = f.readline().split(',')

data = [int(x) for x in data]
data.extend([0]*10000)

POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2

OP_ADD = 1
OP_MULT = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JMP_NZ = 5
OP_JMP_Z = 6
OP_LT = 7
OP_EQ = 8
OP_SET_REL = 9

OP_STOP = 99
param_count = {
    OP_ADD: 3,
    OP_MULT: 3,
    OP_INPUT: 1,
    OP_OUTPUT: 1,
    OP_JMP_NZ: 2,
    OP_JMP_Z: 2,
    OP_LT: 3,
    OP_EQ: 3,
    OP_SET_REL: 1,
    OP_STOP: 0,

}

def decode_op(opcode):
    modes = []
    op = opcode % 100
    num_params = param_count[op]
    opcode = int(opcode / 100)

    for _ in range(num_params):
        modes.append(opcode % 10)
        opcode = int(opcode / 10)

    return (op, modes)

def decode_param(mem, param, mode, rel_base):
    try:
        if mode == POSITION_MODE:
            if param > len(mem):
                mem.extend([0]*(param-len(mem)))
            return mem[param]
        elif mode == IMMEDIATE_MODE:
            return param
        elif mode == RELATIVE_MODE:
            if rel_base+param >= len(mem):
                mem.extend([0]*(1+rel_base+param-len(mem)))
            return mem[rel_base+param]
        else:
            assert(False)
    except:
        print('exception!')


def run(data, input_chan, output_chan):
    pc = 0
    rel_base = 0
    while True:
        opcode = data[pc]
        (op, modes) = decode_op(opcode)
        if op == OP_ADD:

            p1 = decode_param(data, data[pc+1], modes[0], rel_base)
            p2 = decode_param(data, data[pc+2], modes[1], rel_base)
            if modes[2] == POSITION_MODE:
                p3 = data[pc+3]
            elif modes[2] == RELATIVE_MODE:
                p3 = rel_base + data[pc+3]
            data[p3] = p1 + p2
            pc = pc + 1 + param_count[op]
        elif op == OP_MULT:
            p1 = decode_param(data, data[pc+1], modes[0], rel_base)
            p2 = decode_param(data, data[pc+2], modes[1], rel_base)
            if modes[2] == POSITION_MODE:
                p3 = data[pc+3]
            elif modes[2] == RELATIVE_MODE:
                p3 = rel_base + data[pc+3]
            data[p3] = p1 * p2
            pc = pc + 1 + param_count[op]

        elif op == OP_INPUT: 
            if modes[0] == POSITION_MODE:
                p1 = data[pc+1]
            elif modes[0] == RELATIVE_MODE:
                p1 = rel_base + data[pc+1]
            else:
                assert(False)
            data[p1] = input_chan.recv()
            pc = pc + 1 + param_count[op]
        elif op == OP_OUTPUT:
            p1 = decode_param(data, data[pc+1], modes[0], rel_base)
            if output_chan != None:
                output_chan.send(p1)
            else:
                print(p1)
            pc = pc + 1 + param_count[op]

        elif op == OP_JMP_NZ:
            p1 = decode_param(data, data[pc+1], modes[0], rel_base)
            p2 = decode_param(data, data[pc+2], modes[1], rel_base)
            pc = p2 if p1 != 0 else pc + 1 + param_count[op]
        elif op == OP_JMP_Z:
            p1 = decode_param(data, data[pc+1], modes[0], rel_base)
            p2 = decode_param(data, data[pc+2], modes[1], rel_base)
            pc = p2 if p1 == 0 else pc + 1 + param_count[op]


        elif op == OP_LT:
            p1 = decode_param(data, data[pc+1], modes[0], rel_base)
            p2 = decode_param(data, data[pc+2], modes[1], rel_base)
            if modes[2] == POSITION_MODE:
                p3 = data[pc+3]
            elif modes[2] == RELATIVE_MODE:
                p3 = rel_base + data[pc+3]
            data[p3] = 1 if p1 < p2 else 0
            pc = pc + 1 + param_count[op]

        elif op == OP_EQ:
            p1 = decode_param(data, data[pc+1], modes[0], rel_base)
            p2 = decode_param(data, data[pc+2], modes[1], rel_base)
            if modes[2] == POSITION_MODE:
                p3 = data[pc+3]
            elif modes[2] == RELATIVE_MODE:
                p3 = rel_base + data[pc+3]
            data[p3] = 1 if p1 == p2 else 0
            pc = pc + 1 + param_count[op]
        elif op == OP_STOP:
            if output_chan != None:      
                output_chan.close()
            
            return

        elif op == OP_SET_REL:
            p1 = decode_param(data, data[pc+1], modes[0], rel_base)
            rel_base = rel_base + p1
            pc = pc + 1 + param_count[op]

        else:
            assert(False)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

STEP_LEFT = (-1, 0)
STEP_RIGHT = (1,0)
STEP_UP = (0,1)
STEP_DOWN = (0,-1)

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3

def step(curr, dir):
    return tuple(map(operator.add, curr, [STEP_UP, STEP_LEFT, STEP_DOWN, STEP_RIGHT][dir]))

TURN_LEFT = 0
TURN_RIGHT = 1
def turn(curr_dir, turn_dir):
    if turn_dir == TURN_LEFT:
        return [LEFT, DOWN, RIGHT, UP][curr_dir]
    elif turn_dir == TURN_RIGHT:
        return [RIGHT, UP, LEFT, DOWN][curr_dir]
    else:
        assert(0)
    
BLACK = 0
WHITE = 1

curr_point = (0,0)
curr_dir = UP
painted_spots = {curr_point: WHITE}

input_chan = goless.chan()
output_chan = goless.chan()

goless.go(run, data, input_chan, output_chan)

while(True):
    try:
        curr_color = painted_spots[curr_point] if curr_point in painted_spots else BLACK
        input_chan.send(curr_color)
        new_color = output_chan.recv()
        painted_spots[curr_point] = new_color
        turn_dir = output_chan.recv()
        curr_dir = turn(curr_dir, turn_dir)
        curr_point = step(curr_point, curr_dir)

    except:
        print('done')
        break
print(len(painted_spots))

x_coords = [curr_point[0] for curr_point in painted_spots.keys()]
y_coords = [curr_point[1] for curr_point in painted_spots.keys()]
x_range = list(range(min(x_coords),max(x_coords)+1))
y_range = list(range(min(y_coords),max(y_coords)+1))


coords = list(itertools.product(x_range, y_range))
coords.sort(key=lambda x: x[1], reverse=True)
last_coord = coords[0]
for c in coords:
    if c[1] < last_coord[1]:
        print('')
    if c in painted_spots:
        print('#' if painted_spots[c] == WHITE else '.', end="")
    else:
        print('.', end="")
    last_coord = c
