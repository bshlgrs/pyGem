#!/usr/bin/python3

from Frontend import Frontend

def main():
	print "Loading GEM version 0.1. This might take ten seconds..."
	app = Frontend()
	app.mainloop()

if __name__ == "__main__":
    main()