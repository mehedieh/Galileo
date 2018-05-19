#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

from random import choice,randint
from string import lowercase,uppercase,digits

def rand_str(lenght):
	return ''.join(choice(lowercase+uppercase) for i in range(lenght))

def rand_num(lenght):
	return ''.join(choice(digits) for i in range(lenght))

def rand_all(lenght):
	return ''.join(choice(lowercase+digits+uppercase) for i in range(lenght))

def Ragent():
	agents = (
		'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/6.0)',
		'Mozilla/5.0 (Android; Mobile; rv:40.0) Gecko/40.0 Firefox/40.0',
		'Mozilla/5.0 (Android; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0',
		'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0; Xbox; Xbox One)',
		'Mozilla/5.0 (iPad; CPU OS 8_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko)',
		'Opera/9.30 (Nintendo Wii; U; ; 2047-7; en)',
		'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
		'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0',
		'Mozilla/5.0 (X11; OpenBSD i386; rv:36.0) Gecko/20100101 Firefox/36.0 SeaMonkey/2.33.1',
		'Mozilla/5.0 (X11; OpenBSD amd64; rv:42.0) Gecko/20100101 Firefox/42.0'
		)
	return agents[randint(0,len(agents))-1]