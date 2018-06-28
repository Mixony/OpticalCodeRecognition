from constants import *
from utils import *

def parse(words):
	for line in words:
		parseLine(line)

def parseLine(line):
	similarities = checkWord(line[0])
	if(similarities == '#include'):
		print("#include {}".format(checkLibraries(line[1])))
	elif(similarities == 'return'):
		res = []
		for curr in line[1:]:
			res.append(' '+curr)
		print("return {}".format(checkReturn(res)))
	elif(similarities == 'int'):
		print("int {}".format(checkFunction(line[1:])))
	elif(similarities == 'printf'):
		print("printf {}".format(checkPrintf(line[1:])))
	elif(similarities == '{'):
		print(similarities)
	elif(similarities == '}'):
		print(similarities)
	elif(similarities == 'void'):
		print("void {}".format(checkPrintf(line[1:])))

def checkWord(word):
	res = []
	for wrd in first_words:
		similar = 0
		l1 = 0
		l1 = len(wrd) if len(wrd) < len(word) else len(word)
		for i in range(l1):
			if(wrd[i]==word[i].lower()):
				similar+=1
		res.append(similar)
	maxi = 0
	for i in range(len(res)):
		if(res[maxi]<res[i]):
			maxi = i
	return first_words[maxi]

def checkLibraries(word):
	res = []
	for wrd in libraries:
		similar = 0
		l = 0
		if len(wrd) < len(word):
			l = len(wrd)
		else:
			l = len(word)
		for i in range(l):
			if(wrd[i]==word[i]):
				similar+=1
		res.append(similar)
	maxi = 0
	for i in range(len(res)):
		if(res[maxi]<res[i]):
			maxi = i
	return libraries[maxi]

def checkReturn(word):
	retVal = '';
	if(word[0].strip() in ['0','o','O']):
		retVal += '0'
	elif(word[0].strip() in ['1','l','L']):
		retVal += '1'
	if(word[1].strip() in [';',':']):
		retVal += ';'
	else:
		retVal += ';'
	return retVal;

def checkFunction(words):
	res = ''
	for word in words:
		res += word + ' '
	return res

def checkPrintf(words):
	res = ''
	for word in words:
		res += word + ' '
	return res
