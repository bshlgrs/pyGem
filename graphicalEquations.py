import Tkinter as tk

class MyApp (tk.Tk):
	''' Display equations on a Tkinter canvas'''

	def __init__(self,*args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)

        self.canvas = tk.Canvas(width=400, height=400, bg = "grey")




exampleThingToShow = (1,[("Ek",1)],0.5,[("m",1),("v",2)])

def stuffToString(coef, terms):
	if coef==1:
		return " ".join(x[0]+"^"+x[1] for x in terms)
	return str(coef)+" "+" ".join(x[0]+"^"+x[1] for x in terms)

print stuffToString(0.5,[("m",1),("v",2)])
