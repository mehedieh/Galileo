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
        'name': 'Private IP',
        'author': 'Momo Outaadi',
        'description': 'Private IP Disclosure',
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
        # https://www.regular-expressions.info/ip.html
        regexp_ = r'[0-9]+(?:\.[0-9]+){3}'
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
            found_ip = re.findall(regexp,resp.content,re.I)
            if found_ip:
                c = 1
                for ip in found_ip:
                    print('Private IP => %s'%(ip))
            if c == 0:info('Not found private ip...')
        except re.error as e:
            warn(e.message)