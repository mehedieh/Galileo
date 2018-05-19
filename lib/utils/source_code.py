#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

import re

php  = 'PHP'
py   = 'Python'
sh   = 'Shell'
asp  = 'ASP'
aspx = 'ASPX'
rb   = 'Ruby'
java = 'Java'
jsp  = 'JSP'

sources_code = {
	php:(
		r'<\?php .*?\?>',
		r'<\?php\n.*?\?>',
		r'<\?php\r.*?\?>'
		),
	py:(
		r'def .*?\(.*?\)\:',
		r'class .*?[\(.*?\)]\:',
		r'class .*?\:'
		),
	sh:(
		r'#!\/usr\/bin',
		r'#!\/usr',
		r'#!\/bin'
		),
	asp:(
		r'<%.*?%>',
		r'<%\n.*?%>',
		r'<%\r.*?%>'
		),
	aspx:(
		r'<%@.*?%>',
		r'<%@\n.*?%>',
		r'<%@\r.*?%>',
		r'<asp\:.*?%>'
		),
	rb:(
		r'class \w{1,60}\s*<?\s*[a-zA-Z0-9_:]{0,90}.*?\W(def|validates)\s.*?\send($|\W)',
		),
	java:(
		r'import java\.',
		r'public class \w{1,60}\s?\{\s.*\Wpublic',
		r'package\s\w+\;'
		),
	jsp:(
		r'<jsp:.*?>',
		r'<%! .*%>',
		r'<%!\n.*%>',
		r'<%!\r.*%>',
		r'<!--\s*jsp:.*?(--)?>'
		)
}

def source_code(status,content):
	for item in sources_code.items():
		ext,tuple_reg = item
		if status in range(400,499) and content != None:
			for regexp in tuple_reg:
				if re.search(regexp,content):
					return True,ext
	return False,None