-- solver2.hs

type VarName = String
type Var = (VarName, Float)
type SpecialFunction = (String, Float, [Var])
type Product = (Float, [Var], [SpecialFunction])
type EasyExpression = [Product]

data GeneralExpression = GeneralSum [GeneralExpression]
					   | GeneralProduct Float [GeneralExpression]
					   | GeneralSpecial String GeneralExpression
					   | GeneralExponent GeneralExpression GeneralExpression
					   | GeneralVariable VarName
	deriving (Show, Eq)

data VariableStatus = Power Float
					| NotPresent
					| Special
					| MultiplePlaces -- In this context, the variable being in
									 -- multiple places actually does guarantee
									 -- that it's unsolvable
	deriving (Show, Eq)

checkVarInEasy :: VarName -> EasyExpression -> Bool
checkVarInEasy name expr = any [getVariableStatus name x /= NotPresent 
																	| x<-expr]

getVariableStatus :: VarName -> Product -> VariableStatus
getVariableStatus name (_,vars,specials) = case (powers, filteredSpecs) of
			([],[]) -> NotPresent
			([(_,y)],[]) -> Power y
			([],[_]) -> Special
			_ 		 -> MultiplePlaces
				where
				powers = filter (\(x,_) -> x == name) vars
				filteredSpecs = filter (\(_,_,(x,_)) -> x == name) vars