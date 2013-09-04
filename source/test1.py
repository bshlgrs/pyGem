import Backend
from Equation import Equation

a=Backend.Backend()
a.addEquation(Equation("EK","0.5*m*v**2"),{"EK":"J","m":"kg",
                                      "v":"m*s^-1"})
a.addEquation(Equation("EP","m*g*h"),{"EP":"J","m":"kg",
                                    "g":"m*s^-2", "h":"m"})

a.addEquivalency(["EK","EP"])

a.findExpression("v",a.equations[0])

print(a.expressions)

a.rotateVariableInExpression("v","EK")

print(a.expressions)
