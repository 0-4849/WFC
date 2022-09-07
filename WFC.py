import random
from tile import Tile
from cell import Cell
#test
def check_options(cell, direction):
	valid_options = set()
	for option in cell.options:
		valid = rules[option][direction]
		valid_options = valid_options.union(valid)
  
	return valid_options

# Make a tile list with all tiles in it (blank, up, right, down, left)
tiles = [0]*5
tiles[0] = Tile(0, " ", [0,0,0,0])
tiles[1] = Tile(1, "┴", [1,1,0,1])
tiles[2] = Tile(2, "├", [1,1,1,0])
tiles[3] = Tile(3, "┬", [0,1,1,1])
tiles[4] = Tile(4, "┤", [1,0,1,1])

chars = (" ", "┴", "├", "┬", "┤")
SIZE_X, SIZE_Y = 2,2
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

# generate grid
grid = [Cell(i) for i in range(SIZE_X*SIZE_Y)]

while True:
    
    # copy grid, sort it by number of options (__lt__ method in cell class), then filter out collapsed cells
	grid_copy = grid.copy()
	grid_copy.sort()  
	grid_copy = list(filter((lambda x: not x.is_collapsed), grid_copy))
	if len(grid_copy) == 0: break

	# generate list with the cells that have the least options
	possible_cells = [i for i in grid_copy if len(i.options) == len(grid_copy[0].options)] 

	# pick one from the list, collapse it, pick one of its options
	index = random.randrange(len(possible_cells))
	current_cell = possible_cells[index]
	current_cell.is_collapsed = True
	random_key = random.choice(list(current_cell.options))
	current_cell.options = {random_key}
 
	# make a copy of the grid so all cells can be evaluated 
	next_grid = grid.copy()

	x = index % SIZE_X
	y = index // SIZE_X

	### TODO: check cells around current_cell, NOT current_cell itself
 
	if grid[index].is_collapsed:
		next_grid[index] = grid[index]
	else:
		next_options = {0,1,2,3,4}
		
		if y > 0:  # check up
			up = grid[(y-1)*SIZE_X + x]
			next_options &= check_options(up, 2)

		if x < SIZE_X - 1:  # check right
			right = grid[y*SIZE_X + x + 1]
			next_options &= check_options(right, 3)

		if y < SIZE_Y - 1:  # check down
			down = grid[(y+1)*SIZE_X + x]
			next_options &= check_options(down, 0)

		if x > 0:  # check left
			left = grid[y*SIZE_X + x - 1]
			next_options &= check_options(left, 1)
				
		next_grid[index].options = next_options
    
    # transfer the edited board to grid
	grid = next_grid.copy()

# generate a list of characters based on the left over options of the cells
char_list = [chars[i.options.pop()] for i in grid]

for i in range(0,len(char_list),SIZE_X+1): char_list.insert(i+SIZE_X, "\n")

print(*char_list, sep="")
