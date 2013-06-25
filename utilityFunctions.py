# utilityFunctions.py

def numberPrint(number):
    if abs(int(number)-number) < 0.00001:
        return "%d"%number
    if abs(int(number*2)-number*2) < 0.00001:
        return "(%d/2)"%(number*2)
    return "%1f"%number