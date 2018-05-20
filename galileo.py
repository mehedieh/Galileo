#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

from core import base
from lib.utils.printer import *

try:
	x = base.Base()
	x.cmdloop()
except KeyboardInterrupt:
	exit(warn('Exit..'))
