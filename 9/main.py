import sys
import itertools
import time

with open('9/input.txt') as f:
    data = f.readline().split(',')

data = [int(x) for x in data]
data.extend([0]*50000)

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
    if opcode == 21107:
        time.sleep(.1)
    op = opcode % 100
    num_params = param_count[op]
    opcode = int(opcode / 100)

    for _ in range(num_params):
        modes.append(opcode % 10)
        opcode = int(opcode / 10)

    return (op, modes)

def decode_param(mem, param, mode, rel_base):
    if mode == POSITION_MODE:
        if param > len(mem):
            mem.extend([0]*(param-len(mem)))
        return mem[param]
    elif mode == IMMEDIATE_MODE:
        return param
    elif mode == RELATIVE_MODE:
        if param > len(mem):
            mem.extend([0]*(param-len(mem)))
        return mem[rel_base+param]
    else:
        assert(False)



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
            #data[data[pc+1]] = input_chan.recv()
            inval = 2
            data[p1] = inval

            pc = pc + 1 + param_count[op]
        elif op == OP_OUTPUT:
            # p1 = decode_param(data, data[pc+1], modes[0], rel_base)
            if modes[0] == POSITION_MODE:
                p1 = data[pc+1]
            elif modes[0] == RELATIVE_MODE:
                p1 = rel_base + data[pc+1]
            else:
                assert(False)
            #output_chan.send(p1)
            print(data[p1])
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

#goless.go(run, data)
run(data, None, None)
# while(True):
#     try:
#         output_data = output_recv()
#         print(output_data)
#     except:
#         print('done')
#         break
# phase_settings_perms = list(itertools.permutations(range(5, 10)))
# settings = chunks([{'phase': phase, 'out_chan': goless.chan(1)} for phases in phase_settings_perms for phase in phases], 5)

# max_val = 0
# for setting in settings:
#     thruster_chan = goless.chan()
#     setting[4]['out_chan'].send(0)
#     for i in range(5):
#         if i < 4:
#             goless.go(run, data.copy(), setting[i]['phase'], setting[i-1]['out_chan'], setting[i]['out_chan'], None)
#         else:
#             goless.go(run, data.copy(), setting[i]['phase'], setting[i-1]['out_chan'], setting[i]['out_chan'], thruster_chan)
#     thruster_val = 0

#     while True:
#         try:
#             thruster_val = thruster_chan.recv()

#         except:
#             break

#     max_val = max(max_val,thruster_val)
#     print(max_val)
# print(max_val)