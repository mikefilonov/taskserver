import time


from task import Task


class SleepTask(Task):
	def __init__(self, arguments):
		self._seconds = int(arguments[ "seconds" ])
		self._current_seconds = 0
		

	def progress(self):
		return (self._current_seconds * 100)/self._seconds, "Working..."



	def answer(self):
		if self._current_seconds == self._seconds:
			return {"seconds_done": self._seconds}

		else: return None


	def execute(self):
		while self._current_seconds < self._seconds:
			time.sleep(1)
			self._current_seconds+=1


