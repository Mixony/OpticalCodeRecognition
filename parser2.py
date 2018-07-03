from constants import *

tokenList = []
i = 0
j = -1
currToken = []
code = ""

def readTokenList(tl):
	global tokenList
	tokenList = tl

def nextToken():
	global i
	global j
	global currToken
	global code
	j+=1
	if j >= len(tokenList[i]):
		j=0
		i+=1
	if i >= len(tokenList):
		print(code)
		exit()
	currToken = tokenList[i][j]

def error(msg):
	print(msg)

def accept(token):
	global currToken
	if token == currToken[0]:
		nextToken()
		return True
	return False

def expect(token):
	global currToken
	if accept(token):
		return True
	error('Token {} is expected got {}'.format(token[0], currToken))
	return False

def program():
	global code
	global tokenList
	global currToken
	nextToken()
	while i <= len(tokenList):
		tkn = currToken[1]
		if accept('hashtag') :
			code += '#'
			ppdirective()
			code+='\n'
		elif accept('vartype'):
			code += tkn + ' '
			tkn = currToken[1]
			if expect('identifier'):
				code += tkn
				globalSpace()
			code+='\n'
		else:
			nextToken()
	return code

def ppdirective():
	global code
	if accept('include'):
		code+='include '
		includeStatement()
	elif accept('define'):
		code+='define '
		defineVarName()

def includeStatement():
	global code
	if accept('less') or accept('openbracket') or accept('opencbracket'):
		code += '<'
		systemHeader()
		code += '>'
		nextToken()
	elif accept('quote') or accept('apostrophe') or accept('graveaccent'):
		code += '\"'
		usermadeHeader()
		code += '\"'
		nextToken()

def systemHeader():
	global code	
	global currToken
	tkn = currToken[1]
	if accept('system_library'):
		code += tkn
	else:
		print('Couldnt recognize library name')

def usermadeHeader():
	global code
	global currToken
	code += currToken[1]
	nextToken()

def defineVarName():
	global code
	global currToken
	global j
	tkn = currToken[1]
	if expect('identifier'):
		code += tkn + ' '
		if j == 0:
			return
		varValue()

def varValue():
	global code
	global currToken
	tkn = currToken[1]
	if accept('number'):
		intValue(tkn);
		return
	elif accept('float'):
		floatValue(tkn)
		return
	elif accept('double'):
		doubleValue(tkn)
		return
	elif accept('apostrophe') or accept('graveaccent') or accept('quote'):
		stringValue()
		return

def intValue(tkn):
	global code
	code += tkn

def floatValue(tkn):
	global code
	code += tkn

def doubleValue(tkn):
	global code
	code += tkn

def stringValue():
	global code
	global currToken
	tkn = currToken[1]
	if accept('identifier') or accept('number'):
		if len(tkn)==1:
			code += '\''
			code += tkn
			code += '\''
		else:
			code += '\"'
			code += tkn
			code += '\"'

def globalSpace():
	global code
	if accept('semicolon'):
		code += ';'
	elif accept('openbracket'):
		code += '('
		function()
	else:
		nextToken()

def function():
	global code
	global currToken
	tkn = currToken[1]
	if accept('closedbracket'):
		code += tkn
	else:
		argumentsDefinition()
	tkn = currToken[1]
	if accept('opencbracket') or accept('openbracket') or accept('less'):
		code+='\n{\n'
		block()
		code+='\n}'
		return
	elif accept('colon') or accept('semicolon'):
		code += tkn
		return
	else:
		print('expected open curly bracket')

def argumentsDefinition():
	global code
	global currToken
	tkn = currToken[1]
	while not accept('closedbracket'):
		if expect('vartype'):
			code += tkn + ' '
		tkn = currToken[1]
		if expect('identifier'):
			code += tkn
		tkn = currToken[1]
		if accept('comma') or accept('period'):
			code += tkn + ' '
			tkn = currToken[1]
	code += tkn

def block():
	global code
	global currToken
	tkn = currToken[1]
	while not accept('closedcbracket'):
		if accept('vartype'):
			code += tkn + ' '
			varDefinition()
			code += '\n'
		else:
			nextToken()

def varDefinition():
	global code
	global currToken
	global j
	tkn = currToken[1]
	if expect('identifier'):
		code += tkn
		tkn = currToken[1]
		if accept('semicolon') or accept('colon'):
			code += ';'
			return
		elif accept('equals'):
			code += tkn
			expression()
			return
	else:
		print('Paja')

def expression():
	global code
	global currToken
	if accept('openbracket'):
		tkn = currToken[1]
		code += tkn
	tkn = currToken[1]
	if accept('number') or  accept('float') or  accept('double'):
		code += tkn
	else:
		code = code
		#TODO: something else