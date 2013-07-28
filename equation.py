import sympy as s
from sympy.solvers import solve

class Equation():
    """
    The representation of an equation.

    Attributes:
        lhs, rhs: Sympy expressions being the left and right hand sides
        of the function. These are seperate for display purposes.
        equation: lhs-rhs. The actual equation, used for actual things.

    """
    def __init__(self,lhs,rhs):
        self.lhs = s.S(lhs)
        self.rhs = s.S(rhs)
        self.equation = self.lhs - self.rhs

    def __repr__(self):
        return (repr(self.lhs)+' = '+ repr(self.rhs))

    def getVars(self):
        return [x.name for x in self.equation.atoms(s.Symbol)]

    def getVars2(self):
        return ([x.name for x in self.lhs.atoms(s.Symbol)],
                  [x.name for x in self.rhs.atoms(s.Symbol)])

    def rename(self,currentVarNumbers):
        lhs, rhs = self.getVars2()

        for name in lhs:
            if name in currentVarNumbers:
                currentVarNumbers[name]+=1
                self.lhs = self.lhs.replace(name,
                                name+str(currentVarNumbers[name]))
            else:
                currentVarNumbers[name]=1

        for name in rhs:
            if name in currentVarNumbers:
                currentVarNumbers[name]+=1
                self.rhs = self.rhs.replace(name,
                                name+str(currentVarNumbers[name]))
            else:
                currentVarNumbers[name]=1
        self.equation = self.lhs - self.rhs

    def solve(self,variable):
        if variable in self.getVars():
            return solve(self.equation,s.S(variable))
        else:
            return None

if __name__ == '__main__':
    a = Equation("KE","0.5*m*v**2")

    print a

    currentVarNumbers = {"m":1}

    a.rename(currentVarNumbers)

    print a, currentVarNumbers

    s.pprint(a.solve("v"))

