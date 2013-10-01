import Tkinter as tk
# class MyApp (tk.Tk):
# 	''' Display equations on a Tkinter canvas'''

# 	def __init__(self,*args, **kwargs):
# 		tk.Tk.__init__(self, *args, **kwargs)

#         self.canvas = tk.Canvas(width=400, height=400, bg = "grey")




exampleThingToShow = (1,[("Ek",1)],0.5,[("m",1),("v",2)])

def stuffToString(coef, terms):

	def numberShow(number):
	    if abs(int(number)-number) < 0.00001:
	        return "%d"%number
	    if abs(int(number*2)-number*2) < 0.00001:
	        return "(%d/2)"%(number*2)
	    return "%1f"%number
	
	if coef==1:
		return " ".join(x[0]+"^"+x[1] for x in terms)
	return str(coef)+" "+" ".join("%s^%s"%(x[0],numberShow(x[1])) for x in terms)

print stuffToString(0.5,[("m",1),("v",2)])
