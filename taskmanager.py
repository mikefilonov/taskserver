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
		id = uuid.uuid1()
		self.task_table[id] = task
		self.executor.put(task)
		return id

	def get(self, id):
		task = self.task_table.get(id)
		if task is not None and task.status in [DONE, ERROR]:
			self.remove(id)
		return task

	def remove(self, id):
		del self.task_table[id]

