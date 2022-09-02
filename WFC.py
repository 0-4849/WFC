import random, copy

chars = (" ", )

SIZE_X, SIZE_Y = 20,10
LEFT, RIGHT, UP, DOWN, BLANK = 4, 2, 1, 3, 0
"""
rules = {
    BLANK: [
        [BLANK, UP],
        [BLANK, RIGHT],
        [BLANK, DOWN],
        [BLANK, LEFT],
    ],
    UP: [
        [RIGHT, LEFT, DOWN],
        [LEFT, UP, DOWN],
        [BLANK, DOWN],
        [RIGHT, UP, DOWN],
    ],
    RIGHT: [
        [RIGHT, LEFT, DOWN],
        [LEFT, UP, DOWN],
        [RIGHT, LEFT, UP],
        [BLANK, LEFT],
    ],
    DOWN: [
        [BLANK, UP],
        [LEFT, UP, DOWN],
        [RIGHT, LEFT, UP],
        [RIGHT, UP, DOWN],
    ],
    LEFT: [
        [RIGHT, LEFT, DOWN],
        [BLANK, RIGHT],
        [RIGHT, LEFT, UP],
        [UP, DOWN, RIGHT],
    ]
}
"""

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
        self.options = {"blank":0, "up":1, "right":2, "down":3, "left":4}
        self.id = id

    def __lt__(self, other):
        return len(self.options) < len(other.options)
    
tiles = [0]*5
tiles[0] = Tile("blank", " ", [0,0,0,0])
tiles[1] = Tile("up", "┴", [1,1,0,1])
tiles[2] = Tile("right", "├", [1,1,1,0])
tiles[3] = Tile("down", "┬", [0,1,1,1])
tiles[4] = Tile("left", "┤", [1,0,1,1])

# calculate compatabilities for edges
test_rules = {}
tile_names = [i.name for i in tiles]
directions = tile_names[1:]

for i in tiles:
	test_rules[i.name] = {}
	for edge_index, edge in enumerate(i.edges):
		test_rules[i.name].update({directions[edge_index]:[]})
		for j in tiles:
			if edge == j.edges[(edge_index + 2) % 4]:
				test_rules[i.name][directions[edge_index]].append(j.name)
				
# print(test_rules)
			
			


grid = [Cell(i) for i in range(SIZE_X*SIZE_Y)]
output = [" "]*SIZE_X*SIZE_Y

while True:
    
	grid_copy = copy.deepcopy(grid)
	grid_copy.sort()  # sort by number of options (__lt__ method)
	grid_copy = list(filter((lambda x: not x.is_collapsed), grid_copy))
	if len(grid_copy) == 0: break

	possible_tiles = [i for i in grid_copy if len(i.options) == len(grid_copy[0].options)] # pick random tile from all lowest values

	current_tile = random.choice(possible_tiles)
	current_tile.is_collapsed = True
	random_key = random.choice(list(current_tile.options.keys()))
	current_tile.options = {random_key: current_tile.options[random_key]}

	next_grid = grid.copy()

	for y in range(SIZE_Y):
		for x in range(SIZE_X):
			index = y*SIZE_X + x
			if grid[index].is_collapsed:
				next_grid[index] = grid[index]
			else:
				next_options = {0, 1, 2, 3, 4}
				
				if y > 0:  # check up
					up = grid[(y-1)*SIZE_X + x]
					valid_options = set()
					for option in up.options:
						valid = test_rules[option]["down"]
						valid_options = valid_options.union(set(valid))
					next_options = next_options & valid_options

				if x < SIZE_X - 1:  # check right
					right = grid[y*SIZE_X + x + 1]
					valid_options = set()
					for option in right.options:
						valid = test_rules[option]["left"]
						valid_options = valid_options.union(set(valid))
					next_options = next_options & valid_options

				if y < SIZE_Y - 1:  # check down
					down = grid[(y+1)*SIZE_X + x]
					valid_options = set()
					for option in down.options:
						valid = test_rules[option]["up"]
						valid_options = valid_options.union(set(valid))
					next_options = next_options & valid_options

				if x > 0:  # check left
					left = grid[y*SIZE_X + x - 1]
					valid_options = set()
					for option in left.options:
						valid = test_rules[option]["right"]
						valid_options = valid_options.union(set(valid))
					next_options = next_options & valid_options
						
				

				next_grid[index].options = dict(zip(next_options))
				#char_list = [chars[i.options[0]] if len(i.options) == 1 else "█" for i in grid ]

				#for i in range(0,len(char_list),SIZE_X+1): char_list.insert(i+SIZE_X, "\n")
				#print("\033[2J","".join(char_list),sep="")
    
    
    
	grid = copy.deepcopy(next_grid)


char_list = [chars[i.options[0]] for i in grid]

for i in range(0,len(char_list),SIZE_X+1): char_list.insert(i+SIZE_X, "\n")

print(*char_list, sep="")

#comment to test git commit
