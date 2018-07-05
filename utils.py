def unicodeToAscii(text):
	res = ""
	for c in text:		
		if c == u' ':
			res += ' '
		elif c == u'0':
			res += '0'
		elif c == u'1':
			res += '1'
		elif c == u'2':
			res += '2'
		elif c == u'3':
			res += '3'
		elif c == u'4':
			res += '4'
		elif c == u'5':
			res += '5'
		elif c == u'6':
			res += '6'
		elif c == u'7':
			res += '7'
		elif c == u'8':
			res += '8'
		elif c == u'9':
			res += '9'
		elif c == u'a':
			res += 'a'
		elif c == u'b':
			res += 'b'
		elif c == u'c':
			res += 'c'
		elif c == u'd':
			res += 'd'
		elif c == u'e':
			res += 'e'
		elif c == u'f':
			res += 'f'
		elif c == u'g':
			res += 'g'
		elif c == u'h':
			res += 'h'
		elif c == u'i':
			res += 'i'
		elif c == u'j':
			res += 'j'
		elif c == u'k':
			res += 'k'
		elif c == u'l':
			res += 'l'
		elif c == u'm':
			res += 'm'
		elif c == u'n':
			res += 'n'
		elif c == u'o':
			res += 'o'
		elif c == u'p':
			res += 'p'
		elif c == u'q':
			res += 'q'
		elif c == u'r':
			res += 'r'
		elif c == u's':
			res += 's'
		elif c == u't':
			res += 't'
		elif c == u'u':
			res += 'u'
		elif c == u'v':
			res += 'v'
		elif c == u'w':
			res += 'w'
		elif c == u'x':
			res += 'x'
		elif c == u'y':
			res += 'y'
		elif c == u'z':
			res += 'z'
		elif c == u'A':
			res += 'A'
		elif c == u'B':
			res += 'B'
		elif c == u'C':
			res += 'C'
		elif c == u'D':
			res += 'D'
		elif c == u'E':
			res += 'E'
		elif c == u'F':
			res += 'F'
		elif c == u'G':
			res += 'G'
		elif c == u'H':
			res += 'H'
		elif c == u'I':
			res += 'I'
		elif c == u'J':
			res += 'J'
		elif c == u'K':
			res += 'K'
		elif c == u'L':
			res += 'L'
		elif c == u'M':
			res += 'M'
		elif c == u'N':
			res += 'N'
		elif c == u'O':
			res += 'O'
		elif c == u'P':
			res += 'P'
		elif c == u'Q':
			res += 'Q'
		elif c == u'R':
			res += 'R'
		elif c == u'S':
			res += 'S'
		elif c == u'T':
			res += 'T'
		elif c == u'U':
			res += 'U'
		elif c == u'V':
			res += 'V'
		elif c == u'W':
			res += 'W'
		elif c == u'X':
			res += 'X'
		elif c == u'Y':
			res += 'Y'
		elif c == u'Z':
			res += 'Z'
		elif c == u':':
			res += ':'
		elif c == u';':
			res += ';'
		elif c == u'{':
			res += '{'
		elif c == u'}':
			res += '}'
		elif c == u'(':
			res += '('
		elif c == u')':
			res += ')'
		elif c == u'<':
			res += '<'
		elif c == u'>':
			res += '>'
		elif c == u'''\'''':
			res += '''\''''
		elif c == u'''\"''':
			res += '''\"'''
		elif c == u'#':
			res += '#'
		elif c == u'.':
			res += '.'
		elif c == u',':
			res += ','
		elif c == u'%':
			res += '%'
		elif c == u'=':
			res += '='
		elif c == u'+':
			res += '+'
		elif c == u'-':
			res += '-'
		elif c == u'*':
			res += '*'
		elif c == u'/':
			res += '/'
		elif c == u'!':
			res += '!'
	return res

def output(number, words):
	open('output/out{}.txt'.format(number), "w").close()
	f = open('output/out{}.txt'.format(number),'a+')
	for i in range(len(words)):
		st = ''
		for j in range(len(words[i])):
			st+=words[i][j]+' '
			f.write("{}\n".format(words[i][j]))
		print(st)

def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def isFloat(s):
    try: 
        float(s[0:-1])
        if s[-1] not in ['0','1','2','3','4','5','6','7','8','9']:
        	return True
        return False
    except ValueError:
        return False

def isDouble(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

def outputTokens(tokenList):
	for tokenLine in tokenList:
		print(tokenLine)
