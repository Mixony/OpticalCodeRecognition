from constants import *
from ast2code import *

tokenList = []
i = 0
j = -1
currToken = []
code = ""
eof = False

def readTokenList(tl):
	global tokenList
	tokenList = tl

def nextToken():
	global i
	global j
	global currToken
	global code
	global ast
	global eof
	j+=1
	if eof:
		print(code)
		# print('\n')
		# printAST(ast)
		exit()
	if j >= len(tokenList[i]):
		j=0
		i+=1
	if tokenList[i][j][0]=='eof':
		eof = True
	currToken = tokenList[i][j]

def error(msg):
	print(msg)
	return

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
	error('Token {} is expected got {} on {},{}'.format(token, currToken,i,j))
	return False

def program():
	global code
	global tokenList
	global currToken
	global ast
	ast=[]
	nextToken()
	while i <= len(tokenList):
		tkn = currToken[1]
		vartype = tkn
		if accept('hashtag') :
			code += '#'
			ast.append(ppdirective())
			code+='\n'
		elif accept('vartype'):
			code += tkn + ' '
			tkn = currToken[1]
			if expect('identifier'):
				code += tkn
				ast.append(globalSpace(vartype, tkn))
			code+='\n'
		else:
			nextToken()
	return code

def ppdirective():
	global code
	directive = None
	if accept('include'):
		code+='include '
		directive = ['include',includeStatement()]
	elif accept('define'):
		code+='define '
		directive = ['define',defineVarName()]
	return directive

def includeStatement():
	global code
	lib = None
	if accept('less') or accept('openbracket') or accept('opencbracket'):
		code += '<'
		lib = ['system_header',systemHeader()]
		code += '>'
		nextToken()
	elif accept('quote') or accept('apostrophe') or accept('graveaccent'):
		code += '\"'
		lib = ['user_header',usermadeHeader()]
		code += '\"'
		nextToken()
	return lib

def systemHeader():
	global code	
	global currToken
	tkn = currToken[1]
	if accept('system_library'):
		code += tkn
	else:
		print('Couldnt recognize library name')
	return [tkn]

def usermadeHeader():
	global code
	global currToken
	tkn = currToken[1]
	code += tkn
	nextToken()
	return [tkn]

def defineVarName():
	global code
	global currToken
	global j
	tkn = currToken[1]
	varname = None
	if expect('identifier'):
		code += tkn + ' '
		if j == 0:
			return [tkn]
		varname = [tkn,expression()]
	return varname

def intValue(tkn):
	global code
	code += tkn
	return [tkn]

def floatValue(tkn):
	global code
	code += tkn
	return [tkn]

def doubleValue(tkn):
	global code
	code += tkn
	return [tkn]

def stringValue():
	global code
	global currToken
	tkn = currToken[1]
	if accept('identifier') or accept('number') or accept('float') or accept('double'):
		if len(tkn)==1:
			code += '\''
			code += tkn
			code += '\''
			nextToken()
			return ['\''+tkn+'\'']
		else:
			code += '\"'
			code += tkn + ' '
			tkn = currToken
			while not accept('quote'):
				code += tkn[1] + ' '
				nextToken()
				tkn = currToken
			code += '\b\"'
			nextToken()
			return ['\"'+tkn[0]+'\"']

def globalSpace(vt,t):
	global code
	global currToken
	tkn = currToken[1]
	if accept('semicolon'):
		code += ';'
		return ['variable',['type',[vt]],['name',[t]]]
	elif accept('openbracket'):
		code += '('
		args = function()
		return ['function',['ret_type',[vt]],['name',[t]],['args',args]]
	else:
		nextToken()

def function():
	global code
	global currToken
	tkn = currToken[1]
	ret = []
	if accept('closedbracket'):
		code += tkn
	else:
		ret.append(argumentsDefinition())
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
	return [ret]

def argumentsDefinition():
	global code
	global currToken
	tkn = currToken[1]
	vt = None
	t = None
	args = []
	while not (accept('closedbracket') or accept('closedcbracket') or accept('greater')):
		if expect('vartype'):
			code += tkn + ' '
			vt = tkn
		tkn = currToken[1]
		if expect('identifier'):
			code += tkn
			t = tkn
		tkn = currToken[1]
		if accept('comma') or accept('period'):
			code += tkn + ' '
			tkn = currToken[1]
		args.append(['variable',['type',[vt]],['name',[t]]])
	code += tkn
	return args

def block():
	global code
	global currToken
	while not accept('closedcbracket'):
		tkn = currToken[1]
		if accept('vartype'):
			code += tkn + ' '
			varDefinition()
			code += '\n'
		elif accept('return'):
			code += tkn
			if accept('semicolon'):
				code += ';'
				continue
			code += ' '
			expression()
			if accept('semicolon'):
				code += ';'
		elif accept('identifier'):
			if accept('openbracket'):
				code += tkn
				callArguments()
			elif accept('opencbracket'):
				callArguments()
				code += tkn
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
			if accept('semicolon') or accept('colon'):
				code += ';'
			return

def factor():
	global code
	global currToken
	global i
	global j
	tkn = currToken[1]
	if accept('identifier'):
		code += tkn
	elif accept('number'):
		intValue(tkn)
	elif accept('float'):
		floatValue(tkn)
	elif accept('double'):
		doubleValue(tkn)
	elif accept('apostrophe'):
		stringValue()
	elif accept('quote'):
		stringValue()
	elif accept('openbracket'):
		code += tkn
		expression()
		expect('closedbracket')
		code += ')'
	else:
		error('factor not found at line {},{}'.format(i,j))
		nextToken()

def term():
	global code
	global currToken
	factor()
	tkntyp = currToken[0]
	tkn = currToken[1]
	while tkntyp == 'asterisk' or tkntyp == 'slash':
		code += tkn
		nextToken()
		factor()
		tkntyp = currToken[0]

def expression():
	global code
	global currToken
	tkntyp = currToken[0]
	tkn = currToken[1]
	if tkntyp == 'plus' or tkntyp == 'minus':
		code += tkn
		nextToken()
	term()
	tkntyp = currToken[0]
	tkn = currToken[1]
	while tkntyp == 'plus' or tkntyp == 'minus':
		code += tkn
		nextToken()
		term();
		tkntyp = currToken[0]
		tkn = currToken[1]

		#
		#	if accept('semicolon'):
		#		code += ';'
		#		continue

def callArguments():
	global code
	global currToken
	tkn = currToken[1]
	code += '('
	while not (accept('closedbracket') or accept('closedcbracket')):
		code += tkn
		nextToken()
		tkn = currToken[1]
	code += ')'
