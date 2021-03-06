from constants import *
from utils import *
import nltk

def tokenize(words):
	tokenList = []
	for line in words:
		tokenLine = []
		for word in line:
			token = findExacts(word)
			tokenLine.append(token)			
		tokenList.append(tokenLine)
	tokenList[-1].append(['eof','eof'])
	return tokenList

def findExacts(word):
	if isInt(word):
		return ['number',word]
	if isFloat(word):
		return ['float',word]
	if isDouble(word):
		return ['double',word]
	for tokenType in tokens:
		for pattern in tokenType[1:]:
			if word == pattern:
				return [tokenType[0],word]
			elif word.lower() == pattern:
				return [tokenType[0],word.lower()]
	return ['identifier',word]

