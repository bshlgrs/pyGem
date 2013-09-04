#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this script, we use the grid manager
to create a skeleton of a calculator.

author: Jan Bodnar
last modified: December 2010
website: www.zetcode.com
"""

from Tkinter import Tk, W, E, StringVar
from ttk import Frame, Button, Label, Style
from ttk import Entry


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
      
        self.parent.title("Calculator")
        
        Style().configure("TButton", padding=(0, 5, 0, 5), 
            font='serif 10')
        
        self.columnconfigure(0, pad=3)
        self.columnconfigure(1, pad=3)
        self.columnconfigure(2, pad=3)
        self.columnconfigure(3, pad=3)
        
        self.rowconfigure(0, pad=3)
        self.rowconfigure(1, pad=3)
        self.rowconfigure(2, pad=3)
        self.rowconfigure(3, pad=3)
        self.rowconfigure(4, pad=3)
        

        self.v = StringVar()

        entry = Entry(self, textvariable = self.v)
        entry.grid(row=0, columnspan=4, sticky=W+E)
        cls = Button(self, text="Cls")
        cls.grid(row=1, column=0)
        bck = Button(self, text="Back")
        bck.grid(row=1, column=1)
        lbl = Button(self)
        lbl.grid(row=1, column=2)    
        clo = Button(self, text="Close")
        clo.grid(row=1, column=3)        
        sev = Button(self, text="7")
        sev.grid(row=2, column=0)        
        eig = Button(self, text="8")
        eig.grid(row=2, column=1)         
        nin = Button(self, text="9")
        nin.grid(row=2, column=2) 
        div = Button(self, text="/")
        div.grid(row=2, column=3) 
        
        fou = Button(self, text="4")
        fou.grid(row=3, column=0)        
        fiv = Button(self, text="5")
        fiv.grid(row=3, column=1)         
        six = Button(self, text="6", command = self.addSix)
        six.grid(row=3, column=2) 
        mul = Button(self, text="*")
        mul.grid(row=3, column=3)    
        
        one = Button(self, text="1")
        one.grid(row=4, column=0)        
        two = Button(self, text="2")
        two.grid(row=4, column=1)         
        thr = Button(self, text="3")
        thr.grid(row=4, column=2) 
        mns = Button(self, text="-")
        mns.grid(row=4, column=3)         
        
        zer = Button(self, text="0")
        zer.grid(row=5, column=0)        
        dot = Button(self, text=".")
        dot.grid(row=5, column=1)         
        equ = Button(self, text="=")
        equ.grid(row=5, column=2) 
        pls = Button(self, text="+")
        pls.grid(row=5, column=3)
        
        self.pack()

    def addSix(self):
        lol = self.v.get()
        self.v.set(lol+"6")

def main():
  
    root = Tk()
    app = Example(root)
    root.mainloop()  


if __name__ == '__main__':
    main() 