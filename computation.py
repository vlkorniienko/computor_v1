import sys
import re

def checkDegreeSequence(f, itsAfterBlock, equationDictionary):
	if itsAfterBlock == True:
		d = equationDictionary['afterDegree']
		if (f == 0 and d > 0) or (f == 1 and d > 1) or (f == 2 and d > 2):
			print("Error in equation degree sequence")
			sys.exit()
	else:
		d = equationDictionary['beforeDegree']
		if (f == 0 and d > 0) or (f == 1 and d > 1) or (f == 2 and d > 2):
			print("Error in equation degree sequence")
			sys.exit()

def addValueToDictionary(value, key, equationDictionary):
	if key in equationDictionary:
		result = equationDictionary[key] + value
		equationDictionary[key] = result
	else:
		equationDictionary[key] = value

def parseDigit(i, equationList, equationDictionary, itsAfterBlock):
	if re.match(r"[-+]?\d+$", equationList[i]):
		result = int(equationList[i])
	else:
		result = float(equationList[i])
	if equationList[i - 1] == "-":
		result *= -1
	if itsAfterBlock == True:
		result *= -1
	checkDegreeSequence(0, itsAfterBlock, equationDictionary)
	key = 'c'
	addValueToDictionary(result, key, equationDictionary)

def parseTokenWithoutDegree(i, equationList, equationDictionary, itsAfterBlock):
	if equationList[i] == 'X':
		result = 1
	elif re.match(r'^-?\d+X$', equationList[i]) or re.match(r'^-?\d+\*X$', equationList[i]):
		splitted = equationList[i].split('X')
		result = int(splitted[0])
	else:
		splitted = equationList[i].split('X')
		result = float(splitted[0])
	checkDegreeSequence(1, itsAfterBlock, equationDictionary)
	if equationList[i - 1] == "-":
		result *= -1
	if itsAfterBlock == True:
		result *= -1
		equationDictionary['afterDegree'] = 1
	else:
		equationDictionary['beforeDegree'] = 1
	key = 'b'
	addValueToDictionary(result, key, equationDictionary)

def parseTokenWithDegree(i, equationList, equationDictionary, itsAfterBlock):
	xPosition = equationList[i].find('X')
	numberString = equationList[i][0:xPosition]
	if numberString == "":
		number = 1
	elif numberString.isdigit():
		number = int(numberString)
	else:
		number = float(numberString)
	if equationList[i - 1] == "-":
		number *= -1
	if itsAfterBlock == True:
		number *= -1
	degree = int(equationList[i][equationList[i].find('^') + 1:len(equationList[i])])
	if degree > 2:
		print"Polynomial degree:", degree
		print("The polynomial degree is strictly greater than 2, I can't solve.")
		sys.exit()
	elif degree == 0:
		key = 'c'
		addValueToDictionary(number, key, equationDictionary)
		if itsAfterBlock == False:
			equationDictionary['beforeDegree'] = 0
		else:
			equationDictionary['afterDegree'] = 0
	elif degree == 1:
		key = 'b'
		addValueToDictionary(number, key, equationDictionary)
		if itsAfterBlock == False:
			equationDictionary['beforeDegree'] = 1
		else:
			equationDictionary['afterDegree'] = 1
	else:
		key = 'a'
		addValueToDictionary(number, key, equationDictionary)
		if itsAfterBlock == False:
			equationDictionary['beforeDegree'] = 2
		else:
			equationDictionary['afterDegree'] = 2

def parseEquationList(equationList):
	itsAfterBlock = False
	equationDictionary = {'beforeDegree' : 0, 'afterDegree' : 0}
	for i in range(len(equationList)):
		if equationList[i] == '=':
			itsAfterBlock = True
			if equationList[i + 1] == '0':
				break
		elif (re.match(r"[-+]?\d+$", equationList[i])) or (re.match(r'^-?\d+(?:\.\d+)?$', equationList[i])):
			parseDigit(i, equationList, equationDictionary, itsAfterBlock)
		elif re.match(r'^-?\d*(?:\.\d+)?X$', equationList[i]) or re.match(r'^-?\d+(?:\.\d+)?\*X$', equationList[i]):
			parseTokenWithoutDegree(i, equationList, equationDictionary, itsAfterBlock)
		elif re.match(r'^-?\d*(?:\.\d+)?X\^\d+$', equationList[i]) or re.match(r'^-?\d+(?:\.\d+)?\*X\^\d+$', equationList[i]):
			parseTokenWithDegree(i, equationList, equationDictionary, itsAfterBlock)
	findSolutions(equationDictionary)

def findSolutions(equationDictionary):
	reduceDegree(equationDictionary)
	if equationDictionary['beforeDegree'] == 0 and equationDictionary['afterDegree'] == 0:
		print('Polynomial degree: 0\nAll the real numbers are solution')
	elif equationDictionary['beforeDegree'] < 2 and equationDictionary['afterDegree'] < 2:
		firstDegreeEQ(equationDictionary)
	else:
		secondDegreeEQ(equationDictionary)

def reduceDegree(equationDictionary):
	if 'a' in equationDictionary:
		if equationDictionary['a'] == 0:
			del equationDictionary['a']
			equationDictionary['beforeDegree'] = 1
			equationDictionary['afterDegree'] = 1
	if 'b' in equationDictionary:
		if equationDictionary['b'] == 0:
			del equationDictionary['b']
			if not 'c' in equationDictionary:
				equationDictionary['beforeDegree'] = 0
				equationDictionary['afterDegree'] = 0
	if 'c' in equationDictionary:
		if equationDictionary['c'] == 0:
			del equationDictionary['c']


def firstDegreeEQ(equationDictionary):
	if 'c' in equationDictionary:
		b = equationDictionary['b']
		c = equationDictionary['c']
		result = (float(-1 * c) / float(b))
		if b < 0:
			print("Reduced form: %d * X^0 - %d * X^1 = 0" % (c, (-1 * b)))
		else:
			print("Reduced form: %d * X^0 + %d * X^1 = 0" % (c, b))
		print('Polynomial degree: 1\nThe solution is:')
		print(result)
	else:
		print('Polynomial degree: 1\nThe solution is:')
		print(0)

def findSquareRoot(number):
	i = 1
	while(number > (i * i)):
		i += 1
	if i * i == number:
		return i
	f = int(i - 1)
	while (number > (f * f)):
		f += 0.01
	return f

def secondDegreeEQ(equationDictionary):
	a = equationDictionary['a']
	if not 'b' in equationDictionary and not 'c' in equationDictionary:
		print('Polynomial degree: 2\nThe solution is')
		print(0)
	elif not 'b' in equationDictionary:
		c = equationDictionary['c']
		squareX = (float(-1 * c) / float(a))
		if squareX < 0:
			if a < 0:
				print("Reduced form: %d * X^0 - %d * X^2 = 0" % (c, (-1 * a)))
			else:
				print("Reduced form: %d * X^0 + %d * X^2 = 0" % (c, a))
			print("There is no solution in this equation")
			sys.exit()
		result = findSquareRoot(squareX)
		if a < 0:
			print("Reduced form: %d * X^0 - %d * X^2 = 0" % (c, (-1 * a)))
		else:
			print("Reduced form: %d * X^0 + %d * X^2 = 0" % (c, a))
		print('Polynomial degree: 2\nTwo solutions are:')
		print(result)
		print(result * -1)
	elif not 'c' in equationDictionary:
		b = equationDictionary['b']
		if b < 0:
			print("Reduced form: %d * X^0 - %d * X^2 = 0" % (b, (-1 * a)))
		else:
			print("Reduced form: %d * X^0 + %d * X^2 = 0" % (b, a))
		print('Polynomial degree: 2\nTwo solutions are:')
		print(0)
		print(-1 * (b / a))
	else:
		findDiscriminant(equationDictionary)

def findDiscriminant(equationDictionary):
	c = equationDictionary['c']
	a = equationDictionary['a']
	b = equationDictionary['b']
	discriminant = (b * b) - (4 * a * c)
	if discriminant < 0:
		printReducedForm(a, b, c)
		print("Polynomial degree: 2\nDiscriminant is negative, there is no solution")
	elif discriminant == 0:
		printReducedForm(a, b, c)
		print("Polynomial degree: 2\nDiscriminant is equal to zero, the solution is")
		result = ((-1 * b) + findSquareRoot(discriminant)) / 2 * a
		print(result)
	else:
		printReducedForm(a, b, c)
		print("Polynomial degree: 2\nDiscriminant is strictly positive, the two solutions are:")
		result1 = ((-1 * b) + findSquareRoot(discriminant)) / (2 * a)
		result2 = ((-1 * b) - findSquareRoot(discriminant)) / (2 * a)
		print(result1)
		print(result2)

def printReducedForm(a, b, c):
	if b < 0:
		if a < 0:
			print("Reduced form: %d * X^0 - %d * X^1 - %d * X^2 = 0" % (c, (-1 * b), (-1 * a)))
		else:
			print("Reduced form: %d * X^0 - %d * X^1 + %d * X^2 = 0" % (c, (-1 * b), a))
	else:
		if a < 0:
			print("Reduced form: %d * X^0 + %d * X^1 - %d * X^2 = 0" % (c, b, (-1 * a)))
		else:
			print("Reduced form: %d * X^0 + %d * X^1 + %d * X^2 = 0" % (c, b, a))
