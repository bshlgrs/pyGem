# GUIEquation.py

from Equation import Equation
import random

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

        self.textID = None

        self.draw()


    def __del__(self):
        self.root.delete(self.textID)

    def draw(self):
        if self.textID is not None:
            self.root.delete(self.textID)
        self.textID = self.root.create_text((self.x,self.y),text =self.text,
            tags = "Draggable", font = ("Arial", self.root.textSize, "bold"))


    def onClickPress(self,event):
        if self.root.find_closest(event.x, event.y)[0] == self.textID:
            self.dragX = event.x
            self.dragY = event.y
            self.beingDragged = True
            print self.text

    def onClickRelease(self,event):
        self.beingDragged = False

    def handleMotion(self,event):
        if self.beingDragged:
            delta_x = event.x - self.dragX
            delta_y = event.y - self.dragY
            self.root.move(self.textID, delta_x, delta_y)
            self.dragX = event.x
            self.dragY = event.y
            self.x+= delta_x
            self.y+= delta_y
