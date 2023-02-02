import picar_4wd as fc
import time
import numpy as np

current_angle = 0
step = 15

def get_obstacle_XY(angle, distance):
    angle = np.radians(angle)
    X = np.sin(-angle) * distance  + 25
    Y = np.cos(angle) * distance + 0
    return (X, Y)

def interpolate(map, point1, point2):
    if point2[0] - point1[0] == 0:
        slope = 0
    else:
        slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
    y = point1[1] + slope
    for i in range(point1[0] + 1, point2[0]):
        map[int(i)][int(np.round(y))] = 1
        y += slope

def advanced_scan_step(map):
    init = True
    prev_x = 0
    prev_y = 0
    global current_angle, step
    while init == True or (current_angle != 90 and current_angle != -90):
        current_angle += step
        if current_angle >= 90:
            current_angle = 90
            step = -15
        elif current_angle <= -90:
            current_angle = -90
            step = 15

        distance = fc.get_distance_at(current_angle)
        print(distance, " ", current_angle)
        X, Y = get_obstacle_XY(current_angle, distance)
        X = int(np.round(X))
        Y = int(np.round(Y))
        if X < 50 and Y < 50 and X >= 0:
            map[X][Y] = 1
            if init == False:
                interpolate(map, (prev_x, prev_y), (X, Y))
            prev_x = X
            prev_y = Y
        if init == True:
            init = False
    return map

def main():
    fc.servo.set_angle(0)
    while True:
        map = np.zeros((50, 50))
        advanced_scan_step(map)
        for i in range(50):
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
