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

	['ppdirective','include'],
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
