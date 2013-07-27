import sympy, string

def equalityLine(exp):
	newPrint = sympy.pretty(exp+sympy.S("abracadabra")).split("abracadabra")
	return string.count(newPrint[0],"\n")

print equalityLine(sympy.S("x"))