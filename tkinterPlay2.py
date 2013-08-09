import Tkinter as tk
from Tkinter import W, E, N, S
from ttk import Button

import sympy

class SampleApp(tk.Tk):
    '''Illustrate how to drag items on a Tkinter canvas'''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # create a canvas
        self.whiteboard = tk.Canvas(width=400, height=400, bg = "grey")
        self.whiteboard.grid(row=0,column=0,rowspan=2,columnspan=2,
                    sticky=W+E+N+S)

        self.searchSection = tk.Canvas(width=200,height=300,bg = "#eee")
        self.searchSection.grid(row=1,column=2,sticky=W+E+N+S)

        # this data is used to keep track of an
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        self._objects = []
        self._lines = {}

        # create a couple movable objects
        self._create_token((100, 100), "KE - (1/2)*m*v**2+x")
        self._create_token((300, 300), "black")


        # add bindings for clicking, dragging and releasing over
        # any object with the "token" tag
        self.canvas.tag_bind("token", "<ButtonPress-1>", self.OnTokenButtonPress)
        self.canvas.tag_bind("token", "<ButtonRelease-1>", self.OnTokenButtonRelease)
        self.canvas.tag_bind("token", "<B1-Motion>", self.OnTokenMotion)

        self.canvas.tag_bind("token", "<ButtonPress-2>", self.OnTokenRightButtonPress)

        closeButton = Button(self, text="Close",command = self.quit)
        closeButton.grid(row=2,column=2)

        self.newColor = tk.StringVar()

        entryWidget = tk.Entry(self, textvariable = self.newColor)
        entryWidget.grid(row=2,column=0)

        entryWidget.bind("<Return>",self.addDraggableThing)

        self.grid_columnconfigure(1,weight=3)
        self.grid_columnconfigure(2,weight=1)
        self.grid_rowconfigure(1,weight=1)

    def addDraggableThing(self,blah):
        self._create_token((100,100), self.newColor.get())

    def _create_line(self,a,b):
        line = self.canvas.create_line((self.canvas.coords(a),self.canvas.coords(b)))
        if a < b:
            self._lines[(a,b)] = line
        else:
            self._lines[(b,a)] = line

    def _create_token(self, coord, text):
        '''Create a token at the given coordinate with the given text'''
        (x,y) = coord

        myid = self.canvas.create_text((x,y),
                text=sympy.pretty(sympy.S(text)), tags="token", font=("Courier",30))

        for obj in self._objects:
            self._create_line(myid,obj)

        self._objects.append(myid)


    def OnTokenButtonPress(self, event):
        '''Being drag of an object'''
        # record the item and its location

        print self._objects, self._lines

        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def OnTokenRightButtonPress(self, event):
        '''Delete an object'''
        objID = self.canvas.find_closest(event.x, event.y)[0]
        self.canvas.delete(objID)

        toDelete = []

        for line in self._lines:
            if objID in line:
                self.canvas.delete(self._lines[line])
                toDelete.append(line)

        for line in toDelete:
            del self._lines[line]



    def OnTokenButtonRelease(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def OnTokenMotion(self, event):
        '''Handle dragging of an object'''

        currentItem=self._drag_data["item"]

        # compute how much this object has moved

        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        for other in self._objects:
            if other != currentItem:
                propername = (min(other,currentItem),max(other,currentItem))
                self.canvas.delete(self._lines[propername])
                self._create_line(other,currentItem)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
