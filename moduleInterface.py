# moduleInterface

from equation import Equation
from simpleSolver import *
from commandLineInterface import printState
from units import Units, unitsOfEquation, checkDimensionless, parseUnitsList


def addEquation(equation,unitsString):

	newEquation = Equation(equation)
	newUnits = parseUnitsList(unitsStringmoad)

	for variable in newEquation.terms:
		if variable in units:
			print "The variable %d is already used in another equation."
			return

	assert set(newEquation.terms) == set(newUnits)

	for unit in newUnits:
		units[unit] = newUnits[unit]

	assert checkDimensionless(newEquation,units)

	equations.append(newEquation)
	displayEquations.append(equation)

	showAll()
	
def declareEqual(inlist):

	# Check that everything is dimensionally sensible
	commonUnits = units[inlist[0]]
	assert all(commonUnits.terms == units[a].terms for a in inlist)

	addEquivalence(inlist,equivalencies)
	showAll()

def write(var):
	a = rewrite(var,equations)
	print var,"=", a
	rewrites[var] = a

def rewrite(var,without,using):
	expressions[var]=ss.removeTerm(var,without,equations[using],equivalencies)
	print expressions[var]

def showAll():
	printState(equations,equivalencies,expressions)


equations = []
displayEquations = []
equivalencies = []
expressions = {}
units = {}


