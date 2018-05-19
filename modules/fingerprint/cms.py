#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

import re
from lib.utils.printer import *
from core.module import BaseModule
from lib.request.grequest import (
    check_url,check_end
)

class Module(BaseModule):

    info = {
        'name': 'CMS',
        'author': 'Momo Outaadi',
        'description': 'Detect content management system (cms)',
        'options': (
            ('host', None, True, 'The target address'),
            ('url_path', '/',False,'The target URL path'),
            ('method','GET',False,'HTTP method'),
            ('port', 80, False, 'The target port'),
            ('data',None,False,'POST data')
        ),
    }

    def wordpress(self,headers,content):
    	if re.search(r'<meta name="generator" content="WordPress.com" />',content):return True
    	if re.search(r'<a href="http://www.wordpress.com">Powered by WordPress</a>',content):return True
    	if re.search(r'/wp-content/plugins/|/wp-admin/admin-ajax.php',content):return True
    	if re.search(r'<link rel=\'https://api.w.org/\'',content):return True

    def joomla(self,headers,content):
    	if 'set-cookie' in headers.keys():
    		if re.search(r'mosvisitor=',headers['set-cookie']):return True
    	if re.search(r'<meta name=\"Generator\" content=\"Joomla! - Copyright (C) 200[0-9] - 200[0-9] Open Source Matters. All rights reserved.\" />',content):return True
    	if re.search(r'<meta name=\"generator\" content=\"Joomla! (\d\.\d) - Open Source Content Management\" />',content):return True
    	if re.search(r'Powered by <a href=\"http://www.joomla.org\">Joomla!</a>.',content):return True

    def drupal(self,headers,content):
    	if 'set-cookie' in  headers.keys():
    		if re.search(r'SESS[a-z0-9]{32}=[a-z0-9]{32}',headers['set-cookie']):return True
    	if re.search(r'<script type=\"text/javascript\" src=\"[^\"]*/misc/drupal.js[^\"]*\"></script>',content):return True
    	if re.search(r'<[^>]+alt=\"Powered by Drupal, an open source content management system',content):return True
    	if re.search(r'@import \"[^\"]*/misc/drupal.css\"|jQuery.extend\(drupal\.S*|Drupal.extend\(\S*',content):return True


    def module_run(self):
        test('Detecting...')
        host = self.options['host']
        port = self.options['port']
        data = self.options['data']
        method = self.options['method']
        url_path = self.options['url_path']
        url = check_url(check_end(host,url_path),port)
        resp = self.request(url=url,method=method,data=data)
        for cms in ['drupal','joomla','wordpress']:
        	funct = getattr(self,cms)
        	bool_ = funct(resp.headers,resp.content)
        	if bool_:
        		plus('Found %s cms'%(cms.title()))
        		return