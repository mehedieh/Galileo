#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

from __future__ import print_function
import imp,os,re,sys
import __builtin__
from core.framework import *
from lib.utils.printer import *
from lib.utils.rand import *
from lib.utils.options import *
from lib.utils.colors import *
from lib.utils.banner import banner

class Base(framework):
	def __init__(self):
		framework.__init__(self,'base')
		self.name = 'galileo'
		self.prompt_t = '%s #> '
		self.base_prompt = self.prompt_t%(self.name)
		self.advance_prompt = '%s%%s #> '%(self.name)
		self.tool_path = framework.tool_path = sys.path[0]
		self.data_path = framework.data_path = os.path.join(self.tool_path,'data')
		self.core_path = framework.core_path = os.path.join(self.tool_path,'core')
		self.options   = self.global_options
		self.i_global_options()
		self.i_home()
		self.init_run()
		self.show_banner()

	def i_global_options(self):
		self.r_option('pauth',None,False,'Proxy auth credentials (user:pass)')
		self.r_option('proxy',None,False,'Set proxy (host:port)')
		self.r_option('threads',5,False,'Number of threads')
		self.r_option('timeout',5,False,'Set timeout')
		self.r_option('user-agent','Mozilla/5.0 (X11; Ubuntu; Linux x86_64)',True,'Set user-agent')
		self.r_option('redirect',True,False,'Set redirect')
		self.r_option('verbosity',1,True,'Verbosity level (0 = minimal,1 = verbose)')

	def i_home(self):
		self.tool_home = framework.tool_home = os.path.join(self.tool_path,
			'.' + self.name)
		if not os.path.exists(self.tool_home):
			os.makedirs(self.tool_home)
			
	def load_modules(self):
		self.loaded_category = {}
		self.loaded_modules  = framework.loaded_modules
		for path in [os.path.join(x,'modules') for x in (self.tool_path,self.tool_home)]:
			for dirpath,dirnames,filenames in os.walk(path):
				filenames  = [f for f in filenames if not f[0] == '.']
				dirnames[:] = [d for d in dirnames if not d[0] == '.']
				if len(filenames) > 0:
					for filename in [f for f in filenames if f.endswith('.py')]:
						if filename != '__init__.py':
							is_loaded = self.load_module(dirpath,filename)
							mod_category = 'disabled'
							if is_loaded:
								mod_category = re.search('/modules/([^/]*)',dirpath).group(1)
							if not mod_category in self.loaded_category:
								self.loaded_category[mod_category] = 0
							self.loaded_category[mod_category] += 1

	def load_module(self,dirpath,filename):
		mod_name = filename.split('.')[0]
		mod_dispname = '/'.join(re.split('/modules/',dirpath)[-1].split('/')+[mod_name])
		mod_loadname = mod_dispname.replace('/','_')
		mod_loadpath = os.path.join(dirpath,filename)
		mod_file = open(mod_loadpath)
		try:
			mod = imp.load_source(mod_loadname,mod_loadpath,mod_file)
			__import__(mod_loadname)
			self.loaded_modules[mod_dispname] = sys.modules[mod_loadname].Module(mod_dispname)
			return True 
		except ImportError as e:
			warn('Module \'%s\' disabled. Dependency required: \'%s\''%(mod_dispname,e.message[16:]))
		except Exception as e:
			warn(e.__str__())
			warn('Module \'%s\' disabled'%(mod_dispname))
		self.loaded_modules.pop(mod_dispname,None)
		return False 

	def init_run(self,):
		self.prompt = self.base_prompt
		self.i_global_options()
		self.l_config()
		self.load_modules()
		return True

	def show_banner(self):
		banner()
		counts = [(self.loaded_category[x],x) for x in self.loaded_category]
		count_len = len(max([str(x[0]) for x in counts],key=len))
		for count in sorted(counts,reverse=True):
			cnt = '[%s]'%(count[0])
			test('%s modules'%(count[1].title()),cnt.ljust(count_len+2))
		print('')


	def do_reload(self,params):
		'''Reloads all modules'''
		test('Reloading...')
		self.load_modules()

	def do_load(self,params):
		'''Loads selected module'''
		try:
			self.v_option()
		except Exception as e:
			warn(e.message)
			return 
		if not params:
			self.help_load()
			return
		modules = [params] if params in self.loaded_modules else\
		 [x for x in self.loaded_modules if params in x]
		if len(modules) != 1:
			if not modules:warn('Invalid module name')
			else:
				plus('Multiple modules match \'%s\''%(params))
				self.show_modules(modules)
			return
		mod_dispname = modules[0]
		category = mod_dispname.split('/')[0]
		while True:
			y = self.loaded_modules[mod_dispname]
			mod_loadpath = os.path.join(sys.modules[y.__module__].__file__).split('.py')[0]+'.py'
			y.prompt = self.advance_prompt%(" %s(%s%s%s)"%(category,R%1,mod_dispname.split('/')[-1],E))
			try:
				y.cmdloop()
			except KeyboardInterrupt:
				print('')
			if y._exit == 1:
				return True
			if y._reload == 1:
				test('Reloading...')
				is_loaded = self.load_module(os.path.dirname(mod_loadpath),
					os.path.basename(mod_loadpath))
				if is_loaded:
					continue
			break

	def do_use(self,params):
		'''Use selected module'''
		self.do_load(params)