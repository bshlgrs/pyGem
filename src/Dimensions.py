from utilityFunctions import numberPrint

class Dimensions():
    def __init__(self,dimensions):
        self.dimensions = dimensions
    def __repr__(self):
        outlist = []
        for term in self.dimensions:
            power= self.dimensions[term]
            if power==1:
                outlist.append(term)
            else:
                outlist.append("%s^%s"%(term,numberPrint(power)))
        return " ".join(outlist)
    def __mul__(self,other):
        if isinstance(other, Dimensions):
            outunits = dict(self.dimensions)
            for unit in other.dimensions:
                outunits[unit] = outunits.get(unit,0) + other.dimensions[unit]
                if outunits[unit] == 0:
                    outunits.pop(unit)
            return Dimensions(outunits)
        else:
            return self

    def __add__(self,other):
        if isinstance(other, Dimensions):
            assert self.dimensions == other.dimensions
            return
        else:
            raise IncorrectUnitsException()

    def __pow__(self,other):
        raise NotImplementedError()

class IncorrectUnitsException(Exception):
    pass

def dimensionsFromString(instr):
    tokens = [x.strip() for x in instr.split()]

    outdict = {}

    for a in tokens:
        if '^' not in a:
            outdict[a]=1
        else:
            base,exp = a.split("^")
            outdict[base]=float(exp)

    return Dimensions(outdict)

if __name__ == '__main__':
    a = dimensionsFromString("kg m^-2")

    print a * a