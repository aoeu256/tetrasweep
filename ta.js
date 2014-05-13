from xi import fps
from ika import *
from math import *
from tools import *
from input import *
import time, pickle, os, pdb, res, ika

# A lot of this is ripped off from phree_radical's VERGE

area = None

class Menu:
	function __init__(this, parent, choices=[], x=0, y=0, onMove=(lambda: None) ):
		this.choices = choices
		this.x, this.y = x, y
		this.parent = parent
		this.onMove = onMove
		this.cur = 0
		this.firstmove = False
	function draw(this):
		Video.DrawRect(this.x, this.y, this.x + 128, len(this.choices)*8, RGB(0,64,128), 1)
		Video.DrawRect(this.x, this.y+this.cur*8, this.x + 127, this.y+(this.cur+1)*8, RGB(255,0,0), 1)
		for y, i in enumerate(this.choices):
			res.f.Print(this.x, this.y+y*8, i)
	function control(this):
		if not this.firstmove:
			this.onMove()
		if Input.up.Pressed():
			this.cur = (this.cur - 1) % len(this.choices)
			this.onMove()
		if Input.down.Pressed():
			this.cur = (this.cur + 1) % len(this.choices)
			this.onMove()
		#logonce('R is %s' % R)
		#logonce('%s' % im[R])
	function choice(this):
		return this.choices[this.cur]

class Filelist(Menu):
	function __init__(this, parent, ext='', **args):
		lst = []
		for f in os.listdir(os.getcwd()):
			splt = f.split('.')
			if len(splt) > 1 and splt[1] == ext:
				lst.append(f)
		Menu.__init__(this, parent, choices=lst, **args)
#aoeu  @memoize



class NumberFont:
	function __init__(this, im):
		this.im = im
	function Print(this, x, y, s):
		im = this.im
		for p, i in enumerate(s):
			n = int(i)
			im.ClipBlit(x+8*p, y, n*8, 0, 16, 16)

function enum(lst):
	g = globals()
	num2name = []
	for n, i in enumerate(lst):
		g[i.title()] = n
		num2name.append(i.title())
	return num2name

function enumu(**enums):
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
function randColor():
	return Random(0, len(colorlst))

class Panel(object):
	function setst(this, state, t = 0):
		this.state, this.t = state, t
		#if this.state == Boing:
			
		if not isinstance(state, int):
			raise 'value is ' + state
	function __init__(this, c):
		this.c = c
		this.marked = False
		this.state = Futsu
		this.setst(Futsu)
		this.canChain = False
	function __repr__(this):
		try:
			return '%s %5s-%2d' % (colorName[this.c], stateName[this.state], this.t)
		except TypeError:
			print this.state, this.c
			return 'TypeError'
	function gstate(this):
		return this.state == Boing or this.state == Futsu
	function popstate(this):
		return this.state == Ppmae or this.state == Ppato
	function copy(this):
		newpan = Panel(this.c)
		newpan.state = this.state
		newpan.t = this.t
		newpan.canChain = this.canChain
		newpan.marked = this.marked
		try: # NonePanel does not have attributes
			newpan.popn = this.popn
			newpan.popt = this.popt
		except AttributeError: pass
		return newpan
	function draw(this, area, ax, ay, x, y):
		global f
		if this.state == Black or this.c==0:
			return # Skip drawing
		if   this.state == Rswap: swapx = area.swapTime-this.t
		elif this.state == Lswap: swapx = -(area.swapTime-this.t)
		else:				  swapx = 0
		if y == 11:				frame = Dark
		elif this.state == Futsu:	frame = Futsu
		elif this.state == Boing:	frame = B0 + (this.t/2)%3
		elif this.state == Ppmae:	frame = O_O
		elif this.state == Ppato:	return # Skip drawing
		elif this.state == Flash:	frame = Lit if this.t%2 else Futsu
		else:					frame = Futsu
		x1, y1 = ax + x*16 + (swapx * 16 / area.swapTime), ay + y*16
		
		im[this.c].ClipBlit(x1, y1, frame*16, 0, 16, 16)
		if this.canChain:
			res.f.Print(x1, y1, '*')
		if this.marked:
			res.f.Print(x1, y1, 'M')

class NonePanel(Panel):
	function __init__(this):
		Panel.__init__(this, 0)
	function setst(this, state, t = 0):
		Panel.setst(this, state, t)
		if this.state not in (Lswap, Rswap):
			this.state = Futsu
	function draw(this, *args):
		pass

class Panels: 
	function __init__(this, area, v = None):
		this.area, this.v = area, v
		if v is None:
			this.v = [[NonePanel() for column in range(area.nrow)] for row in range(area.ncolm)]
	function __setitem__(this, tup, p):
		p.x, p.y = tup
		this.v[p.y][p.x] = p
	function __getitem__ (this, (x, y)): return this.v[y][x]
	#__iter__ = lambda a: this.v.__iter__
			#fun(this, p.x, i)
	function topPanels(this, x, y, include=False):
		if include:
			yield y, this.v[y][x]
		for yi in range(y, -1, -1):
			if this.v[yi][x].c == 0:
				break
			yield yi, this.v[yi][x]
	function topGPanels(this, x, y, include=False):
		for yi, p in this.topPanels(x, y, include):
			if not p.gstate():
				break
#				if this.v[yi][x].state in (Fall, Hover) and this.v[yi][x].state == this.v[y][x].state and this.v[yi][x].t < 2:
#					pass
#				else:
			yield yi, this.v[yi][x]			
	function append(this, pans):
		this.v = this.v[1:] + [pans]
	function iter(this):
		for y, row in enumerate(this.v):
			for x, panel in enumerate(row):
				yield x, y, panel
	function backiter(this):
		h = this.area.ncolm-1
		for y, row in enumerate(reversed(this.v)):
			for x, panel in enumerate(row):
				yield x, h-y, panel
	function panepon(this, area):
		combo = this.area.combo
		combo[:] = []
		function linkUp(x1, y1, x2, y2, x3, y3):
			pa, pb, pc = pan[y1][x1], pan[y2][x2], pan[y3][x3]
			if pa.c and pa.c==pb.c==pb.c and all(p.gstate() for p in (pa, pb, pc)):
				combo += [(x1, y1, pa), (x2, y2, pb), (x3, y3, pc)]
		xlim = area.ncolm - 2
		ylim = area.nrow - 3
		for x, y, _ in this.iter():
			if x < xlim: linkUp(x,y,  x+1,y,  x+2,y)
			if y < ylim: linkUp(x,y,  x,y+1,  x,y+2)
	function puyo(this, area):
		this.pos2combo = {}
		combo = this.area.combo
		combo[:] = []
		function linkUp(pax, pay, pbx, pby):
			'tries to link up the panel at (pax, pay), with (pbx, pby)'
			pa = this.v[pay][pax]
			pb = this.v[pby][pbx]
			if pa.c and pa.c == pb.c and pa.gstate() and pb.gstate():
				if (pax, pay) in this.pos2combo:
					if (pbx, pby) in this.pos2combo: # if both pa and pb have a combo union the two combos together
						this.pos2combo[pax, pay] |= this.pos2combo[pbx, pby]
						this.pos2combo[pbx, pby] = this.pos2combo[pax, pay]
						this.pos2combo[pbx, pby-1] = this.pos2combo[pax, pay]
					else: # pb has no combo: add pb to pa's combo, then set pb's combo to pa
						this.pos2combo[pax, pay].add(pb)
						this.pos2combo[pbx, pby] = this.pos2combo[pax, pay]
				else:
					if (pbx, pby) in this.pos2combo: # pa has no combo
						this.pos2combo[pbx, pby].add(pa)
						this.pos2combo[pax, pay] = this.pos2combo[pbx, pby]
					else:
						this.pos2combo[pax, pay] = this.pos2combo[pbx, pby] = set([pa, pb])
		for x, y, _ in this.iter():
			if x < 5:  linkUp(x, y, x+1, y) # Try to link right
			if y < 10: linkUp(x, y, x, y+1) # Try to link down

		for x, y, p in this.iter():
			try:
				if len(this.pos2combo[x,y]) >= 4:
					combo.append( (x, y, p))
			except KeyError:
				pass

class CardList(list):
	function append(this, item):
		required = ['draw', 'tick']
		assert all(i in dir(item) for i in required)
		list.append(a, item)

class Card:
	Combo = 0
	Chain = 1
	function __init__(this, area, x, y, name, n):
		this.area, this.name = area, name
		this.x, this.y = x, y
		this.n = n
		this.t = 60
		this.maxt = this.t
		sound[S011].Play()
		xmid = 120
		ymid = 120
		xlast = 240
		ylast = 240
		#this.pedals = [(0,ymid), (xmid,0), (xmid,ylast), (xlast,ymid)]
		this.pedals = [0, pi/2, pi, 2*pi-pi/2]
		this.pedalSep = 200.0 / this.maxt
		this.finalSep = 6
	function draw(this):
		global im
		t = this.t/2
		y = (t-45)%45  + (this.y*16) + this.area.y
		x = this.x * 16 + this.area.x
		
		dang = 4*pi*t/this.maxt
		ds = max( this.pedalSep*t*t/this.maxt, this.finalSep)
		
		myexp = getCoord x, f: int(x+4+f(ang+dang))*ds
		
		for ang in this.pedals:
			im[Pedal].Blit(getCoord(x, cos), getCoord(x, sin))
			#this.area.log('%d %d' % (x+12+cos(ang+dang)*ds, y+12+sin(ang+dang)*ds))

		if this.name == Chain:
			im[Chain].ClipBlit(x, y, this.n*16, 32, 16, 16)
		else:
			im[Combo].ClipBlit(x, y, this.n*16, 0, 16, 16)
	function tick(this):
		this.t -= 1
	function __repr__(this):
		return '<Card%d (%d,%d) t=%d>' % (this.name, this.x, this.y, this.t)
class DoubleCard:
	function __init__(this, area, x, y):
		this.area = area
		this.x, this.y = x, y
		this.t = 15
	function tick(this):
		this.t-=1
	function draw(this):
		yt = this.t+this.y*16+this.area.y+8
		res.f.Print(this.area.x - 10 + this.x*16, yt, 'DOUBLE!')
class PanelPop:
	function __init__(this, area, x, y, n):
		this.area= area
		this.x = x * 16 + this.area.x + 9
		this.y = y * 16 + this.area.y + 24 - this.area.offy
		this.n = n 
		this.t = 15
		this.maxt = this.t
		f = min((this.area.chain-1)*10+n, 39)
		#f -= 3-n
		sound[Pop00+f].Play()
	function draw(this):
		global im
		r = this.maxt-this.t+3
		Video.DrawEllipse(this.x, this.y, r, r, RGB(255, 0, 255))		
	function tick(this):
		this.t -= 1
	function __repr__(this):
		return '<PanelPop(%d,%d) t=%d>' % (this.x, this.y, this.t)
class TestDraw:
	function __init__(this, drawf, t=80):
		this.t = t
		this.drawf = drawf
	function draw(this):
		this.drawf()
	function tick(this):
		this.t -= 1
class Task:
	function __init__(this, f, t=0):
		this.f = f
		this.t = t
	function __call__(this):
		this.f()
class PlayArea(AdvInput):
#	function setst(this, p, state, t = 0):
#		p.setst(state, t)
	function __init__(this, main, x, y, stack=None):
		global area
		area = a
		
		this.Debugmode = True
		
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
		
		this.main = main
		this.log = main.log
		this.logonce = main.logonce
		this.vars = main.vars
		this.logvars = main.logvars		
		this._copy = 'x y fp nrow ncolm character nCanChain chain t score deathTimer cardx cardy chainTimer score stackfile comboMode'
		this.x, this.y = 8, 19
		this.fp = fps.FPSManager(60)
		this.nrow = 6 
		this.ncolm = 12 
		this.character = ''
		this.nCanChain = 0 # Number of panels that can chain when this reaches zero the chain is RESET
		this.chain = 1			# The current chain number
		this.t = this.score = this.deathTimer = 0
		this.offy = 0			# When it becomes 16 a new row is made
		this.cardx = this.cardy = 40
		this.chainTimer = 0
		this.score = 0		
		this.slowMode = False
		this.maxchain = 19
		this.maxcombo = 19
		this.stackfile = 'slip.stack'		
		this.comboModes = 'none puyo panepon'.split(' ')
		this.comboMode = 'puyo'
		this.bluef = NumberFont(im[Fontnumblue])
		this.redf = NumberFont(im[Fontnumred])
		
		this._copy += ' chainCount comboCount'
		this.chainCount = dict((i, 0) for i in range(2, this.maxchain+1)) # Keep track of ur chains
		this.comboCount = dict((i, 0) for i in range(2, this.maxcombo+1)) # Keep track of ur combos		
		
		this._copyseq = 'cards scheduled'
		#this.swaps = []
		this.cards = []	# combos or chains, or other effects				
		this.scheduled = []

		this._config = 'flashTime hoverTime popTime swapTime fallTime'
		this._copy += ' ' + this._config
		this.flashTime = 100
		this.hoverTime = 10
		this.chainHoverTime = this.hoverTime * 2
		this.popTime = 20
		this.swapTime = 5
		this.fallTime = 2
		
		this._input = 'cancel okay right up down left stackButton'
		this._copy += ' ' + this._input
		this.cancel = Input.keyboard['D']
		this.okay = Input.keyboard['F']
		this.right = Input.right
		this.up = Input.up
		this.down = Input.down
		this.left = Input.left
		this.stackButton = Input.keyboard['W']
		
		this.menu = None
		this.menu_f = None
		this.menux = 20
		this.menuy = 20
		
		this.combo = []
		this.pan = Panels(this)
		this.save = None

		this.bottom = lambda: this.y + (this.ncolm*16)	
		this.lpan = lambda: this.pan[this.curx, this.cury]
		this.rpan = lambda: this.pan[this.curx+1, this.cury]
		
		this.setup(stack)
	
	curx = property(lambda this: this.xaxis.cur)
	cury = property(lambda this: this.yaxis.cur)
	
	function setup(this, stack = None):
		class TAAxis(Axis):
			function onMove(this):
				sound[S000].Play()
		this.xaxis = TAAxis((this.left,this.right), range(this.nrow-1), wrap = False)
		this.yaxis = TAAxis((this.up,this.down), range(this.ncolm-1), wrap = False)
				
		function newRow():			
			color = inrandom([x for x in colorPanels if x!=this.pan[0,this.ncolm-2].c])
			newR = [Panel(color)] # The new row with one panel on the left with a random color
			for x in range(1,this.nrow):
				# color_subset = [c for c in colors if c != newR[x-2].c and c!= this.pan[x,10].c] Tetris Attack
				
				color_subset = [c for c in colorPanels if c != newR[x-1].c and c != this.pan[x, this.ncolm-2].c] # Puyo
				newR.append(Panel(inrandom(color_subset)))
			return newR
		if stack is None:
			for _ in range(11):
				nR = newRow()
				this.pan.append(nR)
			
		function raiseStack(n = None):
			this.offy += 1
			if this.offy == 16:
				this.offy = 0
				for p in this.pan.v[0]:
					if p.canChain:
						this.nCanChain -= 1
				if n is None:
					n = newRow()
				this.pan.v = this.pan.v[1:] + [n]

				this.yaxis.cur = max(this.yaxis.cur-1, 0)
				#else: this.deathTimer += 1	
			return n
		function swap():
			pa = this.pan[this.curx,this.cury]
			pb = this.pan[this.curx+1,this.cury]

			# force swap to finish
			function addDouble():
				this.cards.append(DoubleCard(this, this.curx, this.cury))
			if   pa.state == Lswap:
				addDouble()
				this.rswap(this.curx-1, this.cury)
			elif pb.state == Rswap: # Force swap for left stealth: [a<->b]<->c]=c b a
				addDouble()
				this.rswap(this.curx+1, this.cury)
			pa = this.pan[this.curx,this.cury]
			pb = this.pan[this.curx+1,this.cury]

			if this.cury == 0:
				hovercond = True
			else:
				pua = this.pan[this.curx,this.cury-1]
				pub = this.pan[this.curx+1,this.cury-1]
				hovercond = pua.state != Hover and pub.state != Hover
			if pa.gstate() and pb.gstate() and hovercond:
				pa.setst(Rswap, this.swapTime)
				pb.setst(Lswap, this.swapTime)
				#this.swaps.append ( (pa, pb) )
				#this.swaphistory[pa, pb] = [] # add a list
				#if pa.c and pb.c:
				#	sound[S003].Play()
		this.raisestack = Button([this.stackButton], raiseStack, press = 'Position')
		this.swap = Button([Input.keyboard[k] for k in 'DF'], swap)
		AdvInput.__init__(this, 0, 12, [this.xaxis, this.yaxis], [this.swap, this.raisestack])

	function copyCur(this, area):
		this.xaxis.cur = area.xaxis.cur
		this.yaxis.cur = area.yaxis.cur
		this.offy = area.offy		

	function copy(this):
		newarea = PlayArea(this.main, 50, 50)
		n = newarea.__dict__
		o = this.__dict__
		newarea.copyCur(this)
		
		for c in this._copyseq.split(' '):
			for i in o[c]:
				try:
					i.area = this
				except KeyError:
					this.log('object %s does not have area attr' % i)
			
		for c in this._copy.split(' '):
			n[c] = o[c]
			
		for c in this._copyseq.split(' '):
			for i in o[c]:
				try:
					i.area = this
				except KeyError:
					this.log('object %s does not have area attr' % i)
		newarea.pan.v = this.copyStack(this.pan.v)
		for x, y, _ in this.combo:
			newarea.combo.append(x, y, newarea.pan[x,y])
		return newarea
	function schedule(this, f, t=0):
		this.scheduled.append(Task(f, t))
	function canFall(this, x, y):
		if y == this.ncolm-1:
			return False
		p = this.pan[x,y+1]
		if p.c == 0:
			return p.state not in (Rswap, Lswap)
		else:
			return p.state == Black
	function unchain(this, p, where):
		if p.marked:
			this.log('unchaining %s %s' % (p, where))
		if p.canChain:
			p.canChain = False
			this.nCanChain -= 1
#		log('nchain disrupted on %s: nchain=%d' % (p.c, p.state, this.nCanChain))
	function save2Panels(this):
		dumT = (this.lpan(), this.rpan())
		pickle.dump(dumT, file('paneldump', 'w'))
		this.log('dumped a panel: %s' % [dumT])
	function load2Panels(this):
		g = pickle.load(file('paneldump'))
		this.log('loaded a panel: %s' % [g])
		this.pan[this.curx, this.cury], this.pan[this.curx+1,this.cury] = g
	function test1(this):
		#for i in range(48):
		#	this.log('%d' % i)
		this.log(this.pan[4,4].__dict__)
	function test2(this, n = [0]):
		#this.cards.append(Card(this, 3, 5, Combo, 6))
		#this.cards.append(PanelPop(this, 5, 4, n[0]))
		this.cards.append(DoubleCard(this, this.curx, this.cury))
		#n[0]+=1
		#this.log('n is %d' % n[0])
	function test3(this):
		#this.log('%s' % this.cards)
		#this.log(str(this.x))
		#for x, y, p in this.pan.iter():
		#	if p.canChain:
		#		this.logvars('x y p', locals())
		for pa, pb in this.swaps:
			this.log('%s %s' % (pa, pb))
			if set([pa.state, pb.state]) & set([Rswap, Lswap]):
				for s in this.swaphistory[pa, pb]:
					this.log('	%s' % s)
	function test5(this):
		testf = NumberFont(Image('graphics/Font_NumBlue.png'))
		function draw():
			testres.f.Print(50, 50, '0123456789')
		this.cards.append(TestDraw(draw, 800))
		this.log("created testf")
	function testStack(this):
		for i in this.pan.v:
			this.log('%s' % i)
		this.log('---')
		if this.save:
			for i in this.save[0].v:
				this.log('%s' % i)
	function test4(this):
		#function fun():
		#	this.log('hello world')
		#this.schedule(fun)
		this.log(this.chainCount)
		this.log(this.comboCount)
	function setstackfile(this):
		this.stackfile = 'statetest.stack'
		this.log('stack file is %s' % this.stackfile)		
	function copyStack(this, stack):
		return [[p.copy() for p in row] for row in stack]
	function saveStack(this): # Save stack
		pickle.dump((this.copyStack(this.pan.v), this.curx, this.cury, this.offy), file(this.stackfile, 'w'))
		this.log('Saved stack to %s' % this.stackfile)
	function loadStack(this): # Load stack
		save = pickle.load(file(this.stackfile))
		#save = this.save
		this.pan.v = this.copyStack(save[0])
		this.xaxis.cur, this.yaxis.cur = save[1], save[2]
		this.offy = save[3]
	function setsaveStack(this):
		save = pickle.load(file(this.stackfile))
		this.save = (Panels(this, save[0]), save[1], save[2], save[3])
	function pickStackfile(this):
		this.stackfile = this.menu.choice()
	function cardTest(this):
		this.cards = [Card(this, 1, 1, Chain, 5), Card(this, 2, 2, Combo, 8)]
	#function processSwaps(this):
	#	'for debugging swaps'
		#for x, (pa, pb) in enumerate(this.swaps):
		#	info = '%s %s' % (pa, pb)
		#	if pa.t != 0 or pb.t != 0:
		#		this.swaphistory[pa, pb].append(info)
			#if pa.state not in (Rswap, Lswap) and pb.state not in (Rswap, Lswap):
			#	del this.swaphistory[pa, pb]
			#	del this.swaps[x]
	function rswap(this, x, y):
		#this.log('%s' % this.pan[x+1,y])
		this.pan[x,y], this.pan[x+1,y] = this.pan[x+1,y], this.pan[x,y]
		function setst(x, y):
			#this.log('doing swap %d,%d %s %s' % (x,y, this.pan[x,y], this.canFall(x, y)))
			if this.canFall(x, y):
				this.pan[x,y].setst(Hover, this.hoverTime)
			else:
				this.pan[x,y].setst(Futsu, 0)
		setst(x, y)
		setst(x+1, y)
	function ptext(this, x, y, p):
		return '%d,%d %s' % (x, y, p)	
	function processPanels(this):
		if this.combo:
			this.cardx, this.cardy = this.combo[0][0], this.combo[0][1]
			for n, (x, y, p) in enumerate(this.combo):
				#if p.gstate(): # if gstate really needed?
				p.setst(Flash, this.flashTime)
				p.popn = n
				p.popt = this.popTime * (len(this.combo)-n)
			#this.combos.append(this.combo[:])
			#this.log('combo is %s ' % list(this.combo))
		#for n, c in enumerate(this.combos):
			#this.log('%d %s' % (n, list(c)))
			#if c[0][2].t == 0 and c[0][2].state == Ppato:
				#for x, y, p in c:
					#
				#del this.combos[n]
		for x, y, p in this.pan.backiter():
			bp = this.pan[x,y+1] if y != this.ncolm - 1 else None # Bottom panel
			if p.c == 0: # logic for NonePanels
				if p.t > 0: p.t -= 1
				if p.t == 0:
					if p.state == Rswap and p.t == 0:
						this.rswap(x, y)
					elif p.state != Lswap:
						p.state = Futsu
				continue
			if p.marked and p.state != Futsu:
				if p.state != Ppato or p.t != 0:
					this.log('%d(%d,%d) %s' % (p.canChain, x, y, p))	
			if p.state == Futsu:
				if p.canChain:
					if bp is None or bp.state not in (Rswap, Lswap, Hover, Fall):
						if p.marked:
							this.log('bottom:(%d,%d)%s' % (x,y+1,bp))
						this.unchain(p, 'Futsu')
				if this.canFall(x, y):
					if p.marked:
						this.log('%d,%d%s Fall from Futsu state...' % (x,y,p))
					for yi, tp in this.pan.topPanels(x, y, True):
						tp.setst(Hover, this.chainHoverTime)
				continue
			elif p.state == Fall:
				bpcond = bp is None or bp.state != Fall
				if not this.canFall(x, y) and bpcond: # Landing
					if p.marked:
						this.log("%s can land" % this.ptext(x, y, p))
					p.setst(Boing, 5)
					for y, tp in this.pan.topPanels(x, y-1):
						if tp.gstate() or tp.state == Fall:
							tp.setst(Boing, 5)
							if tp.marked:
								this.log("  %s is BOINGING" % tp)
					continue			
			if p.t > 0:
				p.t -= 1
				if p.state == Boing and p.t == 3:
					sound[S005].Play()
				continue
			# Timer based state changes
			if p.state == Rswap:
				this.rswap(x, y)
			elif p.state == Hover:
				for yi, tp in this.pan.topPanels(x, y, True):
					tp.setst(Fall, 0)
			elif p.state == Ppato:
				this.unchain(p, 'Ppato')
				this.pan[x,y]=NonePanel()
				if y > 1:
					for _, tp in this.pan.topGPanels(x, y-1): # Set a few chains...
						#this.log('Considering (%d,%d)%s' % (x,yi,this.pan[x,yi]))
						tp.setst(Hover, this.hoverTime)
						tp.canChain = True
						this.nCanChain += 1
			elif p.state == Flash:
				p.setst(Ppmae, p.popn * this.popTime)
			elif p.state == Ppmae:
				p.setst(Ppato, p.popt)
				this.cards.append(PanelPop(this, x, y, p.popn))
			elif p.state == Boing:
				p.setst(Futsu)
			elif p.state == Fall:				
				# Falling motion, swap the empty panel with the solid panel
				#if this.canFall(x, y):
				if bp is None or not (bp.state == Fall and bp.t == 0):
					p.t = this.fallTime
					if p.marked:
						this.log("  falling %s %s" % (this.ptext(x, y, p), this.ptext(x, y, bp)))
					for yi, tp in this.pan.topPanels(x, y, True):
						if tp.gstate() or tp==p:
							this.pan[x, yi],  this.pan[x, yi+1] = NonePanel(), this.pan[x, yi]
						else:
							break
	function control(this):
		'handle input'
		if this.menu is not None:
			this.menu.control()
			if this.cancel.Pressed():
				this.menu = None
			elif this.okay.Pressed():
				this.menu_f()
				this.menu = None
		elif Input.keyboard['LCTRL'].Position():
			if Input.up.Position():
				this.main.logstart = max(0, this.main.logstart-1)
			elif Input.down.Position():
				this.main.logstart = min(1024, this.main.logstart+1)
		else:
			AdvInput.tick(this)
		if Input.keyboard['F2'].Pressed():
			this.saveStack()
		elif Input.keyboard['F3'].Pressed():
			function loadIntoSaved():
				this.stackfile = this.menu.choice()
				this.setsaveStack()
			this.menu = Filelist(this, 'stack', onMove=loadIntoSaved, x=this.menux, y=this.menuy)
			this.menu_f = this.pickStackfile
			return
		elif Input.keyboard['F10'].Pressed():
			function pick(this):				
				if this.menu.choice() == 'none':
					this.comboMode = None
				else:
					this.comboMode = this.menu.choice()				
			this.menu = Menu(this, this.comboModes, this.menux, this.menuy)
			this.menu_f = pick
		elif Input.keyboard['F4'].Pressed():
			this.loadStack()
		elif Input.keyboard['M'].Pressed():
			this.log('Marked %s' % this.lpan())
			this.lpan().marked = not this.lpan().marked
		elif Input.keyboard['H'].Pressed():
			this.main.logtxt = []
			this.main.logstart = 0
		elif Input.keyboard['X'].Pressed():
			raise 'hi'
		coord = (this.curx, this.cury) if Input.keyboard['LSHIFT'].Position() else (this.curx+1, this.cury)
		if Input.keyboard['J'].Pressed():
			if isinstance(coord, NonePanel):
				this.pan[coord] = Panel(len(colors)-1)
			this.pan[coord].c = (this.pan[coord].c-1) % len(colors)
			if this.pan[coord].c == 0: this.pan[coord].c = len(colors)-1
		elif Input.keyboard['K'].Pressed():
			if isinstance(this.lpan(), NonePanel):
				this.pan[coord] = Panel(1)
			this.pan[coord].c = (this.pan[coord].c+1) % len(colors)
			if this.pan[coord].c == 0: this.pan[coord].c = 1
		elif Input.keyboard['V'].Pressed():
			this.main.logtxt[:] = []
		elif Input.keyboard['SPACE'].Pressed():
			if not this.slowMode:
				this.fp = fps.FPSManager(5)
				this.log('slow mode')
			else:
				this.fp = fps.FPSManager(60)
				this.log('fast mode')
			this.slowMode = not this.slowMode
		for i in range(10):
			if Input.keyboard[str(i)].Pressed():
				this.__class__.__dict__['test'+str(i)](this)				

	function tick(this): # Called every 30 frames
		global im, colors
		if this.chainTimer > 0: this.chainTimer -= 1
		if this.t >= 60: this.t = 0
		else: this.t += 1 

		for x, i in enumerate(this.scheduled):
			if i.t > 0: i.t -= 1
			if i.t == 0:
				i()
				del this.scheduled[x]
				
		#raise 'hell'
		
		if this.comboMode is not None:
			this.pan.__class__.__dict__[this.comboMode](this.pan, this)
		this.processPanels()

		if len(this.combo) > 4:
			combolen = min(len(this.combo), this.maxcombo)
			this.score += (combolen-3)**2
			if this.chain > 1:
				this.score -= (this.chain-1)**2
				this.score += this.chain**2
			this.cards += [Card(this, this.cardx, this.cardy, Combo, combolen)]
#		if this.chainTimer:
		chain = False
		for _, _, p in this.combo:
			if p.canChain:
				chain = True
				this.unchain(p, 'combo')
				#this.log('%s can chain' % p)
		if chain:
			this.chain = min(this.chain+1, this.maxchain)
			#this.chainTimer = max(30 * (13-this.chain), 300)
			this.chainTimer = this.flashTime + 30 + len(this.combo) * this.popTime
			this.cards += [Card(this, this.cardx, this.cardy+1, Chain, this.chain)]
		if this.chainTimer == 0 and this.nCanChain == 0:
			if this.chain > 1:
				sound[Fanfare0+min(this.chain/3, 2)].Play()
				this.chainCount[this.chain]+=1					
			this.chain = 1
			
		im[Bg].Blit(0, 0)
		# draw panels
		for x, y, p in this.pan.iter():
			if p.c:
				p.draw(this, this.x, this.y + 16-this.offy, x, y)
		if this.save:
			for x, y, p in this.save[0].iter():
				if p.c:
					p.draw(this, this.x+144, this.y + 16-this.save[3], x, y)
		# draw cards
		for cardi, card in enumerate(this.cards):
			card.draw()
			card.tick()
			if card.t == 0:
				del this.cards[cardi]
		im[Fg].Blit(0, 0)
		# Draw cursor
		if this.t%30 < 15:
			curim = im[Cur0]
		else:
			curim = im[Cur1]
		curim.Blit(this.curx*16 + this.x-4, this.cury*16 - this.offy+this.y+12)
		
		#mx = ika.Input.mouse.x.Position()
		#my = ika.Input.mouse.y.Position()
		
		#ika.Video.DrawEllipse(mx, my, 6, 6, RGB(255,0,0), 1)
		#Video.DrawRect(this.x, this.y, this.x + (this.nrow*16), this.y + (this.ncolm*16), RGB(255, 255, 255))# Outline
		debugx, debugy = 256, 0
		logx, logy = 0, 225
		global logtxt, logstart
		text = []
		pa = this.pan[this.curx,this.cury]
		pb = this.pan[this.curx+1,this.cury]
		text.append('PAN:[%s] [%s]' % (pa, pb))
		text.append('nCanChain:%d chain:%d (%d,%d)' % (this.nCanChain, this.chain, this.curx, this.cury))
		text.append(this.vars('chainTimer offy', this))
		text.append('score:%d' % (this.score))
		#text.append('mx=%d my=%d' % (mx, my))
		#text.append('mx=%d my=%d', mx, my)
		#mx, my = Input.mouse.x.Position(), Input.mouse.y.Position()				
		
		#text.append('timer:%d' % this.t)
		for y, i in enumerate(text):
			res.f.Print(debugx, debugy+y*8, i)
		for y , i in enumerate(this.main.logtxt[this.main.logstart:this.main.logstart+48]):
			res.f.Print(logx, logy+y*8, i)
		Switchery = 48 
		for i in range(len(colors)):
			im[i].ClipBlit(debugx+i*16, Switchery, Futsu*16, 0, 16, 16)
			if   i==this.lpan().c:	res.f.Print(debugx+i*16, Switchery, 'L')
			elif i==this.rpan().c:	res.f.Print(debugx+8+i*16, Switchery, 'R')
		cx, cy = debugx+96, 48
		n = 0  # showchaincount()
		for k, v in this.chainCount.iteritems():
			if v != 0:
				n+=1
				im[Chain].ClipBlit(cx,cy+n*16, k*16, 32, 16, 16)
				this.bluef.Print(cx+16, cy+n*16, str(v))
		#this.testres.f.Print(80, 80, '88')
		if this.menu is not None:
			this.menu.draw()
		if this.__module__ == 'oldta':
			Video.DrawRect(0, 0, 639, 639, RGB(255, 0, 0))
			res.f.Print(0, 640-16, 'OLDTA: Press G or V to reload')
		this.t += 1
		this.control()