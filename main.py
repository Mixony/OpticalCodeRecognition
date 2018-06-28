#outside libraries
from PIL import Image
import pytesseract
import numpy as np
import sys

#usermade libraries
from constants import *
from parser import *
from utils import output
from image_manipulation import findText
from text_manipulation import *
from tokenizer import *

def main():
	im = findText(resize_width, 'input/text{}.jpg'.format(sys.argv[1]),sys.argv[1])
	im.show()
	text = pytesseract.image_to_string(im, lang=tesseract_language, config=tesseract_config)
	words = separateText(text)
	output(sys.argv[1], words)
	print('\n\nEDITED CODE:')
	tokenList = tokenize(words)
#parse(words)

#text = "#lnclade <s7dio.h>\n#lnclade <stalab.h>\n#lnclade <meth.h>\nint main()\n{\nprintr (\"Paja\");\nfetufn 0;\n}\nvoid pay(int amount)\n{\npfintr (\"%d\",amount);\n}"

if __name__ == '__main__':
	main()
