#outside libraries
from PIL import Image
import pytesseract
import numpy as np
import sys
import nltk

#usermade libraries
from constants import *
from utils import output
from image_manipulation import *
from text_manipulation import *
from tokenizer import *
from parser2 import *

def main():
	im = preprocessImage(resize_width, 'input/text{}.jpg'.format(sys.argv[1]),sys.argv[1])
	text = pytesseract.image_to_string(im, lang=tesseract_language, config=tesseract_config)
	print('TEXT:\n'+text)
	words = separateText(text)
	tokenList = tokenize(words)
	importTokenList(tokenList)
	ast = program()
	code = AstToCode(ast)
	print('CODE:\n'+code)
	outputResults(text, code)

def outputResults(text, code):
	with open('test/text{}.txt'.format(sys.argv[1]), 'r') as f:
		data = f.read()
		print('DATA:\n'+data)
		print('Difference between tesseract and real text is:')
		print(nltk.edit_distance(text,data))
		print('Difference between optimization and real text is:')
		print(nltk.edit_distance(code,data))
		for i in range(len(code)):
			if code[i] != data[i]:
				print(code[i]+'\t\t\t'+data[i])

if __name__ == '__main__':
	main()
