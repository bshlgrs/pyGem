import sympy as s
from sympy.solvers import solve
import re
from utilityFunctions import rewriteExpression, unicodify, censorUnicode

class Equation():
    """
    The representation of an equation.

    Attributes:
        lhs, rhs: Sympy expressions being the left and right hand sides
        of the function. These are seperate for display purposes.
        equation: lhs-rhs. The actual equation, used for actual things.

    """
    def __init__(self,lhs,rhs):
        self.equation = s.S(lhs) - s.S(rhs)
        self.text = unicodify(rewriteExpression(lhs + "=" + rhs))

    def __repr__(self):
        return "Equation %s"%censorUnicode(self.text)

    def __del__(self):
        pass

    def getVars(self):
        return [x.name for x in self.equation.atoms(s.Symbol)]

    def getVars2(self):
        return ([x.name for x in self.lhs.atoms(s.Symbol)],
                  [x.name for x in self.rhs.atoms(s.Symbol)])

    def rename(self,currentVarNumbers,newUnits):

        def replaceString(string,old,new):
            def change(match):
                thing = match.group(0)
                if thing==old:
                    return new
                return thing
            a= re.compile("\w*[a-zA-Z]\w*")
            return a.sub(change,string)

        myVars = self.getVars()

        renamedUnits = {}

        for name in myVars:
            if name in currentVarNumbers:
                currentVarNumbers[name]+=1
                newName = name+str(currentVarNumbers[name])
                newNameVar = s.Symbol(newName,positive=True)
                self.equation = self.equation.subs(name, newName)
                self.text = replaceString(self.text,name,newName)
                if name in newUnits:
                    renamedUnits[newName] = newUnits[name]
                else:
                    renamedUnits[newName] = "?"
            else:
                newVar = s.Symbol(name,positive=True)
             #   self.equation = self.equation.subs(name, newVar)

                currentVarNumbers[name]=1
                if name in newUnits:
                    renamedUnits[name] = newUnits[name]
                else:
                    renamedUnits[name] = "?"

        return renamedUnits

    def solve(self,variable):
        if variable in self.getVars():
            return solve(self.equation,s.S(variable))
        else:
            return None

