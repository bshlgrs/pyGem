import Tkinter as tk
import EquationParser

class SearchSpace(tk.Canvas):
    def __init__(self, root, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.root = root
        self.searchBarWidget = self.root.searchBarWidget
        self.searchTextVar = self.root.searchTextVar

        self.searchBarWidget.bind("<Key>",self.key)

        self.library = EquationParser.loadEquations()

        self.text = None

        self.bind("<ButtonPress-1>",self.addEquation)

    def key(self,event):
        def similarity(list1, list2):
            return all(any(x in y for y in list2) for x in list1)

        string = self.searchTextVar.get()
        mylist = string.split()

        if self.text:
            self.delete(self.text)

        if mylist == []:
            return

        self.matches = [x for x in self.library if similarity(mylist,x[4])]

        matchesText = "\n\n".join(x[0] for x in self.matches)

        self.text = self.create_text(10,10,text = matchesText,
            anchor="nw", font=("Courier", 18, "bold"),fill="#033",tags="search")

    def addEquation(self,event):
        bBox = self.bbox("search")
        numberOfLines = len(self.matches) * 2 - 1
        linePressed = int(((event.y-bBox[1])*float(numberOfLines))/
                            (bBox[3] - bBox[1]))

        if linePressed%2==0:
            equation = self.matches[linePressed/2]
            self.root.whiteboard.addGUIEquation(equation[1],equation[2],
                                            equation[3])
