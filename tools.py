
from itertools import chain
from ika import *

clamp = lambda a, lt, gt: max(min(a ,gt), lt)
flatset = lambda listofsets: set(chain(*listofsets))
inrandom = lambda l: l[Random(0, len(l))]

def ignore(f, ex):
	try:
		f()
	except ex:
		pass
def FrameBlit(img, frame, x, y):
	Video.ClipScreen(x, y, x+16, y+16)	
	img.Blit(x - frame*16, y)		
def ree(a, method, accum = None):			# Returns a set with every piece involved in the method
	if accum is None: accum = set([a])
	for i in a.__dict__[method]():
		if i not in accum: accum |= ree(i, method, accum | set([i]))
	return accum