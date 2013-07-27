data Expression = Sum [(Expression,Float)]
				| Product [(Expression,Float)]
				| Variable String
				| Constant

example1 = Sum [()]

variableInExpression :: String -> Expression -> Bool
variableInExpression var expr = case expr of
		Variable x -> x == var
		Sum list -> or [variableInExpression var x | (x,_)<- list]
		Product list -> or [variableInExpression var x | (x,_)<- list]

