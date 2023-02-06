import picar_4wd as fc
import time
import numpy as np

current_angle = 0
step = 15

def get_obstacle_XY(angle, distance):
    angle = np.radians(angle)
    X = int(np.round(np.sin(angle) * distance  + 50))
    Y = int(np.round(np.cos(angle) * distance + 0))
    return X, Y

def interpolate(map, point1, point2):
    if point2[0] - point1[0] == 0:
        slope = 0
    else:
        slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
    y = point1[1] + slope
    for i in range(point1[0] + 1, point2[0]):
        map[int(i)][int(np.round(y))] = 1
        add_clearance((int(i), int(np.round(y))), map)
        y += slope
        
def add_clearance(point, map):
    for i in range(point[0] - 1, point[0] + 1):
        for j in range(point[1] - 1, point[1] + 1):
            if i >=0 and i < 100 and j >= 0 and j < 100:
                map[i][j] = 1
                
def advanced_scan_step(map):
    step = 5
    prev = (0, 0, -70)
    init = True
    for i in range(-70, 70, step):
        fc.servo.set_angle(i)
        distance = fc.get_distance_at(i)
        if distance <= 50 and distance > 4:
            X, Y = get_obstacle_XY(i, distance)
            map[X][Y] = 1
            add_clearance((X, Y), map)
            if init == True:
                prev = (X, Y, i)
                init = False
            elif np.abs(prev[2] - i) <= step + 1:
                interpolate(map, (prev[0], prev[1]), (X, Y))
                prev = (X, Y, i)
            
    return map

def main():
    while True:
        map = np.zeros((100, 100))
        advanced_scan_step(map)
        for i in range(25, 75):
            for j in range(50):
                print(int(map[i][j]), end=" ")
            print("\n", end="")
        print("\n")
        time.sleep(5)

if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
