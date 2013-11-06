#!/usr/bin/python

from Frontend import Frontend

def main():
    print "Loading GEM version 0.1. This might take ten seconds..."
    app = Frontend()
    print "loaded"
    app.mainloop()

if __name__ == "__main__":
    main()