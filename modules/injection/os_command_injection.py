#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

import re
import os
from lib.utils.rand import *
from lib.utils.readfile import *
from lib.utils.param import *
from lib.utils.printer import *
from core.module import BaseModule
from lib.request.grequest import (
    check_url,check_end
)

class Module(BaseModule):

    info = {
        'name': 'OS Command Injection',
        'author': 'Momo Outaadi',
        'description': 'Operating System Command Injection Vulnerability',
        'options': (
            ('host', None, True, 'The target address'),
            ('url_path', '/',False,'The target URL path'),
            ('method','GET',False,'HTTP method'),
            ('port', 80, False, 'The target port'),
            ('data',None,False,'POST data'),
            ('wordlist',None,False,'Set OS Commands wordlist'),
            ('headers',False,False,'Show return headers'),
            ('status',False,False,'Show return status-code')
        ),
    }

    def module_run(self):
        path = os.path.join(self.data_path,'os_command_injection.galileo')
        test('Injecting...')
        host = self.options['host']
        port = self.options['port']
        data = self.options['data']
        method = self.options['method']
        headers = self.options['headers']
        status = self.options['status']
        url_path = self.options['url_path']
        wordlist = self.options['wordlist'] if self.options['wordlist']!=('' or None) else path
        url = check_url(check_end(host,url_path),port)
        for payload in readfile(wordlist):
            random_string = rand_all(20)
            payload = payload.replace('[PAYLOAD]',random_string) 
            if method == 'GET':
                urls = Replace(url,payload,data).run()
                for url_ in urls:
                    print(url_)
                    resp = self.request(url=url_,method=method,data=data)
                    if re.search(random_string,resp.content,re.I):
                        plus('OS Command Vulnerability was found: %s'%(resp.url))
                        return
            elif method == 'POST':
                url_ = Replace(url,payload,data).run()[:1]
                data_= Replace(url,payload,data).run()[1:]
                for _url_ in url_:
                    for data in data_:
                        resp = self.request(url=_url_,method=method,data=data)
                        if re.search(random_string,resp.content,re.I):
                            plus('OS Command Vulnerability was found:\n \_ URL => %s\n \_ DATA => %s'%(resp.url,data))
                            return
            else:return