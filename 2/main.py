data_filename = 'input.txt'
with open(data_filename) as f:
    data = f.readline().split(',')

backup = [int(x) for x in data]



for x1 in range(100):
    for x2 in range(100):

        data = backup.copy()
        data[1] = x1
        data[2] = x2
        op = data[0]
        idx = 0

        while op != 99:
            operand1 = data[data[idx + 1]]
            operand2 = data[data[idx + 2]]

            if op == 1:
                data[data[idx + 3]] = operand1 + operand2
            elif op == 2:
                data[data[idx + 3]] = operand1 * operand2
            else:
                print('here')
            idx += 4
            op = data[idx]
        
        if data[0] == 19690720:
            print(100*x1 + x2)
            
