# GUIEquation.py

from Equation import Equation
import random
import re

def stringify(num):
    return "".join(chr(ord(x)+17) for x in str(num))

class GUIEquation(Equation):
    def __init__(self,lhs,rhs,root):
        Equation.__init__(self,lhs,rhs)

        self.root = root

        self.x = 200+random.random()*100
        self.y = 200+random.random()*100

        self.dragX = 0
        self.dragY = 0
        self.beingDragged = False

        self.varsTextID = None
        self.opsTextID = None

        self.tagString = stringify(id(self))

        self.varsString, self.opsString = self.splitStrings()

        self.draw()


    def __del__(self):
        if self.varsTextID:
            self.root.delete(self.varsTextID)
            self.root.delete(self.opsTextID)

    def draw(self):
        if self.varsTextID is not None:
            self.root.delete(self.varsTextID)
            self.root.delete(self.opsTextID)
        self.varsTextID = self.root.create_text((self.x,self.y),
            text =self.varsString,
                 fill = "brown",
                    font = ("Courier", self.root.textSize, "bold"))
        self.opsTextID = self.root.create_text((self.x,self.y),
            text =self.opsString, tags = ("Draggable", self.tagString),
                    font = ("Courier", self.root.textSize, "bold"))


    def onClickPress(self,event):
        if self.root.find_closest(event.x, event.y)[0] == self.opsTextID:
            a = self.root.bbox(self.tagString)
            size = float((a[2]-a[0]))/len(self.text)
            textPos = int((event.x-a[0])/size)

            if self.getThingAtTextPosition(textPos)[0] == "Thing":
                self.dragX = event.x
                self.dragY = event.y
                self.beingDragged = True
             #   print (self.dragX-self.x) / self.root.textSize * 1.4

    def onClickRelease(self,event):
        self.beingDragged = False

    def handleMotion(self,event):
        if self.beingDragged:
            delta_x = event.x - self.dragX
            delta_y = event.y - self.dragY
            self.root.move(self.varsTextID, delta_x, delta_y)
            self.root.move(self.opsTextID, delta_x, delta_y)
            self.dragX = event.x
            self.dragY = event.y
            self.x+= delta_x
            self.y+= delta_y

    def getThingAtTextPosition(self,position):
        inlist = re.finditer("\w*[a-zA-Z]\w*",self.text)
        for match in inlist:
            if match.start() <= position < match.end():
                return ("Var",match.group())
        return ("Thing",self.text[position])

    def splitStrings(self):
        string1 = []
        string2 = []
        for a in range(len(self.text)):
            if self.getThingAtTextPosition(a)[0]=="Var":
                string1.append(self.text[a])
                string2.append(" ")
            else:
                string1.append(" ")
                string2.append(self.text[a])
        return ("".join(string1),"".join(string2))

    def getTextPositionsOfVar(self,var):
        inlist = re.finditer("\w*[a-zA-Z]\w*",self.text)
        return [x.span() for x in inlist if x.group()==var]

    def getAveragePositionsOfVar(self,var):
        return [float(x+y)/2 for (x,y) in self.getPositionsOfVar(var)]


def main():
    a = GUIEquation("Ek","0.5*m*v**2",None)
    print a.getThingAtTextPosition(1)
    print a.getPositionsOfVar("Ek")

if __name__ == '__main__':
    main()
