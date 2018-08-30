import nltk

tab = 0

astIncludes = []
astFlags = []
astVariables = []
astFunctions = []
astCode = ''
astLevel = 0

def printAST(ast):
	global tab
	for node in ast:
		if type(node) is list:
			tab += 1
			printAST(node)
			tab -= 1
		else:
			print(('\t'*tab)+str(node))

def AstToCode(ast):
	global astCode
	if(ast[0] == 'program'):
		astProgram(ast[1:])
	if astCode[-1] == '\n':
		return astCode[:-1]
	return astCode

def astProgram(prog):
	global astCode
	for elem in prog:
		if(elem[0] == 'include'):
			astCode += '#include '
			astInclude(elem[1])
		elif(elem[0] == 'define'):
			astCode += '#define '
			astDefine(elem[1:])
		elif(elem[0] == 'variable'):
			astGlobalVariable(elem[1:])
		elif(elem[0] == 'function'):
			astFunction(elem[1])

def astInclude(incl):
	if(incl[0] == 'system'):
		astSysInclude(incl[1])
	elif(incl[0] == 'user'):
		astUserInclude(incl[1])

def astSysInclude(name):
	global astIncludes
	global astCode
	astIncludes.append( [ 'system' , name[0] ] )
	# TODO: check for name
	astCode+=('<{}>\n'.format(name[0]))

def astUserInclude(name):
	global astIncludes
	global astCode
	astIncludes.append( [ 'user' , name[0] ] )
	# TODO: check for name
	astCode+=('"{}"\n'.format(name[0]))

def astDefine(defn):
	global astFlags
	global astVariables
	global astCode
	if(len(defn) == 1):
		astFlags.append(defn)
		astCode += '{}\n'.format(defn[0])
	elif(len(defn) == 2):
		astVariables.append([0,'',defn[0]])
		astCode += '{} '.format(defn[0])
		if(defn[1][0]=='expression'):
			astExpression(defn[1][1:])
		astCode += '\n'
		
def astGlobalVariable(vari):
	global astVariables
	global astCode
	astVariables.append([0,vari[0],vari[1]])
	astCode += vari[0] + ' ' + vari[1]
	if(len(vari) == 3):
		astCode += ' = '
		if(vari[2][0] == 'expression'):
			astExpression(vari[2][1:])
	astCode += ';\n'

def astFunction(func):
	global astFunctions
	global astCode
	astFunctions.append(func[0:3])
	astCode += func[0] + ' ' + func[1] + '('
	if(func[2][0] == 'args'):
		astArguments(func[2][1])
	astCode += ')\n'
	if(len(func) == 4):
		astCode += '{\n'
		if(func[3][0] == 'block'):
			astBlock(func[3][1:])
		astCode += '}\n'
	else:
		astCode += ';\n'

def astArguments(args):
	global astCode
	global astLevel
	global astVariables
	for arg in args:
		astCode += arg[0] + ' ' + arg[1] + ', '
		astVariables.append([astLevel+1,arg[0],arg[1]])
	astCode= astCode[:-2]

def astBlock(blck):
	global astLevel
	astLevel += 1
	for elem in blck:
		if elem[0] == 'var_declaration':
			astVariableDeclaration(elem[1:])
		elif elem[0] == 'return':
			if(len(elem)==1):
				astReturn([])
			else:
				astReturn(elem[1])
		elif elem[0] == 'function_call':
			astFunctionCall(elem[1:])
		elif elem[0] == 'for':
			astForLoop(elem[1:])
		elif elem[0] == 'while':
			astWhileLoop(elem[1:])
		elif elem[0] == 'ifelse':
			astIfStatement(elem[1:])
		elif elem[0] == 'value_assigning':
			astWhileLoop(elem[1:])
	removeVariables()
	astLevel -= 1

def astExpression(expr):
	global astCode
	for elem in expr:
		if elem[0] == 'term':
			astTerm(elem[1:])
		elif elem[0] == '+' or elem[0] == '-':
			astCode += elem[0]

def astTerm(term):
	global astCode
	for elem in term:
		if elem[0] == 'factor':
			astFactor(elem[1:])
		elif elem[0] == '*' or elem[0] == '/':
			astCode += elem[0]

def astFactor(fact):
	global astCode
	global astVariables
	if(fact[0]=='('):
		astCode += '('
		if(fact[1][0]=='expression'):
			astExpression(fact[1][1:])
		astCode += ')'
	elif(fact[0][0] == 'expression'):
		astExpression(fact[0][1:])
	elif(fact[0][0] == 'intValue'):
		astCode += fact[0][1]
	elif(fact[0][0] == 'floatValue'):
		astCode += fact[0][1]
	elif(fact[0][0] == 'doubleValue'):
		astCode += fact[0][1]
	elif(fact[0][0] == 'charValue'):
		astCode += fact[0][1]
	elif(fact[0][0] == 'stringValue'):
		astCode += fact[0][1]
	elif(fact[0][0] == 'identifier'):
		for var in astVariables:
			if var[2] == fact[0][1]:
				astCode += fact[0][1]
				break
		else:
			print('ERROR WITH VARIABLE '+fact[0][1])
			correctIdent(fact[0][1])
		#CHECK IF VARIABLE IS
		#AVAILABLE TO USE

def astVariableDeclaration(vari):
	global astVariables
	global astLevel
	global astCode
	astVariables.append([astLevel,vari[0],vari[1]])
	astCode += vari[0] + ' ' + vari[1]
	if(len(vari)==3):
		astCode += ' = '
		if(vari[2][0] == 'expression'):
			astExpression(vari[2][1:])
	astCode += ';\n'

def astReturn(rtrn):
	global astCode
	astCode += 'return'
	if(len(rtrn)>0):
		if(rtrn[0]=='expression'):
			astCode += ' '
			astExpression(rtrn[1:])
	astCode += ';\n'
	return

def astFunctionCall(call):
	global astCode
	astCode += call[0] + '('
	if(call[1][0] == 'args'):
		if(len(call[1])>1):
			astFunctionCallArgs(call[1][1:])
	astCode += ');\n'

def astFunctionCallArgs(args):
	global astCode
	for arg in args[:-1]:
		if(arg[0] == 'expression'):
			astExpression(arg[1:])
			astCode += ', '
	if(args[len(args)-1][0] == 'expression'):
		astExpression(args[len(args)-1][1:])

def astForLoop(loop):
	global astCode
	astCode += 'for('
	init = loop[0]
	if len(init)>1:
		if init[0] == 'var_init':
			astVarInit(init[1:])
	astCode += ';'
	cond = loop[1]
	if len(cond)>1:
		if cond[0] == 'condition':
			astCondition(cond[1:])
	astCode += ';'
	incr = loop[2]
	if len(incr)>1:
		if incr[0] == 'increment':
			astIncrement(incr[1:])
	astCode+= ')\n'
	blck = loop[3]
	if blck[0] == 'block':
		astCode += '{\n'
		astBlock(blck[1:])
		astCode += '}\n'
	elif blck[0] == 'olblock':
		astOneLineBlock(blck[1])

def astVarInit(init):
	global astCode
	for elem in init:
		if elem == '=':
			astCode += '='
		elif elem == ',':
			astCode += ', '
		elif elem[0] == 'expression':
			astExpression(elem[1:])

def astCondition(cond):
	global astCode
	for elem in cond:
		if elem == '==':
			astCode += '=='
		elif elem == '!=':
			astCode += '!='
		elif elem == '<':
			astCode += '<'
		elif elem == '<=':
			astCode += '<='
		elif elem == '>':
			astCode += '>'
		elif elem == '>=':
			astCode += '>='
		elif elem[0] == 'expression':
			astExpression(elem[1:])

def astIncrement(incr):
	global astCode
	for elem in incr:
		if elem == '++':
			astCode += '++'
		elif elem == '--':
			astCode += '--'
		elif elem == '+=':
			astCode += '+='
		elif elem == '-=':
			astCode += '-='
		elif elem == '*=':
			astCode += '*='
		elif elem == '/=':
			astCode += '/='
		elif elem[0] == 'expression':
			astExpression(elem[1:])
		elif elem[0] == 'factor':
			if(elem[1][0] == 'identifier'):
				astCode += elem[1][1]

def astOneLineBlock(blck):
	global astLevel
	astLevel += 1
	if blck[0] == 'var_declaration':
		astVariableDeclaration(blck[1:])
	elif blck[0] == 'return':
		if(len(blck)==1):
			astReturn([])
		else:
			astReturn(blck[1])
	elif blck[0] == 'function_call':
		astFunctionCall(blck[1:])
	elif blck[0] == 'for':
		astForLoop(blck[1:])
	elif blck[0] == 'while':
		astWhileLoop(blck[1:])
	elif blck[0] == 'ifelse':
		astIfStatement(blck[1:])
	elif blck[0] == 'value_assigning':
		astValueAssign(blck[1:])
	removeVariables()
	astLevel -= 1

def astWhileLoop(loop):
	global astCode
	cond = loop[0]
	body = loop[1]
	astCode += 'while('
	if(cond[0] == 'condition'):
		astCondition(cond[1:])
	astCode += ')\n'
	if(body[0] == 'block'):
		astBlock(body[1:])
	elif(body[0] == 'olblock'):
		astOneLineBlock(body[1])

def astValueAssign(vala):
	global astCode
	name = vala[0]
	valu = vala[1]
	astCode += name + ' = ' 
	if valu[0] == 'expression':
		astExpression(valu[1:])
	astCode += ';\n'

def astIfStatement(stat):
	global astCode
	temp = stat[0]
	if temp[0] == 'if':
		astCode += 'if('
		ifpt = temp[1:]
		cond = ifpt[0]
		if cond[0] == 'condition':
			astCondition(cond[1:])
		astCode += ')\n'
		body = ifpt[1]
		if body[0] == 'block':
			astCode += '{\n'
			astBlock(body[1:])
			astCode += '}\n'
		elif body[0] == 'olblock':
			astOneLineBlock(body[1])
	if len(stat) > 1:
		temp = stat[1]
		if temp[0] == 'else':
			astElseStatement(temp[1])

def astElseStatement(stat):
	global astCode
	astCode += 'else'
	if(stat[0] == 'ifelse'):
		astCode += ' '
		astIfStatement(stat[1:])
	else:
		astCode += '\n'
		if(stat[0] == 'block'):
			astCode += '{\n'
			astBlock(stat[1])
			astCode += '}\n'
		elif(stat[0] == 'olblock'):
			astOneLineBlock(stat[1])

def removeVariables():
	global astVariables
	global astLevel
	tmps = []
	for var in astVariables:
		if int(var[0]) < astLevel:
			tmps.append(var)
	astVariables = tmps

def correctIdent(iden):
	global astVariables
	global astCode

	for var in astVariables:
		if nltk.edit_distance(var[2],iden) < len(iden):
			#TODO: DONT USE FIRST SIMILAR NAME 
			#TODO: CHECK FOR MOST SIMILAR
			astCode += var[2]
			break
	else:
		for char in iden:
			if char in ['D', 'O', 'Q', 'a', 'o', 'U', 'u', 'n']:
				astCode += '0'
			elif char in ['I', 'J', 'L', 'i', 'j', 'l']:
				astCode += '1'
			elif char in ['Z', 'z']:
				astCode += '2'
			elif char in ['E', 'e']:
				astCode += '3'
			elif char in ['A', 'X', 'x']:
				astCode += '4'
			elif char in ['S', 's']:
				astCode += '5'
			elif char in ['G', 'b', 'd', 'C', 'c', 'h']:
				astCode += '6'
			elif char in ['T', 'Y', 't', 'y', 'f']:
				astCode += '7'
			elif char in ['B', 'R']:
				astCode += '8'
			elif char in ['g', 'q', 'P', 'p']:
				astCode += '9'
			else:
				astCode += '3';
