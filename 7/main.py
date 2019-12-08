import sys
import itertools 
import goless
import time

with open('input.txt') as f:
    data = f.readline().split(',')

data = [int(x) for x in data]


POSITION_MODE = 0
IMMEDIATE_MODE = 1

OP_ADD = 1
OP_MULT = 2
OP_INPUT = 3
OP_OUTPUT = 4
OP_JMP_NZ = 5
OP_JMP_Z = 6
OP_LT = 7
OP_EQ = 8

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

def decode_param(mem, param, mode):
    if mode == POSITION_MODE:
        return mem[param]
    elif mode == IMMEDIATE_MODE:
        return param
    else:
        assert(False)



def run(data, phase_setting, input_chan, output_chan, thruster_chan):
    pc = 0
    phase_rcvd = False
    while True:
        opcode = data[pc]
        (op, modes) = decode_op(opcode)
        if op == OP_ADD:

            p1 = decode_param(data, data[pc+1], modes[0])
            p2 = decode_param(data, data[pc+2], modes[1])
            data[data[pc+3]] = p1 + p2
            pc = pc + 1 + param_count[op]
        elif op == OP_MULT:
            p1 = decode_param(data, data[pc+1], modes[0])
            p2 = decode_param(data, data[pc+2], modes[1])
            data[data[pc+3]] = p1 * p2
            pc = pc + 1 + param_count[op]

        elif op == OP_INPUT:
            p1 = decode_param(data, data[pc+1], modes[0])
            if not phase_rcvd:
                phase_rcvd = True
                data[data[pc+1]] = phase_setting
            else:
                data[data[pc+1]] = input_chan.recv()

            pc = pc + 1 + param_count[op]
        elif op == OP_OUTPUT:
            p1 = decode_param(data, data[pc+1], modes[0])
            output_chan.send(p1)
            if thruster_chan != None:
                thruster_chan.send(p1)
            pc = pc + 1 + param_count[op]

        elif op == OP_JMP_NZ:
            p1 = decode_param(data, data[pc+1], modes[0])
            p2 = decode_param(data, data[pc+2], modes[1])
            pc = p2 if p1 != 0 else pc + 1 + param_count[op]
        elif op == OP_JMP_Z:
            p1 = decode_param(data, data[pc+1], modes[0])
            p2 = decode_param(data, data[pc+2], modes[1])
            pc = p2 if p1 == 0 else pc + 1 + param_count[op]


        elif op == OP_LT:
            p1 = decode_param(data, data[pc+1], modes[0])
            p2 = decode_param(data, data[pc+2], modes[1])
            data[data[pc+3]] = 1 if p1 < p2 else 0
            pc = pc + 1 + param_count[op]

        elif op == OP_EQ:
            p1 = decode_param(data, data[pc+1], modes[0])
            p2 = decode_param(data, data[pc+2], modes[1])
            data[data[pc+3]] = 1 if p1 == p2 else 0
            pc = pc + 1 + param_count[op]

        elif op == OP_STOP:
            if thruster_chan != None:
                thruster_chan.close()
            return


        else:
            assert(False)

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

phase_settings_perms = list(itertools.permutations(range(5, 10)))
settings = chunks([{'phase': phase, 'out_chan': goless.chan(1)} for phases in phase_settings_perms for phase in phases], 5)

max_val = 0
for setting in settings:
    thruster_chan = goless.chan()
    setting[4]['out_chan'].send(0)
    for i in range(5):
        if i < 4:
            goless.go(run, data.copy(), setting[i]['phase'], setting[i-1]['out_chan'], setting[i]['out_chan'], None)
        else:
            goless.go(run, data.copy(), setting[i]['phase'], setting[i-1]['out_chan'], setting[i]['out_chan'], thruster_chan)
   # print('waiting')
   # time.sleep(1)
    thruster_val = 0
    
    while True:
        try:
            thruster_val = thruster_chan.recv()

        except:
            break

    max_val = max(max_val,thruster_val)
    print(max_val)
print(max_val)