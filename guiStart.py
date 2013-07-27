Timport Tkinter as tk
from Tkinter import W, E, N, S
from ttk import Button 

class SampleApp(tk.Tk):
    '''Illustrate how to drag items on a Tkinter canvas'''

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # create a canvas
        self.canvas = tk.Canvas(width=400, height=400, bg = "grey")
        self.canvas.grid(row=0,column=0,rowspan=2,columnspan=2,sticky=W+E+N+S)

        self.otherCanvas = tk.Canvas(width=200,height=300,bg = "#eee")
        self.otherCanvas.grid(row=1,column=2,sticky=W+E+N+S)

        # this data is used to keep track of an 
        # item being dragged
        self._drag_data = {"x": 0, "y": 0, "item": None}

        # create a couple movable objects
        self._create_token((100, 100), "blue")
        self._create_token((200, 100), "black")

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
        closeButton = Button(self, text="Add new thing",command = self.addDraggableThing)
        closeButton.grid(row=2,column=1)

        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)

    def addDraggableThing(self):
        self._create_token((100,100), self.newColor.get())

    def _create_token(self, coord, color):
        '''Create a token at the given coordinate in the given color'''
        (x,y) = coord
        self.canvas.create_oval(x-25, y-25, x+25, y+25, 
                                outline=color, fill=color, tags="token")

    def OnTokenButtonPress(self, event):
        '''Being drag of an object'''
        # record the item and its location
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def OnTokenRightButtonPress(self, event):
        '''Delete an object'''
        self.canvas.delete(self.canvas.find_closest(event.x, event.y)[0])


    def OnTokenButtonRelease(self, event):
        '''End drag of an object'''
        # reset the drag information
        self._drag_data["item"] = None
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def OnTokenMotion(self, event):
        '''Handle dragging of an object'''
        # compute how much this object has moved
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # move the object the appropriate amount
        self.canvas.move(self._drag_data["item"], delta_x, delta_y)
        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()