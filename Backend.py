## Backend.py

from Dimensions import Dimensions
from Equation import Equation
from sympy import pretty

class Backend():
    """The backend for my graphical equation manipulator.

    This stores all the actual information about the equations and such
    in use, and is used by a front end.

    Attributes:
        self.equations is a list of Equation objects.

        self.equivalencies is a list of lists of equal variables.
        They're strings, eg [["KE","PE"],["m1","m2"]]

        self.dimensions is a dictionary from names of variables to their
        dimensions, which are stored as Dimensions objects.

        self.expressions is a dictionary from names of variables to
        a list of Sympy expressions.

        self.varNumbers is a dictionary from names of variables, like
        "m", to how many variables with that name are in use. It's
        used when equations need to have variable names changed to not
        conflict with existing variables.

        """

    def __init__(self):
        self.equations = []
        self.equivalencies = []
        self.dimensions = {}
        self.expressions = {}
        self.varNumbers = {}

    def show(self):
        """Prints a simple string representation of the object."""
        print "Equations:"
        for x in self.equations:
            print x

        print "\nEquivalencies:"
        for x in self.equivalencies:
            print "=".join(x)

        print "\nDimensions:"
        for x in self.dimensions:
            print x,"::".dimensions[x].show()

        print "\nExpressions:"
        for x in self.expressions:
            print x," = ",self.expressions[x]

    def addEquation(self,equation,newUnits):
        equation.rename(self.varNumbers)
        self.equations.append(equation)

        for var in newUnits:
            self.dimensions[var] = newUnits[var]


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
        print "We're being dodgy and not checking.dimensions!"
        return
        for group in self.equivalencies:
            if len(group)>1: # I'm pretty sure this should always be true
                firstThing = group[0]
                for thing in group[1:]:
                    assert self.dimensions[firstThing] == self.dimensions[thing]

    def findExpression(self,var,equation):
        if var in equation.getVars():
            exp = equation.solve(var)
            if exp:
                self.expressions[var] = exp
            else:
                raise Exception("No solution found")
            return
        raise Exception("Variable not in expression")


    # Not tested!
    def updateExpressionsWithEquivalency(self):
        newEquivalency = self.equivalencies[-1]

        for var in self.expressions:
            expr = self.expressions[var]

            similarList = [x for expr in newEquivalency if x in expr.getVars()]

            if len(similarList) > 1:
                target = similarList[0]
                for var2 in similarList[1:]:
                    expr = expr.replace(var2,target)
                self.expressions[var] = expr

    def rotateVariableInExpression(self,expression,var):
        raise NotImplementedError()
        group = [x for x in self.equivalencies if var in x]
        varToChangeTo = (group.index(var) + 1) % len(group)

        ## Replace var by varToChangeTo in expression

    def rewriteUsingExpression(self,equation,var,expr):
        raise NotImplementedError()

    def rewriteUsingEquation(self,equation,var,equation2):
        raise NotImplementedError()

if __name__ == '__main__':
    a = Backend()
    a.addEquation(Equation("KE","0.5*m*v**2"),{})
    a.addEquation(Equation("KE","0.5*m*v**2"),{})
    a.addEquivalency(["m","m2"])


    a.findExpression("v",a.equations[0])

    print a.expressions

    a.show()
