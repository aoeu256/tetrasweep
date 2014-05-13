#	def panepon(self, area):
#		combo = self.area.combo
#		combo[:] = []
#		def linkUp(x1, y1, x2, y2, x3, y3):
#			pa, pb, pc = pan[y1][x1], pan[y2][x2], pan[y3][x3]
#			if pa.c and pa.c==pb.c==pb.c and all(p.gstate() for p in (pa, pb, pc)):
#				combo += [(x1, y1, pa), (x2, y2, pb), (x3, y3, pc)]
#		xlim = area.ncolm - 2
#		ylim = area.nrow - 3
#		for x, y, _ in self.iter():
#			if x < xlim: linkUp(x,y,  x+1,y,  x+2,y)
#			if y < ylim: linkUp(x,y,  x,y+1,  x,y+2)

cdef struct Panel:
	int c
	bool marked, canChain
	int state

cdef void newPanel():
	struct Panel panel
	return panel

cdef int WIDTH = 6
cdef int HEIGHT = 12

cdef int[][] panels = [[newPanel() for x in range(WIDTH)] for y in range(HEIGHT)]


#cdef void puyo(self, area):	
#	self.pos2combo = {}
#	combo = self.area.combo
#	combo[:] = []
	
#	def linkUp(pax, pay, pbx, pby):
#		'tries to link up the panel at (pax, pay), with (pbx, pby)'
#		pa = self.v[pay][pax]
#		pb = self.v[pby][pbx]
#		if pa.c and pa.c == pb.c and pa.gstate() and pb.gstate():
#			if (pax, pay) in self.pos2combo:
#				if (pbx, pby) in self.pos2combo: # if both pa and pb have a combo union the two combos together
#					self.pos2combo[pax, pay] |= self.pos2combo[pbx, pby]
#					self.pos2combo[pbx, pby] = self.pos2combo[pax, pay]
#					self.pos2combo[pbx, pby-1] = self.pos2combo[pax, pay]
#				else: # pb has no combo: add pb to pa's combo, then set pb's combo to pa
#					self.pos2combo[pax, pay].add(pb)
#					self.pos2combo[pbx, pby] = self.pos2combo[pax, pay]
#			else:
#				if (pbx, pby) in self.pos2combo: # pa has no combo
#					self.pos2combo[pbx, pby].add(pa)
#					self.pos2combo[pax, pay] = self.pos2combo[pbx, pby]
#				else:
#					self.pos2combo[pax, pay] = self.pos2combo[pbx, pby] = set([pa, pb])
#
#		for x, y, _ in self.iter():
#			if x < 5:  linkUp(x, y, x+1, y) # Try to link right
#			if y < 10: linkUp(x, y, x, y+1) # Try to link down
#		for x, y, p in self.iter():
#			try:
#				if len(self.pos2combo[x,y]) >= 4:
#					combo.append( (x, y, p))
#			except KeyError:
#				pass
					