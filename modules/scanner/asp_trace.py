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
        'name': 'ASP.NET Trace',
        'author': 'Momo Outaadi',
        'description': 'Detect ASP.NET Trace enabled',
        'options': (
            ('host', None, True, 'The target address'),
            ('url_path', '/',False,'The target URL path'),
            ('method','GET',False,'HTTP method'),
            ('port', 80, False, 'The target port'),
            ('data',None,False,'POST data')
        ),
    }

    def module_run(self):
        test('Scanning...')
        host = self.options['host']
        port = self.options['port']
        data = self.options['data']
        method = self.options['method']
        url_path = self.options['url_path']
        url = check_url(check_end(host,url_path),port)
        for path in ['trace.axd','Trace.axd']:
        	url = check_end(url,path)
        	resp = self.request(url=url,method=method,data=data)
        	if resp.code == 200:
        		if re.search(r'<td><h1>Application Trace</h1></td>',resp.content,re.I):
        			plus('ASP.NET trace was found: %s'%(resp.url))
        			return