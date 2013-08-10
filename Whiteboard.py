# Whiteboard.py
import Tkinter as tk
from Backend import Backend
from GUIEquation import GUIEquation

class Whiteboard(tk.Canvas, Backend):
    def __init__(self, root, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        Backend.__init__(self)
        self.root = root

        self.tag_bind("Draggable","<ButtonPress-1>",self.onClickPress)
        self.tag_bind("Draggable",
                                "<ButtonRelease-1>",self.onClickRelease)
        self.tag_bind("Draggable","<B1-Motion>",self.handleMotion)

        self.bind("<Shift-Up>",self.increaseTextSize)

        self.textSize = 26

        self.addGUIEquation("EK","0.5*m*v**2",{})
        self.addGUIEquation("EP","m*g*h",{})
        self.addGUIEquation("f","m*a",{})

    def allTextThings(self):
        return self.equations

    def addGUIEquation(self,lhs,rhs,units):
        self.addEquation(GUIEquation(lhs,rhs,self),units)
        self.equations[-1].draw()

    def onClickPress(self,event):
        for equation in self.equations:
            equation.onClickPress(event)

    def onClickRelease(self,event):
        for equation in self.equations:
            equation.onClickRelease(event)

    def handleMotion(self,event):
        for equation in self.equations:
            equation.handleMotion(event)

    def increaseTextSize(self):
        self.textSize +=2
        for thing in self.allTextThings():
            thing.draw()

    def decreaseTextSize(self):
        self.textSize -=2
        for thing in self.allTextThings():
            thing.draw()
