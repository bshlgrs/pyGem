# utilityFunctions.py
import re
from sympy import S

def numberPrint(number):
    #TODO: Reconsider this:
    return "%4f"%number
    
    if abs(round(number)-number) < 0.00001:
        return "%d"%number
    # if number < 80 and abs(round(number*2)-number*2) < 0.00001:
    #     return "(%d/2)"%(number*2)
    return "%1f"%number

def replaceName(exp,name1,name2):
    return exp.replace(S(name1),S(name2))

def prettyMuchAnInteger(x):
    return abs(x - round(x)) < 0.00001

def numberGuess(number, squareRooting = False):
    if number<0:
        return "-"+numberGuess(-number)
    if prettyMuchAnInteger(number):
        return str(int(round(number)))
    if abs(number-0.5)<0.00001:
        return "1/2"
    # for denominator in range(2,10):
    #   #  print denominator, number*denominator
    #     if prettyMuchAnInteger(number*denominator):
    #         return "%d/%d"%(round(number*denominator),denominator)

    if prettyMuchAnInteger(number**2) and number < 10 and squareRooting:
        return u"sqrt%d"%(round(number**2))
    return "%.3f"%number

def rewriteExpression(instr, squareRooting = False):
    def change(match):
        thing = float(match.group(0))
        return numberGuess(thing, squareRooting)
    return re.sub("[0-9]+[.][0-9]+",change,instr)

def subscript(my_string):
    """
    Unicodifies subscripts, written by Callum Ford.
    """
    final_list = []
    length = len(my_string)
    count = 0
    for char in my_string:
        #Checks if the character is not a number, adds it to the final string with no changes
        if (48 <= ord(char) <= 57) == False:
            final_list += char
        #If the character is a number, checks whether the character before it is a letter and if so converts it to subscript
        elif (48 <= ord(char) <= 57):
            if (97 <= ord(my_string[count-1]) <= 122) or (65 <= ord(my_string[count-1]) <= 90) or (8230 <= ord(final_list[count-1]) <= 8329):
                final_list += unichr(8272 + ord(char))
            else:
                final_list += char
        count += 1

    assert len(final_list) == len(my_string)
    return "".join(final_list)

def unicodify(instr,subscripting=True):

    if subscripting:
        try:
            instr = subscript(instr)
        except Exception:
            pass
            #print "Gah, you should fix the subscripter..."

    instr = instr.replace("sqrt",u"\u221A").replace("**2",u"\u00B2")
    def change(match):

        thing = match.group(0)
      #  print "changing",thing
        if thing=="1/2*":
            return u"\u00BD"
        return thing
    instr = re.sub("[0-9]+/[0-9]+[*]",change,instr)

    instr = instr.replace("+/-",u"\u00B1")
    instr = instr.replace("+-",u"\u00B1")

    def change2(match):
        thing = match.group(0)

    instr = instr.replace("omega",u"\u03C9")

    return instr

def censorUnicode(instr):
    def censorChar(x):
        if ord(x)>127:
            return "?"
        return x
    return "".join(map(censorChar,instr))

def splitStrings(text):
    cleanText= censorUnicode(text)

    def getThingAtTextPosition(position):
        inlist = re.finditer("\w*[a-zA-Z]\w*",cleanText)
        for match in inlist:
            if match.start() <= position < match.end():
                return ("Var",match.group())
        return ("Thing",cleanText[position])
    string1 = []
    string2 = []
    for a in range(len(cleanText)):
        if getThingAtTextPosition(a)[0]=="Var":
            string1.append(text[a])
            string2.append(" ")
        else:
            string1.append(" ")
            string2.append(text[a])
    return ("".join(string1),"".join(string2))

if __name__ == "__main__":
#    print numberGuess(-1.41421356)
    print rewriteExpression("1/2 KE")
