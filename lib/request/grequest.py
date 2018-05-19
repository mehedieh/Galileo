#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

import re
import ssl
import socket
import urllib2
import urlparse

if hasattr(ssl, '_create_unverified_context'): 
    ssl._create_default_https_context = ssl._create_unverified_context

def BasicAuthCredentials(creds):
	# return tuple
	return tuple(
		creds.split(':') 
		)

def ProxyDict(proxy):
	# return dict
	return {
		'http'  : proxy,
		'https' : proxy,
		'ftp'   : proxy
	}

def sheader(headers):
	dict_h = {}
	for i in headers.split(';'):
		dict_h[i.split(':')[0]] = dict_h[i.split(':')[1]]
	return dict_h

def check_url(url,port):
	o = urlparse.urlsplit(url)
	if o.scheme in ['http','https']:
		return url 
	if o.scheme == '':
		if port == 443:
			return 'https://'+url
		else: return 'http://'+url 

def check_end(url,path):
	if url.endswith('/') and path.startswith('/'):
		return url + path[1:]
	elif not url.endswith('/') and not path.startswith('/'):
		return url + "/" + path
	else:
		return url + path

class Request(object):
	auth=proxy=cookie=timeout=pauth=agent=''
	redirect = True
	def Send(self,url,method='GET',data=None,headers=None):
		# make a request
		if method != '':
			method = method.upper()
		else:
			method = 'GET'
		# set data
		if data == '':
			data = None
		# headers
		if headers is None:
			headers = {}
		else:
			if isinstance(headers,dict):
				headers = headers
			else: headers = sheader(headers)
		# authentication
		if self.auth == '': auth = ()
		else: auth = self.auth
		# add user-agent header value
		if 'User-Agent' not in headers:
			headers['User-Agent'] = self.agent
		# process basic authentication
		if auth != None and auth != ():
			if ':' in  auth:
				authorization = ("%s:%s"%(BasicAuthCredentials(auth))).encode('base64')
				headers['Authorization'] = "Basic %s"%(authorization.replace('\n',''))
		# process proxy basic authorization
		if self.pauth != '':
			if ':' in self.pauth:
				proxy_authorization = ("%s:%s"%(BasicAuthCredentials(self.pauth))).encode('base64')
				headers['Proxy-authorization'] = "Basic %s"%(proxy_authorization.replace('\n',''))
		# process socket timeout
		if self.timeout != '':
			socket.setdefaulttimeout(self.timeout)
		# set handlers
		# handled http and https 
		handlers = [urllib2.HTTPHandler(),urllib2.HTTPSHandler()]
		# process cookie handler
		if 'Cookie' not in headers:
			if self.cookie != '':
				headers['Cookie'] = self.cookie
		# process redirect
		if self.redirect is False:
			handlers.append(NoRedirectHandler)
		# process proxies
		if self.proxy != '':
			proxies = ProxyDict(self.proxy)
			handlers.append(urllib2.ProxyHandler(proxies))
		# install opener
		opener = urllib2.build_opener(*handlers)
		urllib2.install_opener(opener)
		# process method
		# method get 
		if method == "GET":
			if data:url = "%s?%s"%(url,data)
			req = urllib2.Request(url,headers=headers)
		# other methods
		elif method == "POST":
			req = urllib2.Request(url,data=data,headers=headers)
		# other methods
		else:
			req = urllib2.Request(url,headers=headers)
			req.get_method = lambda : method
		# response object
		try:
			resp = urllib2.urlopen(req)
		except urllib2.HTTPError as e:
			resp = e
		return ResponseObject(resp)

class NoRedirectHandler(urllib2.HTTPRedirectHandler):
	"""docstring for NoRedirectHandler"""
	def http_error_302(self,req,fp,code,msg,headers):
		pass
	#  http status code 302
	http_error_302 = http_error_302 = http_error_302 = http_error_302

class ResponseObject(object):
	"""docstring for ResponseObject"""
	def __init__(self,resp):
		# get content
		self.content = resp.read()
		# get url 
		self.url = resp.geturl()
		# get status code
		self.code = resp.getcode()
		# get headers
		self.headers = resp.headers.dict