class Tile():
	def __init__(self, name, char, edges) -> None:
		self.name = name		
		self.char = char
		self.edges = edges
  
		self.up = []
		self.right = []
		self.down = []
		self.left = []