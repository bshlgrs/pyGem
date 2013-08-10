## Backend.py

from Dimensions import Dimensions
from Equation import Equation
from sympy import pretty, S
from utilityFunctions import replaceName
from sympy.solvers import solve
from sympy import Symbol

class Backend(object):
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

        self.numericalValues is a dictionary from variable names to
        their numerical values.

        """

    def __init__(self):
        self.equations = []
        self.equivalencies = []
        self.dimensions = {}
        self.expressions = {}
        self.varNumbers = {}
        self.numericalValues = {}

    def show(self):
        """Prints a simple string representation of the object."""
        if self.equations:
            print "Equations:"
            for x in self.equations:
                print x

        if self.equivalencies:
            print "\nEquivalencies:"
            for x in self.equivalencies:
                print "=".join(x)

        if self.dimensions:
            print "\nDimensions:"
            for x in self.dimensions:
                print x,"::",self.dimensions[x]

        if self.expressions:
            print "\nExpressions:"
            for x in self.expressions:
                print x," = ",self.expressions[x]

        if self.numericalValues:
            print "\nNumerical values:"
            for x in self.numericalValues:
                print x," = ",self.numericalValues[x]

    def addEquation(self,equation,newUnits):
        """
        This adds equation to the current list of equations, and updates
        the units dict with the units of equation.

        Args:
            Equation: An Equation object
            newUnits: A dictionary from strings to Dimensions objects

        """
        renamedUnits = equation.rename(self.varNumbers,newUnits)
        self.equations.append(equation)

        for var in renamedUnits:
            self.dimensions[var] = renamedUnits[var]

    # Needs testing
    def removeEquation(self,equation):
        if equation in self.equations:
            self.equations.remove(equation)

            for var in equation.getVars():
                for partition in self.equivalencies:
                    if var in partition:
                        partition.remove(var)

            for partition in self.equivalencies:
                if len(partition)==1:
                    self.equivalencies.remove(partition)

    def findEquationWithVar(self,var):
        """
        Finds an equation with the variable var in it.

        Args:
            var: A string corresponding to the variable we're looking
            for.

        Raises:
            If the var is not in any equation, an exception is raised.
        """
        for equation in self.equations:
            if var in equation.getVars():
                return equation
        raise Exception("Var not found in any equation")

    def addEquivalency(self,newEquivalencies):
        """
        Takes a list of variables and tells the backend that they are
        all equal to each other.

        Equality is transitive, so if for example we know a=b and c=d,
        telling it that b=c makes it infer a=b=c=d.

        Args:
            newEquivalencies: A list of strings corresponding to
            variables.
        """

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
        self.updateExpressionsWithEquivalencies()

    def varsEqual(self,var1,var2):
        """
        Checks if var1 is known to be equal to var2.
        """
        for group in self.equivalencies:
            if var1 in group:
                return var2 in group
        return False

    def equivalenciesOfVariable(self,var):
        """
        Gives a list of variables known to be equal to var, not
        including var itself."""
        for group in self.equivalencies:
            if var in group:
                out = list(group)
                out.remove(var)
                return out
        return []


    def checkUnits(self):
        for group in self.equivalencies:
            if len(group)>1: # I'm pretty sure this should always be true
                for thing in group[1:]:
                    assert (self.dimensions[group[0]] ==
                                                 self.dimensions[thing])

    def findExpression(self,var,equation):
        """
        Finds expressions for var and adds them to the dict of
        expressions.

        Args:
            var: Variable to solve for.
            equation: Equation to solve for var.

        Returns nothing.
        """

        if var in equation.getVars():
            exps = equation.solve(var)
            if exps:
                self.expressions[var] = exps
            else:
                raise Exception("No solution found")
            return
        raise Exception("Variable not in expression")


    def updateExpressionsWithEquivalencies(self):
        """
        Updates all expressions to deal with the current known
        equivalencies. For example, if a=g*m1/m2, and we suddenly
        learn that m1=m2, it will simplify the expression to a=g.
        """

        newEquivalency = self.equivalencies[-1]

        for var in self.expressions:
            self.expressions[var] = [unifyVarsInExpression(x) for
                                    x in self.expressions[var]]

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
                                        replaceName(exp,oldName,newName))

    def rewriteUsingExpression(self,var,varToRemove,varWhoseExpToUse):
        """
        Rewrites the expression for var to not include varToRemove,
        by substituting the expression for varWhoseExpToUse into it.
        """

        assert self.varsEqual(varToRemove,varWhoseExpToUse)

        newExpList = []

        for exp in self.expressions[var]:
            for exp2 in self.expressions[varWhoseExpToUse]:
                newExpList.append(exp.subs(varToRemove,exp2))

        self.expressions[var] = newExpList


    def rewriteUsingEquation(self,var,varToRemove,equation):
        """
        Rewrites the expression for var to not include varToRemove,
        by solving equation for varToRemove, then substituting that
        into the expression for var.
        """

        equat = equation.equation
        for var2 in self.equivalenciesOfVariable(varToRemove):
            equat = equat.subs(var2,varToRemove)

        exps = solve(equat,varToRemove)

        outexps = []

        for exp1 in self.expressions[var]:
            for exp2 in exps:
                outexps.append(exp1.subs(varToRemove,exp2))


        self.expressions[var] = [self.unifyVarsInExpression(x)
                        for x in outexps]

    def unifyVarsInExpression(self,exp):
        varNameList = [x.name for x in exp.atoms(Symbol)]
        for var in varNameList:
            for var2 in self.equivalenciesOfVariable(var):
                exp = exp.subs(var2,var)
        exp.simplify()
        return exp

    def addNumericalValue(self,variable,value):
        others = self.equivalenciesOfVariable(variable)
        for other in others:
            if other in self.numericalValues:
                raise Exception("Inconsistent numerical value added")

        self.numericalValues[variable] = value

    def getNumericalValue(self,variable):
        if variable in self.numericalValues:
            return self.numericalValues[variable]

        others = self.equivalenciesOfVariable(variable)
        for other in others:
            if other in self.numericalValues:
                return self.numericalValues[other]

        return None

    def getNumericalExpressions(self,variable):

        assert variable in self.expressions

        exps = self.expressions[variable]
        outexps = []

        for exp in exps:
            for var2 in [x.name for x in exp.atoms(Symbol)]:
                newVal = self.getNumericalValue(var2)
                if newVal is not None:
                    exp = exp.subs(var2,newVal)
            outexps.append(exp)


        return outexps


if __name__ == '__main__':
    a = Backend()
    a.addEquation(Equation("EK","0.5*m*v**2"),{"EK":"J","m":"kg",
                                          "v":"m*s^-1"})
    a.addEquation(Equation("EP","m*g*h"),{"EP":"J","m":"kg",
                                        "g":"m*s^-2", "h":"m"})

    a.addEquation(Equation("EP","m*g*h"),{"EP":"J","m":"kg",
                                        "g":"m*s^-2", "h":"m"})

    a.addEquivalency(["m","m2"])
    a.addEquivalency(["EK","EP"])

    a.findExpression("v",a.equations[0])

    a.show()

    print

    a.rewriteUsingEquation("v","EK",a.equations[1])

    a.addNumericalValue("g",9.8)

    a.show()

    print a.getNumericalExpressions("v")
