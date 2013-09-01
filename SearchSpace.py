import Tkinter as tk
import EquationParser
from utilityFunctions import rewriteExpression, unicodify

class SearchSpace(tk.Canvas):
    def __init__(self, root, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.root = root
        self.searchBarWidget = self.root.searchBarWidget
        self.searchTextVar = self.root.searchTextVar

        self.searchBarWidget.bind("<Key>",self.key)
        self.searchBarWidget.bind("<Return>",self.clear)

        self.library = EquationParser.loadEquations()

        self.text = None
        self.matches = None

        self.bind("<ButtonPress-1>",self.addEquation)

    def key(self,event):
        def similarity(list1, list2):
            return all(any(x in y for y in list2) for x in list1)

        # This bit is surely hackier than strictly necessary...
        if event.char.lower() in "qwertyuiopasdfghjklzxcvbnm":
            string = self.searchTextVar.get() + event.char
        elif event.char == '\x7f':
            string = self.searchTextVar.get()[:-1]
        else:
            string = self.searchTextVar.get()

        mylist = string.split()

        if self.text:
            self.delete(self.text)

        if mylist == []:
            return

        self.matches = [x for x in self.library if similarity(mylist,x[4])]

        matchesText = "\n\n".join(unicodify(rewriteExpression(x[0]))
                                                 for x in self.matches)

        self.text = self.create_text(10,10,text = matchesText,
                anchor="nw", font=("Courier", 18, "bold"),fill="#033",
                            tags="search")

        if event.char == '\r':
            if len(self.matches) > 0:
                print self.matches
                equation = self.matches[0]
                print equation
                self.root.whiteboard.addGUIEquation(equation[1],equation[2],
                                                equation[3])
            else:
                lhs,rhs = string.split('=')
                self.root.whiteboard.addGUIEquation(lhs,rhs,{})


    def addEquation(self,event):
        if not self.matches:
            # If you want to not have arbitrary equations added, just make this
            # return.
            return

        bBox = self.bbox("search")
        numberOfLines = len(self.matches) * 2 - 1
        linePressed = int(((event.y-bBox[1])*float(numberOfLines))/
                            (bBox[3] - bBox[1]))

        if linePressed%2==0 and linePressed <= len(self.matches)*2:
            equation = self.matches[linePressed/2]
            print equation
            self.root.whiteboard.addGUIEquation(equation[1],equation[2],
                                            equation[3])

    def clear(self,event):
        self.key(event)
        self.searchTextVar.set("")
