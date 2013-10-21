import Tkinter as tk
import EquationParser
from utilityFunctions import rewriteExpression, unicodify
import time

class SearchSpace(tk.Canvas):
    """
    The search space is the bar where you write keywords of equations, and
    numbers, and so on, and where suggested equations are displayed. This module
    implements its behaviour.
    """
    def __init__(self, root, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.root = root
        self.searchBarWidget = self.root.searchBarWidget
        self.searchTextVar = self.root.searchTextVar

        self.searchBarWidget.bind("<Key>", self.key)
        self.searchBarWidget.bind("<Return>", self.clear)

        self.library = EquationParser.loadEquations()

        self.text = None
        self.matches = None

        self.lastClickTime = time.time()

        self.bind("<ButtonPress-1>", self.onClick)

    def key(self, event):
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

        self.matches = [x for x in self.library if similarity(mylist, x[4])]

        matchesText  = "\n\n".join(unicodify(rewriteExpression(x[0]))
                                                 for x in self.matches)

        self.text = self.create_text(10, 10, text = matchesText,
                anchor="nw", font=(self.root.whiteboard.font, 24, "bold"), fill="#033",
                            tags="search")

        if event.char == '\r':
            if len(self.matches) > 0: # If they searched for something
                equation = self.matches[0]
                self.root.whiteboard.addGUIEquation(equation[1], equation[2],
                                                equation[3])
            else:
                try: # Maybe it's a number
                    val = float(string)
                    self.root.whiteboard.createNumber(val)
                    return
                except ValueError:
                    pass

                try: # Maybe it's a number with uncertainty
                    val, sigma = map(float,string.split("+-"))
                    self.root.whiteboard.createNumber(val,sigma)
                    return
                except Exception as e:
                    pass

                try: # Maybe it's a custom equation
                    lhs, rhs = string.split('=')
                    print "rptif", lhs,rhs
                    self.root.whiteboard.addGUIEquation(lhs, rhs, {})
                except Exception as e:
                    print e
                    self.root.whiteboard.write("Equation could not be parsed.")

    def onClick(self, event):
        if not self.matches:
            return

        if time.time() - self.lastClickTime < 0.4:
            return

        self.lastClickTime = time.time()

        bBox = self.bbox("search")
        numberOfLines = len(self.matches) * 2 - 1
        linePressed = int(((event.y-bBox[1])*float(numberOfLines))/
                            (bBox[3] - bBox[1]))

        if linePressed%2==0 and linePressed <= len(self.matches)*2:
            equation = self.matches[linePressed/2]
            print equation
            self.root.whiteboard.addGUIEquation(equation[1], equation[2],
                                            equation[3])

    def clear(self, event):
        self.key(event)
        self.searchTextVar.set("")
