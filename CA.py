# Elementary Cellular Automaton
# Hessel Schut, 2018-11-19

class CA:
	def __init__(self, rule = None, size = None, uniform  = None):
		self.uniform = (uniform == True)
		
		if size != None:
			self.states = [False,] * size
		else:
			self.states = []
		self.previous_states = self.states

		### FIXME! Move this block to set_rule() and call set_rule here...
		if rule != None:
			if type(rule) == type(int()):
				if self.uniform:
					self.rule = rule
				else:
					self.rules = [ rule, ] * len(self.states)
			elif type(rule) == type(list()):
				if len(rule) >= len(states):
					self.rules = rule[0:len(states)]
				else:
					rules = [0, ] * len(self.states)
					for i in range(len(self.states)):
						self.rules[i] = self.states[i % len(self.states)]
		else:
			if self.uniform:
				self.rule = 30
			else:
				self.rules = [ 30, ] * len(self.states);
	
	def __repr__(self):
		# return self.fmt_states(self, symbols = ('0', '1'))
		return self.fmt_states(self)

	def set_rule(self, rule):
		'''
		Setter method to change rule.
		'''
		self.rule = rule

	def single_active_cell(self):
		'''
		Initialize to centered single active cell.
		'''
		self.states = len(self.states) * [False,]
		self.states[int(len(self.states)/2)] = True

	def randomize(self):
		'''
		Set random intial state.
		'''
		from random import getrandbits
		self.states = list(map(
			lambda c: bool(getrandbits(1)), 
			len(self.states)* [None,]))

	def fmt_states(self, symbols = (' ', '*')):
		'''
		Format states in (compact) string representation.
		'''
		return ''.join(map(
			lambda e: symbols[1] if e else symbols[0], 
			self.states))

	def generation(self):
		self.previous_states = self.states[:]
		i = 0 
		while i < len(self.states):
			cellstate = 4 * self.previous_states[(i - 1) % len(self.states)]
			cellstate += 2 * self.previous_states[i]
			cellstate += self.previous_states[(i + 1) % len(self.states)]
			
			self.states[i] = ((self.rule if self.uniform else self.rules[i]) >> cellstate) & 1

			i += 1
		yield self.states

	
