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
		AstToCode(ast)
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
		directive = ['define']+defineVarName()
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
	strVal = ""
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
			strVal += tkn + ' '
			tkn = currToken
			while tkn[0] != 'quote':
				code += tkn[1] + ' '
				strVal += tkn[1] + ' '
				nextToken()
				tkn = currToken
			code = code[:-1]
			code += '\"'
			strVal = strVal[:-1]
			nextToken()
			return ['stringValue','\"'+strVal+'\"']

def globalSpace(vt,t):
	global code
	global currToken
	tkn = currToken[1]
	if accept('semicolon'):
		code += ';'
		return ['variable',vt,t]
	elif accept('equals'):
		code += '='
		eq = ['variable',vt,t,expression()]
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
	body = None
	if accept('closedbracket'):
		code += tkn
	else:
		args.append(argumentsDefinition())
	tkn = currToken[1]
	if accept('opencbracket') or accept('openbracket') or accept('less'):
		code+='\n{\n'
		body=block()
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
	body = ['block']
	while not accept('closedcbracket'):
		tkn = currToken[1]
		if accept('vartype'):
			code += tkn
			code += ' '
			body.append(varDefinition(tkn))
			code += '\n'
		elif accept('return'):
			returnStatement = ['return']
			code += tkn
			if accept('semicolon'):
				code += ';'
				body.append(returnStatement)
				continue
			code += ' '
			returnStatement.append(expression())
			body.append(returnStatement)
			if accept('semicolon'):
				code += ';'
		elif accept('identifier'):
			code += tkn
			ident = tkn
			if accept('openbracket') or accept('opencbracket'):
				functionCall = ['function_call',ident]
				functionCall.append(callArguments())
				if accept('semicolon'):
					code += ';'
				body.append(functionCall)
			elif accept('equals'):
				valueAssigning = ['value_assigning',ident]
				code += '='
				valueAssigning.append(expression())
				if(accept('semicolon')):
					code += ';'
				body.append(valueAssigning)
			code += '\n'
		elif accept('for'):
			code += 'for'
			body.append(forLoop())
		elif accept('while'):
			code += 'while'
			body.append(whileLoop())
		elif accept('if'):
			code += 'if'
			body.append(ifStatement())
		else:
			nextToken()
	return body

def oneLineBlock():
	global code
	global currToken
	tkn = currToken[1]
	ret = ['olblock']
	if accept('vartype'):
			code += tkn
			code += ' '
			ret.append(varDefinition(tkn))
			code += '\n'
	elif accept('return'):
			returnStatement = ['return']
			code += tkn
			if accept('semicolon'):
				code += ';'
				ret.append(returnStatement)
			code += ' '
			returnStatement.append(expression())
			ret.append(returnStatement)
			if accept('semicolon'):
				code += ';'
	elif accept('identifier'):
		code += tkn
		ident = tkn
		if accept('openbracket') or accept('opencbracket'):
			functionCall = ['function_call',ident]
			functionCall.append(callArguments())
			if accept('semicolon'):
				code += ';'
			ret.append(functionCall)
		elif accept('equals'):
			valueAssigning = ['value_assigning',ident]
			code += '='
			valueAssigning.append(expression())
			if(accept('semicolon')):
				code += ';'
			ret.append(valueAssigning)
		code += '\n'
	elif accept('for'):
		code += 'for'
		ret.append(forLoop())
	elif accept('while'):
		code += 'while'
		ret.append(whileLoop())
	elif accept('if'):
		code += 'if'
		ret.append(ifStatement())
	else:
		nextToken()
	return ret

def varDefinition(vt):
	global code
	global currToken
	global j
	variable = ['var_declaration',vt]
	tkn = currToken[1]
	if expect('identifier'):
		code += tkn
		variable.append(tkn)
		tkn = currToken[1]
		if accept('semicolon') or accept('colon'):
			code += ';'
			return variable
		elif accept('equals'):
			code += tkn
			variable.append(expression())
			if accept('semicolon') or accept('colon'):
				code += ';'
			return variable

def factor():
	global code
	global currToken
	global i
	global j
	tkn = currToken[1]
	ret = ['factor']
	if accept('identifier'):
		code += tkn
		ret.append(['identifier',tkn])
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
		ret.append('(')
		ret.append(expression())
		ret.append(')')
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
	arguments = ['arguments']
	tkn = currToken[1]
	code += '('
	while not (accept('closedbracket') or accept('closedcbracket')):
		arguments.append(expression())
		if currToken[0]=='comma':
			code += ','
			nextToken()
		tkn = currToken[1]
	code += ')'
	return arguments

def forLoop():
	global code
	global currToken
	forloop = ['for']
	if currToken[0] == 'openbracket' or currToken[0] == 'opencbracket':
		nextToken()
		code += '('
		forloop.append(varInit())
		if accept('semicolon'):
			code += ';'
		forloop.append(condition())
		if accept('semicolon'):
			code += ';'
		forloop.append(increment())
		if accept('closedbracket'):
			code += ')\n'
		if accept('opencbracket'):
			forloop.append(block())
		else:
			forloop.append(oneLineBlock())
	else:
		print('for loop needs open bracket')
	return forloop

def varInit():
	global code
	global currToken
	ret = ['varInit']
	if currToken[0] == 'semicolon' or currToken[0] == 'colon':
			code += ';'
			nextToken()
			return ret
	while currToken[0] != 'semicolon' and currToken[0] != 'colon':
		ret.append(expression())
		if currToken[0] == 'comma' or currToken[0] == 'period':
			ret.append(',')
			code += ','
			nextToken()
		elif currToken[0] == 'equals':
			ret.append('=')
			code += '='
			nextToken()
	return ret

def condition():
	global code
	global currToken
	tkn = currToken[1]
	ret = ['condition']
	while currToken[0] in ['identifier', 'number', 'float', 'double', 'less', 'greater', 'equals', 'exclamation']:
		ret.append(expression())
		if accept('less'):
			if currToken[0]=='equals':
				ret.append('<=')
				code += '<='
				nextToken()
			else:
				ret.append('<')
				code += '<'
		elif accept('greater'):
			if currToken[0]=='equals':
				ret.append('>=')
				code += '>='
				nextToken()
			else:
				ret.append('>')
				code += '>'
		elif accept('equals'):
			if currToken[0]=='equals':
				ret.append('==')
				code += '=='
				nextToken()
		elif accept('exclamation'):
			if currToken[0]=='equals':
				ret.append('!=')
				code += '!='
				nextToken()
		if currToken[0] == 'closedbracket' or currToken[0] == 'closedcbracket':
			ret.append('0')
			code += '0'
		else:
			ret.append(expression())
	return ret

def increment(): # TODO: WORK ON INCREMENT PARSER
	global code
	global currToken
	ret = ['increment']
	while currToken[0] != 'closedbracket':
		if(currToken[0]=='identifier'):
			ret.append(currToken[1])
			nextToken()
			if(currToken[0] == 'plus'):
				nextToken()
				if(currToken[0]=='plus'):
					ret.append('++')
					nextToken()
				elif(currToken[0]=='equals'):
					ret.append('+=')
					nextToken()
					ret.append(expression())
			elif(currToken[0]=='minus'):
				nextToken()
				if(currToken[0] == 'minus'):
					ret.append('--')
					nextToken()
				elif(currToken[0] == 'equals'):
					ret.append('-=')
					nextToken()
					ret.append(expression())
			elif(currToken[0]=='asterisk'):
				nextToken()
				if(currToken[0] == 'equals'):
					ret.append('*=')
					nextToken()
					ret.append(expression)
			elif(currToken[0] == 'slash'):
				nextToken()
				if(currToken[0]=='equals'):
					ret.append('/=')
					nextToken()
					ret.append(expression)
		code += currToken[1]
	return ret

def whileLoop():
	global code
	global currToken
	ret = ['while']
	if accept('openbracket') or accept('opencbracket'):
		code += '('
	ret.append(condition())
	if accept('closedbracket') or accept('closedcbracket'):
		code += ')\n'
	if accept('opencbracket'):
		ret.append(block())
	else:
		ret.append(oneLineBlock())
	return ret

def ifStatement():
	global code
	global currToken
	retif = ['if']
	retelse = ['else']
	if accept('openbracket') or accept('opencbracket'):
		code += '('
	retif.append(condition())
	if accept('closedbracket') or accept('closedcbracket'):
		code += ')\n'
	if accept('opencbracket'):
		retif.append(block())
	else:
		retif.append(oneLineBlock())
	if accept('else'):
		code += 'else '
		if accept('if'):
			code += 'if'
			retelse.append(ifStatement())
		else:
			retelse.append(elseStatement())
	else:
		return [retif]
	return [retif, retelse]

def elseStatement():
	global code
	global currToken
	if accept('opencbracket'):
		return block()
	else:
		return oneLineBlock()
