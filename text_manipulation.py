from utils import *
from constants import special_characters

def separateText(text):
	lines = separateSpecialCharacters(separateLines(text))
	words = separateWords(lines)
	return words

def separateLines(text):
	lines = text.split('\n')
	while True:
		if '' not in lines:
			break
		lines.remove('')
	return lines

def separateSpecialCharacters(lines):
	for i in range(len(lines)):
		if(len(lines[i]) is 1):
			continue
		line = list(lines[i])
		lines[i] = ''
		for j in range(len(line)):
			if line[j] in ['<','>','(',')','{','}','#','\'','\"',';',':',',','+','-','*','/', '=']:
				if j>0:
					if line[j-1] is not ' ':
						lines[i]+=' '
				lines[i]+=line[j]
				if j<len(line)-1:
					if line[j+1] is not ' ':
						lines[i]+=' '
			else:
				lines[i]+=line[j]
	return lines

def separateWords(lines):
	for i in range(len(lines)):
		lines[i]=unicodeToAscii(lines[i]).split(' ')
		while '' in lines[i]:
			lines[i].remove('')
	return lines

