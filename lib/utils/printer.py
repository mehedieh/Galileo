#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

from lib.utils.colors import *

def plus(STRING,FLAG='[+]'):
	# [+] Plus
	print("{}{}{} {}{}{}".format(
		G%1,FLAG,E,W%0,STRING,E)
	)

def plus2(STRING,FLAG='[+]'):
	# [+] Plus
	print("{}{}{} {}{}{}".format(
		G%1,FLAG,E,G%0,STRING,E)
	)

def less(STRING,FLAG='[-]'):
	# [-] Less
	print("{}{}{} {}{}{}".format(
		R%1,FLAG,E,W%0,STRING,E)
	)

def less2(STRING,FLAG='[-]'):
	# [-] Less
	print("{}{}{} {}{}{}".format(
		R%1,FLAG,E,R%0,STRING,E)
	)

def warn(STRING,FLAG='[!]'):
	# [!] Warn
	print("{}{}{} {}{}{}".format(
		R%1,FLAG,E,R%0,STRING,E)
	)

def warn2(STRING,FLAG='[!]'):
	# [!] Warn
	print("{}{}{} {}{}{}".format(
		R%1,FLAG,E,R%1,STRING,E)
	)

def test(STRING,FLAG='[*]'):
	# [*] Test
	print("{}{}{} {}{}{}".format(
		B%1,FLAG,E,W%0,STRING,E)
	)

def test2(STRING,FLAG='[*]'):
	# [*] Test
	print("{}{}{} {}{}{}".format(
		B%1,FLAG,E,B%0,STRING,E)
	)

def info(STRING,FLAG='[i]'):
	# [i] Info
	print("{}{}{} {}{}{}".format(
		Y%1,FLAG,E,W%0,STRING,E)
	)

def info2(STRING,FLAG='[i]'):
	# [i] Info
	print("{}{}{} {}{}{}".format(
		Y%1,FLAG,E,Y%0,STRING,E)
	)

def more(STRING,name):
	if 'is_status' in name.lower():
		print(' {}\_{} {}Status Code:{} {}'.format(
			C%1,E,G%1,E,STRING)
		)
	if 'is_headers' in name.lower():
		print(' {}\_{} {}Headers:{}'.format(C%1,E,G%1,E))
		if isinstance(STRING,dict):
			for key in STRING.keys():
				print('  | {} : {}'.format(key,STRING[key]))
	if 'is_content' in name.lower():
		print('-'*15+'=[ Content ]='+'-'*18)
		print(STRING)
		print('-'*15+'=[ End Content ]='+'-'*15)
	if 'is_other' in name.lower():
		print(' {}\_{} {}'.format(
			C%1,E,STRING))