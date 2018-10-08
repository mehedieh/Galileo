#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

try:
	unicode        # Python 2
except NameError:
	unicode = str  # Python 2


def to_str(obj):
	if not isinstance(obj,str):
		return str(obj)


def to_unicode(obj):
	if not isinstance(obj,unicode):
		return unicode(obj)
