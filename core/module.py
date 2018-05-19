#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

from __future__ import print_function
import hmac,os,re,sys
import struct,textwrap
from lib.utils.printer import *
from core.framework import *
from lib.utils.options import *
from lib.utils.settings import *

class BaseModule(framework):
	def __init__(self,params,query=None):
		framework.__init__(self,params)
		self.options = options()
		if self.info.get('options'):
			for option in self.info.get('options'):
				self.r_option(*option)
		self._reload = 0

	def show_source(self):
		for path in [os.path.join(x,'modules',self.module_name)+'.py' for x in (self.tool_path,self.tool_home)]:
			if os.path.exists(path):
				filename = path
		with open(filename) as f:
			content = f.readlines()
			nums = [str(x) for x in range(1,len(content)+1)]
			num_len = len(max(nums,key=len))
			for num in nums:
				print('%s|%s'%(num.rjust(num_len),content[int(num)-1]),end='')
			print('')

	def show_info(self):
		self.info['path'] = os.path.join('modules',self.module_name)+'.py'
		print('')
		for item in ['name','path','author','version']:
			if self.info.get(item):
				print('%s: %s'%(item.title().rjust(10),self.info[item]))
		print('')
		if 'description' in self.info:
			print('Description:')
			print('%s%s\n'%(spacer,textwrap.fill(self.info['description'])))
		print('Options:',end='')
		self.show_options()
		if 'comments' in self.info:
			print('Comments:')
			for comment in self.info['comments']:
				prefix = '* '
				if comment.startswith('\t'):
					prefix = spacer+'- '
					comment = comment[1:]
				print('%s%s\n'%(spacer,textwrap.fill(prefix+comment,100,subsequent_indent=spacer)))

	def show_globals(self):
		self.show_options(self.global_options)

	def do_reload(self,params):
		'''Reloads the current module'''
		self._reload = 1
		return True

	def do_run(self,params):
		'''Runs the module'''
		try:
			self.summary_counts = {}
			self.v_option()
			pre = self.module_pre()
			params = [pre] if pre is not None else []
			self.module_run(*params)
			self.module_post()
		except KeyboardInterrupt:
			print('')
		except Exception as e:
			warn(e.message)

	def module_pre(self):
		pass

	def module_run(self):
		pass

	def module_post(self):
		pass
