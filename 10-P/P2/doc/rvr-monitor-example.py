
from mp1 import MP, MPthread

class MonitorExample(MP):
	"""
	An example using the monitor features of the 4410
	Synchronization Library.

	Note: This monitor does not correctly implement the
	implied specification!
	"""
	def __init__(self):
		MP.__init__(self, None)
		self.debug = True
		self.value = self.Shared("value", 0)
		self.lock  = self.Lock("monitor lock")
		self.gt0   = self.lock.Condition("value greater than 0")
		self.lt2   = self.lock.Condition("value less than 2")

	def get_value(self):
		with self.lock:
			return self.value.read()

	def block_until_pos(self):
		with self.lock:
			while not (self.value.read() > 0):
				self.gt0.wait()

	def update(self, value):
		with self.lock:
			self.value.write(value)
			if self.value.read() > 0:
				self.gt0.signal()
			if self.value.read() < 2:
				self.lt2.broadcast()

