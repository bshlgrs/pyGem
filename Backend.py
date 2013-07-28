## Backend.py

from Dimensions import Dimensions
from Equation import Equation

class Backend():
    def __init__(self):
        self.equations = []
        self.equivalencies = []
        self.units = {}
        self.expressions = {}
        self.varNumbers = {}

    def show(self):
        print "Equations:"
        for x in self.equations:
            print x
        
        print "\nEquivalencies:"
        for x in self.equivalencies:
            print "=".join(x)

        print "\nUnits:"
        for x in self.units:
            print x,"::",units[x].show()

        print "\nExpressions:"
        for x in self.expressions:
            print x," = ",pretty(x)

    def addEquation(self,equation,newUnits):
        equation.rename(self.varNumbers)
        self.equations.append(equation)

        for var in newUnits:
            self.units[var] = newUnits[var]


    ## Does this need to be done in the stupid immutable way 
    #  it's currently done?

    # Also, this allows an equivalency between lots of things,
    # which is unnecessary.
    def addEquivalency(self,newEquivalencies):
        newgroup = list(newEquivalencies)
        outlist = [list(x) for x in self.equivalencies] # this is a deep copy
        for group in outlist:
            if any(x in newgroup for x in group):
                outlist.remove(group)
                for x in group:
                    if x not in newgroup:
                        newgroup.append(x)
        outlist.append(newgroup)
        self.equivalencies = outlist
        self.checkUnits()

    def checkUnits(self):
        for group in self.equivalencies:
            if len(group)>1: # I'm pretty sure this should always be true
                firstThing = group[0]
                for thing in group[1:]:
                    assert units[firstThing] == units[thing]

    def findExpression(self,var,equation):
        if var in equation.getVars():
            exp = equation.solve[var]
            if exp:
                self.expressions[var] = exp
            else:
                raise Exception("No solution found")
        raise Exception("Variable not in expression")

    def rewriteUsingExpression(self,equation,var,expr):
        raise NotImplementedError()

    def rewriteUsingEquation(self,equation,var,equation2):
        raise NotImplementedError()

if __name__ == '__main__':
    a = Backend()
    a.addEquation(Equation("KE","0.5*m*v**2"),{})
    a.addEquation(Equation("KE","0.5*m*v**2"),{})
    a.addEquivalency(["m","m2"])
    a.show()
