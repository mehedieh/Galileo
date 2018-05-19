#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

import socks

def RHeader(headers):
	rheader = ''
	if ';' in headers:
		for k in headers.split(';'):
			if k != '' and k != "":
				rheader += '%s:%s\r\n'%(k.split(':')[0],k.split(':')[1])
	else:
		rheader = headers + "\r\n"
	return rheader

def RProxy(proxy):
	if '127.0.0.1' in proxy or 'localhost' in proxy:
		if ':' in proxy:
			host,port = proxy.split(':')
			return 2,host,port
		else:
			return 2,proxy,80
	if ':' in proxy:
		host,port = proxy.split(':')
		if port in range(1,65355):
			return 3,host,port
		else:
			return 3,proxy,80
	return 3,proxy,80

class Gsock(object):
	timeout=None
	proxy=''
	headers = None
	http_version = '1.1'
	method = 'GET'
	protocol ='HTTP'

	def Send(self,target,data=None,port=80,path=''):
		# set socks
		gsock = socks.socksocket()
		# method 
		if self.method != '':method = self.method.upper()
		else: method = 'GET'
		# timeout
		if self.timeout != None:
			print(self.timeout)
			gsock.settimeout(self.timeout)
		# set proxy
		if self.proxy != ('' or None or ""):
			proto,host,port = RProxy(self.proxy)
			if proto == 3:gsock.set_proxy(socks.HTTP,host,port)
			elif proto == 2:gsock.set_proxy(socks.SOCKS5,host,port)
			else:gsock.set_proxy(socks.SOCKS4,host,port)
		# connect
		gsock.connect((target,port))
		# get
		if method == 'GET':
			req  = '\r%s /%s %s/%s\r\n'%(method,data if data != None else '',
				self.protocol.upper(),self.http_version)
			if self.headers != ('' or None):req += '%s'%(RHeader(self.headers))
		# post
		elif method == 'POST':
			req = '\r%s /%s %s/%s\r\n'%(method,data if data != None else '',
				self.protocol.upper(),self.http_version)
			if self.headers != ('' or None):req += '%s'%(RHeader(self.headers))
			if data != ('' or None):req += '\r\n%s\r\n'%(data)
		# other methods
		else:
			req = '\r%s /%s %s/%s\r\n'%(method,data if data != None else '',
				self.protocol.upper(),self.http_version)
			if self.headers != ('' or None):req += '%s'%(RHeader(self.headers))
		# send data
		gsock.sendall(req)
		# return resp
		resp = gsock.recv(4096)
		return resp