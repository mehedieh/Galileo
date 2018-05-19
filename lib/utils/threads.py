#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @name  : Galileo 
# @descr : Web Application Audit Framework
# @author: Momo Outaadi

import time
import threading 
from Queue import Queue,Empty
from lib.utils.printer import *

class Threads(object):
	def thread(self,*args):
		thread_count = self.global_options['threads']
		self.stopped = threading.Event()
		self.q = Queue()
		self.q.put(args[0])
		threads = []
		for i in range(thread_count):
			t = threading.Thread(target=self.thread_wrapper,args=args[1:])
			threads.append(t)
			t.setDaemon(True)
			t.start()
		try:
			while not self.q.empty():
				time.sleep(2)
		except KeyboardInterrupt:
			warn2('Waiting for threads to exit...')
			self.stopped.set()
			for t in threads:
				t.join()
			raise
		self.q.join()
		self.stopped.set()

	def thread_wrapper(self,*args):
		thread_name = threading.current_thread().name
		while not self.stopped.is_set():
			try:
				obj = self.q.get_nowait()
			except Empty:
				continue
			try:
				self.module_thread(obj,*args)
			except Exception as e:
				warn(e.message)
			finally:
				self.q.task_done()