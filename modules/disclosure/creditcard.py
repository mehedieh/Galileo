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
        'name': 'Credit Cards',
        'author': 'Momo Outaadi',
        'description': 'Credit Cards Disclosure',
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
        # https://stackoverflow.com/questions/9315647/regex-credit-card-number-tests
        cc_regex  = {
                        'American Express'  :   r'^[34|37][0-9]{14}$',
                        'Mastercard'        :   r'^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$',
                        'Visa Card'         :   r'^4[0-9]{12}(?:[0-9]{3})?$',
                        'Visa Master Card'  :   r'^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})$'
        }
        test('Searching...')
        host = self.options['host']
        port = self.options['port']
        data = self.options['data']
        regexp = self.options['regexp']
        method = self.options['method']
        url_path = self.options['url_path']
        url = check_url(check_end(host,url_path),port)
        c = 0
        resp = self.request(url=url,method=method,data=data)
        try:
            if regexp == ('' or None):
                for item in cc_regex.items():
                    found_cc = re.findall(item[1],resp.content,re.I)
                    if found_cc:
                        c = 1
                        for xx in found_cc:
                            print('%s => %s'%(item[0],xx))
                if c == 0:info('Not found credit cards...')
            elif regexp != ('' or None):
                found_cc = re.findall(regexp,resp.content,re.I)
                if found_cc:
                    for xx in found_cc:
                        print('Found REGEX => %s'%(x))
                else:info('Not found credit cards...')
            else:
                return
        except re.error as e:
            warn(e.message)