from constants import *
from utils import *

def tokenize(words):
	tokenList = []
	for line in words:
		tokenLine = []
		for word in line:
			token = findExacts(word)
			tokenLine.append(token)			
		tokenList.append(tokenLine)
		print(tokenLine)
	return tokenList

def findExacts(word):
	for tokenType in tokens:
		for pattern in tokenType[1:]:
			if word == pattern:
				return [tokenType[0],word]
			elif word.lower() == pattern:
				return [tokenType[0],word.lower()]
	if isInt(word):
		return ['number',word]
	if isFloat(word):
		return ['float',word]
	if isDouble(word):
		return ['double',word]
	return ['identifier',word]

