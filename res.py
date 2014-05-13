import ika

f = ika.Font('font.fnt')	# A random font

class FakeSound:
	def __init__(self, name):
		self.name = name
		self.realsnd = Sound(name)
	def Play(self):
		#log('Playing %s' % self.name)
		self.realsnd.Play()
		pass