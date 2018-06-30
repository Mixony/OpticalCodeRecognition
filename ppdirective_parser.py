import nltk

from constants import *

def parsePPDirective(tokenLine):
	directive = tokenLine[0]
	if directive[0] == 'ppdirective':
		if directive[1] == 'include':
			return "include {}".format(parseInclude(tokenLine[1:]))
	'''else: 
		tokenString = ''
		for token in tokenLine:
			tokenString+=token[1]+' '
		print(tokenString)'''

def parseInclude(tokenList):
	if tokenList[0][1] in ['(','<','{'] and tokenList[-1][1] in [')','>','}'] :
		return "<{}>".format(parseSystemHeader(tokenList[1:-1]))
	elif tokenList[0][1] in ['\'','\"','`']:
		return "\"{}\"".format(parseSystemHeader(tokenList[1:-1]))

def parseSystemHeader(tokenList):
	if tokenList[0][0] == 'system_library':
		print('Parser')
		return tokenList[0][1]
	return similarityToSystemHeader(tokenList[0])

def similarityToSystemHeader(headerName):
	mindistance = [0, nltk.edit_distance(system_libraries[0],headerName[1])]
	for i in range(2,len(system_libraries),2):
		tmp = nltk.edit_distance(system_libraries[i],headerName[1])	
		if mindistance[1] > tmp:
			mindistance=[i,tmp]
	return system_libraries[mindistance[0]]
