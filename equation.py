import sympy as s
from sympy.solvers import solve

class Equation():
    def __init__(self,lhs,rhs):
        self.lhs = s.S(lhs)
        self.rhs = s.S(rhs)
        self.equation = self.lhs - self.rhs

    def __repr__(self):
        return (repr(self.lhs)+' = '+ repr(self.rhs))

    def getVars(self):
        lhs = []
        rhs = []
        func = s.Symbol("x").func

        for a in s.preorder_traversal(self.lhs):
            if a.func == func:
                lhs.append(a.name)
        for a in s.preorder_traversal(self.rhs):
            if a.func == func:
                rhs.append(a.name)
        return (lhs,rhs)

    def rename(self,currentVarNumbers):
        lhs, rhs = self.getVars()

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
        if variable in self.getVars()[0]+self.getVars()[1]:
            return solve(self.equation,variable)
        else:
            return None

if __name__ == '__main__':
    a = Equation("KE","0.5*m*v**2")

    print a

    currentVarNumbers = {"m":1}

    a.rename(currentVarNumbers)

    print a, currentVarNumbers

    s.pprint(a.solve("v"))

