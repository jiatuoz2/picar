import advanced_mapping as am
import picar_4wd as fc
import numpy as np
import heapq
import time

def neighbors(current):
	neighbors = []
	offset = [(0, 1), (0, -1), (-1, 0), (1, 0)]
	for i in range(4):
		neighbors.append((current[0] + offset[i][0], current[1] + offset[i][1]))
	return neighbors
	
def heuristic(goal, start):
	return abs(goal[0] - start[0]) + abs(goal[1] - start[1])
	

def path_find(start, goal, map):
	frontier = [(0, start)] 
	heapq.heapify(frontier)
	came_from = {}
	cost_so_far = {}
	came_from[start] = "None"
	cost_so_far[start] = 0
	
	while len(frontier) > 0:
		current = heapq.heappop(frontier)[1]
		
		if current == goal:
			break
		
		for neighbor in neighbors(current):
			if neighbor[0] >= 0 and neighbor[0] < 100 and neighbor[1] < 100 and neighbor[1] >= 0 and map[neighbor[0]][neighbor[1]] == 0:
				new_cost = cost_so_far[current] + 1
				if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
					cost_so_far[neighbor] = new_cost
					priority = new_cost + heuristic(goal, neighbor)
					heapq.heappush(frontier, (priority, neighbor))
					came_from[neighbor] = current
	# after finding the goal, retrack for the path
	path = []
	current = goal
	while current != start:
		prev = came_from[current]
		path.append((current[0] - prev[0], current[1] - prev[1]))
		current = prev
	path.reverse()
	return path
	

def main():
	goal = (65, 20)
	map = np.zeros((100, 100))
	current = (50, 0)
	direction = "forward"
	while True:
		fc.servo.set_angle(-90)
		map = am.advanced_scan_step(map)
		goal = (goal[0] - current[0] + 50, goal[1] - current[1] + 0)
		current = (50, 0)
		path = path_find((50, 0), goal, map)
		# only walk for 5 steps
		for i in range(5):
			if i >= len(path):
				break
			if path[i] == (0, 1):
				if direction == "left":
					fc.turn_right(10)
					time.sleep(1)
				elif direction == "right":
					fc.turn_left(10)
					time.sleep(1)
				elif direction == "backward":
					fc.turn_left(10)
					time.sleep(2)
				direction = "forward"
				fc.forward(10)
				time.sleep(0.1)
			elif path[i] == (0, -1):
				if direction == "left":
					fc.turn_left(10)
					time.sleep(1)
				elif direction == "right":
					fc.turn_right(10)
					time.sleep(1)
				elif direction == "forward":
					fc.turn_left(10)
					time.sleep(2)
				direction = "backward"
				fc.forward(10)
				time.sleep(0.1)
			elif path[i] == (1, 0):
				if direction == "left":
					fc.turn_left(10)
					time.sleep(2)
				elif direction == "backward":
					fc.turn_left(10)
					time.sleep(1)
				elif direction == "forward":
					fc.turn_right(10)
					time.sleep(1)
				direction = "right"
				fc.forward(10)
				time.sleep(0.1)
			else:
				if direction == "backward":
					fc.turn_right(10)
					time.sleep(1)
				elif direction == "right":
					fc.turn_right(10)
					time.sleep(2)
				elif direction == "forward":
					fc.turn_left(10)
					time.sleep(1)
				direction = "left"
				fc.forward(10)
				time.sleep(0.1)
			current = (current[0] + path[i][0], current[1] + path[i][1])
		if goal == current:
			print("stop now")
			break
				
if __name__ == "__main__":
    try: 
        main()
    finally: 
        fc.stop()
