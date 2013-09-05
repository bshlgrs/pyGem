# Whiteboard.py


import Tkinter as tk
from Backend import Backend
from GUIEquation import GUIEquation
from GUIExpression import GUIExpression
from math import sqrt
from time import time

class Whiteboard(tk.Canvas, Backend):
    def __init__(self, root, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        Backend.__init__(self)
        self.root = root

        self.tag_bind("Draggable","<ButtonPress-1>",self.onClickPress)

        self.tag_bind("Draggable","<ButtonPress-2>",self.onRightClick)

        self.tag_bind("Draggable",
                                "<ButtonRelease-1>",self.onClickRelease)
        self.tag_bind("Draggable","<B1-Motion>",self.handleMotion)

        self.tag_bind("Draggable","<Double-Button-1>",self.onDoubleClick)

        self.textSize = 26

        self.equivalenceLines = []

        self.guiExpressions = {}

        # currentAction can be None, "Drag", "Equate", "DragFromExp"
        self.currentAction = None

        self.currentDragLine = None
        # self.clickData["variable"] = None
        # self.dragStartExpressionVar = None
        # self.clickData["coords"] = None

        self.clickData = {"clickedObject" : None, # Expression, Equation, etc
                            "variable" : None, # or "EK" or whatever
                            "coords" : None
                            }

        # create a menu
        self.popup = tk.Menu(root, tearoff=0)
        self.popup.add_command(label="Find expression",
                command = self.findGUIExpressionRightClick)
        self.popup.add_command(label="Add numerical value")
        self.popup.add_separator()
        self.popup.add_command(label="Delete equation",
                    command= self.deleteEquation)

    def allTextThings(self):
        return self.equations + self.guiExpressions.values()

    def addGUIEquation(self,lhs,rhs,units):
        self.addEquation(GUIEquation(lhs,rhs,self),units)
        self.equations[-1].draw()

    def onClickPress(self,event):
        for textThing in self.allTextThings():
            textThing.onClickPress(event)

    def onClickRelease(self,event):
        # We need to delete the drag line before we do our loop
        if self.currentAction == "Drag":
            for textThing in self.allTextThings():
                textThing.onClickRelease(event)


        if self.currentAction in ["DragFromExp","Equate"]:
            if self.currentDragLine:
                self.delete(self.currentDragLine)

            for textThing in self.allTextThings():
                textThing.onClickRelease(event)

            self.currentDragLine = None
            self.clickData["variable"] = None
            self.clickData["coords"] = None
            self.dragStartExpressionVar = None

    def handleMotion(self,event):
        for textThing in self.allTextThings():
            textThing.handleMotion(event)
        if self.currentDragLine:
            self.delete(self.currentDragLine)
        if not self.clickData["coords"]:
            return
        startx, starty = self.clickData["coords"]
        self.currentDragLine = self.create_line(startx, starty,
            event.x,event.y, dash=(1,4))

    def onRightClick(self,event):
        clickedEquation, clickedThing = None, None
        for textThing in self.allTextThings():
            a = textThing.onRightClickPress(event)
            if a:
                clickedEquation, clickedThing = a

        self.clickData["variable"] = clickedThing

        if clickedThing:
            # display the popup menu
            try:
                self.popup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.popup.grab_release()

    def onDoubleClick(self,event):
        for thing in self.allTextThings():
            thing.onDoubleClick(event)

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
        if var1 is None or var2 is None:
            return
        if self.varDimensionsAgree(var1,var2):
            self.addEquivalency([var1,var2])

            self.updateEquivalencyLines()
            for a in self.guiExpressions.values():
                a.draw()
        else:
            self.write("Incompatible dimensions")

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

    def findGUIExpression(self, var, equation):
        self.findExpression(var,equation)
        self.guiExpressions[var] = GUIExpression(var,self)

    def findGUIExpressionRightClick(self):
        self.findGUIExpression(self.clickData["variable"],
                        self.findEquationWithVar(self.clickData["variable"]))

    def rewriteUsingEquation(self,var,varToRemove,equation):
        Backend.rewriteUsingEquation(self,var,varToRemove,equation)
        self.guiExpressions[var].draw()

    def rewriteUsingExpression(self,var,varToRemove,varToUse):
        Backend.rewriteUsingExpression(self,var,varToRemove,varToUse)
        self.guiExpressions[var].draw()

    def deleteEquation(self,eqToDelete = None):
        print "deleting"

        if eqToDelete is None:
            eqToDelete = self.equations[self.findEquationIDOfVariable(
                                self.clickData["variable"])]
        print eqToDelete
        self.removeEquation(eqToDelete)
        del eqToDelete

        self.updateEquivalencyLines()

    def deleteExpression(self,expToDelete):
        del self.guiExpressions[expToDelete.var]

    def write(self,*args):
        box = self.root.infoBox
        box.delete('1.0','end')
        box.insert('1.0'," ".join(str(x) for x in args))
