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
	j+=1
	if j >= len(tokenList[i]):
		j=0
		i+=1
	currToken = tokenList[i][j]

def error(msg):
	print(msg)

def accept(token):
	global currToken
	if token[0] == currToken[0] and token[1] == currToken[1]:
		nextToken()
		return True
	return False

def expect(token):
	global currToken
	if accept(token):
		return True
	error('Token {} is expected'.format(token[0]))
	return False

def program():
	global code
	global tokenList
	global currToken
	nextToken()
	while i <= len(tokenList):
		tkn = currToken[1]
		if accept(['hashtag','#']) :
			code+='#'
			ppdirective()
#		elif accept(['vartype',tkn]):
#			print(tkn)
		else:
			break
		
		code+='\n'
	print(code)

def ppdirective():
	global code
	if(accept(['ppdirective','include'])):
		code+='include '
		includeStatement()
	elif(accept(['ppdirective','define'])):
		defineStatement()

def includeStatement():
	global code
	if(accept(['less','<']) or accept(['openbracket','(']) or accept(['opencbracket','{'])):
		code += '<'
		systemHeader()
		code += '>'
		nextToken()
	elif(accept(['quote','\"']) or accept(['apostrophe','\'']) or accept(['graveaccent','`'])):
		code += '\"'
		usermadeHeader()
		code += '\"'
		nextToken()

def systemHeader():
	global code	
	global currToken
	tkn = currToken[1]
	if accept(['system_library', tkn]):
		code += tkn
	else:
		print('Couldnt recognize library name')

def usermadeHeader():
	global code
	global currToken
	code += currToken[1]
	nextToken()

def defineStatement():
	global code
	code += 'define '
	ppVar()
	
def ppVar():
	global code
	global currToken
	global j
	tkn = currToken[1]
	if(expect(['identifier',tkn])):
		code += tkn + ' '
		if j == 0:
			return
		tkn = currToken[1]
		varValue()

def varValue():
	global code
	global currToken
	tkn = currToken[1]
	if(accept(['number',tkn])):
		intValue(tkn);
		return
	elif accept(['float',tkn]):
		floatValue()
		return
	elif accept(['double',tkn]):
		doubleValue()
		return
	elif accept(['apostrophe','\'']) or accept(['graveaccent','`']) or accept(['quote','\"']):
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
	if accept(['identifier',tkn]) or accept(['number',tkn]) :
		if len(tkn)==1:
			code += '\''
			code += tkn
			code += '\''
		else:
			code += '\"'
			code += tkn
			code += '\"'