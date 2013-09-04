from equation import equationToString, Equation

class Units():
	def __init__(self,string=None):
		if string:
			self.terms = parseUnits(string)
		else:
			self.terms = {}
	def __str__(self):
		if self.terms == {}:
			return "Dimensionless"
		dummyEquation = Equation()
		dummyEquation.terms = self.terms
		dummyEquation.coefficient = 1
		return equationToString(dummyEquation)

def parseUnits(instr):
    tokens = [x.strip() for x in instr.split()]

    outdict = {}

    for a in tokens:
        if '^' not in a:
            outdict[a]=1
        else:
            base,exp = a.split("^")
            outdict[base]=float(exp)

    return outdict

# This parses things like "EK::kg m^2 s^-2, m :: kg, v :: m s^-1"
def parseUnitsList(instr):
	outdict = {}
	for fragment in instr.split(","):
		lhs, rhs = fragment.split("::")
		outdict[lhs.strip()] = Units(rhs)
	return outdict

def exponentiateUnits(units,power):
	outunits = Units()
	for term in units.terms:
		outunits.terms[term] = units.terms[term]*power
	return outunits

def multiplyUnits(unitsA, unitsB):
	outunits = dict(unitsA)
	for unit in unitsB:
		outunits[unit] = outunits.get(unit,0) + unitsB[unit]
		if outunits[unit] == 0:
			outunits.pop(unit)
	return outunits

def unitsOfEquation(equation,units):
	out = Units()

	for a in equation.terms:
		adjustedUnits = exponentiateUnits(units[a],equation.terms[a])
		for unit in adjustedUnits.terms:
			out.terms[unit] = out.terms.get(unit,0) + adjustedUnits.terms[unit]
			if out.terms[unit] == 0:
				out.terms.pop(unit)
	return out

def checkDimensionless(equation,units):
	return unitsOfEquation(equation, units).terms == Units().terms

def main():
	assert Units("kg m^3 s^-2 A^1.5").terms == {"m":3,"kg":1,"s":-2,"A":1.5}
	assert exponentiateUnits(Units("kg m^-2"),2).terms == {"kg":2,"m":-4}

	e = Equation("KE = 0.5 m v^2")
	units = {"KE":Units("kg m^2 s^-2"), "m":Units("kg"), "v":Units("m s^-1")}

	autoUnits = parseUnitsList("KE::kg m^2 s^-2, m :: kg, v :: m s^-1")

	for a in autoUnits:
		assert autoUnits[a].terms == units[a].terms

	assert unitsOfEquation(e, units).terms == Units().terms
	assert checkDimensionless(e,units)



if __name__ == '__main__':
	main()