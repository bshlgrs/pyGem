# moduleInterface

from equation import Equation, substituteNumbersIntoExpression, equationToString
from simpleSolver import *
from units import Units, unitsOfEquation, checkDimensionless, parseUnitsList


def addEquation(equation,unitsString):
	newEquation = Equation(equation)
	newUnits = parseUnitsList(unitsString)

	for variable in newEquation.terms:
		if variable in units:
			print "The variable %d is already used in another equation."%variable
			return

	assert set(newEquation.terms) == set(newUnits)

	for unit in newUnits:
		units[unit] = newUnits[unit]

	assert checkDimensionless(newEquation,units)

	equations.append(newEquation)
	displayEquations.append(equation)
	
def declareEqual(inlist):
	# Check that everything is dimensionally sensible
	commonUnits = units[inlist[0]]
	assert all(commonUnits.terms == units[a].terms for a in inlist)

	addEquivalence(inlist)

def addEquivalence(newthing):
	newgroup = list(newthing)
	for group in equivalencies:
		if any(x in newgroup for x in group):
			equivalencies.remove(group)
			for x in group:
				if x not in newgroup:
					newgroup.append(x)
	equivalencies.append(newgroup)
	return equivalencies

def write(var):
	for equation in equations:
		if var in equation.terms:
			a = rearrange(equation,var)

			print var,"=", 
			expressions[var] = a
			return
			
	raise Exception


def rewrite(var,without,using):
	print 'args',(var,without,equations[using],equivalencies)
	expressions[var] = removeTerm(expressions[var],without,equations[using],equivalencies)
	print expressions[var]

def setNumericalValue(variable,value):
	numericalValues[variable] = value

def showAll():
	printState(equations,equivalencies,expressions)

def printState(equations,equivalencies,expressions):
	if equations:
		print "Equations:"
		for (pos,a) in enumerate(equations):
			print "Equation %d:"%pos,a
	else:
		print "No equations"
	print

	if equivalencies:
		print "Equivalencies:"
		for group in equivalencies:
			print "=".join(group)
	else:
		print "No equivalencies"

	print

	if expressions:
		print "Expressions:"
		for a in expressions:
			print a,' :: ', units[a], ' = ', equationToString(expressions[a]), \
				 ' = ', substituteNumbersIntoExpression(expressions[a],numbers)
	else:
		print "No expressions"
	print 

equations = []
displayEquations = []
equivalencies = []
expressions = {}
units = {}
numbers = {"h":13,"g":9.8}

def example():
	addEquation("KE = 0.5 m1 v^2","KE::kg m^2 s^-2, m1::kg, v::m s^-1")
	addEquation("PE = m2 g h","PE::kg m^2 s^-2, m2::kg, g::m s^-2, h::m")
	declareEqual(["KE","PE"])
	declareEqual(["m1","m2"])
	write("v")
	rewrite("v","KE",1)

	showAll()