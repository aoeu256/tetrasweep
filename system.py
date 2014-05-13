from ika import *
from xi import fps
from itertools import chain
f = Font('font.fnt')	
import sys, time, profile, os, traceback, cProfile, pstats, ihooks

###########################

_parent = None

class Importer(ihooks.ModuleImporter):
	'Thanks to This source code was copy and pasted line for line from Jon Parise'
	_dependencies = {}
	def import_module(self, name, globals=None, locals=None, fromlist=None):
		# Track our current parent module.  This is used to find our current
		# place in the dependency graph.
		global _parent
		parent = _parent
		_parent = name
		
		print 'importing %s' % name
		# Perform the actual import using the base import function.
		m = ihooks.ModuleImporter.import_module(self, name, globals, locals, fromlist)
	
		# If we have a parent (i.e. this is a nested import) and this is a
		# reloadable (source-based) module, we append ourself to our parent's
		# dependency list.
		print 'parent is %s, module is %s' % (parent, m)
		if parent is not None and hasattr(m, '__file__'):
			l = Importer._dependencies.setdefault(parent, [])
			l.append(m)
			print 'adding module %s from %s now %s' % (m, parent, l)
			print 'dep is %s' % Importer._dependencies
		# Lastly, we always restore our global _parent pointer.
		_parent = parent
	
		return m
	def _reload(self, m, visited):
		"""Internal module reloading routine."""
		name = m.__name__
	
		# Start by adding this module to our set of visited modules.  We use
		# this set to avoid running into infinite recursion while walking the
		# module dependency graph.
		visited.add(m)
	
		# Start by reloading all of our dependencies in reverse order.  Note
		# that we recursively call ourself to perform the nested reloads.
		deps = Importer._dependencies.get(name, None)
		if deps is not None:
			for dep in reversed(deps):
				if dep not in visited:
					self._reload(dep, visited)
	
		# Clear this module's list of dependencies.  Some import statements
		# may have been removed.  We'll rebuild the dependency list as part
		# of the reload operation below.
		try:
			del Importer._dependencies[name]
		except KeyError:
			pass
	
		# Because we're triggering a reload and not an import, the module
		# itself won't run through our _import hook.  In order for this
		# module's dependencies (which will pass through the _import hook) to
		# be associated with this module, we need to set our parent pointer
		# beforehand.
		global _parent
		_parent = name
	
		# Perform the reload operation.
		ihooks.ModuleImporter.reload(self, m)
	
		# Reset our parent pointer.
		_parent = None			
	def reload(self, m):
		self._reload(m, set())
#myimporter = Importer()
#myimporter.install()
import ta, editor
###############

b = 8
def myfunc(a, b):
	#pydevd.settrace()
	print 'lol'
myfunc(8, 20)
class LogArea:
	'When your module raises an exception, it goes here.  This just shows the error log.'
	def __init__(self, main):
		self.main = main # main is the reloader
		self.fp = fps.FPSManager(60)
	def tick(self):
		x1, y1 = 0, 0
		for y, i in enumerate(self.main.logtxt[self.main.logstart:]):
			f.Print(x1, y1+y*8, i)
		if Input.up.Position():
			self.main.logstart = max(self.main.logstart-1, 0)
		if Input.down.Position():
			self.main.logstart = min(len(self.main.logtxt)-1, self.main.logstart+1)

class Reloader:
	def __init__(self):
		self.DebugMode = True
		self.player1 = None
		self.player2 = None
		self.modulename = 'ta' # The module string.  Change this to what module you want to load.
		self.module = eval(self.modulename)
		self.pyfile = '%s.py' % self.modulename
		self.oldpyfile = 'old%s.py' % self.modulename		
		self.modulefile = lambda m='r': file(self.pyfile, m)
		self.oldmodulefile = lambda m='r': file(self.oldpyfile, m)
		self.logtxt = []
		self.logstart = 0
		self.Loglength = 1024
		self.loglines = 48
		self.t = 0
		self.xres = 640
		self.longestlogstr = self.xres / 8
	def loginput(self):
		if Input.up.Position():
			self.logstart = max(0, self.logstart-1)
		elif Input.down.Position():
			self.logstart = min(1024, self.logstart+1)
		elif Input.keyboard['SPACE'].Position():
			self.logstart = 0
			self.logtxt[:] = []
	def log(self, text):
		if not isinstance(text, str):
			text = '%s:%s' % (__name__, text)
		def loglines(text):
			for i in text.split('\n'):
				self.logtxt.append(i)			
		if len(text) > self.longestlogstr:
			loglines(text[:self.longestlogstr])
			self.log(text[self.longestlogstr:])
		else:
			loglines(text)
		if len(self.logtxt) > self.Loglength:
			self.logtxt = self.logtxt[1:]
		self.logstart = max(len(self.logtxt) - self.loglines, 0)
		print 'log:', text
#	def doonce(self, func, mem=[0]):
#		mem[0] += 1		
	def logonce(self, text, memory = set()):
		text = str(text)
		if text not in memory:
			memory.add(text)
			self.log(text)
	def vars(self, s, d=None):
		"""Takes in a string in the form 'var1 var2 var3' and shows the values of each of variable.  d can be set to an object
		vars('a b c')='a=5 b=5 c=5' # Assuming a, b, and c are local/global variables
		vars('height width', myFont)='height=8 width=8' # given you have a myFont object with height and width attributes
		""" 
		b = s.split(' ')
		lst = []
		if not isinstance(d, dict) and d is not None:
			d = d.__dict__
		for i in b:
			if d is not None and i in d:
				v = d[i]
			else:
				v = eval(i)
			lst.append('%s=%s' % (i, v))
		return '; '.join(lst)
	def logvars(self, s, d=None):
			self.log(self.vars(s, d))
	def logTrace(self):
		text =  traceback.format_exc().split('\n')
		for i in text:
			self.logerr(i)
	def logerr(self, s):
		self.log('#[FF0000FF]%s'%s)
	def reloadold(self, s='oldta'):
		self.player1 = LogArea(self)
		self.logTrace()
#		if self.player1.__module__ == 'oldta':
#			self.player1 = LogArea(self) # Make a simple area that only shows the error messages
#		else:
#			exec('import %s as newmod' % s)
#			reload(newmod)
#			self.module = newmod
#			self.player1 = self.module.PlayArea(self, 50, 50)
#			self.log(s)
#		self.logTrace()
	def newPlayArea(self, savestate = False):
		try:
			reload(self.module)
			#self.module = eval(self.modulename) # Don't think this is neccessary...
			if savestate and 'copy' in dir(self.player1):
				self.numberExceptions = 0
				newplayarea = self.player1.copy()
			else:
				newplayarea = self.module.PlayArea(self, 50, 50)
			if isinstance(self.player1, self.module.PlayArea):
				newplayarea.copyCur(self.player1)
			self.player1 = newplayarea
			self.log('reload succesful')
			# self.oldmodulefile('w').write(self.modulefile().read()) Save the old verison of the module file.  Not used anymore
			name = ''.join(i if i!=':' else ' ' for i in time.ctime())
			file('backup/'+name, 'w').write(self.modulefile().read()) # Save a backup just in case you want to reload the changes
		except:
			self.reloadold()
	def main(self):
		print 'main'
		self.player1 = self.module.PlayArea(self, 50, 50)
		self.mtime = os.path.getmtime(self.pyfile)
		self.numberExceptions = 0
		#self.player1 = LogArea(self)
		self.fp = fps.FPSManager(600)
		fun = self.fp.render
		esckey = Input.keyboard['ESCAPE'].Pressed
		while not esckey():
			Input.Update()
			fun(self.tick)
	
	def pause(self, vars, env=None):
		self.logvars(vars, env)
		
		#while not Input.keyboard['C'].Pressed():
			
		
		
		# Grab the screen		
	
	def tick(self):
		
		
		if self.t < 30:
			self.t += 1
		else:
			self.t = 0
			if self.DebugMode:
				mtime = os.path.getmtime(self.pyfile)
				if mtime != self.mtime:
					self.mtime = mtime
					self.newPlayArea(savestate = not isinstance(self.player1, LogArea) )
		#Handle input
		if Input.keyboard['F10'].Pressed():
			self.newPlayArea(savestate = False)
		elif Input.keyboard['F11'].Pressed():
			self.newPlayArea(savestate = True)
		elif Input.keyboard['F12'].Pressed(): # Note not used
			self.oldmodulefile('w').write(self.modulefile().read())
			self.log('old%s is now %s' % (self.pyfile, self.pyfile))
		# Main part of the reloader
		try:
			self.player1.tick()
		except:
			self.numberExceptions += 1
			self.logTrace()
			# if there is an exception on
			if self.numberExceptions < 2: 
				self.newPlayArea(savestate = False)
			else:
				self.reloadold()
def main():
	myreloader = Reloader()
	Profile = True
	
	if Profile:
		print 'started profiler'
		fun = myreloader.main		
		profile.runctx('fun()', locals(), globals(), 'myprof')
		stats = pstats.Stats('myprof')
		stats.strip_dirs().sort_stats('cumulative').print_stats()
	else:
		myreloader.main()

main()
#replayfile = file(strftime('replays/%a %b %d %y %X').replace(':', '')[:-2]+'.pickle', 'w')
#cPickle.dump(player1.rep, replayfile)
