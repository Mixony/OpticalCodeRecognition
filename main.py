#outside libraries
from PIL import Image
import pytesseract
import numpy as np
import sys

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
	# print(text+'\n\n')
	words = separateText(text)
	output(sys.argv[1], words)
	print('\nEDITED CODE:\n')
	tokenList = tokenize(words)
	outputTokens(tokenList)
	importTokenList(tokenList)
	code = program()
	
	
#text = "#lnclade <s7dio.h>\n#lnclade <stalab.h>\n#lnclade <meth.h>\nint main()\n{\nprintr (\"Paja\");\nfetufn 0;\n}\nvoid pay(int amount)\n{\npfintr (\"%d\",amount);\n}"

if __name__ == '__main__':
	main()
