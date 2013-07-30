## Backend.py

from Dimensions import Dimensions
from Equation import Equation
from sympy import pretty
from sympy.solvers import solve
from sympy import Symbol

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

    def findEquationWithVar(self,var):
        for equation in self.equations:
            if var in equation.getVars():
                return equation
        raise Exception("Var not found in any equation")

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

    def varsEqual(self,var1,var2):
        for group in self.equivalencies:
            if var1 in group:
                return var2 in group
        return False

    def equivalenciesOfVariable(self,var):
        for group in self.equivalencies:
            if var in group:
                out = list(group)
                out.remove(var)
                return out
        return []

    def checkUnits(self):
        print "We're being dodgy and not checking.dimensions!"
        return
        for group in self.equivalencies:
            if len(group)>1: # I'm pretty sure this should always be true
                firstThing = group[0]
                for thing in group[1:]:
                    assert (self.dimensions[firstThing] ==
                                                 self.dimensions[thing])

    def findExpression(self,var,equation):
        if var in equation.getVars():
            exps = equation.solve(var)
            if exps:
                self.expressions[var] = exps
            else:
                raise Exception("No solution found")
            return
        raise Exception("Variable not in expression")


    # Not tested
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

    def rotateVariableInExpression(self,varToChange,oldName):
        """
        Changes a variable in an expression to an equivalent one.

        For example, if we have m and m2, this might change KE=m*v**2 to
        KE=m2*v**2.

        Args:
            varToChange: This is the variable whose expression we want
                to adjust, eg KE in the previous example.
            oldName: This is the name of the variable whose name we want
                to change, eg m in the previous example.
        """

        group = [x for x in self.equivalencies if oldName in x][0]
        newName = group[(group.index(oldName) + 1) % len(group)]

        varExpressions = self.expressions[varToChange]
        self.expressions[varToChange] = []
        for exp in varExpressions:
            self.expressions[varToChange].append(
                                        exp.replace(oldName,newName))

    def rewriteUsingExpression(self,var,varToRemove,varWhoseExpToUse):
        """
        Rewrites the expression for var to not include varToRemove,
        by substituting the expression for varWhoseExpToUse into it.
        """

        assert self.varsEqual(varToRemove,varWhoseExpToUse)

        newExpList = []

        for exp in self.expressions[var]:
            for exp2 in self.expressions[varWhoseExpToUse]:
                newExpList.append(exp.replace(varToRemove,exp2))

        self.expressions[var] = newExpList


    def rewriteUsingEquation(self,var,varToRemove,equation):
        """
        Rewrites the expression for var to not include varToRemove,
        by solving equation for varToRemove, then substituting that
        into the expression for var.
        """

        equat = equation.equation
        for var2 in self.equivalenciesOfVariable(varToRemove):
            equat = equat.replace(var2,varToRemove)

        exps = solve(equat,varToRemove)

        outexps = []

        for exp1 in self.expressions[var]:
            for exp2 in exps:
                outexps.append(exp1.replace(varToRemove,exp2))


        self.expressions[var] = [self.unifyVarsInExpression(x)
                        for x in outexps]

    def unifyVarsInExpression(self,exp):
        varNameList = [x.name for x in exp.atoms(Symbol)]
        for var in varNameList:
            for var2 in self.equivalenciesOfVariable(var):
                exp = exp.replace(var2,var)
        exp.simplify()
        return exp



if __name__ == '__main__':
    a = Backend()
    a.addEquation(Equation("KE","0.5*m*v**2"),{})
    a.addEquation(Equation("PE","m*g*h"),{})
    a.addEquivalency(["m","m2"])
    a.addEquivalency(["KE","PE"])

    a.findExpression("v",a.equations[0])

    a.show()

    a.rewriteUsingEquation("v","KE",a.equations[1])

    a.show()
