## Backend.py

from Dimensions import Dimensions

class Backend():
	def __init__(self):
		self.equations = []
		self.equivalencies = []
		self.units = {}
		self.expressions = {}

	def show(self):
		print "Equations:"
		for x in self.equations:
			print x
		
		print "\nEquivalencies:"
		for x in equivalencies:
			print "=".join(x)

		print "\nUnits:"
		for x in units:
			print x,"::",units[x].show()

		print "\nExpressions:"
		for x in expressions:
			print x," = ",pretty(x)

	def addEquation(equation,newUnits):


