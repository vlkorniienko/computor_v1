import sys
from pyparsing import *
import computation as c

def parseEquation(equation):
	try:
		newEquation = equation.replace(' ', '').replace("\t", "")
		number = Word(nums)
		integer = Combine(Optional(Literal("-")) + number + Optional('.' + number))
		multiplication = Word("*", max=1)
		degree = "^"
		x = (Word("X", max=1) + degree + number | Word("X", max=1))
		token = Combine(Optional(integer) + Optional(Suppress(multiplication)) + Optional(x))
		after_block = (Word("0", max=1) | token + ZeroOrMore(Word("+-", max=1) + token)) + StringEnd()
		result = token + ZeroOrMore(Word("+-", max=1) + token) + "=" + after_block
		equationList = result.parseString(newEquation)
		return equationList
	except ParseException as err:
		print(err.line)
		print(" " * (err.column - 1) + "^")
		print(err)
		sys.exit()
	except Exception as e:
		print(e)
		sys.exit()

def checkSymbols(equation):
	allowedSymbols = '+- *X^=0123456789.'
	for c in equation:
		if c not in allowedSymbols: 
			print "Error in polynomial equation: unrecognized symbol", c
			sys.exit()


if __name__ == "__main__":
	simple = 0
	if len(sys.argv) == 3 or len(sys.argv) == 2:
		if len(sys.argv) == 3:
			if sys.argv[2] != '--simple':
				print("Usage: python computorV1 argument [--simple]")
				sys.exit()
			else:
				simple = 1
		equation = sys.argv[1]
	else:
		print("Usage: python computorV1 argument [--simple]")
		sys.exit()
	checkSymbols(equation)
	equationList = parseEquation(equation)
	p1 = c.parseEquationList(equationList, simple)
