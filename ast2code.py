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
	if(ast[0] == 'program'):
		astProgram(ast[1:])
	'''print(astIncludes)
	print(astFlags)'''
	print(astVariables)
	'''print(astFunctions)'''
	print(astCode)

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
	# TODO: do args formatting and add them to the vars
	astCode += func[0] + ' ' + func[1] + '()\n'
	if(len(func) == 4):
		astCode += '{\n'
		if(func[3][0] == 'block'):
			astBlock(func[3][1:])
		astCode += '}\n'
	else:
		astCode += ';\n'

def astBlock(blck):
	global astLevel
	astLevel += 1
	for elem in blck:
		if elem[0] == 'var_declaration':
			astVariableDeclaration(elem[1:])
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
	i=0 # WARNING: JUST PLACEHOLDER
	return