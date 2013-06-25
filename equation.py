# equation.py

from utilityFunctions import numberPrint

class Equation():
    def __init__(self,instr=None):
        if instr:
            self.terms, self.coefficient = parseEquation(instr)
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

if __name__ == '__main__':
    example = Equation("E_K = 0.5 m v^2")
    print example
