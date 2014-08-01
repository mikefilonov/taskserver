from Queue import Queue
from task import DONE, INPROGRESS, ERROR, QUEUED

class TaskExecutionStrategy(object):
	"""
	Base class for all Strategies for task execution. Implements basic non-threaded execution
	"""

	def __init__(self):
		self.queue = Queue(maxsize=0)

	def start_execution_loop(self):
		"""Should be re-implemented in sub-classes with threads"""
		while True:
			task = self.queue.get() # waits for task in queue
			task.status = INPROGRESS
			task.execute()
			self.queue.task_done()
			task.status = DONE

	def put(self, task):
		"""Adds a task to the queue to be executed"""
		task.status = QUEUED
		self.queue.put(task)

from threading import Thread

class OneThreadStrategy(TaskExecutionStrategy):
	"""Runs the execution loop in one thread"""

	def start_execution_loop(self):
		t = Thread(target=self.threaded_execution_loop)
		t.daemon = True
		t.start()

	def threaded_execution_loop(self):
		while True:
			task = self.queue.get() # bloks until a task in the queue
			try:
				task.status = INPROGRESS
				task.execute()
				task.status = DONE
			except Exception, ex:
				task.status = ERROR
				print ex
			finally:
				self.queue.task_done()
