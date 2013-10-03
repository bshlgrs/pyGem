from sympy.core.mul import Mul
from sympy.core.add import Add
from sympy.core.power import Pow
from sympy.core.symbol import Symbol
from sympy.core.numbers import NumberSymbol, Number

from uncertainties import ufloat

# class UFloat(object):
# 	def __init__(self,value,sigma):
# 		self.value = value
# 		self.sigma = sigma
# 	def __repr__(self):
# 		return "%f+-%f"%(self.value, self.sigma)
# 	def __add__(self,other):
# 		try:
# 			return UFloat(self.value+other.value,
# 					(self.self.sigma**2+other.sigma**2)**0.5)
# 		except AttributeError:
# 			return UFloat(self.value+other,self.sigma)
# 	def __mul__(self,other):
# 		try:
# 			val = self.value*other.value
# 			return UFloat(val, ((self.sigma/self.val)**2 +
# 							(other.sigma/other.val)**2)**0.5*val)
# 		except AttributeError:
# 			return UFloat(self.value*other,self.sigma*other)

# 	def __pow__(self,other):


# 	def __radd__(self,other):
# 		return self + other

# 	def __rmul__(self,other):
# 		return self * other
		
def findUncertainty(exp, variables):
	if exp.func == Mul:
		return findUncertainty(exp.args[0],variables) * \
							findUncertainty(exp.args[1],variables)
	if exp.func == Add:
		return findUncertainty(exp.args[0],variables) + \
							findUncertainty(exp.args[1],variables)
	if exp.func == Pow:
		return (findUncertainty(exp.args[0],variables) ** 
					findUncertainty(exp.args[1],variables))
	if exp.func == Symbol:
		return variables[exp.name]
	if issubclass(exp.func, Number):
		return ufloat(float(exp),0)
	raise Exception(exp)

