from constants import *
from ast2code import *

tokenList = []
i = 0
j = -1
currToken = []
code = ""
eof = False
ast = []

def importTokenList(tl):
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
		print('\n')
		print(ast)
		print('\n')
		printAST(ast)
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
	ast=['program']
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
		lib = ['system',systemHeader()]
		code += '>'
		nextToken()
	elif accept('quote') or accept('apostrophe') or accept('graveaccent'):
		code += '\"'
		lib = ['user',usermadeHeader()]
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
	return ['intValue',tkn]

def floatValue(tkn):
	global code
	code += tkn
	return ['floatValue',tkn]

def doubleValue(tkn):
	global code
	code += tkn
	return ['doubleValue',tkn]

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
			return ['charValue','\''+tkn+'\'']
		else:
			code += '\"'
			code += tkn + ' '
			tkn = currToken
			while tkn[0] != 'quote':
				code += tkn[1] + ' '
				nextToken()
				tkn = currToken
			code += '\b\"'
			nextToken()
			return ['stringValue','\"'+tkn[0]+'\"']

def globalSpace(vt,t):
	global code
	global currToken
	tkn = currToken[1]
	if accept('semicolon'):
		code += ';'
		return ['variable',[vt,t]]
	elif accept('equals'):
		code += '='
		eq = ['equals',['variable',[vt,t]],expression()]
		if accept('semicolon'):
			code += ';'
		return eq
	elif accept('openbracket'):
		code += '('
		func = function()
		return ['function',[vt,t,func[0],func[1]]]
	else:
		nextToken()

def function():
	global code
	global currToken
	tkn = currToken[1]
	args = ['args']
	body = ['body']
	if accept('closedbracket'):
		code += tkn
	else:
		args.append(argumentsDefinition())
	tkn = currToken[1]
	if accept('opencbracket') or accept('openbracket') or accept('less'):
		code+='\n{\n'
		body.append(block())
		code+='\n}'
	elif accept('colon') or accept('semicolon'):
		code += tkn
	else:
		print('expected open curly bracket')
	return [args,body]

def argumentsDefinition():
	global code
	global currToken
	tkn = currToken[1]
	vt = None
	t = None
	args = []
	while not (accept('closedbracket') or accept('closedcbracket') or accept('greater')):
		args.append('var')
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
		args.append([vt,t])
	code += tkn
	return args

def block():
	global code
	global currToken
	body = []
	while not accept('closedcbracket'):
		tkn = currToken[1]
		if accept('vartype'):
			code += tkn
			code += ' '
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
				if accept('semicolon'):
					code += ';'
			elif accept('opencbracket'):
				callArguments()
				code += tkn
			code += '\n'
		elif accept('for'):
			code += 'for'
			forLoop()
		elif accept('while'):
			code += 'while'
			whileLoop()
		elif accept('if'):
			code += 'if'
			ifStatement()
		else:
			nextToken()

def oneLineBlock():
	global code
	global currToken
	tkn = currToken[1]
	if accept('vartype'):
		code += tkn
		if accept('asterisk'):
			code += '*'
		code += ' '
		varDefinition()
		code += '\n'
	elif accept('return'):
		code += tkn
		if accept('semicolon'):
			code += ';'
			return
		code += ' '
		expression()
		if accept('semicolon'):
			code += ';'
	elif accept('identifier'):
		if accept('openbracket'):
			code += tkn
			callArguments()
			if accept('semicolon'):
				code += ';'
		elif accept('opencbracket'):
			callArguments()
			code += tkn
		code += '\n'
	elif accept('for'):
		code += 'for'
		forLoop()
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
	ret = ['factor']
	if accept('identifier'):
		code += tkn
		ret.append(tkn)
	elif accept('number'):
		ret.append(intValue(tkn))
	elif accept('float'):
		ret.append(floatValue(tkn))
	elif accept('double'):
		ret.append(doubleValue(tkn))
	elif accept('apostrophe'):
		ret.append(stringValue())
	elif accept('quote'):
		ret.append(stringValue())
	elif accept('openbracket'):
		code += tkn
		ret.append(expression())
		expect('closedbracket')
		code += ')'
	else:
		error('factor not found at line {},{}, found {}'.format(i,j,currToken))
		nextToken()
	return ret

def term():
	global code
	global currToken
	global i
	ret = ['term']
	ret.append(factor())
	tkntyp = currToken[0]
	tkn = currToken[1]
	while tkntyp == 'asterisk' or tkntyp == 'slash':
		ret.append(tkn)
		code += tkn
		nextToken()
		ret.append(factor())
		tkntyp = currToken[0]
	return ret

def expression():
	global code
	global currToken
	ret = ['expression']
	tkntyp = currToken[0]
	tkn = currToken[1]
	if tkntyp == 'plus' or tkntyp == 'minus':
		code += tkn
		ret.append(tkn)
		nextToken()
	
	ret.append(term())
	tkntyp = currToken[0]
	tkn = currToken[1]
	while tkntyp == 'plus' or tkntyp == 'minus':
		ret.append(tkn)
		code += tkn
		nextToken()
		ret.append(term())
		tkntyp = currToken[0]
		tkn = currToken[1]
	return ret

def callArguments():
	global code
	global currToken
	tkn = currToken[1]
	code += '('
	while not (accept('closedbracket') or accept('closedcbracket')):
		expression()
		if currToken[0]=='comma':
			code += ','
			nextToken()
		tkn = currToken[1]
	code += ')'

def forLoop():
	global code
	global currToken
	if currToken[0] == 'openbracket' or currToken[0] == 'opencbracket':
		nextToken()
		code += '('
		varInit()
		if accept('semicolon'):
			code += ';'
		condition()
		if accept('semicolon'):
			code += ';'
		increment()
		if accept('closedbracket'):
			code += ')\n'
		if accept('opencbracket'):
			block()
		else:
			oneLineBlock()
	else:
		print('for loop needs open bracket')

def varInit():
	global code
	global currToken
	if currToken[0] == 'semicolon' or currToken[0] == 'colon':
			code += ';'
			nextToken()
			return
	while currToken[0] != 'semicolon' and currToken[0] != 'colon':
		expression()
		if currToken[0] == 'comma' or currToken[0] == 'period':
			code += ','
			nextToken()
		elif currToken[0] == 'equals':
			code += '='
			nextToken()

def condition():
	global code
	global currToken
	tkn = currToken[1]
	while currToken[0] in ['identifier', 'number', 'float', 'double', 'less', 'greater', 'equals', 'exclamation']:
		expression()
		if accept('less'):
			if currToken[0]=='equals':
				code += '<='
				nextToken()
			else:
				code += '<'
		elif accept('greater'):
			if currToken[0]=='equals':
				code += '>='
				nextToken()
			else:
				code += '>'
		elif accept('equals'):
			if currToken[0]=='equals':
				code += '=='
				nextToken()
		elif accept('exclamation'):
			if currToken[0]=='equals':
				code += '!='
				nextToken()
		if currToken[0] == 'closedbracket' or currToken[0] == 'closedcbracket':
			code += '0'
		else:
			expression()

def increment():
	global code
	global currToken
	while currToken[0] in ['identifier', 'number', 'float', 'double', 'plus', 'minus', 'equals', 'asteriks', 'slash']:
		code += currToken[1]
		nextToken();

def whileLoop():
	global code
	global currToken
	if accept('openbracket') or accept('opencbracket'):
		code += '('
	condition()
	if accept('closedbracket') or accept('closedcbracket'):
		code += ')\n'
	if accept('opencbracket'):
		block()
	else:
		oneLineBlock()

def ifStatement():
	global code
	global currToken
	if accept('openbracket') or accept('opencbracket'):
		code += '('
	condition()
	if accept('closedbracket') or accept('closedcbracket'):
		code += ')\n'
	if accept('opencbracket'):
		block()
	else:
		oneLineBlock()
	if accept('else'):
		code += 'else '
		if accept('if'):
			code += 'if'
			ifStatement()
		else:
			elseStatement()

def elseStatement():
	global code
	global currToken
	if accept('opencbracket'):
		block()
	else:
		oneLineBlock()
