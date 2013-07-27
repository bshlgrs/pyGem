
class Dimensions():
	def __init__(self,dimensions):
		self.dimensions = dimensions
	def show(self):
		print self.dimensions
	def __mul__(self,other):
		if isinstance(other, Dimensions):
			 