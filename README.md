Readme
=====

This is the start of a graphical equation manipulator. This software
aspires to assist in calculations in the kinds of physics problems which
involve writing down equations, equating variables, and solving for
variables.

It has been made obselete by [its Coffeescript successor](https://github.com/MatthewJA/Graphical-Equation-Manipulator).

You can watch a demo [here](http://www.youtube.com/watch?v=16eiGLrX248).

Installation
------------

This program depends heavily on Sympy.

To my shame, the program currently has a dependency on the uncertainties module,
which itself requires Scipy.

If you install Python, then Scipy, then uncertainties, then Sympy, then run
main.py, this should work.


How to use
----------

The main program is in src/main.py.

Type the first few words of a quantity, eg "kinetic energy". Equations
related to kinetic energy show up. Click on them to introduce them to
the workspace.

Type in another word, like "potential". Add another equation.

You can move equations around by dragging them by their operators -
everything which isn't a variable.

If you click and drag an operator from one variable to another in
a different equation, it will try to equate them. This will only work
if the variables are of the same dimension.

To solve for a variable, double click on it.

To rewrite the expression for a variable, drag from a variable in its
expression to another formula.

To add a numerical value, type it into the search bar. To assign this
value to a variable, drag from that variable to the number. This number
is then substituted into expressions where its variable is mentioned.

Numerical values can have uncertainties. For example, enter "10+-1" into
the search bar.
