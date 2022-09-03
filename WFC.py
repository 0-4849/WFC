import random
#test
class Tile():
	def __init__(self, name, char, edges) -> None:
		self.name = name		
		self.char = char
		self.edges = edges
  
		self.up = []
		self.right = []
		self.down = []
		self.left = []

class Cell():
	def __init__(self, id) -> None:
		self.is_collapsed = False
		self.options = {0,1,2,3,4}
		self.id = id

	def __lt__(self, other):
		return len(self.options) < len(other.options)

tiles = [0]*5
tiles[0] = Tile(0, " ", [0,0,0,0])
tiles[1] = Tile(1, "┴", [1,1,0,1])
tiles[2] = Tile(2, "├", [1,1,1,0])
tiles[3] = Tile(3, "┬", [0,1,1,1])
tiles[4] = Tile(4, "┤", [1,0,1,1])

chars = (" ", "┴", "├", "┬", "┤")
SIZE_X, SIZE_Y = 20, 10
BLANK, UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3, 4
# calculate compatabilities for edges
rules = {}

for i in tiles:
	rules[i.name] = {}
	for edge_index, edge in enumerate(i.edges):
		rules[i.name].update({edge_index:set()})
		for j in tiles:
			if edge == j.edges[(edge_index + 2) % 4]:
				rules[i.name][edge_index] |= {j.name}
				

grid = [Cell(i) for i in range(SIZE_X*SIZE_Y)]
output = [" "]*SIZE_X*SIZE_Y

while True:
    
	grid_copy = grid.copy()
	grid_copy.sort()  # sort by number of options (__lt__ method)
	grid_copy = list(filter((lambda x: not x.is_collapsed), grid_copy))
	if len(grid_copy) == 0: break

	possible_tiles = [i for i in grid_copy if len(i.options) == len(grid_copy[0].options)] # pick random tile from all lowest values

	current_tile = random.choice(possible_tiles)
	current_tile.is_collapsed = True
	random_key = random.choice(list(current_tile.options))
	current_tile.options = set([random_key])

	next_grid = grid.copy()

	for y in range(SIZE_Y):
		for x in range(SIZE_X):
			index = y*SIZE_X + x
			if grid[index].is_collapsed:
				next_grid[index] = grid[index]
			else:
				next_options = {0,1,2,3,4}
				
				if y > 0:  # check up
					up = grid[(y-1)*SIZE_X + x]
					valid_options = set()
					for option in up.options:
						valid = rules[option][2]
						valid_options = valid_options.union(valid)
					next_options = next_options & valid_options

				if x < SIZE_X - 1:  # check right
					right = grid[y*SIZE_X + x + 1]
					valid_options = set()
					for option in right.options:
						valid = rules[option][3]
						valid_options = valid_options.union(valid)
					next_options = next_options & valid_options

				if y < SIZE_Y - 1:  # check down
					down = grid[(y+1)*SIZE_X + x]
					valid_options = set()
					for option in down.options:
						valid = rules[option][0]
						valid_options = valid_options.union(valid)
					next_options = next_options & valid_options

				if x > 0:  # check left
					left = grid[y*SIZE_X + x - 1]
					valid_options = set()
					for option in left.options:
						valid = rules[option][1]
						valid_options = valid_options.union(valid)
					next_options = next_options & valid_options
						
				

				next_grid[index].options = next_options
    
    
    
	grid = next_grid.copy()

char_list = [chars[list(i.options)[0]] for i in grid]

for i in range(0,len(char_list),SIZE_X+1): char_list.insert(i+SIZE_X, "\n")

print(*char_list, sep="")