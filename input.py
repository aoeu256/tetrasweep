from ika import *
from xi import fps
from tools import *
f = Font('font.fnt')
fp = fps.FPSManager(30)
class Axis: # Maps two inputs onto an axis
	def __init__(a, inputs, choices, wrap = True, default = 0):
		a.inputs, a.choices, a.wrap, a.default = inputs, choices, wrap, default
	def __repr__(a):
		return '-%d/%d' %(a.cur, len(a.choices))
	def onMove(a):
		pass
class Button: # Maps several controls onto one control
	def __init__(a, inputs, action, default = [], press = 'Pressed'):
		a.inputs, a.action, a.default, a.press = inputs, action, default, press
class Action:
	def __init__(a, control, result = None):
		a.control, a.result = control, result
	def __repr__(a):
		return "(%s, %s)" % (a.control, a.result)
class AdvInput:
	def __init__(a, repeat, pause, axilist = [], buttonlist = [], rep = []):
		a.repeat, a.pause, a.rep, a.axilist, a.buttonlist = repeat, pause, rep, axilist, buttonlist
		a.c, a.frame = a.pause, 0
		for i in axilist + buttonlist:
			i.cur = i.default
	def tick(a, replay = False):
		press = False
		a.rep.append([])
		#try:
		for ax, axi in enumerate(a.axilist):
		#try:
			for v, inp in enumerate(axi.inputs):
				if inp.Pressed():
						axi.onMove()
				if (replay and any(f.control is inp for f in a.rep[a.frame])) or (not replay and inp.Position()):
					if not any(f.control is inp for f in a.rep[-2]):
						a.c = a.pause
					if a.c in (0, a.pause):
						curs, l = axi.cur + [-1,1][v], len(axi.choices)
						axi.cur = axi.wrap and curs % l or clamp(curs, 0, l-1)
					a.c -= 1
					if a.c < 0:
						a.c = a.repeat
					if not replay:
						a.rep[-1] += [Action(inp)]
					press = True
					#raise 'mystop'
		#except 'mystop': pass
		if not press:
			a.c = a.pause
		for b in a.buttonlist:
			if replay:
				for f in a.rep[a.frame]:
					if f.control is b:
						b.cur = f.result
						b.action(f.result)
					break
			elif not replay and any(inp.__getattribute__(b.press)() for inp in b.inputs):
				b.cur = b.action()
				a.rep[-1] += [Action(b, b.cur)]
		a.frame += 1
		Input.Update()
	def do(a, replay = False):
		a.frame = 0
		if not replay: a.rep = []
		while not Input.keyboard['K'].Pressed():
			#try:
			if replay:
				fp.render(lambda: a.tick(True))
			else:
				fp.render(a.tick)
			#except IndexError: #End replay
			#	f.Print(10, 10, "Press (K) to continue!")
		return a.rep