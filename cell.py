class Cell():
	def __init__(self, id) -> None:
		self.is_collapsed = False
		self.options = {0,1,2,3,4}
		self.id = id

	def __lt__(self, other):
		return len(self.options) < len(other.options)