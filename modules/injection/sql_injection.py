#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

import os
from lib.utils.sql_errors import *
from lib.utils.readfile import *
from lib.utils.param import *
from lib.utils.printer import *
from core.module import BaseModule
from lib.request.grequest import (
    check_url,check_end
)

class Module(BaseModule):

    info = {
        'name': 'SQL Injection',
        'author': 'Momo Outaadi',
        'description': 'SQL Injection',
        'options': (
            ('host', None, True, 'The target address'),
            ('url_path', '/',False,'The target URL path'),
            ('method','GET',False,'HTTP method'),
            ('port', 80, False, 'The target port'),
            ('data',None,False,'POST data'),
            ('wordlist',None,False,'Set SQL Injection payload')
        ),
    }

    def module_run(self):
        path = os.path.join(self.data_path,'sql_injection.galileo')
        test('Injecting...')
        host = self.options['host']
        port = self.options['port']
        data = self.options['data']
        method = self.options['method']
        url_path = self.options['url_path']
        wordlist = self.options['wordlist'] if self.options['wordlist']!=('' or None) else path
        url = check_url(check_end(host,url_path),port)
        for payload in readfile(wordlist):
            if method == 'GET':
                urls = Replace(url,payload,data).run()
                for url_ in urls:
                    resp = self.request(url=url_,method=method,data=data)
                    name,error = sql_error(resp.content)
                    if name and error:
                        plus('SQL Injection was found: %s'%(resp.url))
                        print(' \_ DBMS => %s\n \_ ERROR => %s'%(name,error))
                        return
            elif method == 'POST':
                url_ = Replace(url,payload,data).run()[:1]
                data_= Replace(url,payload,data).run()[1:]
                for _url_ in url_:
                    for data in data_:
                        resp = self.request(url=_url_,method=method,data=data)
                        name,error = sql_error(resp.content)
                        if name and error:
                            plus('SQL Injection was found: %s'%(resp.url))
                            print(' \_ DATA => %s\n \_ NAME => %s\n \_ ERROR => %s'%(data,name,error))
                            return
            else:
                return