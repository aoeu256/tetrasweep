from xi import fps
from ika import *
from math import *
from tools import *
from input import *
import time, pickle, os, pdb, res, ika

# A lot of this is ripped off from phree_radical's VERGE

area = None

class Menu:
	def __init__(self, parent, choices=[], x=0, y=0, onMove=(lambda: None) ):
		self.choices = choices
		self.x, self.y = x, y
		self.parent = parent
		self.onMove = onMove
		self.cur = 0
		self.firstmove = False
	def draw(self):
		Video.DrawRect(self.x, self.y, self.x + 128, len(self.choices)*8, RGB(0,64,128), 1)
		Video.DrawRect(self.x, self.y+self.cur*8, self.x + 127, self.y+(self.cur+1)*8, RGB(255,0,0), 1)
		for y, i in enumerate(self.choices):
			res.f.Print(self.x, self.y+y*8, i)
	def control(self):
		if not self.firstmove:
			self.onMove()
		if Input.up.Pressed():
			self.cur = (self.cur - 1) % len(self.choices)
			self.onMove()
		if Input.down.Pressed():
			self.cur = (self.cur + 1) % len(self.choices)
			self.onMove()
		#logonce('R is %s' % R)
		#logonce('%s' % im[R])
	def choice(self):
		return self.choices[self.cur]

class Filelist(Menu):
	def __init__(self, parent, ext='', **args):
		lst = []
		for f in os.listdir(os.getcwd()):
			splt = f.split('.')
			if len(splt) > 1 and splt[1] == ext:
				lst.append(f)
		Menu.__init__(self, parent, choices=lst, **args)
#aoeu  @memoize



class NumberFont:
	def __init__(self, im):
		self.im = im
	def Print(self, x, y, s):
		im = self.im
		for p, i in enumerate(s):
			n = int(i)
			im.ClipBlit(x+8*p, y, n*8, 0, 16, 16)

def enum(lst):
	g = globals()
	num2name = []
	for n, i in enumerate(lst):
		g[i.title()] = n
		num2name.append(i.title())
	return num2name

def enumu(**enums):
	return type('Enum', (), enums)

colors = list('vrgpyc')
states = ['futsu', 'flash', 'ppmae', 'ppato', 'black', 'rswap', 'lswap', 'hover', 'boing', 'fall']
images = ['bg'] + colors[1:] + ['pedal', 'cur0', 'cur1', 'combo', 'chain', 'fg', 'fontnumblue', 'fontnumred']
sounds = ['s'+str(i).zfill(3) for i in range(30)] + \
			['fanfare'+str(i) for i in range(3)]+ \
			['pop'+str(a).zfill(2) for a in range(40)]
frames = ['futsu', 'b0', 'b1', 'b2', 'lit', 'o_o', 'dark']
colorName = enum(colors)
stateName = enum(states)
imageName = enum(images)
soundName = enum(sounds)
frameName = enum(frames)

colorPanels = range(1, len(colors))
im = [Image('graphics/'+k+'.png') for k in images]
sound = [Sound('sounds/sfx/'+k+'.wav') for k in sounds]
#frames = dict((k, v) for v, k in enumerate([Futsu, 'b0', 'b1', 'b2', Flash, 'o_o', 'dark']))
colorlst = [x for x in range(len(colors))]
def randColor():
	return Random(0, len(colorlst))

class Panel(object):
	def setst(self, state, t = 0):
		self.state, self.t = state, t
		#if self.state == Boing:
			
		if not isinstance(state, int):
			raise 'value is ' + state
	def __init__(self, c):
		self.c = c
		self.marked = False
		self.state = Futsu
		self.setst(Futsu)
		self.canChain = False
	def __repr__(self):
		try:
			return '%s %5s-%2d' % (colorName[self.c], stateName[self.state], self.t)
		except TypeError:
			print self.state, self.c
			return 'TypeError'
	def gstate(self):
		return self.state == Boing or self.state == Futsu
	def popstate(self):
		return self.state == Ppmae or self.state == Ppato
	def copy(self):
		newpan = Panel(self.c)
		newpan.state = self.state
		newpan.t = self.t
		newpan.canChain = self.canChain
		newpan.marked = self.marked
		try: # NonePanel does not have attributes
			newpan.popn = self.popn
			newpan.popt = self.popt
		except AttributeError: pass
		return newpan
	def draw(self, area, ax, ay, x, y):
		global f
		if self.state == Black or self.c==0:
			return # Skip drawing
		if   self.state == Rswap: swapx = area.swapTime-self.t
		elif self.state == Lswap: swapx = -(area.swapTime-self.t)
		else:				  swapx = 0
		if y == 11:				frame = Dark
		elif self.state == Futsu:	frame = Futsu
		elif self.state == Boing:	frame = B0 + (self.t/2)%3
		elif self.state == Ppmae:	frame = O_O
		elif self.state == Ppato:	return # Skip drawing
		elif self.state == Flash:	frame = Lit if self.t%2 else Futsu
		else:					frame = Futsu
		x1, y1 = ax + x*16 + (swapx * 16 / area.swapTime), ay + y*16
		
		im[self.c].ClipBlit(x1, y1, frame*16, 0, 16, 16)
		if self.canChain:
			res.f.Print(x1, y1, '*')
		if self.marked:
			res.f.Print(x1, y1, 'M')

class NonePanel(Panel):
	def __init__(self):
		Panel.__init__(self, 0)
	def setst(self, state, t = 0):
		Panel.setst(self, state, t)
		if self.state not in (Lswap, Rswap):
			self.state = Futsu
	def draw(self, *args):
		pass

class Panels: 
	def __init__(self, area, v = None):
		self.area, self.v = area, v
		if v is None:
			self.v = [[NonePanel() for column in range(area.nrow)] for row in range(area.ncolm)]
	def __setitem__(self, tup, p):
		p.x, p.y = tup
		self.v[p.y][p.x] = p
	def __getitem__ (self, (x, y)): return self.v[y][x]
	#__iter__ = lambda a: self.v.__iter__
			#fun(self, p.x, i)
	def topPanels(self, x, y, include=False):
		if include:
			yield y, self.v[y][x]
		for yi in range(y, -1, -1):
			if self.v[yi][x].c == 0:
				break
			yield yi, self.v[yi][x]
	def topGPanels(self, x, y, include=False):
		for yi, p in self.topPanels(x, y, include):
			if not p.gstate():
				break
#				if self.v[yi][x].state in (Fall, Hover) and self.v[yi][x].state == self.v[y][x].state and self.v[yi][x].t < 2:
#					pass
#				else:
			yield yi, self.v[yi][x]			
	def append(self, pans):
		self.v = self.v[1:] + [pans]
	def iter(self):
		for y, row in enumerate(self.v):
			for x, panel in enumerate(row):
				yield x, y, panel
	def backiter(self):
		h = self.area.ncolm-1
		for y, row in enumerate(reversed(self.v)):
			for x, panel in enumerate(row):
				yield x, h-y, panel
	def panepon(self, area):
		combo = self.area.combo
		combo[:] = []
		def linkUp(x1, y1, x2, y2, x3, y3):
			pa, pb, pc = pan[y1][x1], pan[y2][x2], pan[y3][x3]
			if pa.c and pa.c==pb.c==pb.c and all(p.gstate() for p in (pa, pb, pc)):
				combo += [(x1, y1, pa), (x2, y2, pb), (x3, y3, pc)]
		xlim = area.ncolm - 2
		ylim = area.nrow - 3
		for x, y, _ in self.iter():
			if x < xlim: linkUp(x,y,  x+1,y,  x+2,y)
			if y < ylim: linkUp(x,y,  x,y+1,  x,y+2)
	def puyo(self, area):
		self.pos2combo = {}
		combo = self.area.combo
		combo[:] = []
		def linkUp(pax, pay, pbx, pby):
			'tries to link up the panel at (pax, pay), with (pbx, pby)'
			pa = self.v[pay][pax]
			pb = self.v[pby][pbx]
			if pa.c and pa.c == pb.c and pa.gstate() and pb.gstate():
				if (pax, pay) in self.pos2combo:
					if (pbx, pby) in self.pos2combo: # if both pa and pb have a combo union the two combos together
						self.pos2combo[pax, pay] |= self.pos2combo[pbx, pby]
						self.pos2combo[pbx, pby] = self.pos2combo[pax, pay]
						self.pos2combo[pbx, pby-1] = self.pos2combo[pax, pay]
					else: # pb has no combo: add pb to pa's combo, then set pb's combo to pa
						self.pos2combo[pax, pay].add(pb)
						self.pos2combo[pbx, pby] = self.pos2combo[pax, pay]
				else:
					if (pbx, pby) in self.pos2combo: # pa has no combo
						self.pos2combo[pbx, pby].add(pa)
						self.pos2combo[pax, pay] = self.pos2combo[pbx, pby]
					else:
						self.pos2combo[pax, pay] = self.pos2combo[pbx, pby] = set([pa, pb])
		for x, y, _ in self.iter():
			if x < 5:  linkUp(x, y, x+1, y) # Try to link right
			if y < 10: linkUp(x, y, x, y+1) # Try to link down

		for x, y, p in self.iter():
			try:
				if len(self.pos2combo[x,y]) >= 4:
					combo.append( (x, y, p))
			except KeyError:
				pass

class CardList(list):
	def append(self, item):
		required = ['draw', 'tick']
		assert all(i in dir(item) for i in required)
		list.append(a, item)

class Card:
	Combo = 0
	Chain = 1
	def __init__(self, area, x, y, name, n):
		self.area, self.name = area, name
		self.x, self.y = x, y
		self.n = n
		self.t = 60
		self.maxt = self.t
		sound[S011].Play()
		xmid = 120
		ymid = 120
		xlast = 240
		ylast = 240
		#self.pedals = [(0,ymid), (xmid,0), (xmid,ylast), (xlast,ymid)]
		self.pedals = [0, pi/2, pi, 2*pi-pi/2]
		self.pedalSep = 200.0 / self.maxt
		self.finalSep = 6
	def draw(self):
		global im
		t = self.t/2
		y = (t-45)%45  + (self.y*16) + self.area.y
		x = self.x * 16 + self.area.x
		
		dang = 4*pi*t/self.maxt
		ds = max( self.pedalSep*t*t/self.maxt, self.finalSep)
		
		getCoord = lambda x, f: int(x+4+f(ang+dang))*ds
		
		for ang in self.pedals:
			im[Pedal].Blit(getCoord(x, cos), getCoord(x, sin))
			#self.area.log('%d %d' % (x+12+cos(ang+dang)*ds, y+12+sin(ang+dang)*ds))

		if self.name == Chain:
			im[Chain].ClipBlit(x, y, self.n*16, 32, 16, 16)
		else:
			im[Combo].ClipBlit(x, y, self.n*16, 0, 16, 16)
	def tick(self):
		self.t -= 1
	def __repr__(self):
		return '<Card%d (%d,%d) t=%d>' % (self.name, self.x, self.y, self.t)
class DoubleCard:
	def __init__(self, area, x, y):
		self.area = area
		self.x, self.y = x, y
		self.t = 15
	def tick(self):
		self.t-=1
	def draw(self):
		yt = self.t+self.y*16+self.area.y+8
		res.f.Print(self.area.x - 10 + self.x*16, yt, 'DOUBLE!')
class PanelPop:
	def __init__(self, area, x, y, n):
		self.area= area
		self.x = x * 16 + self.area.x + 9
		self.y = y * 16 + self.area.y + 24 - self.area.offy
		self.n = n 
		self.t = 15
		self.maxt = self.t
		f = min((self.area.chain-1)*10+n, 39)
		#f -= 3-n
		sound[Pop00+f].Play()
	def draw(self):
		global im
		r = self.maxt-self.t+3
		Video.DrawEllipse(self.x, self.y, r, r, RGB(255, 0, 255))		
	def tick(self):
		self.t -= 1
	def __repr__(self):
		return '<PanelPop(%d,%d) t=%d>' % (self.x, self.y, self.t)
class TestDraw:
	def __init__(self, drawf, t=80):
		self.t = t
		self.drawf = drawf
	def draw(self):
		self.drawf()
	def tick(self):
		self.t -= 1
class Task:
	def __init__(self, f, t=0):
		self.f = f
		self.t = t
	def __call__(self):
		self.f()
class PlayArea(AdvInput):
#	def setst(self, p, state, t = 0):
#		p.setst(state, t)
	def __init__(self, main, x, y, stack=None):
		global area
		area = a
		
		self.Debugmode = True
		
		main.log(' ')
		main.log('Loading Ta.py from '+time.ctime())
		main.log('Press F and D to swap (press both to double swap).')
		main.log('Press W to raise the stack.')
		main.log('Press V to empty the log.')
		main.log('Press J and K (Shift+J Shift+K) to change the color of the panel')
		main.log('Press F2 to save state, and F4 to load state.')
		main.log('======')
		
		#try:
		#	pdb.set_trace()
		#except:
		#	pass
		
		self.main = main
		self.log = main.log
		self.logonce = main.logonce
		self.vars = main.vars
		self.logvars = main.logvars		
		self._copy = 'x y fp nrow ncolm character nCanChain chain t score deathTimer cardx cardy chainTimer score stackfile comboMode'
		self.x, self.y = 8, 19
		self.fp = fps.FPSManager(60)
		self.nrow = 6 
		self.ncolm = 12 
		self.character = ''
		self.nCanChain = 0 # Number of panels that can chain when this reaches zero the chain is RESET
		self.chain = 1			# The current chain number
		self.t = self.score = self.deathTimer = 0
		self.offy = 0			# When it becomes 16 a new row is made
		self.cardx = self.cardy = 40
		self.chainTimer = 0
		self.score = 0		
		self.slowMode = False
		self.maxchain = 19
		self.maxcombo = 19
		self.stackfile = 'slip.stack'		
		self.comboModes = 'none puyo panepon'.split(' ')
		self.comboMode = 'puyo'
		self.bluef = NumberFont(im[Fontnumblue])
		self.redf = NumberFont(im[Fontnumred])
		
		self._copy += ' chainCount comboCount'
		self.chainCount = dict((i, 0) for i in range(2, self.maxchain+1)) # Keep track of ur chains
		self.comboCount = dict((i, 0) for i in range(2, self.maxcombo+1)) # Keep track of ur combos		
		
		self._copyseq = 'cards scheduled'
		#self.swaps = []
		self.cards = []	# combos or chains, or other effects				
		self.scheduled = []

		self._config = 'flashTime hoverTime popTime swapTime fallTime'
		self._copy += ' ' + self._config
		self.flashTime = 100
		self.hoverTime = 10
		self.chainHoverTime = self.hoverTime * 2
		self.popTime = 20
		self.swapTime = 5
		self.fallTime = 2
		
		self._input = 'cancel okay right up down left stackButton'
		self._copy += ' ' + self._input
		self.cancel = Input.keyboard['D']
		self.okay = Input.keyboard['F']
		self.right = Input.right
		self.up = Input.up
		self.down = Input.down
		self.left = Input.left
		self.stackButton = Input.keyboard['W']
		
		self.menu = None
		self.menu_f = None
		self.menux = 20
		self.menuy = 20
		
		self.combo = []
		self.pan = Panels(self)
		self.save = None

		self.bottom = lambda: self.y + (self.ncolm*16)	
		self.lpan = lambda: self.pan[self.curx, self.cury]
		self.rpan = lambda: self.pan[self.curx+1, self.cury]
		
		self.setup(stack)
	
	curx = property(lambda self: self.xaxis.cur)
	cury = property(lambda self: self.yaxis.cur)
	
	def setup(self, stack = None):
		class TAAxis(Axis):
			def onMove(self):
				sound[S000].Play()
		self.xaxis = TAAxis((self.left,self.right), range(self.nrow-1), wrap = False)
		self.yaxis = TAAxis((self.up,self.down), range(self.ncolm-1), wrap = False)
				
		def newRow():			
			color = inrandom([x for x in colorPanels if x!=self.pan[0,self.ncolm-2].c])
			newR = [Panel(color)] # The new row with one panel on the left with a random color
			for x in range(1,self.nrow):
				# color_subset = [c for c in colors if c != newR[x-2].c and c!= self.pan[x,10].c] Tetris Attack
				
				color_subset = [c for c in colorPanels if c != newR[x-1].c and c != self.pan[x, self.ncolm-2].c] # Puyo
				newR.append(Panel(inrandom(color_subset)))
			return newR
		if stack is None:
			for _ in range(11):
				nR = newRow()
				self.pan.append(nR)
			
		def raiseStack(n = None):
			self.offy += 1
			if self.offy == 16:
				self.offy = 0
				for p in self.pan.v[0]:
					if p.canChain:
						self.nCanChain -= 1
				if n is None:
					n = newRow()
				self.pan.v = self.pan.v[1:] + [n]

				self.yaxis.cur = max(self.yaxis.cur-1, 0)
				#else: self.deathTimer += 1	
			return n
		def swap():
			pa = self.pan[self.curx,self.cury]
			pb = self.pan[self.curx+1,self.cury]

			# force swap to finish
			def addDouble():
				self.cards.append(DoubleCard(self, self.curx, self.cury))
			if   pa.state == Lswap:
				addDouble()
				self.rswap(self.curx-1, self.cury)
			elif pb.state == Rswap: # Force swap for left stealth: [a<->b]<->c]=c b a
				addDouble()
				self.rswap(self.curx+1, self.cury)
			pa = self.pan[self.curx,self.cury]
			pb = self.pan[self.curx+1,self.cury]

			if self.cury == 0:
				hovercond = True
			else:
				pua = self.pan[self.curx,self.cury-1]
				pub = self.pan[self.curx+1,self.cury-1]
				hovercond = pua.state != Hover and pub.state != Hover
			if pa.gstate() and pb.gstate() and hovercond:
				pa.setst(Rswap, self.swapTime)
				pb.setst(Lswap, self.swapTime)
				#self.swaps.append ( (pa, pb) )
				#self.swaphistory[pa, pb] = [] # add a list
				#if pa.c and pb.c:
				#	sound[S003].Play()
		self.raisestack = Button([self.stackButton], raiseStack, press = 'Position')
		self.swap = Button([Input.keyboard[k] for k in 'DF'], swap)
		AdvInput.__init__(self, 0, 12, [self.xaxis, self.yaxis], [self.swap, self.raisestack])

	def copyCur(self, area):
		self.xaxis.cur = area.xaxis.cur
		self.yaxis.cur = area.yaxis.cur
		self.offy = area.offy		

	def copy(self):
		newarea = PlayArea(self.main, 50, 50)
		n = newarea.__dict__
		o = self.__dict__
		newarea.copyCur(self)
		
		for c in self._copyseq.split(' '):
			for i in o[c]:
				try:
					i.area = self
				except KeyError:
					self.log('object %s does not have area attr' % i)
			
		for c in self._copy.split(' '):
			n[c] = o[c]
			
		for c in self._copyseq.split(' '):
			for i in o[c]:
				try:
					i.area = self
				except KeyError:
					self.log('object %s does not have area attr' % i)
		newarea.pan.v = self.copyStack(self.pan.v)
		for x, y, _ in self.combo:
			newarea.combo.append(x, y, newarea.pan[x,y])
		return newarea
	def schedule(self, f, t=0):
		self.scheduled.append(Task(f, t))
	def canFall(self, x, y):
		if y == self.ncolm-1:
			return False
		p = self.pan[x,y+1]
		if p.c == 0:
			return p.state not in (Rswap, Lswap)
		else:
			return p.state == Black
	def unchain(self, p, where):
		if p.marked:
			self.log('unchaining %s %s' % (p, where))
		if p.canChain:
			p.canChain = False
			self.nCanChain -= 1
#		log('nchain disrupted on %s: nchain=%d' % (p.c, p.state, self.nCanChain))
	def save2Panels(self):
		dumT = (self.lpan(), self.rpan())
		pickle.dump(dumT, file('paneldump', 'w'))
		self.log('dumped a panel: %s' % [dumT])
	def load2Panels(self):
		g = pickle.load(file('paneldump'))
		self.log('loaded a panel: %s' % [g])
		self.pan[self.curx, self.cury], self.pan[self.curx+1,self.cury] = g
	def test1(self):
		#for i in range(48):
		#	self.log('%d' % i)
		self.log(self.pan[4,4].__dict__)
	def test2(self, n = [0]):
		#self.cards.append(Card(self, 3, 5, Combo, 6))
		#self.cards.append(PanelPop(self, 5, 4, n[0]))
		self.cards.append(DoubleCard(self, self.curx, self.cury))
		#n[0]+=1
		#self.log('n is %d' % n[0])
	def test3(self):
		#self.log('%s' % self.cards)
		#self.log(str(self.x))
		#for x, y, p in self.pan.iter():
		#	if p.canChain:
		#		self.logvars('x y p', locals())
		for pa, pb in self.swaps:
			self.log('%s %s' % (pa, pb))
			if set([pa.state, pb.state]) & set([Rswap, Lswap]):
				for s in self.swaphistory[pa, pb]:
					self.log('	%s' % s)
	def test5(self):
		testf = NumberFont(Image('graphics/Font_NumBlue.png'))
		def draw():
			testres.f.Print(50, 50, '0123456789')
		self.cards.append(TestDraw(draw, 800))
		self.log("created testf")
	def testStack(self):
		for i in self.pan.v:
			self.log('%s' % i)
		self.log('---')
		if self.save:
			for i in self.save[0].v:
				self.log('%s' % i)
	def test4(self):
		#def fun():
		#	self.log('hello world')
		#self.schedule(fun)
		self.log(self.chainCount)
		self.log(self.comboCount)
	def setstackfile(self):
		self.stackfile = 'statetest.stack'
		self.log('stack file is %s' % self.stackfile)		
	def copyStack(self, stack):
		return [[p.copy() for p in row] for row in stack]
	def saveStack(self): # Save stack
		pickle.dump((self.copyStack(self.pan.v), self.curx, self.cury, self.offy), file(self.stackfile, 'w'))
		self.log('Saved stack to %s' % self.stackfile)
	def loadStack(self): # Load stack
		save = pickle.load(file(self.stackfile))
		#save = self.save
		self.pan.v = self.copyStack(save[0])
		self.xaxis.cur, self.yaxis.cur = save[1], save[2]
		self.offy = save[3]
	def setsaveStack(self):
		save = pickle.load(file(self.stackfile))
		self.save = (Panels(self, save[0]), save[1], save[2], save[3])
	def pickStackfile(self):
		self.stackfile = self.menu.choice()
	def cardTest(self):
		self.cards = [Card(self, 1, 1, Chain, 5), Card(self, 2, 2, Combo, 8)]
	#def processSwaps(self):
	#	'for debugging swaps'
		#for x, (pa, pb) in enumerate(self.swaps):
		#	info = '%s %s' % (pa, pb)
		#	if pa.t != 0 or pb.t != 0:
		#		self.swaphistory[pa, pb].append(info)
			#if pa.state not in (Rswap, Lswap) and pb.state not in (Rswap, Lswap):
			#	del self.swaphistory[pa, pb]
			#	del self.swaps[x]
	def rswap(self, x, y):
		#self.log('%s' % self.pan[x+1,y])
		self.pan[x,y], self.pan[x+1,y] = self.pan[x+1,y], self.pan[x,y]
		def setst(x, y):
			#self.log('doing swap %d,%d %s %s' % (x,y, self.pan[x,y], self.canFall(x, y)))
			if self.canFall(x, y):
				self.pan[x,y].setst(Hover, self.hoverTime)
			else:
				self.pan[x,y].setst(Futsu, 0)
		setst(x, y)
		setst(x+1, y)
	def ptext(self, x, y, p):
		return '%d,%d %s' % (x, y, p)	
	def processPanels(self):
		if self.combo:
			self.cardx, self.cardy = self.combo[0][0], self.combo[0][1]
			for n, (x, y, p) in enumerate(self.combo):
				#if p.gstate(): # if gstate really needed?
				p.setst(Flash, self.flashTime)
				p.popn = n
				p.popt = self.popTime * (len(self.combo)-n)
			#self.combos.append(self.combo[:])
			#self.log('combo is %s ' % list(self.combo))
		#for n, c in enumerate(self.combos):
			#self.log('%d %s' % (n, list(c)))
			#if c[0][2].t == 0 and c[0][2].state == Ppato:
				#for x, y, p in c:
					#
				#del self.combos[n]
		for x, y, p in self.pan.backiter():
			bp = self.pan[x,y+1] if y != self.ncolm - 1 else None # Bottom panel
			if p.c == 0: # logic for NonePanels
				if p.t > 0: p.t -= 1
				if p.t == 0:
					if p.state == Rswap and p.t == 0:
						self.rswap(x, y)
					elif p.state != Lswap:
						p.state = Futsu
				continue
			if p.marked and p.state != Futsu:
				if p.state != Ppato or p.t != 0:
					self.log('%d(%d,%d) %s' % (p.canChain, x, y, p))	
			if p.state == Futsu:
				if p.canChain:
					if bp is None or bp.state not in (Rswap, Lswap, Hover, Fall):
						if p.marked:
							self.log('bottom:(%d,%d)%s' % (x,y+1,bp))
						self.unchain(p, 'Futsu')
				if self.canFall(x, y):
					if p.marked:
						self.log('%d,%d%s Fall from Futsu state...' % (x,y,p))
					for yi, tp in self.pan.topPanels(x, y, True):
						tp.setst(Hover, self.chainHoverTime)
				continue
			elif p.state == Fall:
				bpcond = bp is None or bp.state != Fall
				if not self.canFall(x, y) and bpcond: # Landing
					if p.marked:
						self.log("%s can land" % self.ptext(x, y, p))
					p.setst(Boing, 5)
					for y, tp in self.pan.topPanels(x, y-1):
						if tp.gstate() or tp.state == Fall:
							tp.setst(Boing, 5)
							if tp.marked:
								self.log("  %s is BOINGING" % tp)
					continue			
			if p.t > 0:
				p.t -= 1
				if p.state == Boing and p.t == 3:
					sound[S005].Play()
				continue
			# Timer based state changes
			if p.state == Rswap:
				self.rswap(x, y)
			elif p.state == Hover:
				for yi, tp in self.pan.topPanels(x, y, True):
					tp.setst(Fall, 0)
			elif p.state == Ppato:
				self.unchain(p, 'Ppato')
				self.pan[x,y]=NonePanel()
				if y > 1:
					for _, tp in self.pan.topGPanels(x, y-1): # Set a few chains...
						#self.log('Considering (%d,%d)%s' % (x,yi,self.pan[x,yi]))
						tp.setst(Hover, self.hoverTime)
						tp.canChain = True
						self.nCanChain += 1
			elif p.state == Flash:
				p.setst(Ppmae, p.popn * self.popTime)
			elif p.state == Ppmae:
				p.setst(Ppato, p.popt)
				self.cards.append(PanelPop(self, x, y, p.popn))
			elif p.state == Boing:
				p.setst(Futsu)
			elif p.state == Fall:				
				# Falling motion, swap the empty panel with the solid panel
				#if self.canFall(x, y):
				if bp is None or not (bp.state == Fall and bp.t == 0):
					p.t = self.fallTime
					if p.marked:
						self.log("  falling %s %s" % (self.ptext(x, y, p), self.ptext(x, y, bp)))
					for yi, tp in self.pan.topPanels(x, y, True):
						if tp.gstate() or tp==p:
							self.pan[x, yi],  self.pan[x, yi+1] = NonePanel(), self.pan[x, yi]
						else:
							break
	def control(self):
		'handle input'
		if self.menu is not None:
			self.menu.control()
			if self.cancel.Pressed():
				self.menu = None
			elif self.okay.Pressed():
				self.menu_f()
				self.menu = None
		elif Input.keyboard['LCTRL'].Position():
			if Input.up.Position():
				self.main.logstart = max(0, self.main.logstart-1)
			elif Input.down.Position():
				self.main.logstart = min(1024, self.main.logstart+1)
		else:
			AdvInput.tick(self)
		if Input.keyboard['F2'].Pressed():
			self.saveStack()
		elif Input.keyboard['F3'].Pressed():
			def loadIntoSaved():
				self.stackfile = self.menu.choice()
				self.setsaveStack()
			self.menu = Filelist(self, 'stack', onMove=loadIntoSaved, x=self.menux, y=self.menuy)
			self.menu_f = self.pickStackfile
			return
		elif Input.keyboard['F10'].Pressed():
			def pick(self):				
				if self.menu.choice() == 'none':
					self.comboMode = None
				else:
					self.comboMode = self.menu.choice()				
			self.menu = Menu(self, self.comboModes, self.menux, self.menuy)
			self.menu_f = pick
		elif Input.keyboard['F4'].Pressed():
			self.loadStack()
		elif Input.keyboard['M'].Pressed():
			self.log('Marked %s' % self.lpan())
			self.lpan().marked = not self.lpan().marked
		elif Input.keyboard['H'].Pressed():
			self.main.logtxt = []
			self.main.logstart = 0
		elif Input.keyboard['X'].Pressed():
			raise 'hi'
		coord = (self.curx, self.cury) if Input.keyboard['LSHIFT'].Position() else (self.curx+1, self.cury)
		if Input.keyboard['J'].Pressed():
			if isinstance(coord, NonePanel):
				self.pan[coord] = Panel(len(colors)-1)
			self.pan[coord].c = (self.pan[coord].c-1) % len(colors)
			if self.pan[coord].c == 0: self.pan[coord].c = len(colors)-1
		elif Input.keyboard['K'].Pressed():
			if isinstance(self.lpan(), NonePanel):
				self.pan[coord] = Panel(1)
			self.pan[coord].c = (self.pan[coord].c+1) % len(colors)
			if self.pan[coord].c == 0: self.pan[coord].c = 1
		elif Input.keyboard['V'].Pressed():
			self.main.logtxt[:] = []
		elif Input.keyboard['SPACE'].Pressed():
			if not self.slowMode:
				self.fp = fps.FPSManager(5)
				self.log('slow mode')
			else:
				self.fp = fps.FPSManager(60)
				self.log('fast mode')
			self.slowMode = not self.slowMode
		for i in range(10):
			if Input.keyboard[str(i)].Pressed():
				self.__class__.__dict__['test'+str(i)](self)				

	def tick(self): # Called every 30 frames
		global im, colors
		if self.chainTimer > 0: self.chainTimer -= 1
		if self.t >= 60: self.t = 0
		else: self.t += 1 

		for x, i in enumerate(self.scheduled):
			if i.t > 0: i.t -= 1
			if i.t == 0:
				i()
				del self.scheduled[x]
				
		#raise 'hell'
		
		if self.comboMode is not None:
			self.pan.__class__.__dict__[self.comboMode](self.pan, self)
		self.processPanels()

		if len(self.combo) > 4:
			combolen = min(len(self.combo), self.maxcombo)
			self.score += (combolen-3)**2
			if self.chain > 1:
				self.score -= (self.chain-1)**2
				self.score += self.chain**2
			self.cards += [Card(self, self.cardx, self.cardy, Combo, combolen)]
#		if self.chainTimer:
		chain = False
		for _, _, p in self.combo:
			if p.canChain:
				chain = True
				self.unchain(p, 'combo')
				#self.log('%s can chain' % p)
		if chain:
			self.chain = min(self.chain+1, self.maxchain)
			#self.chainTimer = max(30 * (13-self.chain), 300)
			self.chainTimer = self.flashTime + 30 + len(self.combo) * self.popTime
			self.cards += [Card(self, self.cardx, self.cardy+1, Chain, self.chain)]
		if self.chainTimer == 0 and self.nCanChain == 0:
			if self.chain > 1:
				sound[Fanfare0+min(self.chain/3, 2)].Play()
				self.chainCount[self.chain]+=1					
			self.chain = 1
			
		im[Bg].Blit(0, 0)
		# draw panels
		for x, y, p in self.pan.iter():
			if p.c:
				p.draw(self, self.x, self.y + 16-self.offy, x, y)
		if self.save:
			for x, y, p in self.save[0].iter():
				if p.c:
					p.draw(self, self.x+144, self.y + 16-self.save[3], x, y)
		# draw cards
		for cardi, card in enumerate(self.cards):
			card.draw()
			card.tick()
			if card.t == 0:
				del self.cards[cardi]
		im[Fg].Blit(0, 0)
		# Draw cursor
		if self.t%30 < 15:
			curim = im[Cur0]
		else:
			curim = im[Cur1]
		curim.Blit(self.curx*16 + self.x-4, self.cury*16 - self.offy+self.y+12)
		
		#mx = ika.Input.mouse.x.Position()
		#my = ika.Input.mouse.y.Position()
		
		#ika.Video.DrawEllipse(mx, my, 6, 6, RGB(255,0,0), 1)
		#Video.DrawRect(self.x, self.y, self.x + (self.nrow*16), self.y + (self.ncolm*16), RGB(255, 255, 255))# Outline
		debugx, debugy = 256, 0
		logx, logy = 0, 225
		global logtxt, logstart
		text = []
		pa = self.pan[self.curx,self.cury]
		pb = self.pan[self.curx+1,self.cury]
		text.append('PAN:[%s] [%s]' % (pa, pb))
		text.append('nCanChain:%d chain:%d (%d,%d)' % (self.nCanChain, self.chain, self.curx, self.cury))
		text.append(self.vars('chainTimer offy', self))
		text.append('score:%d' % (self.score))
		#text.append('mx=%d my=%d' % (mx, my))
		#text.append('mx=%d my=%d', mx, my)
		#mx, my = Input.mouse.x.Position(), Input.mouse.y.Position()				
		
		#text.append('timer:%d' % self.t)
		for y, i in enumerate(text):
			res.f.Print(debugx, debugy+y*8, i)
		for y , i in enumerate(self.main.logtxt[self.main.logstart:self.main.logstart+48]):
			res.f.Print(logx, logy+y*8, i)
		Switchery = 48 
		for i in range(len(colors)):
			im[i].ClipBlit(debugx+i*16, Switchery, Futsu*16, 0, 16, 16)
			if   i==self.lpan().c:	res.f.Print(debugx+i*16, Switchery, 'L')
			elif i==self.rpan().c:	res.f.Print(debugx+8+i*16, Switchery, 'R')
		cx, cy = debugx+96, 48
		n = 0  # showchaincount()
		for k, v in self.chainCount.iteritems():
			if v != 0:
				n+=1
				im[Chain].ClipBlit(cx,cy+n*16, k*16, 32, 16, 16)
				self.bluef.Print(cx+16, cy+n*16, str(v))
		#self.testres.f.Print(80, 80, '88')
		if self.menu is not None:
			self.menu.draw()
		if self.__module__ == 'oldta':
			Video.DrawRect(0, 0, 639, 639, RGB(255, 0, 0))
			res.f.Print(0, 640-16, 'OLDTA: Press G or V to reload')
		self.t += 1
		self.control()