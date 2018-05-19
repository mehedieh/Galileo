#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

import re
from lib.utils.colors import *
from lib.utils.printer import *
from core.module import BaseModule
from lib.request.grequest import (
    check_url,check_end
)

class Module(BaseModule):

    info = {
        'name': 'Email Disclosure',
        'author': 'Momo Outaadi',
        'description': 'Email Disclosure',
        'options': (
            ('host', None, True, 'The target address'),
            ('url_path', '/',False,'The target URL path'),
            ('method','GET',False,'HTTP method'),
            ('port', 80, False, 'The target port'),
            ('data',None,False,'POST data'),
            ('regexp',None,False,'Set regular expression')
        ),
    }

    def module_run(self):
        # https://www.regular-expressions.info/email.html
        regexp_ = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}'
        test('Searching...')
        host = self.options['host']
        port = self.options['port']
        data = self.options['data']
        regexp = self.options['regexp'] if self.options['regexp'] != (''or None) else regexp_
        method = self.options['method']
        url_path = self.options['url_path']
        url = check_url(check_end(host,url_path),port)
        c = 0
        resp = self.request(url=url,method=method,data=data)
        try:
            found_email = re.findall(regexp,resp.content,re.I)
            if found_email:
                c = 1
                for email in found_email:
                    print('Email => %s'%(email))
            if c == 0:info('Not found emails...')
        except re.error as e:
            warn(e.message)