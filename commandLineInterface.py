# commandLineInterface.py

## This is obsolete -- I'm only improving moduleInterface at the moment

import simpleSolver as ss
import equation as ep
import sys

show = ep.equationToString

# Interface is:

# add equation Ek = 0.5 m1 v^2
# write v
# declare equal m1 m2
# rewrite v without Ek using 2

def main(livemode):

	equations = []
	
	displayEquations = []

	equivalencies = []
	expressions = {}
	
	while True:
		try:
			if livemode:
				printState(displayEquations,equivalencies,expressions)

				instruction = raw_input(">> ")
			else:
				instruction = raw_input()

			if instruction == "":
				pass
			elif instruction[:5]=="add e":
				equations.append(ep.Equation(instruction[12:]))
				displayEquations.append(instruction[12:].strip())
			elif instruction[:5]=="write":
				arg = instruction.split()[1]
				expressions[arg] = write(arg,equations)
			elif instruction[:5]=="decla":
				equivalencies.append(instruction.split()[2:])
			elif instruction[:5]=="rewri":
				args = instruction.split()
				expressions[args[1]] = ss.removeTerm(expressions[args[1]],args[3],
											equations[int(args[5])],equivalencies)
			elif instruction=="finish":
				if not livemode:
					printState(displayEquations,equivalencies,expressions)
				return
			else:
				print "Instruction not understood"
			if livemode:
				print
		except Exception as e:
			print "Something broke!"
			print e
			print


def write(arg,equations):
	for equation in equations:
		if arg in equation.terms:
			return ss.rearrange(equation,arg)
	raise Exception

def printState(equations,equivalencies,expressions):
	if equations:
		print "Equations:"
		for (pos,a) in enumerate(equations):
			print "Equation %d: "%pos,a
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
		print "expressions:"
		for a in expressions:
			print a,' = ', (ep.equationToString(expressions[a]))
	else:
		print "No expressions"

	print 

if __name__ == '__main__':
	if len(sys.argv)==1:
		main(False)
	else:
		main(True)

	# equations = [ep.Equation("ek = 0.5 m1 v^2"),ep.Equation("ep = m2 g h")]
	# equivalencies = [["m1","m2"],["ek","ep"]]
	# expressions = {"v":ss.rearrange(equations[0],"v")}
