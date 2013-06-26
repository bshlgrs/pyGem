# equation.py

from utilityFunctions import numberPrint

class Equation():
    def __init__(self,instr=None):
        if instr:
            self.terms, self.coefficient = parseEquation(instr)
        else:
            self.terms = {}
            self.coefficient = 1
    def __str__(self):
        return equationToString(self)


def parseEquation(instr):
    lhs, rhs = instr.split("=")
    lhs = [x.strip() for x in lhs.split()]
    rhs = [x.strip() for x in rhs.split()]

    outdict = {}

    factor = 1

    for a in lhs:
        try:
            factor *= float(a)
        except Exception:
            if '^' not in a:
                outdict[a]=1
            else:
                base,exp = a.split("^")
                outdict[base]=float(exp)

    for a in rhs:
        try:
            factor /= float(a)
        except Exception:
            if '^' not in a:
                outdict[a]=-1
            else:
                base,exp = a.split("^")
                outdict[base]=-float(exp)

    return (outdict,factor)

def equationToString(equation,lhs=None):
    if lhs:
        outlist = [lhs,"="]
    else:
        outlist = []

    if str(equation.coefficient)!= "1":
        outlist.append(str(equation.coefficient))
    for term in equation.terms:
        power= equation.terms[term]
        if power==1:
            outlist.append(term)
        else:
            outlist.append("%s^%s"%(term,numberPrint(power)))
    return " ".join(outlist)

def substituteNumbersIntoExpression(expression,numbers):
    out = Equation()
    out.coefficient = expression.coefficient
    for variable in expression.terms:
        if variable in numbers:
            out.coefficient *= numbers[variable]**expression.terms[variable]
        else:
            out.terms[variable] = expression.terms[variable]
    return out

if __name__ == '__main__':
    example = Equation("KE = 0.5 m v^2")
    assert example.terms == {"KE":1,"m":-1,"v":-2}
    assert substituteNumbersIntoExpression(Equation("a b = 1"),{"a":3,"b":4}).coefficient == 12.0
