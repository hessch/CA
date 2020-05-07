# LOC.py - Unbounded cellular automaton
# Hessel Schut, 2018-01-25

# Left of center / Off of the strip -- Suzanne Vega

class LeftOfCenter:

    def __init__(self, states=[[], []]):
        if init_state != None:
            self.states = [[], []]
        else:
            self.states = states

    def getLeft(self):
        return self.states[0]

    def getCenter(self):
        return self.states[1][0]

    def getRight(self):
        return self.states[1]

    def appendLeft(self, cellstate):
        self.states[0].append(cellstate)

    def appendRight(self, cellstate):
        self.states[1].append(cellstate)

    def getStates(self):
        return self.states[0][::-1] + self.states[1]

    def getBinString(self):
        return ''.join(map(lambda s: str(s), self.getStates()))


class UnboundedCA:
    """
        Unbounded elementary cellular automaton.
        UnboundedCA starts with an initial state surrounded by infinite implicit cells
        in inactive state, but expanding only by a single cell at a time. 
        This means a transition rule like 000 -> _1_ will not lead to "infinite ones" 
        as transistions will only be calculated for the current known space, expanding 
        at most one cell per generation outwards.
        """
    __module__ = __name__
    __qualname__ = 'UnboundedCA'

    def __init__(self, rule = 9, init_state=[[], [1]]):
        """
                Create new UnboundedCA instance, defaults to rule 30 and inital single
                single active cell.
                """
        if rule != None:
            self.rule = rule
        else:
            self.rule = 30
        if init_state != None:
            self.states = init_state
        else:
            self.states = [[], [1]]
        self.leftlen = len(self.states[0])

    def setRule(self, rule):
        self.rule = rule

    def ca(self, state):
        return self.rule >> state & 1

    def update(self):
        lstates = [[], []]
        if self.ca(4 * self.states[1][(-1)]):
            lstates[1].append(1)
        for ci, cs in enumerate(self.states[1]):
            if ci == 0:
                left = 0 if len(self.states[0]) == 0 else self.states[0][0]
                right = 0 if len(self.states[1]) <= 1 else self.states[1][1]
                lstates[1].append(self.ca(left<<2 | cs<<1 | right))
            else:
                if ci == len(self.states[1]) - 1:
                    right = 0
                else:
                    right = self.states[1][(ci + 1)]
                lstates[1].append(self.ca(self.states[1][(ci - 1)]<<2 | cs<<1 | right))

        if len(self.states[0]) == 0:
            if self.ca(self.states[1][0]):
                lstates[0].append(1)
            self.states = lstates
            self.leftlen = len(lstates[0])
            return
        if self.ca(self.states[0][(-1)]):
            lstates[0].append(1)
        for ci, cs in enumerate(self.states[0]):
            if ci < len(self.states[0]) - 1:
                left = self.states[0][(ci + 1)]
            else:
                left = 0
            if ci == 0:
                right = self.states[1][0]
            else:
                right = self.states[0][(ci - 1)]
            lstates[0].append(self.ca(left<<2 | cs<<1 | right))

        self.states = lstates
        self.leftlen = len(lstates[0])

    def iterateCenterColumn(self, n=8, asInteger=True):
        """Return n iterations of center cell, return as either bit
                        vector or as little endian integer."""
        terms = []
        for bit in range(n, 0, -1):
            terms.append(self.states[1][0] << bit)
            self.update()

        if asInteger:
            return sum(terms)
        else:
            return map(lambda t: t > 0, terms)

    def getStates(self):
        """Return states as single vector."""
        return self.states[0][::-1] + self.states[1]

    def formatStates(self):
        """Return states as a string of ones and zeros."""
        return ''.join(map(lambda s: str(s), self.getStates()))
