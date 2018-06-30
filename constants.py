resize_width = 720

diff = 20

tesseract_config = r"""-c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ#%\'\"<>(){};:,."""
tesseract_language = "eng"

keywords = ['auto','break','case','char','const','continue','default','do','double','else','enum','extern','float','for','goto',
'if','int','long','register','return','short','signed','sizeof','static','struct','switch','typedef','union','unsigned','void',
'volatile','while']
preprocessor = ['#define','#elif','#else','#endif''#error','#if','#ifdef','#ifndef','#include','#line','#pragma','#undef']

first_words = ['#include', 'int', 'return', 'printf', '{', '}', 'void']

syntax=[
['#include', 'library'],
['variable', 'name', '(', 'arguments', ')'],
['{'],
['}'],
['function', '(', 'arguments', ')', ';'],
['return', 'value', ';']
]

variableTypes=['int', 'float', 'double', 'char', 'void']
libraries = ['<stdio.h>','<stdlib.h>','<math.h>']


special_characters = ['<','>','(',')','{','}','#','\'','\"',';',':']

tokens = [	
	
	['system_library','assert.h','complex.h','ctype.h','errno.h','fenv.h','float.h',
	'inttypes.h','iso646.h','limits.h','locale.h','math.h','setjmp.h','signal.h',
	'stdalign.h','stdarg.h','stdatomic.h','stdbool.h','stddef.h','stdint.h','stdio.h',
	'stdlib.h','stdnoreturn.h','string.h','tgmath.h','threads.h','time.h','uchar.h',
	'wchar.h','wctype.h'],
	['ppdirective', 'include', 'define', 'undef ', 'ifdef', 'ifndef', 'if', 'error'],
	['varname', 'int', 'float', 'double', 'void' ],
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
	['equals','=']

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

included_libraries = [

	

]
