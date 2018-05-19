#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

class options(dict):
	def __init__(self,*args,**kwargs):
		self.required = {}
		self.description = {}
		super(options,self).__init__(*args,**kwargs)

	def auto(self,value):
		orig = value
		if value in (None,True,False): return value
		if isinstance(value,str) and value.lower() in ('none','""',"''"):
			return None
		for type_ in (self.r_bool,int,float):
			try:
				value = type_(value)
				break
			except KeyError: pass
			except ValueError: pass
			except AttributeError: pass
		if type(value) is int and '.' in str(orig):
			return float(orig)
		return value

	def __setitem__(self,name,value):
		super(options,self).__setitem__(name,self.auto(value))

	def __delitem__(self,name):
		super(options,self).__delitem__(name)
		if name in self.required:del self.required[name]
		if name in self.description:del self.description[name]

	def r_bool(self,value):
		return {'true':True,'false':False}[value.lower()]

	def i_option(self,name,value=None,required=False,description=''):
		self[name] = value
		self.required[name] = required
		self.description[name] = description