#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

import os
import time
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
        'name': 'Auth Brute',
        'author': 'Momo Outaadi',
        'description': 'Basic HTTP login bruteforce',
        'options': (
            ('host', None, True, 'The target address'),
            ('url_path', '/',False,'The target URL path'),
            ('method','GET',False,'HTTP method'),
            ('port', 80, False, 'The target port'),
            ('wuser',None,True,'Username wordlist'),
            ('wpass',None,True,'Password wordlist')
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
        wpass = self.options['wpass']
        wuser = self.options['wuser']
        url_path = self.options['url_path']
        url = check_url(check_end(host,url_path),port)
        for user in readfile(self.check(wuser)):
            for passwd in readfile(self.check(wpass)):
                self.thread(url,method,user,passwd)
            
    def module_thread(self,url,method,user,passwd):
        while True:
            resp = self.request(url = url,
                method = method, auth='%s:%s'%(user,passwd))
            print('[%s] %s - %s  - %s'%(time.strftime(time_format),
                resp.code,"%s:%s"%(user,passwd),resp.url))
            break