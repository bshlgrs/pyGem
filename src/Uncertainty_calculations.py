"""
This module propogates uncertainties as described here:
http://www.mso.anu.edu.au/~pfrancis/phys1101/Propagation_Equations.pdf

"""


from sympy.core.mul import Mul
from sympy.core.add import Add
from sympy.core.power import Pow
from sympy.core.symbol import Symbol
from sympy.core.numbers import NumberSymbol, Number

try:
	from uncertainties import ufloat
except ImportError:
	print "Uh, you don't have the uncertainties module."

class Ufloat(object):
	def __init__(self,value,sigma):
		self.value = float(value)
		self.sigma = float(sigma)
	def __add__(self,other):
		return Ufloat(self.value+other.value,
 					(self.sigma**2+other.sigma**2)**0.5)

	def __sub__(self,other):
		return Ufloat(self.value-other.value,
 					(self.sigma**2+other.sigma**2)**0.5)

	def __mul__(self,other):
		val = self.value*other.value
		return Ufloat(val, ((self.sigma/self.value)**2 +
						(other.sigma/other.value)**2)**0.5*val)

	def __pow__(self,other):
		return Ufloat(self.value**other.value,self.sigma*other.value)

	def __str__(self):
		return "%f+-%f"%(self.value,self.sigma)

	def __repr__(self):
		return str(self)

def findUncertainty(exp, variables):
	print exp, exp.func, exp.args
	if exp.func == Mul:
		out = Ufloat(1,0)
		for arg in exp.args:
			out *= findUncertainty(arg,variables)
		return out 
	if exp.func == Add:
		out = Ufloat(0,0)
		for arg in exp.args:
			out += findUncertainty(arg,variables)
		return out 	
	if exp.func == Pow:
		return (findUncertainty(exp.args[0],variables) ** 
					findUncertainty(exp.args[1],variables))
	if exp.func == Symbol:
		return variables[exp.name]
	if issubclass(exp.func, Number):
		return Ufloat(float(exp),0)
	raise Exception(exp)

def nominal_value(x):
	try:
		return x.value
	except AttributeError:
		return x.nominal_value
