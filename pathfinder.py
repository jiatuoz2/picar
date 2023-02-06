import advanced_mapping as am
import picar_4wd as fc
import numpy as np
import time
from math import sqrt
from vision import run


def A_star(start, goal, map):
    closed_set = set()
    open_set = {start}
    came_from = {}

    g_score = {}
    h_score = {}
    f_score = {}

    g_score[start] = 0
    h_score[start] = euclidean_distance(start, goal)
    f_score[start] = h_score[start]

    while open_set != set():
        x = list(open_set)[0]
        tmp = f_score[x]
        for node in open_set:
            if f_score[node] < tmp:
                x = node
                tmp = f_score[node]

        if x == goal:
            return reconstruct_path(came_from, start, goal)
        open_set.remove(x)

        closed_set.add(x)

        for y in neighbor_nodes(x):
            if y in closed_set or (y[0] > 99 or y[1] > 99 or y[0] < 0 or y[1] < 0) or map[y[0]][y[1]] == 1:
                continue
            tentative_g_score = g_score[x] + euclidean_distance(x, y)

            if y not in open_set:
                tentative_is_better = True
            elif tentative_g_score < g_score[y]:
                tentative_is_better = True
            else:
                tentative_is_better = False

            if tentative_is_better:
                came_from[y] = x
                g_score[y] = tentative_g_score
                h_score[y] = euclidean_distance(y, goal)
                f_score[y] = g_score[y] + h_score[y]
                open_set.add(y)

    return []


def reconstruct_path(came_from, start, goal):
    result = []
    current = goal

    while current != start:
        result.append(current)
        current = came_from[current]

    # result.append(start)
    result.reverse()

    n = len(result) - 1

    operations = []
    for t in result:
        operations.append([t[0], t[1]])

    while n > 0:
        operations[n][0] -= operations[n-1][0]
        operations[n][1] -= operations[n-1][1]
        n -= 1

    operations[0][0] -= start[0]
    operations[0][1] -= start[1]
    print(operations)
    return operations


def euclidean_distance(start, goal):
    return sqrt((start[0] - goal[0]) * (start[0] - goal[0]) + (start[1] - goal[1]) * (start[1] - goal[1]))


def neighbor_nodes(node):
    up = (node[0], node[1] + 1)
    down = (node[0], node[1] - 1)
    left = (node[0] - 1, node[1])
    right = (node[0] + 1, node[1])
    return {up, down, left, right}


def main():
	goal = (50, 99)
	current = (50, 0)
	direction = "forward"
	while True:
		fc.stop()
		run()
		map = np.zeros((100, 100))
		map = am.advanced_scan_step(map)
		goal = (goal[0] - current[0] + 50, goal[1] - current[1] + 0)
		current = (50, 0)
		path = A_star((50, 0), goal, map)
		# only walk for 5 steps
		for i in range(20):
			if i >= len(path):
				break
			if path[i] == [0, 1]:
				if direction == "left":
					fc.turn_right(20)
					time.sleep(0.85)
				elif direction == "right":
					fc.turn_left(20)
					time.sleep(0.95)
				elif direction == "backward":
					fc.turn_left(20)
					time.sleep(1.9)
				direction = "forward"
				fc.forward(10)
				time.sleep(0.05)
			elif path[i] == [0, -1]:
				if direction == "left":
					fc.turn_left(20)
					time.sleep(0.95)
				elif direction == "right":
					fc.turn_right(20)
					time.sleep(0.85)
				elif direction == "forward":
					fc.turn_left(20)
					time.sleep(1.9)
				direction = "backward"
				fc.forward(10)
				time.sleep(0.05)
			elif path[i] == [1, 0]:
				if direction == "left":
					fc.turn_left(20)
					time.sleep(1.9)
				elif direction == "backward":
					fc.turn_left(20)
					time.sleep(0.95)
				elif direction == "forward":
					fc.turn_right(20)
					time.sleep(0.85)
				direction = "right"
				fc.forward(10)
				time.sleep(0.20)
			else:
				if direction == "backward":
					fc.turn_right(20)
					time.sleep(0.85)
				elif direction == "right":
					fc.turn_right(20)
					time.sleep(1.7)
				elif direction == "forward":
					fc.turn_left(20)
					time.sleep(0.95)
				direction = "left"
				fc.forward(10)
				time.sleep(0.20)
			current = (current[0] + path[i][0], current[1] + path[i][1])
			print(current)
		if goal == current:
			print("stop now")
			break
				
if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
