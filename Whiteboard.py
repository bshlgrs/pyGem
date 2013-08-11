# Whiteboard.py
import Tkinter as tk
from Backend import Backend
from GUIEquation import GUIEquation
from math import sqrt
from time import time

class Whiteboard(tk.Canvas, Backend):
    def __init__(self, root, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        Backend.__init__(self)
        self.root = root

        self.tag_bind("Draggable","<ButtonPress-1>",self.onClickPress)
        self.tag_bind("Draggable",
                                "<ButtonRelease-1>",self.onClickRelease)
        self.tag_bind("Draggable","<B1-Motion>",self.handleMotion)
        self.tag_bind("Draggable","<ButtonPress-2>",self.onRightClickPress)

        self.bind("<B2-Motion>",self.handleRightMotion)
        self.bind("<ButtonRelease-2>",self.onRightClickRelease)

        self.textSize = 26

        self.equivalenceLines = []

        self.currentDragLine = None
        self.dragStartVar = None
        self.dragStartCoords = None

    def allTextThings(self):
        return self.equations

    def addGUIEquation(self,lhs,rhs,units):
        self.addEquation(GUIEquation(lhs,rhs,self),units)
        self.equations[-1].draw()

    def onClickPress(self,event):
        for textThing in self.allTextThings():
            textThing.onClickPress(event)

    def onClickRelease(self,event):
        for textThing in self.allTextThings():
            textThing.onClickRelease(event)

    def handleMotion(self,event):
        for textThing in self.allTextThings():
            textThing.handleMotion(event)

    def onRightClickPress(self,event):
        for textThing in self.equations:
            textThing.onRightClickPress(event)

    def onRightClickRelease(self,event):
        for textThing in self.equations:
            textThing.onRightClickRelease(event)
        self.delete(self.currentDragLine)
        self.currentDragLine = None
        self.dragStartCoords = None

    def handleRightMotion(self,event):
        if self.currentDragLine:
            self.delete(self.currentDragLine)
        if not self.dragStartCoords:
            return
        startx, starty = self.dragStartCoords
        self.currentDragLine = self.create_line(startx, starty,
            event.x,event.y, dash=(1,4))

    def increaseTextSize(self):
        self.textSize += 2
        for thing in self.allTextThings():
            thing.draw()

    def decreaseTextSize(self):
        self.textSize -= 2
        for thing in self.allTextThings():
            thing.draw()

    def findVariablePosition(self,var):
        for equation in self.equations:
            if var in equation.getVars():
                return equation.getActualCanvasPositionOfVar(var)

    def findEquationIDOfVariable(self,var):
        for (pos,equation) in enumerate(self.equations):
            if var in equation.getVars():
                return pos

    def addGUIEquivalence(self,var1,var2):
        if self.dimensions[var1] == self.dimensions[var2]:
            self.addEquivalency([var1,var2])

            self.updateEquivalencyLines()
        else:
            print "incompatible dimensions"

    def updateEquivalencyLines(self):
        # This function has more functionality than it strictly needs to
        def drawShrunkLines(start,end,shrink1,shrink2,**kwargs):
            def step(x1,y1,x2,y2,stepSize):
                if (x1,y1)!=(x2,y2):
                    length = sqrt((x1-x2)**2+(y1-y2)**2)
                    ratio = (length+stepSize)/ length
                    return ((x2-x1)/ratio+x1,(y2-y1)/ratio+y1)
                return (x1,y1)

            (x1,y1),(x2,y2) = start, end
            return self.create_line(step(x1,y1,x2,y2,shrink1),
                                    step(x2,y2,x1,y1,shrink2),
                                    **kwargs)

        outlist = []

        for line in self.equivalenceLines:
            self.delete(line)

        self.equivalenceLines = []

        for partition in self.equivalencies:
            for (pos,var1) in enumerate(partition):
                for var2 in partition[pos+1:]:
                    newline = drawShrunkLines(self.findVariablePosition(var1),
                            self.findVariablePosition(var2),16,16,dash=(4,4))
                    self.equivalenceLines.append(newline)
