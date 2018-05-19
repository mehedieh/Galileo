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
        'name': 'Server',
        'author': 'Momo Outaadi',
        'description': 'Detect Server',
        'options': (
            ('host', None, True, 'The target address'),
            ('url_path', '/',False,'The target URL path'),
            ('port', 80, False, 'The target port')
        ),
    }

    def module_run(self):
        test('Detecting...')
        host = self.options['host']
        port = self.options['port']
        url_path = self.options['url_path']
        url = check_url(check_end(host,url_path),port)
        for m in ['GET','HEAD','BLABLA','OPTIONS','DELETE']:
        	resp = self.request(url=url,method=m)
        	if 'server' in resp.headers.keys():
        		plus('Detect Server: %s'%(resp.headers['server']))
        		return