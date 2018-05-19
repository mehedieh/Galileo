#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

import re
from lib.utils.printer import *

def errors(content,url):
	patterns = (
		r"<font face=\"Arial\" size=2>error \'800a0005\'</font>",
		r"<h2> <i>Runtime Error</i> </h2></span>",
		r"<p>Active Server Pages</font> <font face=\"Arial\" size=2>error \'ASP 0126\'</font>",
		r"<b> Description: </b>An unhandled exception occurred during the execution of the",
		r"<H1>Error page exception</H1>",
		r"<h2> <i>Runtime Error</i> </h2></span>",
		r"<h2> <i>Access is denied</i> </h2></span>",
		r"<H3>Original Exception: </H3>",
		r"Server object error",
		r"invalid literal for int()",
		r"exceptions.ValueError",
		r"\[an error occurred while processing this directive\]",
		r"<HTML><HEAD><TITLE>Error Occurred While Processing Request</TITLE>",
		r"</HEAD><BODY><HR><H3>Error Occurred While Processing Request</H3><P>",
		r"\[java.lang.",
		r"class java.lang.",
		r"java.lang.NullPointerException",
		r"java.rmi.ServerException",
		r"at java.lang.",
		r"onclick=\"toggle(\'full exception chain stacktrace\')",
		r"at org.apache.catalina",
		r"at org.apache.coyote.",
		r"at org.apache.tomcat.",
		r"at org.apache.jasper.",
		r"<html><head><title>Application Exception</title>",
		r"<p>Microsoft VBScript runtime </font>",
		r"<font face=\"Arial\" size=2>error '800a000d'</font>",
		r"<TITLE>nwwcgi Error",
		r"\] does not contain handler parameter named",
		r"PythonHandler django.core.handlers.modpython",
		r"t = loader.get_template(template_name) # You need to create a 404.html template.",
		r"<h2>Traceback <span>(innermost last)</span></h2>",
		r"<h1 class=\"error_title\">Ruby on Rails application could not be started</h1>",
		r"<title>Error Occurred While Processing Request</title></head><body><p></p>",
		r"<HTML><HEAD><TITLE>Error Occurred While Processing Request</TITLE></HEAD><BODY><HR><H3>",
		r"<TR><TD><H4>Error Diagnostic Information</H4><P><P>",
		r"<li>Search the <a href=\"http://www.macromedia.com/support/coldfusion/\"",
		r"target=\"new\">Knowledge Base</a> to find a solution to your problem.</li>",
		r"Server.Execute Error",
		r"<h2 style=\"font:8pt/11pt verdana; color:000000\">HTTP 403.6 - Forbidden: IP address rejected<br>",
		r"<TITLE>500 Internal Server Error</TITLE>",
		r"<b>warning</b>[/]\w\/\w\/\S*",
		r"<b>Fatal error</b>:",
		r"<b>Warning</b>:",
		r"open_basedir restriction in effect",
		r"eval()'d code</b> on line <b>",
		r"Fatal error</b>:  preg_replace",
		r"thrown in <b>",
		r"Stack trace:",
		r"</b> on line <b>"
		)
	for err in patterns:
		if re.search(err,content):
			plus2('%s was found in: %s'%(err,url))