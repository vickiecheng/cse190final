class grid():
    def __init__(self, x, y, reachable):
        self.x = x
        self.y = y
        self.g = 0
        self.h = 0
        self.f = 0
        self.reachable = reachable
        self.parent = None

class AStar():
    def __init__(self, move_list, start, goal, map_size, wall, pits):
        (height, width) = map_size
        self.grid_height = height
        self.grid_width = width
        self.start = start
	self.goal = goal
	self.wall = wall
	self.pits = pits
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.grids = []

	def init_grid(self):
	    for x in range(self.grid_width):
		for y in range(self.grid_height):
		    if (x, y) in self.wall or self.pits:
			reachable = False
		    else:
			reachable = True
		    self.cells.append(grid(x, y, reachable))

	def process(self):
	    # add starting cell to open heap queue
	    heapq.heappush(self.opened, (self.start.f, self.start))
	    while len(self.opened):
		# pop cell from heap queue 
		f, grid = heapq.heappop(self.opened)
		# add cell to closed list so we don't process it twice
		self.closed.add(grid)
		# if ending cell, display found path
		if grid is self.goal:
		    self.display_path()
		    break
		# get adjacent cells for cell
		adj_cells = self.get_adjacent_grids(grid)
		for adj_cell in adj_cells:
		    if adj_cell.reachable and adj_cell not in self.closed:
			if (adj_cell.f, adj_cell) in self.opened:
			    # if adj cell in open list, check if current path is
			    # better than the one previously found for this adj
			    # cell.
			    if adj_cell.g > grid.g + 1:
				self.update_grid(adj_cell, grid)
			else:
			    self.update_grid(adj_cell, grid)
			    # add adj cell to open list
			    heapq.heappush(self.opened, (adj_cell.f, adj_cell))

	def get_heuristic(self, grid):
	    return (abs(grid.x - self.end.x) + abs(grid.y - self.end.y))

	def get_grid(self, x, y):
	    return self.grids[x * self.grid_height + y]

	def get_adjacent_grids(self, grid):
	    grids = []
	    if grid.x < self.grid_width-1:
		grids.append(self.get_cell(grid.x+1, grid.y))
	    if grid.y > 0:
		grids.append(self.get_cell(grid.x, grid.y-1))
	    if grid.x > 0:
		gridss.append(self.get_cell(grid.x-1, grid.y))
	    if grid.y < self.grid_height-1:
		grids.append(self.get_cell(grid.x, grid.y+1))
	    return grids

	def display_path(self):
	    grid = self.goal
	    while grid.parent is not self.start:
		grid = grid.parent
		print 'path: cell: %d,%d' % (grid.x, grid.y)

	def update_grid(self, adj, grid):
	    adj.g = grid.g + 1
	    adj.h = self.get_heuristic(adj)
	    adj.parent = grid
	    adj.f = adj.h + adj.g
