import sys
import re

def checkDegreeSequence(f, itsAfterBlock, equationDictionary):
	if itsAfterBlock == True:
		d = equationDictionary['afterDegree']
		if (f == 0 and d > 0) or (f == 1 and d > 1) or (f == 2 and d > 2):
			print("Error in equation sequence: {X^0} {X^1} {X^2}")
			sys.exit()
	else:
		d = equationDictionary['beforeDegree']
		if (f == 0 and d > 0) or (f == 1 and d > 1) or (f == 2 and d > 2):
			print("Error in equation sequence: {X^0} {X^1} {X^2}")
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


def parseEquationList(equationList, simple):
	itsAfterBlock = False
	equationDictionary = {'beforeDegree' : 0, 'afterDegree' : 0, 'simple' : simple}
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
		resolveFirstDegree(equationDictionary)
	else:
		resolveSecondDegree(equationDictionary)


def reduceDegree(equationDictionary):
	if 'a' in equationDictionary:
		if not 'b' in equationDictionary and not 'c' in equationDictionary:
			return
		if equationDictionary['a'] == 0:
			del equationDictionary['a']
			equationDictionary['beforeDegree'] = 1
			equationDictionary['afterDegree'] = 1
	if 'b' in equationDictionary:
		if not 'a' in equationDictionary and not 'c' in equationDictionary:
			return
		if equationDictionary['b'] == 0:
			del equationDictionary['b']
			if not 'c' in equationDictionary:
				equationDictionary['beforeDegree'] = 0
				equationDictionary['afterDegree'] = 0
	if 'c' in equationDictionary:
		if not 'b' in equationDictionary and not 'a' in equationDictionary:
			return
		if equationDictionary['c'] == 0:
			del equationDictionary['c']


def resolveFirstDegree(equationDictionary):
	if not 'c' in equationDictionary and not 'a' in equationDictionary:
		if equationDictionary['b'] == 0:
			print('Polynomial degree: 1\nAll the real number are solutions')
			sys.exit()
	if 'c' in equationDictionary:
		b = equationDictionary['b']
		c = equationDictionary['c']
		result = (float(-1 * c) / float(b))
		printReducedForm(equationDictionary)
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


def resolveSecondDegree(equationDictionary):
	if not 'c' in equationDictionary and not 'b' in equationDictionary:
		if equationDictionary['a'] == 0:
			print('Polynomial degree: 2\nAll the real number are solutions')
			sys.exit()
	a = equationDictionary['a']
	if not 'b' in equationDictionary and not 'c' in equationDictionary:
		print('Polynomial degree: 2\nThe solution is')
		print(0)
	elif not 'b' in equationDictionary:
		c = equationDictionary['c']
		squareX = (float(-1 * c) / float(a))
		if squareX < 0:
			printReducedForm(equationDictionary)
			print("There is no solution in this equation")
			sys.exit()
		result = findSquareRoot(squareX)
		printReducedForm(equationDictionary)
		print('Polynomial degree: 2\nTwo solutions are:')
		print(result)
		print(result * -1)
	elif not 'c' in equationDictionary:
		b = equationDictionary['b']
		printReducedForm(equationDictionary)
		print('Polynomial degree: 2\nTwo solutions are:')
		print(0)
		print(-1 * (float(b) / float(a)))
	else:
		findDiscriminant(equationDictionary)


def findDiscriminant(equationDictionary):
	c = equationDictionary['c']
	a = equationDictionary['a']
	b = equationDictionary['b']
	discriminant = (b * b) - (4 * a * c)
	if discriminant < 0:
		printReducedForm(equationDictionary)
		print("Polynomial degree: 2\nDiscriminant is negative, there is no solution")
	elif discriminant == 0:
		printReducedForm(equationDictionary)
		print("Polynomial degree: 2\nDiscriminant is equal to zero, the solution is")
		result = (-1 * float(b)) / (2 * float(a))
		print(result)
	else:
		printReducedForm(equationDictionary)
		print("Polynomial degree: 2\nDiscriminant is strictly positive, the two solutions are:")
		result1 = ((-1 * float(b)) + findSquareRoot(discriminant)) / (2 * float(a))
		result2 = ((-1 * float(b)) - findSquareRoot(discriminant)) / (2 * float(a))
		print(result1)
		print(result2)

def printReducedForm(equationDictionary):
	result = ""
	if 'c' in equationDictionary:
		c = equationDictionary['c']
		if int(c) == float(c):
			decimals = 0
		else:
			decimals = 1
		result += '{0:.{1}f}'.format(c, decimals)
		if equationDictionary['simple'] == 0:
			result += ' * X^0'
	if 'b' in equationDictionary:
		b = equationDictionary['b']
		if int(b) == float(b):
			decimals = 0
		else:
			decimals = 1
		if b > 0:
			if 'c' in equationDictionary:
				result += ' + '
			if b != 1:
				result += '{0:.{1}f}'.format(b, decimals)
		else:
			if 'c' in equationDictionary:
				result += ' - '
			else:
				result += '-'
			if b != -1:
				result += '{0:.{1}f}'.format((b * -1), decimals)
		if equationDictionary['simple'] == 0:
			result += ' * X^1'
		else:
			result += 'X'
	if 'a' in equationDictionary:
		a = equationDictionary['a']
		if int(a) == float(a):
			decimals = 0
		else:
			decimals = 1
		if a > 0:
			if 'c' or 'b' in equationDictionary:
				result += ' + '
			if a != 1:
				result += '{0:.{1}f}'.format(a, decimals)
		else:
			if 'c' or 'b' in equationDictionary:
				result += ' - '
			else:
				result += '-'
			if a != -1:
				result += '{0:.{1}f}'.format((a * -1), decimals)
		if equationDictionary['simple'] == 0:
			result += ' * X^2'
		else:
			result += 'X^2'
	result += ' = 0'
	print 'Reduced form:', result
