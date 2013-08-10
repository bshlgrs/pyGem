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

    def key(self,event):
        def similarity(list1, list2):
            return all(any(x in y for y in list2) for x in list1)

        string = self.searchTextVar.get()
        mylist = string.split()

        if self.text:
            self.delete(self.text)

        if mylist == []:
            return

        matches = [x[0] for x in self.library if similarity(mylist,x[2])]
        self.text = self.create_text(10,10,text = "\n\n".join(matches),
            anchor="nw", font=("Courier", 18, "bold"))

        print "\n\n\n"+"\n".join(matches)

