#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

from lib.utils.printer import *
from core.module import BaseModule
from lib.request.gsocket import *

class Module(BaseModule):

    info = {
        'name': 'Socket',
        'author': 'Momo Outaadi',
        'description': 'Send request with socket',
        'options': (
            ('host', None, True, 'The target address'),
            ('method','GET',False,'HTTP method'),
            ('data',None,False,'Send data'),
            ('headers', None, False, 'Add custom headers'),
            ('port', 80, False, 'The target port'),
            ('path',None,False,'URL path'),
            ('http','1.1',True,'HTTP version'),
            ('protocol','HTTP',True,'Set custom protocol'),
            ('content',True,False,'Print return content')
        ),
    }

    def module_run(self):
        host = self.options['host']
        port = self.options['port']
        data = self.options['data']
        path = self.options['path']
        http = self.options['http']
        method = self.options['method']
        content = self.options['content']
        headers = self.options['headers']
        protocol = self.options['protocol']
        test('Connecting...')
        resp = self.socket(host=host,
            port=port,method=method,data=data,
            path=path,http=http,protocol=protocol,headers=headers
            )
        if content:
            print('-' * 60)
            print(resp)
            print('-' * 60)