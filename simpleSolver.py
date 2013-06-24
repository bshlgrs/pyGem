from equation import Equation

_debug = True

# We assume that each variable name is only in one place in all the formulas.


def legitEquation(equation,equivalencies = None):
	assert equation.coefficient != 0
	assert all(lambda x: equation.terms[x]!=0 for x in equation.terms)

def without(indict,value):
	outdict = dict(indict)
	outdict.pop(value)
	return outdict

def rearrange(expression, variable):
	if _debug:
		legitEquation(expression)
	if variable in expression.terms:
		coefficient = expression.terms[variable]
		out = Equation()
		out.terms= {x:expression.terms[x]/(-coefficient) for x in 
						without(expression.terms, variable)}
		out.coefficient = expression.coefficient**(1/coefficient)
		return out
	return None

def multiplyExpressions(a,b,equivalencies):
	if _debug:
		legitEquation(a) and legitEquation(b)
	
	outdict = dict(a.terms)

	for term in b.terms:
		eqVar = findEqualVariable(term,equivalencies,a.terms)
		if eqVar:
			outdict[eqVar] += b.terms[term]
			if outdict[eqVar] == 0:
				outdict.pop(eqVar)
		else:
			outdict[term] = b.terms[term]
	out = Equation()
	out.terms = outdict
	out.coefficient = a.coefficient * b.coefficient
	return out

def exponentiateExpression(exp,power):
	if _debug:
		legitEquation(exp)
	out=Equation()
	out.terms = {a:exp.terms[a]*power for a in exp.terms}
	out.coefficient = exp.coefficient**power
	return out

def isEquivalent(a,b,equivalencies):
	for group in equivalencies:
		if a in group:
			return b in group
	return False

def findEqualVariable(variable,equivalencies,terms):
	for term in terms:
		if isEquivalent(term,variable,equivalencies):
			return term
	return None

# This function finds an expression for 'variable' with 'eq2', and substitutes
# that into 'eq1', using the equivalencies stated in 'equivalencies'
def removeTerm(eq1,variable,eq2,equivalencies):
	if _debug:
		legitEquation(eq1) and legitEquation(eq2)
	assert variable in eq1.terms
	assert any(map (lambda x: isEquivalent(x,variable,equivalencies), eq2.terms))

	newVar = findEqualVariable(variable,equivalencies,eq2.terms)

	new = exponentiateExpression(eq2,-eq1.terms[variable]/eq2.terms[newVar])

	return multiplyExpressions(eq1,new,equivalencies)

def main():
	tests()

	universe = map(Equation, ["E_K = 0.5 m1 v^2","E_P = m2 g h"])
	print universe[0]
	a=rearrange(universe[0],"v")
	print "v =", a
	print "v =", removeTerm(a,"E_K",universe[1],[["m1","m2"],["E_K","E_P"]])

def tests():
	legitEquation(Equation("E_K = 0.5 m1 v^2"))
	assert without({1:2,3:4,5:6},3)=={1:2,5:6}

if __name__ == '__main__':
	main()

