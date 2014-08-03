from execution import OneThreadStrategy

import uuid

from task import DONE, INPROGRESS, ERROR, QUEUED


class TaskManager(object):
	def __init__(self):
		self.executor = OneThreadStrategy()

		self.task_table = {}

	def start(self):
		self.executor.start_execution_loop()

	def put(self, task):
		id = str(uuid.uuid4())
		self.task_table[id] = task
		self.executor.put(task)
		return id

	def get(self, id):
		return self.task_table.get(id)

	def remove(self, id):
		del self.task_table[id]

