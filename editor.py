from symbol import if_stmt
import itertools
import sys
import re
import traceback
from xi import fps
from ika import *
import copy, res, ika, inspect, re, traceback, parent, keyword, tokenize, token, getword
from StringIO import StringIO
from itertools import chain

import pdb

#a = pdb.Pdb()

repeatRate = 2
repeatDelay = 15
repeatCount = 0

same = lambda char: (char, char)
control2key = {'BACKQUOTE':('`','~'), 'TAB':same('\t'), 'SPACE':same(' '), 'LEFTBRACKET':('[','{'), 'RIGHTBRACKET':(']','}'), 'SLASH':('/', '?'), 'BACKSLASH':('\\', '|'), 'QUOTE':("'", '"'), 'COMMA':(',', '<'), 'PERIOD':('.', '>'), 'SEMICOLON':(';', ':'), 'MINUS':('-', '_'), 'EQUALS':('=', '+')}
unshifted = ' abcdefghijklmnopqrstuvwxyz1234567890'
shifted =   ' ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()'
qwerty =   r" abcdefghijklmnopqrstuvwxyz1234567890-=[]/',.\;`"
dvorak =   r" axje.uidchtnmbrl'poygk,qf;1234567890[]/=z-wv\s`"
qwertys =  r' ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+{}?"<>|:~'
dvoraks =  r' AXJE>UIDCHTNMBRL"POYGK<QF:!@#$%^&*(){}?+Z_WV|S~'
allqwerty = ''.join([qwerty, qwertys])
alldvorak =''.join([dvorak, dvorak])

clipboard = ''
qwerty2dvorak = dict((allqwerty[i], alldvorak[i]) for i in range(len(allqwerty)))

for i in range(len(unshifted)):
	control2key[unshifted[i].upper()] = (unshifted[i], shifted[i])

key2control = dict((v1,k) for k, (v1, _) in control2key.iteritems())

shifted = dict((qwerty[i], qwertys[i]) for i in range(len(qwerty)))

clamp = lambda x, lt, gt: max(min(x, gt), lt)
sorted2 = lambda a, b: (b, a) if a > b else (a, b)

class EditCursor:
	def __init__(self, line, col):
		self.line, self.col = line, col
	def __repr__(self):
		return '[Cur %d %d]' % (self.col, self.line)

class SyntaxColoredf(object):
	kset = set(keyword.kwlist)
	def __init__(self, f=res.f):
		self.f = f
	def __getattr__(self, attr):
		return getattr(self.f, attr)
	def Print(self, x, y, text):
		Print = self.f.Print
		
		comment = 53 
		colors = {53:'A0A0A0', token.NAME:'FFFFFF', token.STRING:'0000FF', token.NUMBER:'FF00FF'}
		amt = 0
		try:
			for (typeId, tok, start_tup, end_tup, _) in tokenize.generate_tokens(StringIO(text).readline):			
				if typeId == token.NAME: 
					if tok in kset:
						color = 'FFA000'
					else:
						color = 'FFFFFF'
				else:
					color = colors.get(typeId, 'FFFFFF')
				Print(x+start_tup[1]*f.width, y, '#[FF%s]%s'% (color, tok))
				amt = end_tup[1] # How much of the line was consumed
		except tokenize.TokenError:
			Print(x+amt*f.width, y, text[amt:])
#class SyntaxColoredLine(object):
#	def __init__(self, text):		
#		self._img = None
#		self.text = text
#	def _settext(self, text):
#		self._text = text
#		f = res.f
#		kset = set(keyword.kwlist)
#		
#		comment = 53 
#		colors = {53:'A0A0A0', token.NAME:'FFFFFF', token.STRING:'0000FF', token.NUMBER:'FF00FF'}
#		
#		canvas = ika.Canvas(len(text)*f.width, 8)
#		for (typeId, tok, start_tup, end_tup, _) in tokenize.generate_tokens(StringIO(text).readline):			
#			if typeId == token.NAME: 
#				if tok in kset:
#					color = 'FFA000'
#				else:
#					color = 'FFFFFF'
#			else:
#				color = colors.get(typeId, 'FFFFFF')			
#			canvas.DrawText(f, start_tup[1]*f.width, 0, '#[FF%s]%s'% (color, tok))
#		self._image = ika.Image(canvas)
#	text = property(lambda self: self._text, _settext)
#		
#	def Print(self, x, y):
#		self._image.Blit(x, y)


class GuiArea(object):
	def __init__(self, x1, y1, x2=0, y2=0):
		self.x1 = x1
		self.y1 = y1 
		self.x2 = x2
		self.y2 = y2
	width = property(lambda self: self.x2 - self.x)
	height = property(lambda self: self.y2 - self.y)
	def setpos(self, x, y):
		self.x2 = self.width + x
		self.y2 = self.height + y
		self.x1 = x
		self.y1 = y
	def resize(self, width, height):
		self.x2 = self.x1+width
		self.y2 = self.y1+height
	def inArea(self):
		x, y = self.mousepos()
		return self.x1 < x < self.x2 and self.y1 < y < self.y2 
	def mousepos(self):
		return (int(ika.Input.mouse.x.Position()), int(ika.Input.mouse.y.Position()))	
	def mousetotextpos(self, f=res.f):
		mx, my = self.mousepos()
		return ((mx-self.x1)/f.width, (my-self.y1)/f.height)
	def draw(self):
		outlineColor = RGB(255, 255, 255)
		ika.Video.DrawRect(self.x1, self.y1, self.x2, self.y2, outlineColor)
		
class Canvas(GuiArea):
		def __init__(self, x=0, y=0, width=80, height=80, m=10):
			self.mx, self.my = width/m, height/m
			self.pix = [[0 for x in range(self.mx)] for y in range(self.my)]
			self.m = m
			GuiArea.__init__(self, x, y, width+x, height+y)
		def draw(self):
			
			GuiArea.draw(self)
			for x in range(self.mx):
				for y in range(self.my):
					if self.pix[y][x]:
						ika.Video.DrawRect(x*self.mx, y*self.my, (x+1)*self.mx, (y+1)*self.my, RGB(255, 255, 255))
		def onClick(self, x, y):
			self.pix[y][x] = 1
class PopupMenu(GuiArea):
	outSize = 2
	popf = res.f
	def __init__(self, parent, x, y, choices):
		self.visible = True
		self.parent = parent
		self.log = self.parent.log		
		self.inputCatch = False
		GuiArea.__init__(self, x, y)
		self.choices = choices # call _setchoices
	def _setchoices(self, choices):
		f = PopupMenu.popf
		self._choices = choices
		self.choice = 0
		longestchoice =  max(len(choice) for choice in self._choices)
		oZ = PopupMenu.outSize*2
		self.resize(oZ+f.width*longestchoice, oZ+f.height*len(choices))
	choices = property(lambda self: self._choices, _setchoices)
	
	def draw(self):
		f = res.f
		x1, y1 =  self.x1 - PopupMenu.outSize, self.y1 - PopupMenu.outSize  
		x2, y2 =  self.x2 + PopupMenu.outSize, self.y2 + PopupMenu.outSize
		ika.Video.DrawRect(x1, y1, x2, y2, RGB(0,0,0), 1)
		ika.Video.DrawRect(x1, y1, x2, y2, RGB(255, 255, 255))
		#self.log('drawing')
		if self.inArea():
			mx, my = self.mousepos()			
			self.choice = min((int(my) - self.y1) / f.height, len(self.choices)-1)
		cy = self.choice*res.f.height
		ika.Video.DrawRect(self.x1, self.y1+cy, self.x2, self.y1+cy+f.height, RGB(0,0,196), 1)
		for y, i in enumerate(self.choices):
			res.f.Print(self.x1, self.y1+y*f.height, i)
		#draw.hline(self.x1, self.y1, self.x2, (255,0,0))
		#draw.hline(self.x1, self.y2, self.x2, (0,255,0))
	def click(self):
		if self.inArea():
			self.RETURN()
	def move(self, dire):		
		self.choice = (self.choice+dire) % len(self.choices)
		self.log('%d %d' % (self.choice, dire))
	def UP(self):
		self.move(-1)
	def DOWN(self):
		self.move(1)		
	def RETURN(self):
		name = self.choices[self.choice]
		try:
			getattr(self, name)()
		except KeyError:
			self.log("%s is not found." % name)
		self.visible = False
	def TAB(self):
		self.log('Cant think of anything now')
	def input(self, cmds = ('UP', 'DOWN', 'RETURN', 'TAB')):
		#self.log("input is being called")
		self.inputCatch = False # did not catch input
		for i in cmds:
			if ika.Input.keyboard[i].Pressed():
				self.log(i+'is being pressed')
				getattr(self, i)()
				self.inputCatch = True

class Region(GuiArea):
	'subclass and replace curline'
	keyRepeat = 3
	keyDelay = 20
	defaultCommands = set('home end left right delete f1 f2 f3 f4 f5'.split(' '))
	defaultCtrlCommands = set('')
	defaultAltCommands = set('')
	tabchar = '    '
	speckeys = {'\r':'return', '\x08':'backspace', '\x7f':'delete', ' ':'space', '\t':'tab'}
	invertspeckeys = dict((v,k) for k, v in speckeys.iteritems())
	def __init__(self, main, x, y, keyCommands=None, setcurline=True):
		if setcurline:
			self.curline = ''
		self.cur = EditCursor(0,0)
		self.marker = None
		self.name = ''
		self.main = main
		self.log = self.main.log
		self.lastkey = None
		self.lastcontrol = None
		self.lastcommand = None
		self.keytimer = 0
		GuiArea.__init__(self, x, y, x2=x + res.f.width * 60, y2=y + res.f.height)
		self.topline = 0
		self.activeMarker = lambda: self.marker is not None and (self.marker.col, self.marker.line) != (self.cur.col, self.cur.line)
		self.shifted = False
		self.t = 0
		if keyCommands is None:
			self.keyCommands = Region.defaultCommands
		else:
			self.keyCommands = keyCommands
		self.ctrlCommands = {'c':'copySelection', 'v':'pasteSelection', 
			'd':'end', 'a':'home', 'b':'eval', 'k':'deleteline'}		
		self.altCommands = {}	
	def allCommands(self):
		return itertools.chain(self.keyCommands, self.ctrlCommands, self.altCommands)
	def copy(self):
		return copy.copy(self)
	def trykey(self, key):
		if key.Position():
			d = key.Delta()
			if d == 1.0:
				self.repeatCount = 0
				return True
			else:
				self.repeatCount += 1
				if self.repeatCount == self.repeatDelay:
					self.repeatCount = self.repeatDelay - self.repeatRate
					return True
		return False
#	line = property(lambda: ) Make the other guys implement this.
	def shift(self):
		if self.marker is None:
			self.marker = EditCursor(self.cur.line, self.cur.col)
	def deleteSelection(self):
		a, b = sorted2(self.cur.col, self.marker.col)		
		self.cur.col = a
		self.marker = None
		self.curline =	''.join([self.curline[:a], self.curline[b:]])
	def drawSelection(self):
		if self.activeMarker():
			Video.DrawRect(self.x1 + self.cur.col * res.f.height , 
						   self.y1 + self.cur.line * res.f.height,
						   self.x1 + self.marker.col * res.f.height,
						   self.y1 + (self.cur.line+1) * res.f.height, RGB(0,0,196), 1) 
	def drawOutline(self):
		Video.DrawRect(self.x1, self.y1, self.x2, self.y2, RGB(0,0,0), 1)
		Video.DrawRect(self.x1, self.y1, self.x2, self.y2, RGB(255,255,255))
		#Video.DrawRect(self.x-4, self.y2+4, self.x2+4, self.y2+res.f.height+8, RGB(255, 255, 255))
	def drawTextCursor(self):
		curx = self.x1 + 1 + res.f.width * self.cur.col
		cury = self.y1 + 1 + (self.cur.line - self.topline)*res.f.height
		col = [RGB(255,0,255), RGB(255,0,0)]
		Video.DrawLine(curx, cury, curx, cury + res.f.height, col[(self.t / 30) % 2]) # Cursor		
	def drawText(self):
		x1 = self.x1+1
		y1 = self.y1+1
		try:
			res.f.Print(x1, y1, self.curline)
		except AttributeError:
			self.log(self)
			raise
	def draw(self):
		self.drawOutline()
		self.drawSelection()
		self.drawText()
		self.drawTextCursor()
	def replaceField(self, field, value, line):
		line = re.sub(r'\b(%s=[0-9]*)' % field, '%s=%s'% (field, value), line)
	def move(self, cur, col, line): # Use for Home, End, Left, Right, Down, Up
		#if not Input.keyboard['LSHIFT'].Position():
		#	self.marker = None
		#cur.col = max(col, 0)
		#cur.line = clamp(line, 0, len(self.lines)-1)
		self.shifted = Input.keyboard['LSHIFT'].Position()
		if self.shifted and self.marker is None:
			self.marker = EditCursor(self.cur.line, self.cur.col)
		if not self.shifted:
			self.marker = None
		self.cur.line = line
		self.cur.col = clamp(col, 0, len(self.curline))	
	def f1(self):
		self.log(self.curline)
	def space(self):
		self.handleChar(' ')
	def shiftposition(self):
		return Input.keyboard['LSHIFT'].Position() or Input.keyboard['RSHIFT'].Position() 
	def tab(self):
		#if self.activeMarker():
		#	self.deleteSelection()
		if self.shiftposition():			
			self.pressTab(self.removeTab)
			self.cur.col = max(self.cur.col-len(Region.tabchar), 0) 
		else:
			self.pressTab(self.addTab)
			self.cur.col = min(self.cur.col+len(Region.tabchar), len(self.curline))
			
	def pressTab(self, tabf):
		#if self.marker is not None:
		self.curline = tabf(self.curline)
		self.cur.col += len(Region.tabchar)	
	def addTab(self, line):
		return ''.join([Region.tabchar, line])
	def removeTab(self, line):
		for x in range(len(Region.tabchar)):
			if line == '':
				break
			if line[0] == ' ':
				line = line[1:]
		return line
	def handleChar(self, key, dvorak=True):
		if key is None:
			return
		if self.activeMarker():
			self.deleteSelection()
		if dvorak:
			char = qwerty2dvorak.get(key, key)

		if Input.keyboard['LSHIFT'].Position() or Input.keyboard['RSHIFT'].Position():
			char = shifted[char]				 
		self.curline = ''.join([self.curline[:self.cur.col], char, self.curline[self.cur.col:]])
		self.cur.col += len(char)

	def copySelection(self):
		a, b = sorted2(self.cur.col, self.marker.col)
		self.clipboard = self.curline[a:b]
	def pasteSelection(self):
		self.curline = ''.join([self.curline[:self.cur.col], self.clipboard, self.curline[self.cur.col:]])
	def left(self):
		self.move(self.cur, self.cur.col-1, self.cur.line)
	def right(self):
		self.move(self.cur, self.cur.col+1, self.cur.line)
	def backspace(self):
		if self.activeMarker():
			self.deleteSelection()		
		elif self.cur.col > 0:
			self.curline = ''.join([self.curline[:self.cur.col-1], self.curline[self.cur.col:]])
			self.cur.col -= 1
	def home(self):
		wp = 0
		for x, i in enumerate(self.curline):
			if i not in (' ', '\n'):
				wp = x
				break
		self.move(self.cur, 0 if self.cur.col == wp else wp, self.cur.line)
	def end(self):
		self.move(self.cur, len(self.curline), self.cur.line)
	def delete(self):
		if self.activeMarker():
			self.deleteSelection()
		else:
			self.right()
			self.backspace()
	def copyCur(self, region):
		self.cur = region.cur		
	def CtrlPress(self, inp):
		return inp.Pressed()
	def deleteline(self):
		self.curline = ''
	def listCommands(self, dict):
		self.log('%-8s %-15s %s' % ('KEY', 'NAME', 'DESCRIPTION'))
		for k, v in dict.iteritems():
			self.log("%-8s %-15s %s" % (k.upper(), v, getattr(self, v).__doc__))
	def input(self):
		keyboard = ika.Input.keyboard
		if Input.keyboard['LCTRL'].Position():
			key = ika.Input.keyboard.GetKey()
			if key is None:
				for direction in ('UP', 'RIGHT', 'LEFT', 'DOWN'):
					if Input.keyboard[direction].Pressed():
						key = direction
						break
				if key is None:
					return
			try:
				getattr(self, self.ctrlCommands[key])()
			except KeyError:
				self.log("CTRL+%s is not in the CTRL command list:" % key)
				self.listCommands(self.ctrlCommands)
			ika.Input.keyboard['LCTRL'].Pressed() # Unpress
			return
		if self.lastcontrol is not None and not self.lastcontrol.Position():
			self.lastcontrol = self.lastkey = self.lastcommand = None
			self.lastkey = None
			self.keytimer = 0
			return
		cmd = None
		for k in self.keyCommands:
			if Input.keyboard[k.upper()].Pressed():
				self.lastcontrol = Input.keyboard[k.upper()]
				self.lastcontrol.Pressed() # Force unpress
				cmd = self.lastcommand = k
				self.keytimer = Region.keyDelay
				break
		key = None
		if self.keytimer > 0:
			self.keytimer -= 1
			if self.keytimer == 0:
				if self.lastkey is not None:
					key = self.lastkey
				else:
					cmd = self.lastcommand
				self.keytimer = Region.keyRepeat
		elif cmd is None:
			key = Input.keyboard.GetKey()
			if key is None:
				return
			self.keytimer = Region.keyDelay
			if key in Region.speckeys:
				control = Region.speckeys[key].upper()
			else:
				try:
					control = key2control[key]
				except KeyError:
					self.log('keyerror %s not in %s' % (control, key2control))
			self.lastkey = key	
			self.lastcontrol = ika.Input.keyboard[control] 
			self.lastcontrol.Pressed() # Unpress			
		if cmd is not None:
			try:
				a = self.__getattribute__(cmd.lower())
			except AttributeError:
				self.log("The key %s is not linked to any special commands" % k)
			a()			
			return
		if key is not None:
			global key2control
			#self.log('key is %s' % key)
			if key == '\r':
				self.enter()
			elif key in Region.speckeys:
				control = Region.speckeys[key].upper()
				getattr(self, Region.speckeys[key])()
			else:
				control = key2control[key]
				self.handleChar(key)
			#self.log('key %s gets control %s' % (key, key2control[key]))
	def tick(self):
		self.input()
		self.draw()
		
class Drawable(object):
	def __init__(self, t=90, x=50, y=50, layer='top', **args):
		self.t, self.x, self.y, self.layer = t, x, y, layer
		self.__dict__.update(args)
		self.parent.log('the __dict__ of object %s is %s' % (self, self.__dict__))
 
class Body(Region):
	' A multiline text field'
	layers = ('b4txt', 'top')
	def __init__(self, main, x, y, nlines=4, ncols=20, **args):				
		self.nlines = nlines
		self.ncols = ncols
		self.topline = 0
		self.logonce = main.logonce
		self.evalhistory = []
		self.evalhistorycur = 0
		self.clipboard = ''
		try:
			lines = file('lines.py').read().split('\n')
			self.log('read lines.py')
			if lines == []:
				self.log('lines.py is empty')
				lines = ['']
		except IOError:
			self.log('lines.py does not exist')
			lines = ['']
		self.lines = lines
		Region.__init__(self, main, x, y, keyCommands = Region.defaultCommands | set(['up', 'down']), setcurline=False, **args)
		self.y2 = y+self.nlines*res.f.height
		self.upHistory = lambda: self.moveHistory(-1)
		self.downHistory = lambda: self.moveHistory(1)
		self.getcurword = lambda: self.getWord(self.curline, self.cur.col)
		newCtrlCommands = {'UP':'upHistory', 'DOWN':'downHistory', 's':'save', 'W':'getcurword'}
		self.ctrlCommands.update(newCtrlCommands)
		self.objects = dict((i, []) for i in Body.layers)
		self.paniclabel = ''
		self.popup = None
		#self.coloredLines = [SyntaxColoredLine('for i in range(200): print "love" # cmt') for i in range(64)]
		#self.normallines = ['for i in range(200): print "love" # cmt' for i in range(64)]
		self.f = SyntaxColoredf(res.f)
		self._curlineUpdate = False
		self._matches = {}
		
		self.f3()
		
	def add(self, object, layer='top'): # add an object
		self.log("is an exception being caought")
		assert layer in Body.layers
		self.objects[layer].append(object)
		self.log('objects are %s' % self.objects)
	def tick(self):
		Region.tick(self)
		self.t += 1
		ob = self.objects
		for x, i in enumerate(chain(*(lst for lst in ob.values()))):
			i.t -= 1
		
		for layer in ob.keys():
			ob[layer] = [i for i in ob[layer] if i.t>=1]
	def _setline(self, v):
		self.lines[self.cur.line] = v
		self._curlineUpdate = True
		#self.paniclabel = v
	def _getline(self):
		try:
			return self.lines[self.cur.line]
		except IndexError:
			raise "IndexError: %d" % self.cur.line
	curline = property(_getline, _setline)
	def save(self):
		file('lines.py', 'w').write('\n'.join(self.lines))
		self.log('Saved lines.py')
	def eval(self, erase=False):
		cmds = 'raise = for if def while try except class import assert'.split()
		log = self.log
		def stripComment(i):
			try:
				return i[:i.index('#')]
			except ValueError:
				return i
			
		statement = self.lastStatementWithLines()
		line = '\n'.join(stripComment(i) for i, linen in statement).strip()
		
		class StatementDrawer(Drawable):
			def draw(self):				
				x1, y1 = self.parent.charpos(0, linemin)
				_, y2 = self.parent.charpos(0, linemax)
				x2 = self.parent.x2-1
				x = 196
				c = ika.RGB(x, x, x) if (self.t / 4) % 2 == 0 else ika.RGB(x, 0, 0)
				self.parent.logonce('%s'% [x1, y1, x2, y2, c, 1])
				ika.Video.DrawRect(x1, y1, x2, y2, c, 1)
		
		linenumbers = [linen for _, linen in statement]
		linemax = max(linenumbers)+1
		linemin = min(linenumbers) 
		r = StatementDrawer(parent=self, linemax=linemax, linemin=linemin, t=20)
		self.add(r, layer='b4txt')
		
		try:
			if any(i in line for i in cmds) and '==' not in line:
				exec line in locals(), globals()
				self.log('#[00FF00]executed %s' % repr(line))
			else:
				e = eval(line)
				self.log('#[00FF00]%s=%s'%(line, e))
				if erase:
					self.evalhistory.append(self.lines[:])
					self.lines[:] = ['']
					self.cur.col = self.cur.line = 0					
			
		except:
			self.main.logTrace()
	def moveHistory(self, dir):
		'dir is either -1 or 1'
		self.evalhistorycur = clamp(self.evalhistorycur+dir, 0, len(self.evalhistory)-1)
		self.log('historycur is now %d' % self.evalhistorycur)
		try:
			self.lines = self.evalhistory[self.evalhistorycur]
			self.cur.line = len(self.lines)-1
			self.cur.col = len(self.curline)
		except IndexError:
			self.log('there is no history')
	def copy(self):
		self.save()
		#a = self.__class__(self.main, self.x1, self.y) 
		#a.__dict__.update(self.__dict__)
		return copy.copy(self)
	def copySelection(self):
		if self.activeMarker():
			if Input.keyboard['C'].Position():
				if self.cur.line == self.marker.line:
					a, b = sorted2(self.cur.col, self.marker.col)
					self.clipboard = self.curline[a:b] 
				else:
					a, b = sorted2(self.cur.line, self.marker.line)
					self.clipboard = self.lines[a:b]
	def f1(self):
		self.main.logtxt[:] = []
	def f2(self):
		#self.log('marker%s cur:%s'%(self.marker,self.cur))
#		while not Input.keyboard['RETURN'].Pressed():
#			x,y,x2,y2 = tuple(ika.Random(0,700) for i in range(4))
#			Video.DrawRect(x,y,x2,y2, RGB(255,0,0))
#			ika.Video.ShowPage()
#			ika.Input.Update()
		pass
	def f3(self):
		s = 'changed the text'
		s2 = 'cali cali califorina'
		self.log(s)
		self.log('made a change to the source code')
		#import pydevd;pydevd.settrace()		
		self.log(s2)
		
	def deleteSelection(self):
		if self.cur.line == self.marker.line:
			Region.deleteSelection(self)	
		else:
			a, b = sorted2(self.cur.line, self.marker.line)
			self.lines = self.lines[:a] + self.lines[b:]
			self.cur.line = a
		self.marker = None
	def backspace(self):		
		myvar = 8
		if self.activeMarker():
			self.deleteSelection()
		else:
			if self.cur.col > 0:
				Region.backspace(self)
			elif self.cur.line > 0:
				self.cur.line -= 1			  
				self.cur.col = len(self.curline)
				import pydevd;pydevd.settrace(stdoutToServer=True, stderrToServer=True)
				myvar = 6
				self.curline = ''.join([self.curline, self.lines[self.cur.line+1]]) 
				del self.lines[self.cur.line+1] 	  
				self.updateText()
	def updateText(self):
		pass
	def up(self):
		if self.cur.line > 0:
			self.move(self.cur, min(self.cur.col, len(self.curline)), self.cur.line-1)
			#self.topline = min(self.topline, self.cur.line)
	def down(self):
		if self.cur.line < len(self.lines) - 1:
			self.move(self.cur, min(self.cur.col, len(self.curline)), self.cur.line+1)
			#self.topline = max(self.topline, self.cur.line - (self.nlines-1))
	def drawSelection(self):
		if not self.activeMarker():
			return
		if self.marker.line == self.cur.line:
			Region.drawSelection(self)
			return
		self.logonce("HSSTHNSTH")
		lo, hi = sorted2(self.cur.line, self.marker.line)
		lo = max(lo-self.topline, 0)
		hi = min(hi-self.topline, self.nlines)
		fh = res.f.height
		self.logonce('cur,m=%d,%d %d %d' % (self.cur.line, self.marker.line, lo, hi))
		ika.Video.DrawRect(self.x1+1, self.y1+1+lo*fh, 
						   self.x2-1, self.y1+1+hi*fh, RGB(0,0,196), 1)
	def enter(self): # An exception to the rule...
		newtext = self.curline[self.cur.col:]		
		self.curline = self.curline[:self.cur.col]				 
		self.cur.line += 1
		self.lines = self.lines[:self.cur.line] + [newtext] + self.lines[self.cur.line:]
		self.cur.col = 0
	def left(self):
		if self.cur.col > 0:
			self.move(self.cur, self.cur.col-1, self.cur.line)
		elif self.cur.line > 0:
			self.move(self.cur, len(self.curline) - 1, self.cur.line-1)
	def right(self):
		if self.cur.col < len(self.curline):
			self.move(self.cur, self.cur.col+1, self.cur.line)
		elif self.cur.line < len(self.lines) - 1:
			self.move(self.cur, 0, self.cur.line+1)
	def tab(self):
		if self.shiftposition():
			tabf = self.removeTab
			self.cur.col = max(self.cur.col-len(Region.tabchar), 0) 
		else:
			tabf = self.addTab
			self.cur.col = min(self.cur.col+len(Region.tabchar), len(self.curline))
		if self.activeMarker():
			lt = min(self.marker.line, self.cur.line)
			gt = max(self.marker.line, self.cur.line)
			for i in xrange(lt, gt+1):
				self.lines[i] = tabf(self.lines[i])
		else:
			self.curline = tabf(self.curline)
		if self.shiftposition():
			self.cur.col = max(self.cur.col-len(Region.tabchar), 0) 
		else:
			self.cur.col = min(self.cur.col+len(Region.tabchar), len(self.curline))

	def drawText(self):
		#f = self.f  
		x1 = self.x1+1
		y1 = self.y1+1
		Print = self.f.Print
		range = xrange
		topline = self.topline
		h = self.f.height
		lines = self.lines
		for i in range(self.topline, min(len(self.lines),self.topline + self.nlines)):
			Print(x1, y1 + (i-topline) * h, lines[i])
	def drawMatchingBraces(self):
		#x = 255
		#		
		#for k, v in self._matches.iteritems():
		#	x, y = self.charpos(k, self.cur.line+1)
		self.updateBraces()
		try:
			self.logonce('%s %s' % (self.cur.col, self._matches))
			for col in self._matches[self.cur.col-1]:
				x, y = self.charpos(col, self.cur.line+1)
				ika.Video.DrawLine(x+1, y-1, x+7, y-1, RGB(255,255,255))			
		except KeyError:
			pass
	def drawMouseCursor(self):
		mx, my = self.mousepos()
		m = 5
		mi = 2
		ika.Video.DrawLine(mx-mi, my-m, mx+mi+1, my-m, RGB(255,0,0))	
		ika.Video.DrawLine(mx, my-m, mx, my+m+1, RGB(255,0,0))
		ika.Video.DrawLine(mx-mi, my+m+1, mx+mi+1, my+m+1, RGB(255,0,0))
		res.f.Print(500, 8, 'mx=%3d my=%3d' % (mx, my))						
	def draw(self):			
		Region.draw(self)
		for i in self.objects['b4txt']:
			i.draw()
		if self.popup is not None:
			self.popup.draw()
		self.drawLog2()
		self.drawMatchingBraces()		
		self.drawMouseCursor()
		# draw objects
		for i in self.objects['top']:
			i.draw()
	def drawLog(self):
		logx, logy = 0, 200
		Print = res.f.Print
		for y , i in enumerate(self.main.logtxt[self.main.logstart:self.main.logstart+48]):
			Print(logx, logy+y*8, i)
	def drawLog2(self, cache=[None], lastloglen=[-1], lastlogstart=[-1]):
		logx, logy = 0, 200
		if (lastloglen[0], lastlogstart[0]) != (len(self.main.logtxt), lastlogstart[0]):
			lastloglen[0] = len(self.main.logtxt)
			lastlogstart[0] = self.main.logstart
			txt = self.main.logtxt
			start = self.main.logstart
			Print = res.f.Print
			for y , i in enumerate(txt[start:start+48]):
				Print(logx, logy+y*8, i)			
			cache[0] = ika.Video.GrabImage(logx, logy, 640, 640)
		if cache[0]:
			cache[0].Blit(logx, logy)
	def pasteSelection(self):
		if isinstance(self.clipboard, list):
			self.lines = self.lines[:self.cur.line] + self.clipboard + self.lines[self.cur.line:]
		elif isinstance(self.clipboard, str):
			self.curline = ''.join([self.curline[:self.cur.col], self.clipboard, self.curline[self.cur.col:]])
	def input(self):
		self.t += 1
		if self.t == 60: self.t = 0				
		if self.popup is not None:
			self.popup.input()
			inp = self.popup.inputCatch
			if not self.popup.visible:
				self.popup = None
			if inp:
				self.log("caught input")
				ika.Input.keyboard.ClearKeyQueue()
				return
		Region.input(self)
		#if self.curline[-1] == '.':
		#	self.popup = PopupMenu(self, dir(eval(self.curline)))			
		if self._curlineUpdate:
			self.listCompletions()
			#self.updateBraces()
			self._curlineUpdate = False
				
		self.topline = clamp(self.topline, self.cur.line-self.nlines, self.cur.line)
		if ika.Input.mouse.left.Pressed():
			if self.inArea():
				x, y = self.mousetotextpos()
				self.move(self.cur, x, y)
			
		if ika.Input.mouse.right.Pressed():
			self.popup = PopupMenu(self, ['orange', 'apple', 'cucumber'])					
	def updateBraces(self, line=None, col=None, matchDic = {'(':')', '{':'}', '[':']'}):
		self._nbraces = 0
		braces = []
		self._matches = {}
		if line is None:
			line = self.curline
		if col is None:
			col = self.cur.col
		for n, c in enumerate(self.curline):
			if c in '[({':
				braces.append((c, self._nbraces, n))
				self._nbraces += 1
			elif c in '])}':
				self._nbraces -= 1
				if 0 <= self._nbraces <= len(braces):
					(matchc, matchi, matchn) = braces.pop()
					if c == matchDic[matchc]:
						self._matches[matchn] = self._matches[n] = (matchn, n)
		#return (self._braceStart, self._braceEnd)
			
	def lastStatementWithLines(self):
		line = self.curline
		statement = []
		linestart = self.cur.line
		self.log("%d<->%d" % (self.cur.line, len(self.lines)))
		while self.lines[linestart].strip() == '':
			linestart -= 1
			if linestart < 0:
				self.log("lol")
				return None	
		def indentLevel(line):			
			spaces = list(itertools.takewhile(str.isspace, line))
			if spaces == []:
				return 0
			s = sum(4 if i=='\t' else 1 for i in spaces)
			self.log('sum %s %d %s'%(line,s,spaces))
			return s
		curlevel = indentLevel(self.lines[linestart])
		statement.append((self.lines[linestart], linestart))
		self.log('linstart:%s' % self.lines[linestart])
		self.log('linstart:%s %d' % (self.lines[linestart-1], indentLevel(self.lines[linestart-1])))
		for i in range(linestart-1, -1, -1):
			newlevel = indentLevel(self.lines[i])
			self.log('lin:%-32s %d %d' % (self.lines[i], curlevel, newlevel))
			if newlevel >= curlevel:
				break
			curlevel = newlevel
			statement.append((self.lines[i], i))			
		statement.reverse()
		return statement
	def lastStatement(self):
		return [text for (text, i) in self.lastStatementWithLines()]
	def listCompletions(self):
		completions = []
		curline = self.curline # I only need to read this
		#self.log('list completions called')
		def dirCompletions(col, text, debug=None):
			try:
				beg, end, word = getword.bounds(text, col, wordf=(lambda c: c.isalpha() or c == '.'))
			except getword.WordError:
				return []
			
			if debug == '.s':	self.log('dirCompletions:%s'%[beg, end, word])
			try:
				return dir(eval(word, locals(), globals()))
			except:
				return []
		try:
			if len(curline) < 2:
				raise getword.WordError("The line is too short for autocompletionse")
			if curline[self.cur.col-1] == '.':
				completions = dirCompletions(self.cur.col-1, curline[:self.cur.col-1], debug = '.')
				beg = end = self.cur.col
			else:
				beg, end, word = getword.bounds(curline, self.cur.col, wordf=str.isalpha)
				if len(curline) > len(word)+2 and curline[-(len(word)+1)] == '.':
					self.log("slice <%s> <%s> word:<%s>" % (curline[-(len(word)+1)], curline[:-(len(word)+1)], word))
					completions = dirCompletions(-(len(word)+1), curline[:-(len(word)+1)], debug='.s')
					completions = [i for i in completions if i[:len(word)]==word]
				elif word is not None and len(word) > 1:
					completions = chain(globals().keys(), locals().keys(), keyword.kwlist)
					completions = [i for i in completions if i[:len(word)]==word]
			if not completions:
				raise getword.WordError("No completions")
			class CompletionPopup(PopupMenu):
				def __init__(self, beg, end, *args):
					self.beg, self.end = beg, end
					PopupMenu.__init__(self, *args)
				def RETURN(self):
					word=self.choices[self.choice]					
					beg, end = self.beg, self.end
					line = self.parent.curline[:]
					self.parent.curline = ''.join([line[:beg], word, line[end:] ])
					self.parent.cur.col += len(self.parent.curline) - len(line)
	#					self.log(self.parent.cur.col) 
					self.visible = False
					self.inputCatch = True
		except getword.WordError:
			self.popup = None
			return
		if len(completions) == 1 and completions[0] == word:
			self.popup = None
			return
		else:
			if self.popup is not None and isinstance(self.popup, CompletionPopup):
				self.popup.choices = completions
			else:
				(x, y) = self.charpos(self.cur.col, self.cur.line+1)
				self.popup = CompletionPopup(beg, end, self, x, y, completions)
	def charpos(self, col, line, dbg=False):
		if dbg:
			self.log('X1 IS %d' % col)
		return (self.x1+1+col*res.f.width, self.y1+1+line*res.f.height)
	def getWordBounds(self, line, col):
		i = col
		begin = None
		end = None
		for i in range(col, -1, -1):
			if not line[i-1].isalnum():
				begin = i
				break
		if not begin:
			begin = 0
		while i < len(line)-1 and end is None:
			if not line[i+1].isalnum():
				end = i+1
				break
			i += 1
		if not end:
			end = len(line)
		if not line[begin:end].isalnum():
			return None
		return (begin, end, line[begin:end])
	def getWord(self, line, col):
		_, _, word = self.getWordBounds(line, col)
		return word
	def deleteline(self):
		global clamp
		del self.lines[self.cur.line]		
		self.cur.line = clamp(self.cur.line, 0, len(self.lines)-1)
		if self.lines == []:
			self.lines[:] = ['']
class Editor(Body):
	modes = ('edit', 'play', 'search')
	def __init__(self, area):
		Body.__init__(self, area, nlines=30, ncols=150)
		self.t = 0.0
		res.file = ''
		self.objects = []
		self.error = 'No Errors'
		self.punc = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
		res.findbox = Region()
		res.filename = 'myfile'
		self.start()
		self.lines = [i.strip('\n') for i in file('%s.py' % res.filename, 'r').readlines()]
		if self.lines == []:
			self.lines = ['']
		self.bottom = lambda: self.topline + self.nlines
		self.x1, self.y1 = 4, 500
		self.mode = 'edit'
		
	def save(self):
		out = file('%s.py' % res.filename, 'w')
		out.write('\n'.join(self.lines))
		try:
			self.reload()
			file('backup/%s.py' % res.filename, 'w').write('\n'.join(self.lines))	
		except:
			self.error = traceback.format_exc()
			out.write(file('backup/%s.py' % res.filename, 'r').read())
			self.reload() # Make sure nothing screwy goes on...
	   	out.close()
		
	def main(self):
		self.handleInput()
		self.draw()
		#self.patternmain()
		   
	def reload(self):
		try:
			reload(self.levelm)
			self.error = 'No Errors'
		except:
			raise
			#a, b, c = sys.exc_info()
			#self.error = b.message 
			#self.cur.line = c.tb_lineno
			#del c		
	def start(self):
		exec("import %s as levelm" % res.filename)
		self.levelm = levelm #@UndefinedVariable
	
	def patternmain(self):
		self.objects = [i for i in self.objects if 0<i.x<410 and 0<i.y<510 and i.t>0] + self.levelm.level(self.t, self.objects)
		#Video.DrawRect(0,0,400,500, RGB(255,255,255))
		
		if Input.keyboard['F3'].Pressed():
			self.t = 0
			self.objects = []
		
		for i in self.objects:
			i.tick()
			i.draw()
		res.f.Print(0,0, 't:%6d #Bullets: %d' % (self.t, len(self.objects)))
				
	def drawMessages(self):
		res.f.Print(self.x1, self.y2+8, '%3d:%2d %3d %s %s ' % (self.cur.line, self.cur.col, self.topline, res.filename, self.error))
		res.f.Print(300, 0, '%s' % self.clipboard)			
	def draw(self):
		self.drawOutline()
		self.drawMessages()
		self.drawCursor()
		self.drawSelection()
		self.drawText()
		self.drawTextCursor()
	def handleInput(self):
		pass
	def handlePlay(self):
		pass
	def handleSearch(self):		
		self.searchfor = ''		
		if Input.keyboard['ESC'].Pressed():
			self.mode = 'edit'
	def handleEdit(self):
		cur = self.cur		
		#print '%d : %d len=%d' % ( self.cur.line, self.cur.col, len(self.lines)	 
		mx, my = int(Input.mouse.x.Position()), int(Input.mouse.y.Position())
		if Input.mouse.left.Pressed():
			if self.x1 < mx < self.x2 and  self.y1 < my < self.y2:				 
				cur.line = min((my - self.y)/res.f.height+self.topline, len(self.lines)-1)
				cur.col = min((mx - self.x)/res.f.width, len(self.curline))
		
		if Input.keyboard['LCTRL'].Position():
			if Input.keyboard['S'].Pressed():
				self.save()
			elif Input.keyboard['Q'].Pressed():
				self.done = True
			
			if self.activeMarker():
				if Input.keyboard['C'].Position():
					if self.cur.line == self.marker.line:
						a, b = sorted2(self.cur.col, self.marker.col)
						self.clipboard = self.curline[a:b] 
					else:
						a, b = sorted2(self.cur.line, self.marker.line)
						self.clipboard = self.lines[a:b]
		else:
			if Input.keyboard['LSHIFT'].Position():
				if self.marker is None:
					self.marker = EditCursor(self.cur.line, self.cur.col)
				if self.marker.line != self.cur.line:
					self.marker.col = 0

class PlayArea(Body):
	def __init__(self, main, x, y, **args):
		self.log = main.log
		self.fp = fps.FPSManager(60)
		
		d = args
		d['nlines'] = 20
		d['ncols']  = 64
		Body.__init__(self, main, 0, 0, **d)
		#lines = [''.join([s, '\n']) for s in self.generateIKADocumentation(ika, 0)]

		
		#obj = testika2.Input.mouse		
		#img = testika2.Image('myfile.png')		
			#self.log(line)
	def generateIKADocumentation(self, obj, tab=0):
		lines = []
		formatdoc = lambda doc: '\n\t'.join(doc.split('\n'))			
		try:
			def addcode(s, tab=tab): 
				for i in s.split('\n'):
					lines.append(''.join(['\t'*tab, i]))
				#lines.append(''.join([tabs, s]))|
			addclass = lambda name: addcode('class %s(object):'%name)
			def addproperty(name, val):
				addcode('@property')
				addcode('def %s():'%name)
				addcode('\t"""%s"""' % formatdoc(val.__doc__))
				addcode('\tpass')
			if obj is ika:
				control = ika.Input.mouse.right
				addcode('class Control:')
				addcode('\t"""%s"""' % formatdoc(control.__doc__))
				lines += self.generateIKADocumentation(control, tab+1)

			for i in dir(obj):
				if i[:2] == '__':
					continue
				if i == 'GetControl':
					continue
				#self.log('getatr %s %s' % (obj, i))
				val = getattr(obj, i)
				rs = repr(val)
				#self.log('rs is %s' % str(val))
				
				if obj is ika.Input.mouse.right:
					self.log('%s:%s:%s'%(i,val,rs))
				if 'function' in rs or 'method' in rs:					
					doc = val.__doc__.split('\n')
					setRenderList = 'SetRenderList' in val.__doc__
					try:
						if not setRenderList:
							funcname = doc[0].split('.')[-1]
	#						def logfunc(enable, var=[0]):							
	#							if enable:
	#								self.log('FUNCNAME: %d%s'%(var[0], funcname))
	#								var[0]+=1
							if '->' in funcname:
								funcname = funcname[:funcname.index('->')]
							funcname = re.sub(r'\.\.\.', '*args', funcname)
							if '[' in funcname:
								funcname = funcname[:funcname.index('[')] + ')'
							funcname = re.sub(r'\,[^A-z]*\)', ')', funcname) # get rid of dangling parens
							funcname = funcname.strip()
							if funcname[-1] != ')':
								funcname += ')'
						else:
							funcname = 'SetRenderList(index, *args)'
						addcode('def %s:#%s\n\t"""%s"""\n\tpass' % (funcname, rs, '\n\t'.join(doc)))
					except IndexError:
						addcode('# Error %s: can\'t extract properties from docstring. ' % i)
				elif 'type' in rs or 'module' in rs or 'class' in rs:
					addclass(i)
					addcode('\t"""%s"""' % formatdoc(val.__doc__))
					lines += self.generateIKADocumentation(val, tab+1)
				elif 'attribute' in rs:
#					addcode('@property')
#					addcode('def %s():'%i)
#					addcode('\t"""%s"""' % formatdoc(val.__doc__))
#					addcode('\tpass')
					addproperty(i, val)
				elif 'object' in rs:
					objtype = re.findall('\<([A-z0-9]*)\ ', rs)[0] # Get the name of the object

					if objtype =='Control':
						addcode('%s=%s() # %s'%(i, objtype, val))
					elif objtype in set(['Map', 'Tileset']): # Ignore
						pass
					elif objtype in set(['Input', 'Video', 'Keyboard', 'Mouse', 'Colours']):
						addclass(i)
						addcode('\t"""%s"""' % formatdoc(val.__doc__))
						def subsetModule(local, *methods): 
							# Make a module and only show a subset of the methods
							for i in methods:
#								for prop in ['Position', 'Pressed', 'Delta']:
#									local['addproperty'](prop, getattr(ika.Input.mouse.right, prop))
								#local['addcode']('%s=Control()'%i, tab=local['tab']+1)
								local['addcode']('%s=Control()'%i, tab=local['tab']+1)
						if objtype == 'Mouse':
							subsetModule(locals(), 'left', 'middle', 'right', 'wheel', 'x', 'y')
						elif objtype == 'Keyboard':
							subsetModule(locals(), 'ClearKeyQueue', 'GetKey', 'WasKeyPressed')
						elif objtype == 'Map':
							pass
						else:
							lines += self.generateIKADocumentation(val, tab+1)
					else:
						addcode('%s=%s'%(i,val))
				else:
					addcode('%s=%s'%(i,val))
		except:
			addcode("# Error on %s" % (i))
			self.main.logTrace()
		return lines
	def input(self):
		#self.log(ika.Input.keyboard.GetControl())
		if Input.keyboard['LALT'].Position():
			self.main.loginput()
			if Input.keyboard['E'].Pressed():
				self.evalCurline()
			ika.Input.keyboard.ClearKeyQueue()
		else:
			Body.input(self)
	def copy(self):
		a = PlayArea(self.main, self.x1, self.y1)		 
		a.lines = self.lines
		a.cur = self.cur
		a.marker = self.marker
		return a
	def callParent(self):
		return parent.func()
	def draw(self):
		Body.draw(self)
