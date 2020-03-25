import sys
from pyparsing import *
import computation as c

# "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0 + 9.8 * X^2"
# "5 * X^0 + 4 * X^1 - 9.3 * X^2 = 0 + 5 * X^0"
# "5 + 4 * X + X^2= X^2"

def parseEquation(equation):
	try:
		number = Word(nums)
		integer = Combine(Optional(Literal("-")) + number + Optional('.' + number))
		multiplication = Word("*", max=1)
		degree = "^"
		x = (Word("X", max=1) + degree + number | Word("X", max=1))
		token = Optional(integer) + Optional(Suppress(multiplication)) + Optional(x)
		after_block = (Word("0", max=1) | token + ZeroOrMore(Word("+-", max=1) + token))
		result = token + ZeroOrMore(Word("+-", max=1) + token) + "=" + after_block
		equationList = result.parseString(equation)
		return equationList
	except ParseException as err:
		print(err.line)
		print(" " * (err.column - 1) + "^")
		print(err)
		sys.exit()

def checkSymbols(equation):
	allowedSymbols = '+- *X^=0123456789.'
	for c in equation:
		if c not in allowedSymbols: 
			print "Error in polynomial equation: unrecognized symbol", c
			sys.exit()


if __name__ == "__main__":
	if len(sys.argv) == 2:
		equation = sys.argv[1]
	else:
		print("Usage: python computorV1 [argument]")
		sys.exit()
	checkSymbols(equation)
	equationList = parseEquation(equation)
	#print(equationList)
	p1 = c.Equation(1, 2, 3)
	for i in equationList: 
		print(i)
