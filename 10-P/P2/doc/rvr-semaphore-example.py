from mp1 import MP, MPthread

class SemaphoreExample(MP):
	"""An example using the semaphore features of the 
	4410 Synchronization Library"""

	def __init__(self):
		MP.__init__(self, None)
		self.value     = self.Shared("value", 0)
		self.valueLock = self.Semaphore("value lock", 1)

	def update(self, newValue):
		self.valueLock.procure()
		self.value = newValue
		self.valueLock.vacate()

