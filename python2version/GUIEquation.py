# GUIEquation.py

from Equation import Equation
from Draggable import Draggable
import random
import re
from utilityFunctions import unicodify, splitStrings, censorUnicode

class GUIEquation(Equation, Draggable):
    def __init__(self,lhs,rhs,root):
        Equation.__init__(self,lhs,rhs)

        self.root = root

        Draggable.__init__(self,200,
                    (200+70*self.getMyEqNo()%int(root.cget("height"))))

        self.varsTextID = None
        self.opsTextID = None

        self.tagString = "".join(chr(ord(x)+17) for x in str(id(self)))

        self.varsString, self.opsString = splitStrings(self.text)

        self.draw()

    def __repr__(self):
        return "GUIEquation %s"%censorUnicode(self.text)

    def __del__(self):
        print "lolololololol"
        if self.varsTextID:
            self.root.delete(self.varsTextID)
            self.root.delete(self.opsTextID)

    def getMyEqNo(self):
        try:
            return self.root.equations.index(self)
        except Exception:
            return len(self.root.equations)

    def draw(self):
        self.varsString, self.opsString = splitStrings(self.text)
        if self.varsTextID is not None:
            self.root.delete(self.varsTextID)
            self.root.delete(self.opsTextID)
        self.varsTextID = self.root.create_text((self.x,self.y),
            text =unicodify(self.varsString),
                 fill = "#066",
                    font = ("Courier", self.root.textSize, "bold"))
        self.opsTextID = self.root.create_text((self.x,self.y),
            text =unicodify(self.opsString), tags = ("Draggable", "Equation",
                self.tagString),
                    font = ("Courier", self.root.textSize, "normal"))


    def onClickPress(self,event):
        if self.root.find_closest(event.x, event.y)[0] == self.opsTextID:
            clickedThing = self.getClickedThing(event)

            if clickedThing[0] == "Thing":
                self.dragX = event.x
                self.dragY = event.y
                self.beingDragged = True
                self.root.currentAction = "Drag"
            elif clickedThing[0] == "Var":
                self.beingEqualled = True
                self.root.write("%s :: "%clickedThing[1]
                             + self.root.dimensions[clickedThing[1]])
                self.root.clickData["variable"] = clickedThing[1]
                self.root.clickData["coords"] = (
                        self.getActualCanvasPositionOfVar(
                                                clickedThing[1]))
                self.root.currentAction = "DragFromEquationVar"

    def onRightClickPress(self,event):
        if self.root.find_closest(event.x, event.y)[0] == self.opsTextID:
            clickedThing = self.getClickedThing(event)

            if clickedThing[0] == "Thing":
                self.root.clickData["variable"] = None
                self.root.clickData["clickedObject"] = self
                return (self,None)
            elif clickedThing[0] == "Var":
                self.root.clickData["variable"] = clickedThing[1]
                self.root.clickData["clickedObject"] = self
                return (self, clickedThing[1])
        return None


    def onClickRelease(self,event):
        if self.root.currentAction == "Drag":
            if self.beingDragged:
                self.beingDragged = False
                if self.y<0:
                    self.root.deleteEquation(self)
                    return

        elif self.root.currentAction == "DragFromEquationVar":
            if self.beingEqualled:
                self.beingEqualled = False

            if (self.root.find_closest(event.x, event.y)[0] == self.opsTextID):
                clickedThing=self.getClickedThing(event)

                if clickedThing and clickedThing[0] == "Var":
                    self.root.addGUIEquivalence(
                            self.root.clickData["variable"],
                                                    clickedThing[1])

        elif self.root.currentAction == "DragFromExp":
            if (self.root.find_closest(event.x, event.y)[0] == self.opsTextID):
                self.root.rewriteUsingEquation(
                            self.root.dragStartExpressionVar,
                                            self.root.clickData["variable"], self)

    def onDoubleClick(self,event):
        if self.root.find_closest(event.x, event.y)[0] == self.opsTextID:
            clickedThing = self.getClickedThing(event)

            if clickedThing[0] == "Var":
                self.root.findGUIExpression(clickedThing[1],self)

    def handleMotion(self,event):
        if self.beingDragged:
            delta_x = event.x - self.dragX
            delta_y = event.y - self.dragY
            self.root.move(self.varsTextID, delta_x, delta_y)
            self.root.move(self.opsTextID, delta_x, delta_y)
            self.dragX = event.x
            self.dragY = event.y
            self.x += delta_x
            self.y += delta_y
            self.root.updateEquivalencyLines()

    def getThingAtTextPosition(self,position):
        inlist = re.finditer("\w*[a-zA-Z]\w*",self.text)
        for match in inlist:
            if match.start() <= position < match.end():
                return ("Var",match.group())
        try:
            return ("Thing",self.text[position])
        except IndexError:
            return None

    def getTextPositionOfVar(self,var):
        inlist = re.finditer("\w*[a-zA-Z]\w*",self.text)
        return [x.span() for x in inlist if x.group()==var][0]

    def getAveragePositionOfVar(self,var):
        (x,y) = self.getTextPositionOfVar(var)
        return float(x+y)/2.0

    def getActualCanvasPositionOfVar(self,var):
        bBox = self.root.bbox(self.tagString)
        return ((bBox[2]-bBox[0])*self.getAveragePositionOfVar(var)
                    /len(self.text) + bBox[0],(bBox[1]+bBox[3])/2.0)

    def getClickedThing(self,event):
        a = self.root.bbox(self.tagString)
        size = float((a[2]-a[0]))/len(self.text)
        textPos = int((event.x-a[0])/size)

        return self.getThingAtTextPosition(textPos)

def main():
    pass

if __name__ == '__main__':
    main()
