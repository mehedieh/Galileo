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
        'name': 'Backup Brute',
        'author': 'Momo Outaadi',
        'description': 'Common directory and file backup bruteforce',
        'options': (
            ('host', 'None', True, 'The target address'),
            ('url_path', '/',False,'The target URL path'),
            ('method','GET',False,'HTTP method'),
            ('port', 80, False, 'The target port'),
            ('wordlist','None',True,'Common directory wordlist'),
            ('exts',None,False,'Set backup extensions')
        ),
    }

    def check(self,path):
        if not os.path.exists(path):
            warn('Path \'%s\' not found')
            return  
        return path

    def to_dict(self,exts):
        if exts != None:
            return exts.split(',')

    def module_run(self):
        test('Starting bruteforce...')
        back_ext = [
            ' (copy)/','_copy/', '- Copy/','~/','.7z',
            '.gz','.tar.gz','.tar','.tar.7z','.tar.bz2','.bak',
            '.old','.zip','.rar','.bac','_old','_bak','_backup','1','2','3'
        ]
        host = self.options['host']
        port = self.options['port']
        method = self.options['method']
        wordlist = self.options['wordlist']
        url_path = self.options['url_path']
        extensions = self.to_dict(self.options['exts']) if self.options['exts'] != None else back_ext
        url_ = check_url(check_end(host,url_path),port)
        for dir_ in readfile(self.check(wordlist)):
            for bk in extensions:
                url = check_end(url_,dir_+bk)
                self.thread(url,method)
            
    def module_thread(self,url,method):
        while True:
            resp = self.request(url = url,
                method = method)
            if resp.url == url:
                if resp.code in range(200,299):
                    print('%s[%s] %s -   %s%s'%(G%1,time.strftime(time_format),resp.code,resp.url,E))
                elif resp.code in range(300,399):
                    print('%s[%s] %s -   %s%s'%(Y%0,time.strftime(time_format),resp.code,resp.url,E))
                elif resp.code in range(400,599):
                    print('[%s] %s -   %s'%(time.strftime(time_format),resp.code,resp.url))
            elif resp.url != url:
                print('%s[%s] %s -   %s%s'%(Y%0,time.strftime(time_format),resp.code,resp.url,E))
            break