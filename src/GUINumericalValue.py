from Draggable import Draggable
from random import random
from utilityFunctions import unicodify

class GUINumericalValue(Draggable):
    def __init__(self,root,value,sigma=None):
        Draggable.__init__(self,100+150*random(),100+(40*len(root.expressions)*random())%300)

        self.root = root
        self.value = value

        if sigma is not None and abs(sigma) > 0.00001 * value:
            self.valString= "%g+/-%g"%(value,sigma)
        else:
            self.valString = str(value)

        self.sigma = sigma

        self.textID = None

        self.draw()

    def __del__(self):
        if self.textID:
            self.root.delete(self.textID)

    def draw(self):
        if self.textID is None:
            self.textID = self.root.create_text((self.x,self.y),
                text = unicodify(self.valString),
                    fill = "#C00633", tags = "Draggable",
                        font = (self.root.font, self.root.textSize-4, "bold"))

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
