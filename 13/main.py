import operator

import sys
import itertools
import goless
import time
import os

with open('13/input.txt') as f:
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


EMPTY_TILE = 0
WALL_TILE = 1
BLOCK_TILE = 2
HORIZONTAL_PADDLE_TILE = 3
BALL_TILE = 4

def tile_to_char(tile):
    return [' ','|','#','=','O'][tile]



GRID_SIZE = 10000
grid = [[0 for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

max_x = 0
max_y = 0

output_chan = goless.chan(-1)
ball_chan = goless.chan(-1)
paddle_chan = goless.chan(-1)
control_chan = goless.chan(-1)

def controller(ball_chan, paddle_chan, control_chan):
    while(True):
        try:
            ball_x = ball_chan.recv()
            paddle_x = paddle_chan.recv()
            if ball_x > paddle_x:
                control_chan.send(1)
            elif ball_x < paddle_x:
                control_chan.send(-1)
            else:
                control_chan.send(0)
        except:
            print("asdf")
            return

goless.go(run, data, control_chan, output_chan)
goless.go(controller, ball_chan, paddle_chan, control_chan)



def print_grid(grid, max_x, max_y):
    os.system('cls')
    for y in range(max_y, -1, -1):
        for x in range(0, max_x+1):
            print(tile_to_char(grid[x][y]), end='')
        print('')

score = 0




while(True):
    try:
        x = output_chan.recv()
        y = output_chan.recv()
        if x == -1 and y == 0:
            score = output_chan.recv()
        else:
            max_x = max(x, max_x)
            max_y = max(y, max_y)
            tile = output_chan.recv()
            grid[x][y] = tile
            # if tile == BALL_TILE:
            #     ball_chan.send(x)
            # if tile == HORIZONTAL_PADDLE_TILE:
            #     paddle_chan.send(x)
      #  print_grid(grid, max_x, max_y)
    except Exception as e:
        print(e)
        break

print(sum(x.count(BLOCK_TILE) for x in grid))
print(score)