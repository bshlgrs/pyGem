from Draggable import Draggable

class GUINumericalValue(Draggable):
    def __init__(self,root,value,uncertainty=None):
        Draggable.__init__(self,300,100+(40*len(root.expressions))%300)
        if uncertainty is not None:
            self.valstring= "%f +/- %f"%(value,uncertainty)
        else:
            self.valstring = "%f"%value

        self.textID = None

        self.draw()

    def draw(self):
        if self.textID is None:
            self.root.create_text((self.x,self.y),
                text = varsString,
                    fill = "#CC6633", tags = "Draggable",
                        font = ("Courier", self.root.textSize-2, "bold"))

    def onClickPress(self,event):
        if (self.root.find_closest(event.x, event.y)[0]
                            == self.textID):
            self.root.currentAction = "DragFromExp"
            self.root.clickData["variable"] = clickedThing[1]
            self.root.dragStartExpressionVar = self.var
            self.root.clickData["coords"] = \
                        self.getActualCanvasPositionOfVar(clickedThing[1])

