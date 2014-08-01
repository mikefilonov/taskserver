NOTQUEUED = 0
QUEUED = 1
INPROGRESS = 2
DONE = 3
ERROR = 4

class Task(object):
	
	"""
	Base class for Tasks.

	Provides status information for task-executor:
	task.status = NOTSTARTED | INPROGRESS | DONE

	Subclasses should re-implements basic interface for Task:
	
	execute()
	progress()
	titile()
	"""

	def __init__(self, arguments):
		""""Initialize task with arguments (any json-able object)"""
		self.status = NOTQUEUED

	def execute(self):
		"""Do actual work of the task

		Should be implemented in sub-classes. 
		"""		
		pass

	def progress(self):
		"""Return a progress of the task in a form of a touple (progress, message) 

		Should be re-implemented in sub-classes. 
		"""		
		return (0, "no progress implemented")
		

	def title(self):
		"""Return a title of a task"""		
		return self.__class__.__name__

