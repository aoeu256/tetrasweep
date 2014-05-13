

class Pattern:
	
	
	
	
2patterns = [
	'A\nA',
	'AA',
	'A*\n*A',
	'A**\n**A',
	'A*A',
	'A\n*\nA'
]

3pattern = {
	'H2H': [Complete('AA', -1, -1),
		Complete('')]
	'V2v'::[
}

class Complete:
	def __init__(a, pattern, boundx, boundy):
		a.pattern, a.boundx, a.boundy = pattern, boundx, boundy
	def search(a, panel):
		for x in boundx:
			for y in boundy:
				
		