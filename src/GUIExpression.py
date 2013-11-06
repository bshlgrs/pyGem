import re
from utilityFunctions import rewriteExpression, unicodify, splitStrings
from GUIEquation import GUIEquation
from Draggable import Draggable

class GUIExpression(GUIEquation,Draggable):
    def __init__(self,var,root,pos=None):
        self.var = var
        self.root = root
        if pos:
            Draggable.__init__(self,pos[0],pos[1])
        else:
            Draggable.__init__(self,300,100+(40*len(root.expressions))%300)

        self.varsTextID = None
        self.opsTextID = None

        self.tagString = "".join(chr(ord(x)+17) for x in str(id(self)))

        self.draw()

    def __del__(self):
        if self.varsTextID:
            self.root.delete(self.varsTextID)
            self.root.delete(self.opsTextID)

    def draw(self):
        if self.varsTextID:
            self.root.delete(self.varsTextID)
            self.root.delete(self.opsTextID)

        self.text = self.var+"="+self.expString()
        self.text = unicodify(self.text,False)

        varsString, opsString = splitStrings(self.text)

        self.varsTextID = self.root.create_text((self.x,self.y),
            text = varsString,
                fill = "#CC6633", tags = "Draggable",
                    font = (self.root.font, self.root.textSize-2, "bold"))

        self.opsTextID = self.root.create_text((self.x,self.y),
            text = opsString,
                fill = "#000", tags = ("Draggable",self.tagString),
                    font = (self.root.font, self.root.textSize-2, "normal"))

    def expString(self):
        expString1 = self.makeString(self.root.expressions[self.var])
        numExpsString = self.makeString(self.root.getNumericalExpressions(self.var))
        if expString1 == numExpsString:
            return rewriteExpression(expString1,True)
        else:
            return "%s=%s"%(rewriteExpression(expString1,True),
                    rewriteExpression(numExpsString))


    def makeString(self,inlist):
        if len(inlist) == 1:
            return str(inlist[0])

        return inlist.__repr__()

    def onClickPress(self,event):
        if (self.root.find_closest(event.x, event.y)[0]
                        == self.opsTextID):
            clickedThing = self.getClickedThing(event)
            if clickedThing is None:
                return
            elif clickedThing[0]=="Thing":
                self.dragX = event.x
                self.dragY = event.y
                self.beingDragged = True
                self.root.currentAction = "Drag"
            elif clickedThing[0]=="Var":
                self.root.currentAction = "DragFromExp"
                self.root.clickData["variable"] = clickedThing[1]
                self.root.dragStartExpressionVar = self.var
                self.root.clickData["coords"] = \
                            self.getActualCanvasPositionOfVar(clickedThing[1])

            else:
                raise Exception("This shouldn't happen!")

    def onRightClickPress(self,event):
        return

    def onClickRelease(self,event):
        self.beingDragged = False

        if self.root.currentAction == "DragFromExp":
            if (self.root.find_closest(event.x, event.y)[0] == self.opsTextID) \
                            and self.root.dragStartExpressionVar != self.var:
                self.root.rewriteUsingExpression(
                            self.root.dragStartExpressionVar,
                                            self.root.dragStartVar, self.var)

        if self.y<0:
            self.root.deleteExpression(self)

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

    def onDoubleClick(self,event):
        if (self.root.find_closest(event.x, event.y)[0]
                        == self.opsTextID):
            clickedThing = self.getClickedThing(event)

            if clickedThing[0] != "Thing":
                if clickedThing[1]==self.var:
                    self.root.findExpression(self.var)
                else:
                    self.root.rotateVariableInExpression(self.var,
                                                            clickedThing[1])
                self.draw()
