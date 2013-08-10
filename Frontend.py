# Frontend.py
import Tkinter as tk
from Backend import Backend
from Whiteboard import Whiteboard
from SearchSpace import SearchSpace

from Tkinter import N, E, W, S
from ttk import Button

class Frontend(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.wm_title("Graphical equation manipulator")

        self.whiteboard = Whiteboard(self,width=600, height=600, bg = "white",
                            bd=1, relief='raised')
        self.whiteboard.grid(row=0,column=0,rowspan=5,columnspan=1,
                                sticky=W+E+N+S)

        self.searchLabel = tk.Label(self,text="Search for equations:")
        self.searchLabel.grid(row=0,column=1)

        self.searchTextVar = tk.StringVar()
        self.searchBarWidget = tk.Entry(self,textvariable = self.searchTextVar)
        self.searchBarWidget.grid(row=1,column=1)

        self.searchSpace = SearchSpace(self,width=250,height=300,bg = "#eee",
                    bd=1, relief='raised')
        self.searchSpace.grid(row=2,column=1,sticky=W+E+N+S)

        self.infoLabel = tk.Label(self,text="Info:")
        self.infoLabel.grid(row=3,column=1)

        self.infoBox = tk.Text(self,width=5,height=5,bd=1,
                relief = 'raised',bg = "#eee",
                        font = ("Courier", 20, "normal"))
        self.infoBox.grid(row=4,column=1, sticky=W+E+N+S)

        self.grid_columnconfigure(0,weight=3)
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure(1,weight=0)
        self.grid_rowconfigure(2,weight=1)
        self.grid_rowconfigure(3,weight=0)
        self.grid_rowconfigure(4,weight=1)

        menubar = tk.Menu(self)
        self.config(menu=menubar)

        fileMenu = tk.Menu(menubar)
        fileMenu.add_command(label="Quit", command=self.quit)
        menubar.add_cascade(label="File", menu=fileMenu)

        viewMenu = tk.Menu(menubar)
        viewMenu.add_command(label="Text bigger",
                    command=self.whiteboard.increaseTextSize)
        viewMenu.add_command(label="Text smaller",
                    command=self.whiteboard.decreaseTextSize)
        menubar.add_cascade(label="View", menu=viewMenu)

if __name__ == "__main__":
    app = Frontend()
    app.mainloop()
