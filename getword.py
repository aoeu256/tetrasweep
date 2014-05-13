
def bounds(line, col, wordf=(lambda c: c.isalnum() or c in '.()[]' )):
	''' 
	Returns a contigious region inside a string where wordf is true in which at least
	one letter in the region is at index col.  
	>>> bounds('', 0)
	IndexError: string index out of range
	>>> bounds('self.help(a.help, love.death.match, destroy)', 1)
	(0, 9, 'self.help')
	>>> bounds('self.help(a.help, love.death.match, destroy)', 10)
	(10, 16, 'a.help')
	'''
	begin = 0
	end = len(line) 
	for i in range(col, -1, -1):
		if not wordf(line[i-1]):
			begin = i
			break
	for i in range(begin, len(line)-1):
		if not wordf(line[i+1]):
			end = i+1
			break
	if not all(wordf(c) for c in line[begin:end]):
		raise WordError("Word not found")
	
	return (begin, end, line[begin:end])

def word(line, col, **args):
	_, _, word = bounds(line, col, **args)
	return word

class WordError(Exception):
	pass

if __name__ == "__main__":
	import doctest
	doctest.testmod(raise_on_error=True)
	
bounds('lol.lol', 2)