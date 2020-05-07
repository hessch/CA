"""
CAX.py - Elementary Cellular Automaton 
Expanding list of cells from a single active cell on an ether of inactive cells.

Hessel Schut, hessel@isquared.nl 2018-01-25
"""

class ElementaryCA:
	"""
	Utility class for CA cells.

	Example usage:
		>>> from CAX import ElementaryCA
		>>> ca = ElementaryCA(rule = 30)
		>>> ca
			1
		>>> ca.update()
		>>> ca.getStates()
			{'states': [True, False], 'root': 1}
		>>> ca.update()
		>>> ca.getCells()
		    {'cells': [
		        <CAX.Cell instance at 0x10cab0248>, 
		        <CAX.Cell instance at 0x10cab01b8>, 
		        <CAX.Cell instance at 0x10cab0200>, 
		        <CAX.Cell instance at 0x10cab0320>	],
		     'root': 2}

		>>> c.getCells()['cells'][c.getCells()['root']].neigh
		    {'right': <CAX.Cell instance at 0x10cab0320>, 
		     'left': <CAX.Cell instance at 0x10cab02d8>}
	"""
	def __init__(self, rule = 0):
		"""
		Create a new CA with one single active cell.
		"""
		self.rule = rule
		self.root = Cell(rule = self.rule, state = True)

	def getCells(self):
		"""
		Return cells for the current iteration of the CA.
		"""
		left = self.root.recurseNeigh('left')
		# (rootpointer, [cell list])
		return {
			'root': len(left) - 1, 
			'cells': left[:-1] + self.root.recurseNeigh('right') }

	def getStates(self):
		"""
		Return a list of cell states for the current iteration of the CA.
		"""
		cl = self.getCells()
		return {
			'root': cl['root'],
			'states': list(map(lambda c: c.getState(), cl['cells'])) }

	def update(self):
		"""
		Calculate next state for all cells in the CA, starting from the root cell.
		"""
		self.root.update()

	def prune(self, dir = None):
		"""
		Recursively remove outer `False' cells from cell list
		"""
		if dir == None:
			self.prune(dir = 'right')
			self.prune(dir = 'left')
			return
		cells = self.getCells()['cells']
		if  dir == 'left':
			if not cells[0].state and cells[0] != self.root:
				if cells[0].neigh['right']: 
					cells[0].neigh['right'].neigh['left'] = None
				cells[0].neigh['right'] = None
			else: return
		if dir == 'right':
			if not cells[-1].state and cells[-1] != self.root:
				if cells[-1].neigh['left']: 
					cells[-1].neigh['left'].neigh['right'] = None
				cells[-1].neigh['left'] = None
			else: return
		self.prune(dir = dir)

	def __repr__(self):
		"""
		Print cells formatted as binary string.
		"""
		return ''.join(map(lambda s: '1' if s else '0', 
			self.getStates()['states']))

class Cell:
	"""
	Cellular Automaton cell instance.
	
	Example:
		>>> from CAX import Cell
		>>> c = Cell(state = True, rule = 110)
		>>> (c.neigh, c.state)

			({'right': None, 'left': None}, True)	

		>>> c.update()
		>>> (c.neigh, c.state)

			({	'right': <CAX.Cell instance at 0x10196a200>, 
				'left': <CAX.Cell instance at 0x10196a1b8>}, True)

		>>> c.update()
		>>> map(lambda c: c.getState(), 
				c.recurseNeigh('left')[0].recurseNeigh('right'))

			[False, True, False]
		
	"""
	def __init__(self, left = None, right = None, rule = 0, state = False):
		"""
		Create a new cell instance.
		Optionally assign pre-defined left or right cell instance.
		"""
		self.rule = rule
		self.state = state
		self.neigh = {
			'left': left,
			'right': right
		}

	def extend(self, side, cell = None, state = True):
		"""
		Extend cell with a neighbouring cell. `side' Can either be `left' or
		`right'. With the `cell' parameter a CAX.Cell instance can be supplied,
		by default CAX.Cell.extend() creates a new cell by itself, sets up 
		forward and backward links and sets the rule to be the same as the 
		extending neighbour. By default the neighbouring cell will have a `True'
		state as CAX implies infinite cells with state `False' to the left and
		to the right of the linked list of cells.
		"""
		# FIXME: backlinks to current cell when passed as argument
		if side == 'left':
			self.neigh['left'] = cell if cell != None else Cell(
				state = state, rule = self.rule, right = self)
		if side == 'right':
			self.neigh['right'] = cell if cell != None else Cell(
				state = state, rule = self.rule, left = self)
	
	def update(self, receiveFrom = None, senderState = False):
		"""
		Trigger an update of all cells to the next generation. Cell.update()
		recurses to its neighbouring cells and extends the list of cells with
		implicit `False' boundary cells that become `True' in the next generation.
		"""
		(leftstate, rightstate) = (False, False)

		if self.neigh['left'] != None:
			leftstate |= self.neigh['left'].state
			if receiveFrom != 'left': self.neigh['left'].update(
				receiveFrom = 'right', senderState = self.state)
		elif self.rule >> self.state & 1: self.extend('left')

		if self.neigh['right'] != None:
			rightstate |= self.neigh['right'].state
			if receiveFrom != 'right': self.neigh['right'].update(
				receiveFrom = 'left', senderState = self.state)
		elif self.rule >> (self.state << 2) & 1: self.extend('right')

		leftstate |= (senderState and receiveFrom == 'left')
		rightstate |= (senderState and receiveFrom == 'right')
		self.state = bool(self.rule>>(leftstate<<2 | self.state<<1 | rightstate) & 1)
	
	def recurseNeigh(self, dir = None):
		"""
		Recursively get a list of cells `left' or `right' of this cell.
		"""
		if dir != None:
			neighbors = []
			if self.neigh[dir]:
				neighbors = self.neigh[dir].recurseNeigh(dir)
			if dir == 'left':
				return neighbors + [self]
			if dir == 'right':
				return [self] + neighbors
		return { 'left': self.recurseNeigh(dir = 'left')[0:-1],
			'right': self.recurseNeigh(dir = 'right')[1:]	}

	def setState(self, state):
		"""
		Set this cell's state to `state'.
		"""
		self.state = state
	
	def getState(self):
		"""
		Get this cell's state.
		"""
		return self.state
	
	def setRule(self, rule):
		"""
		Set this cell's rule to `rule'.
		"""
		self.rule = rule
