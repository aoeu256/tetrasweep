
list = TypeCheckCollection([])

def showMethods(p):
	global list
	list.append(p)

def function():
	global list
	for p in list:
		p.lol()

		
# * When you iter through an array, it returns a view of an element.  Any function
# that you call 

class TypeCheckCollection:
	def __init__(self, v):
		self.v = v
		self.attributes = [] # Attributes supported
		if '__iter__' in v.__class__.__dict__:
			pass
	def __getattr__(self, s):
		return getattr(self.v, s)
	
