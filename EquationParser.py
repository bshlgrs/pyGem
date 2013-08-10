from sympy import S

def loadEquations():
    with open("Equations.txt") as textfile:
        mystr = textfile.read()

    equationsList = mystr.split(".\n")
    sublists = [[y.strip() for y in x.split(";")]
                                for x in equationsList if len(x)>1]

    outlist = []

    for sublist in sublists:
        equation = sublist[0]
        lhs,rhs = equation.split("=")
        unitsDict = {}
        for bit in sublist[1:-1]:
            lhs2,rhs2 = bit.split("::")
            for var in lhs2.split(","):
                unitsDict[var.strip()]=rhs2.strip()
        tags = [x.strip() for x in sublist[-1].split() if len(x)>1]
        outlist.append((equation,lhs,rhs,unitsDict,tags))

    return outlist

if __name__ == '__main__':
    print loadEquations()
