import math
import numpy

with open('10/input.txt') as f:
    data = f.read().split('\n')

nrows = len(data)
ncols = len(data[0])


ASTEROID = '#'
SPACE = '.'
(best_val, best_idx, best_rays) = (0, (0,0), {})
for y in range(nrows):
    for x in range(ncols):
        if data[y][x] == ASTEROID:
            rays = {}
            for yy in range(nrows):
                for xx in range(ncols):
                    if (yy, xx) != (y,x) and data[yy][xx] == ASTEROID: # find all blocked spots
                        (dy,dx) = (y-yy,xx-x)
                        angle = math.atan2(dx,dy)
                        if angle < 0:
                            angle = angle + 2*math.pi
                        dist = math.sqrt(dy**2 + dx**2)
                        if angle in rays:
                            rays[angle].append((dist, (xx,yy)))
                        else:
                            rays[angle] = [(dist, (xx,yy))]
            if len(rays) > best_val:
                (best_val, best_idx, best_rays) = (len(rays), (x,y), rays.copy())




print((best_val, best_idx))


for theta in sorted(best_rays):
    best_rays[theta].sort(key=lambda tup: tup[0])

destroyed = 0

while(True):
    for theta in sorted(best_rays):
       # print(theta)
        if len(best_rays[theta]) > 0:
            destroyed = destroyed + 1
            if destroyed == 200:
                coord = best_rays[theta][0][1]
                print(100*coord[0] + coord[1])
                exit(0)
            best_rays[theta] = best_rays[theta][1:]