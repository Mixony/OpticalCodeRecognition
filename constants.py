resize_width = 720

diff = 20

tesseract_config = r"""-psm 6 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#%\'\"<>(){};:,.=+-*/\\"""
tesseract_language = "eng"

tokens = [	
	
	['system_library','assert.h','complex.h','ctype.h','errno.h','fenv.h','float.h',
	'inttypes.h','iso646.h','limits.h','locale.h','math.h','setjmp.h','signal.h',
	'stdalign.h','stdarg.h','stdatomic.h','stdbool.h','stddef.h','stdint.h','stdio.h',
	'stdlib.h','stdnoreturn.h','string.h','tgmath.h','threads.h','time.h','uchar.h',
	'wchar.h','wctype.h'],
	['include', 'include'], 
	['define', 'define'], 
	['undef' , 'undef'], 
	['ifdef','ifdef'], 
	['ifndef','ifndef'], 
	['if','if'],
	['error','error'],
	['vartype', 'int', 'float', 'double', 'void', 'char'],
	['return','return'],
	['opencbracket','{'],
	['closedcbracket','}'],
	['openbracket','('],
	['closedbracket',')'],
	['quote','\"'],
	['apostrophe','\''],
	['semicolon',';'],
	['colon',':'],
	['hashtag','#'],
	['greater','>'],
	['less','<'],
	['equals','='],
	['graveaccent','`'],
	['opensbracket','['],
	['closedsbracket',']'],
	['comma',','],
	['period','.'],
	['plus','+'],
	['minus','-'],
	['asterisk','*'],
	['slash','/'],
	['exclamation','!'],
	['if','if'],
	['for','for'],
	['while','while'],
	['else','else']

]

system_libraries = [

	'assert.h',[],
	'complex.h',[],
	'ctype.h',[],
	'errno.h',[],
	'fenv.h',[],
	'float.h',[],
	'inttypes.h',[],
	'iso646.h',[],
	'limits.h',[],
	'locale.h',[],
	'math.h',[],
	'setjmp.h',[],
	'signal.h',[],
	'stdalign.h',[],
	'stdarg.h',[],
	'stdatomic.h',[],
	'stdbool.h',[],
	'stddef.h',[],
	'stdint.h',[],
	'stdio.h',[],
	'stdlib.h',[],
	'stdnoreturn.h',[],
	'string.h',[],
	'tgmath.h',[],
	'threads.h',[],
	'time.h',[],
	'uchar.h',[],
	'wchar.h',[],
	'wctype.h',[]

]
