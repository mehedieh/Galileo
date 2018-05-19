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
        'name': 'Framework',
        'author': 'Momo Outaadi',
        'description': 'Detect common Web Framework',
        'options': (
            ('host', None, True, 'The target address'),
            ('url_path', '/',False,'The target URL path'),
            ('method','GET',False,'HTTP method'),
            ('port', 80, False, 'The target port'),
            ('data',None,False,'POST data')
        ),
    }

    def mvc(self,headers,content):
        '''ASP MVC'''
        if 'x-aspnet-version' in headers.keys():return True
        if 'x-aspnetmvc-version' in headers.keys():return True
        if re.search(r'Web Settings for Active Server Pages',content):return True
        if re.search(r'__requestverificationtoken',str(headers.values())):return True
        if re.search(r'asp.net|anonymousID\=|chkvalues\=',str(headers.values())):return True
        if re.search(r'name=\"__VIEWSTATEENCRYPTED\" id=\"__VIEWSTATEENCRYPTED\"',content):return True


    def cakephp(self,headers,content):
        '''CakePHP'''
        for value in headers.values():
            if re.search(r'cakephp\=',value,re.I):
                return True

    def cherrypy(self,headers,content):
        '''CherryPy'''
        for value in headers.values():
            if re.search(r'cherrypy',value,re.I):
                return True

    def django(self,headers,content):
        '''Django'''
        for value in headers.values():
            if re.search(r'wsgiserver\/|python\/|csrftoken\=',
                value,re.I):return True
        if re.search(r'\<title\>Welcome to Django\<\/title\>',
            content):return True

    def flask(self,headers,content):
        '''Flask'''
        for value in headers.values():
            if re.search(r'flask',value,re.I):
                return True

    def fuelphp(self,headers,content):
        '''FuelPHP'''
        for value in headers.values():
            if re.search(r'fuelcid\=',value,re.I):
                return True
        if re.search(r'Powered by \<a href\=\"http://fuelphp.com\"\>FuelPHP\<\/a\>',
            content,re.I):return True

    def larvel(self,headers,content):
        '''Larvel'''
        for value in headers.values():
            if re.search(r'larvel|larvel_session\=',value,re.I):
                return True

    def grails(self,headers,content):
        '''Grails'''
        for key in headers.keys():
            if re.search('grails',headers[key],re.I):return True
            if re.search(r'x-grails|x-grails-cached',key,re.I):return True

    def nette(self,headers,content):
        '''Nette'''
        for value in headers.values():
            if re.search(r'nette|nette-browser=',value,re.I):return True

    def rails(self,headers,content):
        '''Ruby on Rails'''
        for key in headers.keys():
            if re.search(r'phusion|passenger',headers[key],re.I):return True
            if re.search(r'rails|_rails_admin_session=',headers[key],re.I):return True
            if re.search(r'x-rails',key,re.I):return True
        if re.search(r'\<script[^>]*\/assets\/application-?\w{32}?\.js\"',content,re.I):
            return True
        if re.search(r'\<link[^>]*href\=\"[^\"]*\/assets\/application-?\w{32}?\.css\"',
            content,re.I):return True

    def symfony(self,headers,content):
        '''Symfony'''
        for value in headers.values():
            if re.search('symfony=',value,re.I):return True
        if re.search('\"powered by symfony\"',content,re.I):return True
        if re.search(r'Powered by \<a \href\=\"http://www.symfony-project.org/\"\>',
            content,re.I):return True

    def module_run(self):
        test('Detecting...')
        host = self.options['host']
        port = self.options['port']
        data = self.options['data']
        method = self.options['method']
        url_path = self.options['url_path']
        url = check_url(check_end(host,url_path),port)
        resp = self.request(url=url)
        frameworks = [
                        'mvc','cakephp','cherrypy','django','flask',
                        'fuelphp','larvel','grails','nette','rails','symfony'
                    ]
        for fm in frameworks:
            funct = getattr(self,fm)
            bool_ = funct(resp.headers,resp.content)
            if bool_:
                plus('Found %s Framework'%(funct.__doc__))
                return