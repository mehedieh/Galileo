#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

from __future__ import print_function
from contextlib import closing
import sys
import cmd
import os
import subprocess
import json
from lib.utils.colors import *
from lib.utils.decoder import * 
from lib.utils.options import options
from lib.utils.settings import *
from lib.utils.printer import *
from lib.utils.rand import *
from lib.request.grequest import *
from lib.request.gsocket import *

class framework(cmd.Cmd):
	prompt = '#> '
	# ------------------------
	_script = 0
	_loaded = 0
	# ------------------------
	global_options = options()
	loaded_modules = {}
	summary_counts = {}
	# ------------------------
	tool_path = ''
	data_path = ''
	core_path = ''
	tool_home = ''
	t_abapath = ''
	# ------------------------
	def __init__(self,params):
		cmd.Cmd.__init__(self)
		self._exit = 0
		self.ruler = '-'
		self.module_name = params
		self.doc_header = 'Help command: [help|?] <topics>'
		self.nohelp = '%s[!]%s %sNo help on %%s%s'%(R%1,E,R%0,E)
		self.do_help.__func__.__doc__ = '''Show this menu and exit'''

	def default(self,line):
		self.do_shell(line)

	def emptyline(self):
		return 0

	def precmd(self,line):
		if self._loaded:print('\r',end='')
		if self._script:print('%s'%(line))
		return line

	def onecmd(self,line):
		cmd,arg,line = self.parseline(line)
		if not line: return self.emptyline()
		if line == 'EOF':
			sys.stdin = sys.__stdin__
			self._script = self._loaded = 0
			return 0
		if cmd is None: return self.default(line)
		# cmd.Cmd().lastcmd
		self.lastcmd = line
		if cmd == '': return self.default(line)
		else:
			try:
				# find functions with getattr
				function = getattr(self, "do_" + cmd)
			except AttributeError as e:
				return self.default(line)
			return function(arg)

	def print_topics(self,header,cmds,cmdlen,maxcol):
		if cmds:
			self.stdout.write("%s\n"%(str(header)))
			if self.ruler:self.stdout.write("%s\n"%(str(self.ruler * len(header))))
			for cmd in cmds:
				self.stdout.write("%s %s\n"%(cmd.ljust(15),getattr(self,"do_"+cmd).__doc__))
			self.stdout.write("\n")

	def heading(self,line,level=1):
		line = to_unicode(line)
		print('')
		if level == 0:
			print(self.ruler * len(line))
			print(line.upper())
			print(self.ruler * len(line))
		if level == 1:
			print('%s%s'%(spacer,line.title()))
			print('%s%s'%(spacer,self.ruler*len(line)))

	def request(self,url,auth='',agent='',proxy='',pauth='',cookie='',timeout=None,redir=True,headers=None,data=None,method='get'):
		request = Request()
		request.auth     = auth if auth != ('' or None or " ") else self.global_options['auth']
		request.cookie   = cookie if cookie != ('' or None or " ") else self.global_options['cookie']
		request.timeout  = timeout if timeout != ('' or None or " ") else self.global_options['timeout']
		request.pauth    = pauth if pauth != ('' or None or " ") else self.global_options['pauth']
		request.redirect = redir if redir != ('' or None or " ") else self.global_options['redirect']
		request.agent    = agent if agent != ('' or None or " ") else self.global_options['agent']
		request.proxy    = proxy if proxy != ('' or None or " ") else self.global_options['proxy']
		return request.Send(url,method,data,headers)

	def socket(self,host,port=80,timeout=None,headers=None,proxy='',pauth='',method='GET',path='',http='1.1',protocol='HTTP',data=None):
		sock = Gsock()
		sock.timeout = timeout if timeout != ('' or None or " ") else self.global_options['timeout']
		sock.proxy = proxy if proxy != ('' or None or " ") else self.global_options['proxy']
		sock.pauth = pauth if pauth != ('' or " " or None) else self.global_options['pauth']
		sock.http_version = http
		sock.headers = headers
		sock.protocol = protocol
		sock.method = method
		return sock.Send(target=host,data=data,port=port,path=path)


	def r_option(self,name,value,required,description):
		self.options.i_option(name=name.lower(),value=value,
			required=required,description=description)
		self.l_config()

	def v_option(self):
		for option in self.options:
			if not type(self.options[option]) in [bool,int]:
				if self.options.required[option] is True and not self.options[option]:
					warn('Value required for the \'%s\' option'%(option.upper()))
		return

	def l_config(self):
		config_path = os.path.join(self.t_abapath,'.galileo/config.dat')
		if os.path.exists(config_path):
			with open(config_path) as config_file:
				try:
					config_data = json.loads(config_file.read())
				except ValueError:
					pass
				else:
					for key in self.options:
						try:
							self.options[key] = config_data[self.module_name][key]
						except KeyError:
							continue
	def s_config(self,name):
		config_path = os.path.join(self.t_abapath,'.galileo/config.dat')
		open(config_path,'a').close()
		with open(config_path) as config_file:
			try:
				config_data = json.loads(config_file.read())
			except ValueError:
				config_data = {}
		if self.module_name not in config_data:config_data[self.module_name] = {}
		config_data[self.module_name][name] = self.options[name]
		if config_data[self.module_name][name] is None:
			del config_data[self.module_name][name]
		if not config_data[self.module_name]:
			del config_data[self.module_name]
		with open(config_path,'w') as config_file:
			json.dump(config_data,config_file,indent=4)

	def show_modules(self,params):
		if type(params) is list:
			modules = params
		elif params:
			modules = [x for x in self.loaded_modules if x.startswith(params)]
			if not modules:
				warn('Invalid module category')
				return 
		else:
			modules = self.loaded_modules
		key_len = len(max(modules,key=len))+len(spacer)
		last_category = ''
		for module in sorted(modules):
			category = module.split('/')[0]
			if category != last_category:
				last_category = category
				self.heading(last_category)
			print('%s%s'%(spacer*2,module))
		print('')

	def show_options(self,options=None):
		if options is None:
			options = self.options
		if options:
			pattern = '%s%%s  %%s  %%s  %%s'%(spacer)
			key_len = len(max(options,key=len))
			if key_len < 4: key_len = 4
			try:
				val_len = len(max([to_unicode(options[x]) for x in options],key=len))
			except Exception:
				val_len = 13
			if val_len < 13: val_len = 13
			print('')
			print(pattern%('Name'.ljust(key_len),'Current Value'.ljust(val_len),'Required','Description'))
			print(pattern%(self.ruler*key_len,(self.ruler*13).ljust(val_len),self.ruler*8,self.ruler*11))
			for key in sorted(options):
				value = options[key] if options[key] != None else ""
				reqd = 'no' if options.required[key] is False else 'yes'
				desc = options.description[key]
				try:
					print(pattern%(key.upper().ljust(key_len),to_unicode(value).ljust(val_len),to_unicode(reqd).ljust(8),desc))
				except AttributeError:
					self.clear()
			print('')
		else:
			print('\n%sNo options available for this module\n'%(spacer))

	def get_show_names(self):
		return [x[len('show_'):] for x in self.get_names() if x.startswith('show_')]

	def do_exit(self,param):
		'''Exit the console'''
		self.clear()
		self._exit = 1
		sys.exit(0)

	def clear(self):
		import shutil
		path = os.path.join(self.tool_path,'.galileo/')
		if os.path.exists(path):
			shutil.rmtree(path)

	def do_random(self,params):
		'''Random variable generators'''
		if not params:
			self.help_random()
			return
		try:
			type_,lenght = params.split(' ')
			if type_ == 's':
				print('Random String => %s'%(rand_str(int(lenght))))
			elif type_ == 'n':
				print('Random Number => %s'%(rand_num(int(lenght))))
			elif type_ == 'a':
				print('Random All => %s'%(rand_all(int(lenght))))
			else:
				self.help_random()
				return
		except Exception as e:
			self.help_random()
			return

	def do_back(self,params):
		'''Move back from the current context'''
		return True

	def do_set(self,params):
		'''Set a context-specific variable to a value'''
		options = params.split()
		if len(options) < 2:
			self.help_set()
			return
		name = options[0].lower()
		if name in self.options:
			value = ' '.join(options[1:])
			self.options[name] = value
			print('%s => %s'%(name.upper(),value))
			self.s_config(name)
		else:warn('Invalid options')

	def do_unset(self,params):
		'''Unset one or more context-specific variables'''
		if not params:
			self.help_unset()
			return 
		self.do_set('%s %s'%(params,'None'))

	def do_show(self,params):
		'''Displays variouse framework items'''
		if not params:
			self.help_show()
			return 
		_params = params
		params = params.lower().split()
		arg = params[0]
		params = ' '.join(params[1:])
		if arg in self.get_show_names():
			func = getattr(self,'show_'+arg)
			if arg == 'modules':
				func(params)
			else:
				func()
		else:
			self.help_show()

	def do_md5(self,params):
		'''Hash MD5'''
		import md5
		if not params:
			self.help_md5()
			return 
		print('MD5 => %s'%(md5.new(params).hexdigest()))

	def do_sha1(self,params):
		'''Hash SHA1'''
		import sha
		if not params:
			self.help_sha1()
			return 
		print('SHA1 => %s'%(sha.new(params).hexdigest()))

	def do_base64(self,params):
		'''Base64 encode and decode'''
		import base64
		if not params:
			self.help_base64()
			return
		try:
			type_,string_ = params.split(' ')
			if type_ == 'encode':
				if string_ != ('' or " "):
					print('Encode => %s'%(base64.b64encode(string_)))
				else:
					self.help_base64()
					return 
			elif type_  == 'decode':
				if string_ != (''or" "):
					print('Decode => %s'%(base64.b64decode(string_)))
				else:
					self.help_base64()
					return 
			else:
				self.help_base64()
				return 
		except Exception as e:
			self.help_base64()
			return

	def do_urlencode(self,params):
		'''URL encode'''
		from urllib import quote
		if not params:
			self.help_urlencode()
			return 
		print('URL Encode => %s'%(quote(params)))

	def do_hex(self,params):
		'''Hex number'''
		if not params:
			self.help_hex()
			return 
		try:
			number,lenght = params.split(' ')
			print('Hex => %s'%(hex(int(number))*int(lenght)))
		except Exception:
			self.help_hex()
			return 

	def do_multi(self,params):
		'''Multiply (x) n times'''
		if not params:
			self.help_multi()
			return 
		try:
			string,lenght = params.split(' ')
			print('Multi => %s'%(string*int(lenght)))
		except Exception:
			self.help_multi()
			return 

	def do_urldecode(self,params):
		'''URL decode'''
		from urllib import unquote_plus
		if not params:
			self.help_urldecode()
			return 
		print('URL Decode => %s'%(unquote_plus(params)))

	def do_invoke(self,params):
		'''Invoke external tools'''
		import os
		if not params:
			self.help_invoke()
			return 
		try:
			print(Y%0)
			status = os.system(params)
			print(E)
		except Exception:
			self.help_invoke()
			return 

	def do_search(self,params):
		'''Searches available modules'''
		if not params:
			self.help_search()
			return 
		text = params.split()[0]
		plus('Searching for \'%s\'...'%(text))
		modules = [x for x in self.loaded_modules if text in x]
		if not modules:
			warn('No modules found containing \'%s\''%(text))
		else:
			self.show_modules(modules)

	def do_shell(self,params):
		'''Executes shell commands'''
		if not params:
			self.help_shell()
			return 
		proc = subprocess.Popen(params,
			shell=True,stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,stdin=subprocess.PIPE)
		test('Command: %s'%(params))
		stdout = proc.stdout.read()
		stderr = proc.stderr.read()
		if stdout:print('%s%s%s'%(Y%0,stdout,E))
		if stderr:warn('%s%s%s'%(R%0,stderr,E))

	def do_load(self,params):
		'''Loads selected module'''
		if not params:
			self.help_load()
			return 
		modules = [params] if params in self.loaded_modules else [\
		x for x in self.loaded_modules if params in x]
		if len(modules) != 1:
			if not modules:warn('Invalid module name')
			else:
				info('Multiple modules match \'%s\''%(params))
				self.show_modules(modules)
			return
		import StringIO
		if self._script:end_string = sys.stdin.read()
		else:
			end_string = 'EOF'
			self._loaded = 1
		sys.stdin = StringIO.StringIO('load %s\n%s'%(modules[0],end_string))
		return True

	def do_use(self,params):
		'''Use selected module'''
		self.do_load(params)

	def help_random(self):
		doc = getattr(self,'do_random').__doc__
		self.heading(doc)
		print('%s- Usage: <(s)tring|(n)umber|(a)ll> <lenght>'%(spacer))
		print('%s- Example: random s 20\n'%(spacer))

	def help_load(self):
		doc = getattr(self,'do_load').__doc__
		self.heading(doc)
		print('%s- Usage: [load|use] <module>'%(spacer))
		print('%s- Example: load fingerprint/cms\n'%(spacer))

	def help_use(self):
		self.help_load()

	def help_search(self):
		doc = getattr(self,'do_search').__doc__
		self.heading(doc)
		print('%s- Usage: search <string>'%(spacer))
		print('%s- Example: search scanner\n'%(spacer))

	def help_set(self):
		doc = getattr(self,'do_set').__doc__
		self.heading(doc)
		print('%s- Usage: set <option> <value>'%(spacer))
		print('%s- Usage: set COOKIE phpsess=hacker_test\n'%(spacer))
		self.show_options()

	def help_unset(self):
		doc = getattr(self,'do_unset').__doc__
		self.heading(doc)
		print('%s- Usage: unset <option>'%(spacer))
		print('%s- Example: unset COOKIE\n'%(spacer))
		self.show_options()

	def help_shell(self):
		doc = getattr(self,'do_shell').__doc__
		self.heading(doc)
		print('%s- Usage: shell <command>'%(spacer))
		print('%s- Example: shell ls -lash\n'%(spacer))

	def help_show(self):
		options = sorted(self.get_show_names())
		doc = getattr(self,'do_show').__doc__
		self.heading(doc)
		print('%s- Usage: show [%s]'%(spacer,'|'.join(options)))
		print('%s- Example: show banner\n'%(spacer))

	def help_multi(self):
		doc = getattr(self,'do_multi').__doc__
		self.heading(doc)
		print('%s- Usage: multi <string> <lenght>'%(spacer))
		print('%s- Example: multi hello 10\n'%(spacer))

	def help_md5(self):
		doc = getattr(self,'do_md5').__doc__
		self.heading(doc)
		print('%s- Usage: md5 <string>'%(spacer))
		print('%s- Example: md5 helloword\n'%(spacer))

	def help_invoke(self):
		doc = getattr(self,'do_invoke').__doc__
		self.heading(doc)
		print('%s- Usage: invoke <command>'%(spacer))
		print('%s- Example: invoke nmap -Pn -p 21 xxx.xxx.xxx.xxx\n'%(spacer))

	def help_sha1(self):
		doc = getattr(self,'do_sha1').__doc__
		self.heading(doc)
		print('%s- Usage: sha1 <string>'%(spacer))
		print('%s- Example: sha1 helloword\n'%(spacer))

	def help_base64(self):
		doc = getattr(self,'do_base64').__doc__
		self.heading(doc)
		print('%s- Usage: base64 <encode|decode> <string>'%(spacer))
		print('%s- Example: base64 encode helloword\n'%(spacer))

	def help_urlencode(self):
		doc = getattr(self,'do_urlencode').__doc__
		self.heading(doc)
		print('%s- Usage: urlencode <url|string>'%(spacer))
		print('%s- Example: urlencode http://xxxxxxx.com/?id=1&t=1\n'%(spacer))

	def help_urldecode(self):
		doc = getattr(self,'do_urldecode').__doc__
		self.heading(doc)
		print('%s- Usage: urldecode <url|string>'%(spacer))
		print('%s- Example: urldecode %s\n'%(spacer,
			r'http%3A//xxxxxxx.com/%3Fid%3D1%26t%3D1'))

	def help_hex(self):
		self.heading(getattr(self,'do_hex').__doc__)
		print('%s- Usage: hex <number> <lenght>'%(spacer))
		print('%s- Example: hex 1024 10\n'%(spacer))

	def complete_base64(self,text,*ignored):
		return [x for x in ['encode','decode'] if x.startswith(text)]

	def complete_load(self,text,*ignored):
		return [x for x in self.loaded_modules if x.startswith(text)]

	def complete_use(self,text,*ignored):
		return [x for x in self.loaded_modules if x.startswith(text)]

	def complete_random(self,text,*ignored):
		return [x for x in ['s','n','a'] if x.startswith(text)]

	def complete_set(self,text,*ignored):
		return [x.upper() for x in self.options if x.upper().startswith(text.upper())]

	def complete_unset(self,text,*ignored):
		return [x.upper() for x in self.options if x.upper().startswith(text.upper())]

	def complete_show(self,text,line,*ignored):
		args = line.split()
		if len(args) > 1 and args[1].lower() == 'modules':
			if len(args) > 2: return [x for x in self.loaded_modules if x.startswith(args[2])]
			else:return [x for x in self.loaded_modules]
		options = sorted(self.get_show_names())
		return [x for x in options if x.startswith(text)]