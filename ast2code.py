tab = 0

astIncludes = []
astFlags = []
astVariables = []
astFunctions = []
code = ''

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
	print(astIncludes)
	print(astFlags)
	print(astVariables)
	print(astFunctions)
	print(code)

def astProgram(prog):
	global code
	for elem in prog:
		if(elem[0] == 'include'):
			code += '#include '
			astInclude(elem[1])
		elif(elem[0] == 'define'):
			code += '#define '
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
	global code
	astIncludes.append( [ 'system' , name[0] ] )
	# TODO: check for name
	code+=('<{}>\n'.format(name[0]))

def astUserInclude(name):
	global astIncludes
	global code
	astIncludes.append( [ 'user' , name[0] ] )
	# TODO: check for name
	code+=('"{}"\n'.format(name[0]))

def astDefine(defn):
	global astFlags
	global astVariables
	global code
	if(len(defn) == 1):
		astFlags.append(defn)
		code += "{}\n".format(defn[0])
	elif(len(defn) == 2):
		astVariables.append(defn)
		code += "{} ".format(defn[0])
		if(defn[1][0]=='expression'):
			astExpression(defn[1][1:])
		
def astGlobalVariable(vari):
	global astVariables
	global code
	astVariables.append([vari[0],vari[1]])
	# TODO: check value if it's set
	code += ''

def astFunction(func):
	global astFunctions
	global code
	astFunctions.append(func[0:3])
	# TODO: check for args and body of function

def astExpression(expr):
	global code
	print("EXPRESSION")
	print(expr)
	for elem in expr:
		if elem[0] == 'term':
			astTerm(elem[1:])
		elif elem[0] == '+' or elem[0] == '-':
			code += elem[0]

def astTerm(term):
	global code
	print("TERM")
	print(term)
	for elem in term:
		if elem[0] == 'factor':
			astFactor(elem[1:])
		elif elem[0] == '*' or elem[0] == '/':
			code += elem[0]

def astFactor(fact):
	global code
	print('FACTOR')
	print(fact)
	if(fact[0]=='('):
		code += '('
		if(fact[1][0]=='expression'): # and fact[2] == ')'
			astExpression(fact[1])
	return
