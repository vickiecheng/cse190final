from read_config import read_config
import random

class qlearning():
    def __init__(self):
        self.config = read_config()
	self.goal = self.config["goal"]
	self.walls = self.config["walls"]
	self.pits = self.config["pits"]
        (self.height, self.width) = self.config["map_size"]
        (self.startX, self.startY) = self.config["start"]
        (self.goalX, self.goalY) = self.config["goal"]
	self.move_list = [0, 1, 2, 3]
	self.gamma = self.config["discount_factor"]
	self.position = [self.startX, self.startY]
	self.iteration = 0
	self.exploration_rate = self.config["exploration_rate"]
	self.alpha = self.config["learning_rate"]
	self.discount = self.config["discount_factor"]
	self.rewards = [[0.0 for i in range(self.width)] for j in range(self.height)]
        # Create map with four values in each grid
        self.q_values = [[[0.0 for moves in range(len(self.move_list))] for i in range(self.width)] for j in range(self.height)]
        
	self.rewards_init()
	print self.q_values

    def rewards_init(self):
        for x in range(self.height):
	    for y in range(self.width):
		if [x, y] in self.walls:
		    self.rewards[x][y] = self.config["reward_for_hitting_wall"]
		
		elif [x, y] in self.pits:
		    self.rewards[x][y] = self.config["reward_for_falling_in_pit"] + self.config["reward_for_each_step"]

		elif [x, y]  == self.goal:
		    self.rewards[x][y] = self.config["reward_for_reaching_goal"] + self.config["reward_for_each_step"]

		else:
		    self.rewards[x][y] = self.config["reward_for_each_step"]

    # Algorithm to update q values
    def update_q_values(self):
	(x, y) = self.position

	# Check if wall
	if [x, y] in self.walls:
	    for i in range(len(self.q_values[x][y])):
		self.q_values[x][y][i] = self.config["reward_for_hitting_wall"]
	    return self.config["start"]
	elif [x, y] == self.goal:
	    for i in range(len(self.q_values[x][y])):
		self.q_values[x][y][i] = self.config["reward_for_reaching_goal"]
	    return self.config["start"]
        elif [x, y] in self.pits:
	    for i in range(len(self.q_values[x][y])):
		self.q_values[x][y][i] = self.config["reward_for_falling_in_pit"]
	    return self.config["start"]
 
        action = self.get_next_move()
	next_state = self.move(action)
	if self.get_valid_moves(self.position):
	    self.q_values[x][y][action] += self.alpha * (self.rewards[x][y] + self.discount * self.get_value(next_state) - self.q_values[x][y][action])
	else:
	    self.q_values[x][y][action] = self.rewards[x][y]	
	self.iteration += 1
	return next_state
	# Remember to and uncertainty variable


    # Get valid moves
    def get_valid_moves(self, position):
    	valid_moves = list()
	
	# 0 = South
	if position[0] < (self.height -1):
	    valid_moves.append(0)

	# 1 = North
	if position[0] > 0:
	    valid_moves.append(1)

	# 2 = East
	if position[1] < (self.width - 1):
	    valid_moves.append(2)

	# 3 = West
	if position[1] > 0:
	    valid_moves.append(3)

	return valid_moves
  
    # Get next move
    def get_next_move(self):
        valid_moves = self.get_valid_moves(self.position)
	move = None

	if valid_moves:
	    if random.random() < self.exploration_rate:
	        move = random.choice(valid_moves)
	    else:
	        move = self.get_policy(self.position)
	return move

    # Take move
    def move(self, move):
	next_state = self.position
	if move == 0:
	    next_state = [self.position[0] + 1, self.position[1]]
	elif move == 1:
	    next_state = [self.position[0] - 1, self.position[1]]
	elif move == 2:
	    next_state = [self.position[0], self.position[1] + 1]
	elif move == 3:
	    next_state = [self.position[0], self.position[1] - 1]
	return next_state

    # Get the best policy at a given state
    def get_policy(self, state):
        (x, y) = state
	curr_values = self.q_values[x][y]
	valid_moves = self.get_valid_moves(state)
	valid_moves_values = list()
	for move in valid_moves:
	    valid_moves_values.append(curr_values[move])
	return valid_moves[valid_moves_values.index(max(valid_moves_values))]

    def get_value(self, state):
	(x, y) = state
	return max(self.q_values[x][y])

