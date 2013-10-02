from Draggable import Draggable
from random import random

class GUINumericalValue(Draggable):
    def __init__(self,root,value,uncertainty=None):
        Draggable.__init__(self,100+150*random(),100+(40*len(root.expressions)*random())%300)

        self.root = root
        self.value = value

        if uncertainty is not None:
            self.valString= "%s +/- %s"%(str(value),str(uncertainty))
        else:
            self.valString = str(value)

        self.textID = None

        self.draw()

    def __del__(self):
        if self.varsTextID:
            self.root.delete(self.textID)

    def draw(self):
        if self.textID is None:
            self.textID = self.root.create_text((self.x,self.y),
                text = self.valString,
                    fill = "#C00633", tags = "Draggable",
                        font = ("Courier", self.root.textSize-2, "bold"))

    def onClickPress(self,event):
        if (self.root.find_closest(event.x, event.y)[0]
                            == self.textID):
            self.root.currentAction = "Drag"
            self.dragX = event.x
            self.dragY = event.y
            self.beingDragged = True

    def onClickRelease(self,event):
        self.beingDragged = False

        if (self.root.find_closest(event.x, event.y)[0] == self.textID):
            if self.root.clickData["variable"]:
                self.root.addNumericalValueToGUI(self.root.clickData["variable"],self)

    

    def handleMotion(self,event):
        if self.beingDragged:
            delta_x = event.x - self.dragX
            delta_y = event.y - self.dragY
            self.root.move(self.textID, delta_x, delta_y)
            self.dragX = event.x
            self.dragY = event.y
            self.x += delta_x
            self.y += delta_y
            self.root.updateEquivalencyLines()

    def getActualCanvasPosition(self):
        bBox = self.root.bbox(self.textID)
        return (bBox[0]+bBox[2])/2, (bBox[1]+bBox[3])/2
