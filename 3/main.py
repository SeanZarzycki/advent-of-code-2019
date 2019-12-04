data_filename = 'input.txt'
with open(data_filename) as f:
    data = f.readline().split(',')




def point_change(pt, dir):
    card = dir[0]
    num = int(dir[1:])
    if card == 'R':
        return (pt[0] + num, pt[1])
    elif card == 'U':
        return (pt[0], pt[1]+num)
    elif card == 'D':
        return (pt[0], pt[1]-num)
    elif card == 'L':
        return (pt[0]-num, pt[1])

def pts_to_wire(pt1, pt2):
    wire = []
    if pt1[0] == pt2[0]:
        stride = -1 if pt2[1] < pt1[1] else 1
        for y in range(pt1[1]+stride, pt2[1], stride):
            wire.append((pt1[0], y))
    else:
        stride = -1 if pt2[0] < pt1[0] else 1
        for x in range(pt1[0]+stride, pt2[0], stride):
            wire.append((x, pt1[1]))

    wire.append(pt2)   
    return wire

def directions_to_points(ds):
    pts = [(0,0)]
    timing = [0]
    length = 0
    for d in ds:
        last_pt = pts[-1]
        pt2 = point_change(last_pt, d)
        wire = pts_to_wire(last_pt, pt2)
        for s in wire:
            length += 1
            timing.append(length)
            
            pts.append(s)
    return (pts,timing)

data_filename = 'input.txt'
with open(data_filename) as f:
    wire1data = f.readline().split(',')
    wire2data = f.readline().split(',')

(w1,t1) = directions_to_points(wire1data)
(w2,t2) = directions_to_points(wire2data)

crosses = set(w1)&set(w2)
crosses.remove((0,0))
min_val = min([abs(x) + abs(y) for (x,y) in crosses])
cross_pt = [(x,y) for (x,y) in crosses if abs(x)+abs(y) == min_val][0]
best_timing = min([t1[w1.index(pt)] + t2[w2.index(pt)] for pt in crosses])
print(min_val, best_timing)