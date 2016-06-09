# mdp implementation needs to go here

from read_config import read_config

class mdp():
    def __init__(self, move_list, map_size, goal, wall, pits):
	self.config = read_config()
        self.goal = goal
	self.wall = wall
	self.pits = pits
	self.p_forward = self.config["prob_move_forward"]
	self.p_backward = self.config["prob_move_backward"]
	self.p_left = self.config["prob_move_left"]
	self.p_right = self.config["prob_move_right"]
	(height, width) = map_size
	self.height = height
	self.width = width
	self.rewards = [[0.0 for i in range(width)] for j in range(height)]
	self.values = [[0.0 for i in range(width)] for j in range(height)]
	self.policy = [["" for i in range(width)] for j in range(height)]
	self.gamma = self.config["discount_factor"]
	self.iteration = 0
	self.moves = ['N', 'S', 'E', 'W']
	self.value_init()

    def value_init(self):
	for x in range(self.height):
	    for y in range(self.width):
	        if [x, y] in self.wall:
		    self.rewards[x][y] = self.config["reward_for_hitting_wall"]
		    self.policy[x][y] = 'WALL'

		elif [x, y] in self.pits:
		    self.rewards[x][y] = self.config["reward_for_falling_in_pit"] + self.config["reward_for_each_step"]
		    self.policy[x][y] = 'PIT'
		    
		elif [x, y] == self.goal:
  		    self.rewards[x][y] = self.config["reward_for_reaching_goal"] + self.config["reward_for_each_step"]
		    self.policy[x][y] = 'GOAL'

		else:
		    self.rewards[x][y] = self.config["reward_for_each_step"]

    def value_iteration(self):
	new_values = [[0.0 for i in range(self.width)] for j in range(self.height)]
        for x in range(self.height):
	    for y in range(self.width):
	        valid_moves = self.get_valid_moves((x,y))
		probabilities = list()

		if [x,y] not in self.wall and not ([x,y] == self.goal) and [x,y] not in self.pits:
		    for move in self.moves:
		        up_util = 0
 	 	        down_util = 0
 		        right_util = 0
		        left_util = 0

		        if move == 'N':
			    if move not in valid_moves:
				up_util = 0
			    elif [x-1, y] in self.wall:
			        up_util = self.p_forward * (self.rewards[x-1][y] + self.gamma * (self.values[x][y]))
			    else:
			        up_util = self.p_forward * (self.rewards[x-1][y] + self.gamma * (self.values[x-1][y]))

			    if 'S' in valid_moves:
				if [x+1, y] in self.wall:
			            down_util = self.p_backward * (self.rewards[x+1][y] + self.gamma * (self.values[x][y]))
				else:
			            down_util = self.p_backward * (self.rewards[x+1][y] + self.gamma * (self.values[x+1][y]))
			    if 'E' in valid_moves:
				if [x, y+1] in self.wall:
			            right_util = self.p_right * (self.rewards[x][y+1] + self.gamma * (self.values[x][y]))
				else:
			            right_util = self.p_right * (self.rewards[x][y+1] + self.gamma * (self.values[x][y+1]))
			    if 'W' in valid_moves:
				if [x, y-1] in self.wall:
			            left_util = self.p_left * (self.rewards[x][y-1] + self.gamma * (self.values[x][y]))
				else:
			            left_util = self.p_left * (self.rewards[x][y-1] + self.gamma * (self.values[x][y-1]))
			    
		        elif move == 'S':
			    if move not in valid_moves:
				down_util = 0
			    elif [x+1, y] in self.wall:
			        down_util = self.p_forward * (self.rewards[x+1][y] + self.gamma * (self.values[x][y]))
			    else:
			        down_util = self.p_forward * (self.rewards[x+1][y] + self.gamma * (self.values[x+1][y]))

			    if 'N' in valid_moves:
			        if [x-1, y] in self.wall:
			            up_util = self.p_backward * (self.rewards[x-1][y] + self.gamma * (self.values[x][y]))
				else:
			            up_util = self.p_backward * (self.rewards[x-1][y] + self.gamma * (self.values[x-1][y]))
		            if 'E' in valid_moves:
				if [x, y+1] in self.wall:
			            right_util = self.p_left * (self.rewards[x][y+1] + self.gamma * (self.values[x][y]))
				else:
			            right_util = self.p_left * (self.rewards[x][y+1] + self.gamma * (self.values[x][y+1]))
			    if 'W' in valid_moves:
				if [x, y-1] in self.wall:
			            left_util = self.p_right * (self.rewards[x][y-1] + self.gamma * (self.values[x][y]))
				else:
			            left_util = self.p_right * (self.rewards[x][y-1] + self.gamma * (self.values[x][y-1]))
				
		        elif move == 'E':
			    if move not in valid_moves:
				right_util = 0
			    elif [x, y+1] in self.wall:
			        right_util = self.p_forward * (self.rewards[x][y+1] + self.gamma * (self.values[x][y]))
			    else:
		   	        right_util = self.p_forward * (self.rewards[x][y+1] + self.gamma * (self.values[x][y+1]))

			    if 'W' in valid_moves:
				if [x, y-1] in self.wall:
			            left_util = self.p_backward * (self.rewards[x][y-1] + self.gamma * (self.values[x][y]))
				else:
			            left_util = self.p_backward * (self.rewards[x][y-1] + self.gamma * (self.values[x][y-1]))
			    if 'N' in valid_moves:
			        if [x-1, y] in self.wall:
			            up_util = self.p_left * (self.rewards[x-1][y] + self.gamma * (self.values[x][y]))
				else:
			            up_util = self.p_left * (self.rewards[x-1][y] + self.gamma * (self.values[x-1][y]))
			    if 'S' in valid_moves:
			        if [x+1, y] in self.wall:
			            down_util = self.p_right * (self.rewards[x+1][y] + self.gamma * (self.values[x][y]))
				else:
			            down_util = self.p_right * (self.rewards[x+1][y] + self.gamma * (self.values[x+1][y]))

		        elif move == 'W':
			    if move not in valid_moves:
				left_util = 0
			    if [x, y-1] in self.wall:
			        left_util = self.p_forward * (self.rewards[x][y-1] + self.gamma * (self.values[x][y]))
			    else:
			        left_util = self.p_forward * (self.rewards[x][y-1] + self.gamma * (self.values[x][y-1]))

			    if 'E' in valid_moves:
				if [x, y+1] in self.wall:
			            right_util = self.p_backward * (self.rewards[x][y+1] + self.gamma * (self.values[x][y]))
				else:
			            right_util = self.p_backward * (self.rewards[x][y+1] + self.gamma * (self.values[x][y+1]))
			    if 'N' in valid_moves:
			        if [x-1, y] in self.wall:
			            up_util = self.p_right * (self.rewards[x-1][y] + self.gamma * (self.values[x][y]))
				else:
			            up_util = self.p_right * (self.rewards[x-1][y] + self.gamma * (self.values[x-1][y]))
			    if 'S' in valid_moves:
			        if [x+1, y] in self.wall:
			            down_util = self.p_left * (self.rewards[x+1][y] + self.gamma * (self.values[x][y]))
				else:
			            down_util = self.p_left * (self.rewards[x+1][y] + self.gamma * (self.values[x+1][y]))
			    
		        probabilities.append(up_util + down_util + right_util + left_util)   
			
		    new_values[x][y] = max(probabilities)	    
		    self.policy[x][y] = self.moves[probabilities.index(max(probabilities))]
	self.values = new_values
	self.iteration += 1
		    
    def get_valid_moves(self, position):
	valid_moves = list()

	# Check if moving right is valid
        if position[0] < (self.height - 1):
	    valid_moves.append('S')

        # Check if moving left is valid
        if position[0] > 0:
	    valid_moves.append('N') 

        # Check if moving up is valid
        if position[1] < (self.width - 1):
	    valid_moves.append('E')

        if position[1] > 0:
    	    valid_moves.append('W')

        return valid_moves

