#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

from lib.utils.source_code import *
from lib.utils.printer import *
from core.module import BaseModule
from lib.request.grequest import (
    check_url,check_end
)

class Module(BaseModule):

    info = {
        'name': 'Code Disclosure',
        'author': 'Momo Outaadi',
        'description': 'Search the Code Disclosure vulnerability',
        'options': (
            ('host', None, True, 'The target address'),
            ('url_path', '/',False,'The target URL path'),
            ('method','GET',False,'HTTP method'),
            ('port', 80, False, 'The target port'),
            ('data',None,False,'POST data'),
            ('regexp',None,False,'Search the regexp in content')
        ),
    }

    def module_run(self):
        test('Searching...')
        host = self.options['host']
        port = self.options['port']
        data = self.options['data']
        method = self.options['method']
        regexp = self.options['regexp']
        url_path = self.options['url_path']
        url = check_url(check_end(host,url_path),port)
        resp = self.request(url=url,method=method,data=data)
        bool_,lang = source_code(resp.code,resp.content)
        if bool_ and lang:
            plus2('Code disclosure vulnerability was found in: %s'%(resp.url))
        if bool_ is False and lang is None:
            return