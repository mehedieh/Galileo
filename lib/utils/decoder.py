#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

def to_str(obj):
	if not isinstance(obj,str):
		return str(obj)

def to_unicode(obj):
	if not isinstance(obj,unicode):
		return unicode(obj)