#!/usr/bin/env python3
""" @brief 
"""

###################################################################
# Telecom Paris - J-L. Dessalles 2022                             #
# Cognitive Approach to Natural Language Processing               #
#            http://teaching.dessalles.fr/CANLP                   #
###################################################################

# class centralizing the concept of Predicate
# implements the methods of the class
# many of these methods take as a parameter a sign which allows to know if we are dealing with the positive or negative version of the predicate

# 3 possible states : "True", "False", "Unknown"

from rel_utils import trace

PERCEPTION = 100	# necessity of perception

def inverseSign(state):
	if state == '+':	return '-'
	return '+'
	
def inverseState(state):
	if state == 'True':	return 'False'
	elif state == 'False':	return 'True'
	return state	# 'Unknown' left unchanged
	

class WPredicate:
	"""	Boolean variable in the world. 
		Not really a predicate (as predicate will have necessity)
	"""
	def __init__(self, name, state='Unknown', type=None, origin=None):
		self._name = name
		self._state = state	# 'True', 'False' or 'Unknown'
		self._type = type	# action or idea
		self._origin = origin	# None or default, belief, preference, inferred

	def getName(self):	return self._name

	def isNamed(self, name):
		return self._name == name

	def getState(self, sign='+'):
		if sign == '-':
			return self.invertedState()	# no internal change
		return(self._state)

	def setState(self, state, sign='+', force=False, origin=None):
		"""	tentative state change
		"""
		if force or self._state == 'Unknown' or self._type == 'action':
			# only change if state = 'Unknown' or if action
			self._state = state
			if sign == '-':	self.reverseState()
			if origin is not None:	self._origin = origin
			trace(f'changed:  {self}', 5)
			return True
		return False
		
	def getOrigin(self): 	return self._origin
	
	def same(self, other):
		"""	checks name equality
		"""
		return self._name == other._name

	def update(self, other):
		" update self with other's values "
		if not self.same(other):
			raise Exception(f'Updating {self} with foreign predicate {other}')
		if other._state != 'Unknown':	self._state = other._state
		if other._type is not None:	self._type = other._type
		if other._origin is not None:	self._origin = other._origin
	
	def invertedState(self, state=None):
		if state is None:	# inverse own state
			state = self._state
		state = inverseState(state)	# 'Unknown' left unchanged
		return state
	
	def reverseState(self, state=None):
		"""	reverses state in place
		"""
		self._state = self.invertedState(state=state)
		return self._state
	
	def reset(self):
		"""	forget inferred facts
		"""
		if self._origin == 'inferred':	self._state = "False"
		
	def __str__(self):
		return(f'''{self._name}:{self.getState('+')}''')

	__repr__ = __str__

class sPredicate:
	"""	(W)Predicate + its sign (- meaning negative version of the state)
	"""
	def __init__(self, predicate, sign='+'):
		self.predicate = predicate
		self.sign = sign

	def getName(self):	return self.predicate.getName()

	def getPredicate(self):	return self.predicate

	def getSign(self):	return self.sign

	def setSign(self, sign):	self.sign = sign 
	
	def getState(self):
		"""	True if sign == '+' and "True"
			or sign == '-' and "False"
		"""
		return self.predicate.getState(sign=self.sign)

	def setState(self, state, force=False, origin=None):
		return self.predicate.setState(state, sign=self.sign, force=force, origin=origin)
	
	def setOpposite(self):	
		"""	modification of sign *in place*
		"""
		if self.sign == '+':	self.setSign('-')
		else:					self.setSign('+')

	def opposedPredicate(self):	 
		""" negation used in CAN.
			Uses the oppositePredicate function, but not directly on the sPredicate but on a copy of it.
			Otherwise we would have the same issues as when the sign was an attribute of the Predicate class.
		"""
		opposed_predicate = sPredicate(self.predicate, self.sign)
		opposed_predicate.setOpposite()
		return(opposed_predicate)

	def signature(self):
		return (self.predicate._name, self.sign)

	def __str__(self):
		return f"{'-' * (self.sign == '-')}{self.predicate._name}"

	__repr__ = __str__


class LPredicate:
	"""	Logical predicate: receives necessity
	"""
	def __init__(self, name, necessity=0):
		self._name = name
		self._necessity = necessity	# positive or negative number 
		self._wanted = 0	# can only be changed through revision
		self._origin = None
	
	def getName(self):	return self._name

	def isNamed(self, name):
		return self._name == name

	def same(self, other):
		"""	checks name equality
		"""
		return self._name == other._name

	def setNecessity(self, necessity):
		self._necessity = necessity

	def wanted_(self, intensity=None, origin=None):
		"""	Stores/reads belief or preferene
		"""
		if intensity is not None:
			self.setNecessity(intensity)
			self._wanted = intensity	# can only be changed through revision
			self._origin = origin
		return self._wanted, self._origin
		
	def getNecessity(self, sign='+'):
		if sign == '+':	return self._necessity
		else:			return -self._necessity

	def observe(self, World):
		return World.observe(self._name)
		
	def setState(self, state, World):
		return World.setState(self._name, state)
		
	"""
	def reviseState(self, sign):
		if self.getState(sign) == 'False' or 'Unknown':
			self.setState('True', sign)
		else:
			self.setState('False')			
	"""
	
	def revisable(self):
		return True	# to be overloaded
	
	def conflicting(self, World):
		"""	A predicate is conflicting if:
			- its necessity and its state are opposite 
			- its necessity and its belief/preference are opposite
		"""
		PNec = self.getNecessity()
		PState = self.observe(World)
		PWant, origin = self.wanted_()
		if PNec > 0:
			if PState == "False":	return -PERCEPTION, 'perception'
			if PWant < 0:	return PWant, origin
		elif PNec < 0:
			if PState == "True":	return PERCEPTION, 'perception'
			if PWant > 0:	return PWant, origin
		return 0, None

		
	def __str__(self):	return f"{self._name}({self.getNecessity()})"


class LsPredicate(sPredicate):

	def getNecessity(self):
		return self.predicate.getNecessity(sign=self.sign)

	def setNecessity(self, necessity, sign=None):
		if self.sign == '-':	necessity = -necessity
		if sign == '-':	necessity = -necessity	# possible double negation
		self.predicate.setNecessity(necessity)

	def same(self, other):
		"""	Checks that to sPredicates are equal
		"""
		return self.predicate.same(other.predicate) and self.sign == other.sign
	
	def getState(self, World):
		return self.predicate.observe(World)
	
	def setState(self, state, World):
		if self.sign == '-':	state = inverseState(state)
		return self.predicate.setState(state, World)

	def actual(self, World):
		state = self.getState(World)
		return	self.sign == '+' and state != "False" \
				or self.sign == '-' and state != "True"

	def aligned(self, other, World):
		"""	True if self and other have compatible truth values
		"""
		return self.actual(World) == other.actual(World)
	
	def wanted_(self, intensity=None, origin=None):
		wantness, origin = self.predicate.wanted_(intensity=intensity, origin=origin)
		if self.sign == '-':	return -wantness, origin
		return wantness, origin
		
	def __str__(self):	
			return f"{'-' * (self.sign == '-')}{self.getName()}({self.getNecessity()})"
		
class EltList:
	"""	Basically a set of elements with printing capabilities
	"""
	def __init__(self, PredicateList):
		self.Preds = list(PredicateList)
		
	def __iter__(self):	return iter(self.Preds)
	
	def __str__(self):
		return '\n\t' + '\n\t'.join(sorted(str(P) for P in self)) + '\n'
	
	__repr__ = __str__
	
class WPredicates(dict):
	"""	list of WPredicate with update capability
	"""
	def add(self, WP):
		"""	Adding or updating world-predicate
		"""
		for P in self:
			if P == WP.getName():
				# updating
				self[P].update(WP)
				return
		# ------ adding WP
		self[WP.getName()] = WP
		return
	
class Predicates(EltList):
	"""	List of predicates with search capabilities
	"""
	def stringToPred(self, predStr):
		for P in self:
			if P.isNamed(predStr):	return(P)
		raise Exception(f"{predStr} has not been found among predicates")


__author__ = 'Harith Proietti & jean-louis Dessalles'
