from sympy import *

def readEquation(instr):
	lhs,rhs = instr.split("=")
	return S(lhs)-S(rhs)

# print readEquation("KE=0.5*m*v**2")

# x= Symbol("x",positive=True)
# z,y= symbols("z y")
# print solve(z*x**2-y,x)

# equivs might be {"KE":["PE"],"m1":["m2","m3"]}
def simplifyEquivalencies(exp,equivs):
	outexp = exp
	for var in equivs:
		for var2 in equivs[var]:
			outexp = outexp.subs(var2,var)
	return outexp.simplify()

a,b,c,d,e = symbols('a b c d e')

pprint(simplifyEquivalencies(a*c/b+c**2+d+e,{a:[b,d],c:[e]}))