tab = 0

def AstToCode(ast):
	print(ast)

def printAST(ast):
	# global tab
	# for node in ast:
	# 	if type(node) is list:
	# 		tab += 1
	# 		printAST(node)
	# 		tab -= 1
	# 	else:
	# 		print('|\n+'+('='* tab)+str(node))
	global tab
	for node in ast:
		if type(node) is list:
			tab += 1
			printAST(node)
			tab -= 1
		else:
			print(('\t'*tab)+str(node))