import sys

with open('5/input.txt') as f:
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

i = 0

while True:
    opcode = data[i]
    (op, modes) = decode_op(opcode)
    if op == OP_ADD:

        p1 = decode_param(data, data[i+1], modes[0])
        p2 = decode_param(data, data[i+2], modes[1])
        data[data[i+3]] = p1 + p2
        i = i + 1 + param_count[op]
    elif op == OP_MULT:
        p1 = decode_param(data, data[i+1], modes[0])
        p2 = decode_param(data, data[i+2], modes[1])
        data[data[i+3]] = p1 * p2
        i = i + 1 + param_count[op]

    elif op == OP_INPUT:
        p1 = decode_param(data, data[i+1], modes[0])
        inval = int(input("Enter: "))
        data[data[i+1]] = inval
        i = i + 1 + param_count[op]
    elif op == OP_OUTPUT:
        p1 = decode_param(data, data[i+1], modes[0])
        print(p1)
        i = i + 1 + param_count[op]

    elif op == OP_JMP_NZ:
        p1 = decode_param(data, data[i+1], modes[0])
        p2 = decode_param(data, data[i+2], modes[1])
        i = p2 if p1 != 0 else i + 1 + param_count[op]
    elif op == OP_JMP_Z:
        p1 = decode_param(data, data[i+1], modes[0])
        p2 = decode_param(data, data[i+2], modes[1])
        i = p2 if p1 == 0 else i + 1 + param_count[op]


    elif op == OP_LT:
        p1 = decode_param(data, data[i+1], modes[0])
        p2 = decode_param(data, data[i+2], modes[1])
        data[data[i+3]] = 1 if p1 < p2 else 0
        i = i + 1 + param_count[op]

    elif op == OP_EQ:
        p1 = decode_param(data, data[i+1], modes[0])
        p2 = decode_param(data, data[i+2], modes[1])
        data[data[i+3]] = 1 if p1 == p2 else 0
        i = i + 1 + param_count[op]

    elif op == OP_STOP:
        exit(1)


    else:
        assert(False)


print(data[0])