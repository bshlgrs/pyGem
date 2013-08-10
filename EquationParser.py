from sympy import S

def loadEquations():
    with open("Equations.txt") as textfile:
        mystr = textfile.read()

    equationsList = mystr.split(".\n")
    sublists = [[y.strip() for y in x.split(";")]
                                for x in equationsList if len(x)>1]

    outlist = []

    for sublist in sublists:
        lhs,rhs = sublist[0].split("=")
        equation = str(S(lhs))+"="+str(S(rhs))
        unitsDict = {}
        for bit in sublist[1:-1]:
            lhs,rhs = bit.split("::")
            for var in lhs.split(","):
                unitsDict[var.strip()]=rhs.strip()
        tags = [x.strip() for x in sublist[-1].split() if len(x)>1]
        outlist.append((equation,unitsDict,tags))

    return outlist

if __name__ == '__main__':
    print loadEquations()
