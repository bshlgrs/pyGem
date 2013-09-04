import re
from utilityFunctions import rewriteExpression, unicodify, splitStrings
from GUIEquation import GUIEquation

class GUIExpression(GUIEquation):
    def __init__(self,var,root):
        self.var = var
        self.root = root
        self.x,self.y = 300,100+(40*len(root.expressions))%300

        self.varsTextID = None
        self.opsTextID = None

        self.tagString = "".join(chr(ord(x)+17) for x in str(id(self)))

        self.draw()

        self.dragX = 0
        self.dragY = 0
        self.beingDragged = False

    def __del__(self):
        try:
            del self.root.expressions[self.var]
        except KeyError:
            pass
        if self.varsTextID:
            self.root.delete(self.varsTextID)
            self.root.delete(self.opsTextID)

    def draw(self):
        if self.varsTextID:
            self.root.delete(self.varsTextID)
            self.root.delete(self.opsTextID)

        self.text = self.var+"="+rewriteExpression(self.expString())
        self.text = unicodify(self.text,False)

        varsString, opsString = splitStrings(self.text)

        self.varsTextID = self.root.create_text((self.x,self.y),
            text = varsString,
                fill = "#CC6633", tags = "Draggable",
                    font = ("Courier", self.root.textSize-2, "bold"))

        self.opsTextID = self.root.create_text((self.x,self.y),
            text = opsString,
                fill = "#000", tags = ("Draggable",self.tagString),
                    font = ("Courier", self.root.textSize-2, "normal"))

    def expString(self):
        exps = self.root.expressions[self.var]
        if len(exps) == 1:
            return exps[0].__repr__()
        if len(exps) == 2 and exps[0]+exps[1]==0:
            a = exps[0].__repr__()
            b = exps[1].__repr__()
            if len(a)>len(b):
                return "\u00B1"+b
            return "\u00B1("+a+")"
        return exps.__repr__()

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
                self.root.dragStartVar = clickedThing[1]
                self.root.dragStartExpressionVar = self.var
                self.root.dragStartCoords = \
                            self.getActualCanvasPositionOfVar(clickedThing[1])

            else:
                raise Exception("This shouldn't happen!")

    def onRightClickPress(self,event):
        return

    def onClickRelease(self,event):
        self.beingDragged = False

        # if self.root.currentAction = "DragFromExp":
        #     self.root.s


        if self.y<0:
            self.__del__()

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
