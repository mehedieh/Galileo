#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

import os
import time
from lib.utils.colors import *
from lib.utils.printer import *
from lib.utils.settings import *
from lib.utils.readfile import *
from core.module import BaseModule
from lib.utils.threads import Threads
from lib.request.grequest import (
    check_url,check_end
)

class Module(BaseModule,Threads):

    info = {
        'name': 'File Dir Brute',
        'author': 'Momo Outaadi',
        'description': 'Common directory and file bruteforce',
        'options': (
            ('host', None, True, 'The target address'),
            ('url_path', '/',False,'The target URL path'),
            ('method','GET',False,'HTTP method'),
            ('port', 80, False, 'The target port'),
            ('wordlist',None,True,'Set wordlist')
        ),
    }

    def check(self,path):
        if not os.path.exists(path):
            warn('Path \'%s\' not found')
            return  
        return path

    def module_run(self):
        test('Starting bruteforce...')
        host = self.options['host']
        port = self.options['port']
        method = self.options['method']
        wordlist = self.options['wordlist']
        url_path = self.options['url_path']
        url_ = check_url(check_end(host,url_path),port)
        for line in readfile(self.check(wordlist)):
            url = check_end(url_,line)
            self.thread(url,method)
            
    def module_thread(self,url,method):
        while True:
            resp = self.request(url = url,method = method)
            if resp.url == url:
                if resp.code in range(200,299):
                    print('%s[%s] %s -  %s%s'%(G%1,time.strftime(time_format),
                        resp.code,resp.url,E))
                if resp.code in range(300,399):
                    print('%s[%s] %s -  %s%s'%(Y%0,time.strftime(time_format),
                        resp.code,resp.url,E))
                if resp.code in range(400,599):
                    print('[%s] %s -  %s'%(time.strftime(time_format),
                        resp.code,resp.url))
            elif resp.url != url:
                print('%s[%s] %s -  %s -> %s%s'%(Y%0,time.strftime(time_format),
                    resp.code,url,resp.url,E))
            break