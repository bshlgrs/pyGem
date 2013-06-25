# moduleInterface

from equation import Equation
from simpleSolver import *

			elif instruction[:5]=="add e":
				equations.append(ep.Equation(instruction[12:]))
				displayEquations.append(instruction[12:].strip())
			elif instruction[:5]=="rewri":
				arg = instruction.split()[1]
				rewrites[arg] = rewrite(arg,equations)
			elif instruction[:5]=="decla":
				equivalencies.append(instruction.split()[2:])
			elif instruction[:5]=="resta":
				args = instruction.split()
				rewrites[args[1]] = ss.removeTerm(rewrites[args[1]],args[3],
											equations[int(args[5])],equivalencies)

def addEquation(equation):
	equations.append(Equation(equation))
	displayEquations.append(equation)

def write(var):
	a = rewrite(var,equations)
	print var,"=", a
	rewrites[var] = a

def declareEqual(inlist):
	addEquivalence(inlist,equivalencies)

def rewrite(var,without,using):
	expressions[var]=ss.removeTerm(var,without,equations[using],equivalencies)
	print expressions[var]


equations = []

displayEquations = []

equivalencies = []
expressions = {}

