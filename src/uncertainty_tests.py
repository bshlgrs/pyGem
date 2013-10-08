from uncertainties import ufloat
from Uncertainty_calculations import Ufloat

from random import random

a1,b1,c1,d1 = random()*10, random()*10, random()*10, random()*10

def convert(myUfloat):
	return ufloat(myUfloat.value,myUfloat.sigma)

print "Testing uncertainties module"

tests = "a+b,a*b,a**b".split(",")
for test in tests:
	a1,b1,c1,d1 = random()*10, random()*10, random()*10, random()*10
	val1 = eval(test,{'a':ufloat(a1,b1),'b':ufloat(c1,d1)})
	val2 = eval(test,{'a':Ufloat(a1,b1),'b':Ufloat(c1,d1)})
	print val1.nominal_value - val2.value, val1.std_dev - val2.sigma
	assert abs(val1.nominal_value - val2.value)<0.01 and abs(val1.std_dev - val2.sigma) < 0.01

