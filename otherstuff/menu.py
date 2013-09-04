from Tkinter import *
import tkMessageBox
import Tkinter
from ttk import Button

top = Tk()

mb=  Menubutton ( top, text="condiments", relief=RAISED )
mb.grid()
mb.menu  =  Menu ( mb, tearoff = 0 )
mb["menu"]  =  mb.menu
    
mayoVar  = IntVar()
ketchVar = IntVar()

mb.menu.add_checkbutton ( label="mayo",
                          variable=mayoVar )
mb.menu.add_checkbutton ( label="ketchup",
                          variable=ketchVar )

mb.pack()

def printThings():
	print mayoVar, ketchVar

button = Button(text = "lol", command = printThings)
button.pack()

top.mainloop()