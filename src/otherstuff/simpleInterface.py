# simpleInterface.py

import simpleSolver as ss
import equationParse as ep

show = ep.equationToString

# Interface is:

# add equation Ek = 0.5 m1 v^2
# rewrite v
# declare equal m1 m2
# restate v without Ek using 2

def main():
	equations = [ep.Equation("ek = 0.5 m1 v^2"),ep.Equation("ep = m2 g h")]
	equivalencies = [["m1","m2"],["ek","ep"]]
	rewrites = {"v":ss.rearrange(equations[0],"v")}

	while True:
		printState(equations,equivalencies,rewrites)

		instruction = raw_input(">> ")

		if instruction == "":
			pass
		elif instruction[:5]=="add e":
			equations.append(ep.Equation(instruction[12:]))
		elif instruction[:5]=="rewri":
			arg = instruction.split()[1]
			rewrites[arg] = ss.rewrite(arg,equations)
		elif instruction[:5]=="decla":
			equivalencies.append(instruction.split()[2:])
		elif instruction[:5]=="resta":
			args = instruction.split()
			rewrites[args[1]] = ss.removeTerm(rewrites[args[1]],args[3],
										equations[int(args[5])],equivalencies)
		elif instruction=="quit":
			return
		else:
			print "Instruction not understood"

		print

def rewrite(arg,equations):
	for equation in equations:
		if arg in equation.terms:
			return ss.rearrange(equation,arg)
	raise Exception

def printState(equations,equivalencies,rewrites):
	if equations:
		print "Equations:"
		for (pos,a) in enumerate(equations):
			print "Equation %d: "%pos,a,"= 1"
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

	if rewrites:
		print "Rewrites:"
		for a in rewrites:
			print a,' = ', (ep.equationToString(rewrites[a]))
	else:
		print "No rewrites"

	print 

if __name__ == '__main__':
	main()