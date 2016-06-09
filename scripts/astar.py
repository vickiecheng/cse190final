# astar implementation needs to go here
import Queue
import heapq


def astar(move_list, start, goal, map_size,  wall, pits):
    (height, width) = map_size
    (startX, startY) = start
    (goalX, goalY) = goal
    greedy = [[0.0 for i in range(width)] for j in range(height)]
    manhattan = [[0.0 for i in range(width)] for j in range(height)]
    f = [[0.0 for i in range(width)] for j in range(height)]
    

    # List of nodes that have been visited but not expanded
    frontier = []

    # List of nodes that have been visited and expanded
    explored = list()

    # Greedy heuristic
    distance_traveled = 0

    # Keep track of optimal moves made
    cameFrom = dict()
    origin = -1
 
    # Setup start
    heapq.heappush(frontier, (distance_traveled + manhattan_distance(start, goal, map_size), start))
    # Loop while there are still nodes to explore
    while not len(frontier) == 0:
        curr = heapq.heappop(frontier)[1]

        if curr == goal:
            return get_traceback(cameFrom, curr)

        valid_moves = get_valid_moves(curr, map_size, wall, pits)
        explored.append(curr)

	for move in valid_moves:
            newPosition = take_move(curr, move)
	    if newPosition not in explored:
	        heapq.heappush(frontier, (distance_traveled + manhattan_distance(newPosition, goal, map_size), newPosition))
	        (x,y) = newPosition
                cameFrom.update({(x,y):curr})

	distance_traveled += 1
        origin += 1
    
def manhattan_distance(position, goal, map_size):
    x_dist = abs(position[0] - goal[0]) % map_size[0]
    y_dist = abs(position[1] - goal[1]) % map_size[1]
    return x_dist + y_dist

def get_valid_moves(position, map_size, wall, pits):
    valid_moves = list()
    (x, y) = position
    (height, width) = map_size

    # Check if moving right is valid
    if y < (width - 1) and [x, y + 1] not in wall and [x, y + 1] not in pits:
        valid_moves.append((0,1))

    # Check if moving up is valid
    if x > 0 and [x - 1, y] not in wall and [x - 1, y] not in pits:
        valid_moves.append((-1,0))

    if x < (height - 1) and [x + 1, y] not in wall and [x + 1, y] not in pits:
        valid_moves.append((1,0))

    # Check if moving left is valid
    if y > 0 and [x, y-1] not in wall and [x, y-1] not in pits:
        valid_moves.append((0,-1)) 

    return valid_moves

def take_move(position, move):
    return [abs(position[0] + move[0]), abs(position[1] + move[1])]

def get_traceback(cameFrom, curr):
    sequence = list()
    (currX, currY) = curr
    sequence.append([currX, currY])
    while cameFrom.has_key((currX, currY)):
	print (currX, currY)
	(currX, currY) = cameFrom[(currX, currY)]
        sequence.append([currX, currY])
    return sequence[::-1]
