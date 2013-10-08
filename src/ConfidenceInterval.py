# ConfidenceInterval.py

import Uncertainty_calculations
from sympy.statistics import Normal

def getStdDev(distance,confidence,x = Normal(0,1)):
	"Distance = end point - mean"
	confidenceDistance = x.confidence(confidence)[1]
	stddev = confidenceDistance * distance
	return stddev

def confidenceInterval(start,end,confidence):
	"""If I give a 50 percent chance that my variable x is between 10 and 13,  
	then this function converts that to a Gaussian centered at 11.5 with an 
	appropriate standard deviation."""

	mean = 0.5*(end+start)
	stddev = getStdDev(0.5*(end-start), confidence)

	return (mean,stddev)
