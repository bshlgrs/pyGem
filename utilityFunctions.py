# utilityFunctions.py
import re
from sympy import S

def numberPrint(number):
    if abs(round(number)-number) < 0.00001:
        return "%d"%number
    if abs(round(number*2)-number*2) < 0.00001:
        return "(%d/2)"%(number*2)
    return "%1f"%number

def replaceName(exp,name1,name2):
    return exp.replace(S(name1),S(name2))

def prettyMuchAnInteger(x):
    return abs(x - round(x)) < 0.00001

def numberGuess(number):
    if number<0:
        return "-"+numberGuess(-number)
    if prettyMuchAnInteger(number):
        return str(int(round(number)))
    for denominator in range(2,10):
      #  print denominator, number*denominator
        if prettyMuchAnInteger(number*denominator):
            return "%d/%d"%(round(number*denominator),denominator)

    if prettyMuchAnInteger(number**2):
        return u"sqrt(%d)"%(round(number**2))
    return str(number)

def rewriteExpression(instr):
    def change(match):
        thing = float(match.group(0))
        return numberGuess(thing)
    return re.sub("[0-9]+[.][0-9]+",change,instr)

def unicodify(instr):
    instr = instr.replace("sqrt",u"\u221A").replace("**2",u"\u00B2")
    def change(match):
        thing = match.group(0)
        if thing=="1/2*":
            return u"\u00BD"
        return thing
    return re.sub("[0-9]+/[0-9]+[*]",change,instr)


if __name__ == "__main__":
#    print numberGuess(-1.41421356)
    print rewriteExpression("1/2 KE")
