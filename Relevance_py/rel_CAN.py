#!/usr/bin/env python3
""" @brief 
"""

###################################################################
# Telecom Paris - J-L. Dessalles 2022                             #
# Cognitive Approach to Natural Language Processing               #
#            http://teaching.dessalles.fr/CANLP                   #
###################################################################

import re
import random

from rel_Predicate import LPredicate, LsPredicate, EltList, Predicates
from rel_Rules import CausalRule, Incompatibility
from rel_World import World
from rel_utils import trace, ask, stop

Correction___ = 1

class LCausalRule(CausalRule):
	"""	Logical version of CausalRule: terms are predicates instead of mere strings
	"""
	def __init__(self, causalrule, predsearch):
		"""	receives a standard CausalRule and transforms it into a logical causal rule
		"""
		consequence, causes = causalrule
		predStr, sign = consequence
		self._consequence = LsPredicate(predsearch(predStr), sign)
		self._causes = []
		for Cpred, Csign in causes:
			C = LsPredicate(predsearch(Cpred), Csign)
			self._causes.append(C)
			
	def abduction(self, Consequence):
		"""	Returns list of causes if Consequence matches the rule's head
		"""
		if self._consequence.same(Consequence):	return self._causes
		return None

class LIncompatibility(Incompatibility):
	"""	Logical version of Incompatibility: terms are predicates instead of mere strings
	"""
	def __init__(self, incompatibility, predsearch):
		"""	receives a standard incompatibility and transforms it into a logical incompatibility
		"""
		self.terms = []
		for Tpred, Tsign in incompatibility:
			T = LsPredicate(predsearch(Tpred), Tsign)
			self.terms.append(T)

	def contains(self, Lspredicate):  
		"""	This function checks if a predicate (with the good sign) is present in an incompatibility
			and if so, it also returns the index where the predicate is found (useful for cause research done in abduction, we know that the causes have to be searched at the other indexes)
		"""
		
	def abduction(self, Consequence):
		"""	Returns list of other terms if the negation of Consequence is found in rule
		"""
		NegConsequence = Consequence.opposedPredicate()
		for i, sp in enumerate(self.terms):
			if sp.same(NegConsequence):	
				otherTerms = self.terms[:]	# copy of term list
				otherTerms.pop(i)
				return otherTerms
		return None
			
class Knowledge:
	"""	This class handles all notions linked to predicates.
	It realizes most of the steps of the CAN procedure
	including conflict detection, abduction, necessity transfer from consequence to cause using rules, the negation and the give-up/revision phase
	Here we deal with the real predicates, which have an attribute "name" which is how predicates are represented in the world
	
	Actually, these functions rather deal with LsPredicates than Predicates
	since sPredicates are more convenient to deal with signed predicates
	"""
	
	def __init__(self, knowledgeBase):
		"""	Shares with th World:
			- actions
			- ideas
			- causal rules
			- incompatibilities
			Ideally, this is should not be the case.
			The world should rely on finer grain 'knowledge', such as simulation.
			Here, the same 'knowledge' is used for abduction (here)
			and for world processing (World).
		"""
		self.predicates = Predicates(map(LPredicate, knowledgeBase.getWPredicates()))
		self.stringToPred = self.predicates.stringToPred
		self.causalRules = EltList(map(
			lambda CR: LCausalRule(CR, self.stringToPred),
			knowledgeBase.getCausalRules()))
		self.incompatibilities = EltList(map(
			lambda I: LIncompatibility(I, self.stringToPred), 
			knowledgeBase.getIncompatibilities()))
		self.readBeliefsAndPreferences(knowledgeBase.beliefs, 'belief')
		self.readBeliefsAndPreferences(knowledgeBase.preferences, 'preference')
		self.World = knowledgeBase	# World also maintains current state
		self.conflicting_predicate = None	# current conflicting predicate
		self.given_up = []	# List of predicates that could not be mutated
		trace(str(self), 3)	# print initial knowledge state


	def readBeliefsAndPreferences(self, wanted, origin):
		"""	retrieves necessities from knowledgeBase and updates predicates
		"""
		for predStr, necStr in wanted:
			pred = self.stringToPred(predStr)
			pred.wanted_(int(necStr), origin=origin)
			trace(f"{origin} {predStr} stored with necessity {necStr}", 3)

	# ------ CAN-methods
	def CAN(self):
		while True:
			if self.findConflict() is None:	break
			# ------ if the conflict has been given-up, the user can revise their preference
			self.revision()
			# ------ maybe the conflicting predicate can be changed (eg. action can be performed)
			self.makeItSo()
			# resolution through abduction
			self.conflictResolution()
			# print(self)
			stop(2)	# stops display
		trace(str(self), 2)	# printing end result
		
	def findConflict(self):
		if self.conflicting_predicate is None:
			for P in self.predicates:
				conflictIntensity, origin = P.conflicting(self.World)
				if origin is not None:
					PNec = P.getNecessity()
					self.conflicting_predicate = LsPredicate(P, '-' if PNec > 0 else '+')
					# trace(f"Conflict of intensity {conflictIntensity} found due to {origin}: {self.conflicting_predicate}")
					trace(f"Conflict due to {origin}: {self.conflicting_predicate}", 3)
					break
		if self.conflicting_predicate is None: trace('No conflict left', 1)
		return self.conflicting_predicate
	
	def makeItSo(self):
		"""	perform action or decide on unknown predicate
		"""
		if self.conflicting_predicate is not None:
			trace(f'Attempt to mutate {self.conflicting_predicate}', 4)
			if self.conflicting_predicate.getNecessity() > 0:
				if self.conflicting_predicate.setState("True", self.World):
					trace(f">>>>>>> deciding that {self.conflicting_predicate}", 1)
					self.conflicting_predicate = None
					self.World.update()
			else:	# conflicting predicate has negative necessity
				if self.conflicting_predicate.setState("False", self.World):
					trace(f">>>>>>> deciding that {self.conflicting_predicate.opposedPredicate()}", 1)
					self.conflicting_predicate = None
					self.World.update()

	def revision(self):
		CP = self.conflicting_predicate
		if CP is not None and CP.getPredicate() in self.given_up:
			while True:
				Answer = ask(f'We are left with a problem concerning {CP.getName()} of intensity -{abs(CP.getNecessity())}.\nDo you want to revise it? [enter a number or nothing or "show"]')
				if Answer and Answer.lower()[0] == 's':	print(self.World); print(self)
				else:	break
			try:	
				CP.wanted_(int(Answer), origin='preference')
				self.given_up.remove(CP.getPredicate())
			except ValueError:
				CP.wanted_(0, origin='preference')
			self.conflicting_predicate = None
		
	def abduction(self, consequence):
		"""	takes a consequence as input, and returns a new consequence
			if a mutable cause is a found, or None otherwise.
		"""
		trace(f"Searching causes for {consequence}", 3)
		candidate_rules = []	# list of lists of causes
		# ------ Abduction from causal rules
		for CR in self.causalRules:
			Causes = CR.abduction(consequence)
			if Causes is not None:	candidate_rules.append(Causes)
		# ------ Abduction from incompatibilities
		# ------ If we look for a cause of A, we search for an incompatibility rule where -A appears
		for incomp in self.incompatibilities:
			Causes = incomp.abduction(consequence)
			if Causes is not None:	candidate_rules.append(Causes)
		if candidate_rules == []:   # not a consequence in any causal rule or incompatibility
			return None
		trace(f"{len(candidate_rules)} rule(s) could cause {consequence}", 4)
		# random.shuffle(candidate_rules)
		for Causes in candidate_rules:
			trace(f"Looking for a weak cause in {Causes} with necessity {consequence.getNecessity()}", 4)
			candidate_causes = Causes[:]	# copie
			# random.shuffle(candidate_causes)
			for cause in candidate_causes:
				# ------ considering only causes that have the same truth value as the consequence
				if consequence.aligned(cause, self.World):
					consequenceNec = consequence.getNecessity()
					causeNec = cause.getNecessity()
					trace(f"cause of {consequence}: {cause}", 5)
					# mutability condition
					if (consequenceNec * causeNec > 0) or abs(causeNec) < abs(consequenceNec):
						yield cause
	
	def giveUp(self):
		trace(f"Giving up on {self.conflicting_predicate}", 1)
		# ------ we remember that CP resisted change with its necessity
		# ------ so we set necessity to its opposite
		trace(f"storing {self.conflicting_predicate} with opposite necessity", 4)
		self.conflicting_predicate.setNecessity(self.conflicting_predicate.getNecessity(), sign='-')
		self.given_up.append(self.conflicting_predicate.getPredicate())
		self.conflicting_predicate = None
		
	def conflictResolution(self):
		if self.conflicting_predicate is None:	return
		CP = self.conflicting_predicate
		trace(f"Conflict of intensity {CP.getNecessity()} with {CP.getSign()}{CP.getName()}", 1) 
		Negation = False  # Used to know if we are in the direct or negation phase, and then stop to avoid looping.
		while True:
			conflicting_pred = self.conflicting_predicate
			# ------ looking for a weak cause
			for weak_cause in self.abduction(conflicting_pred):
				if weak_cause is not None:
					trace(f"Propagating conflit onto cause: {weak_cause}", 2)
					weak_cause.setNecessity(conflicting_pred.getNecessity())
					# print(weak_cause.predicate)
					self.conflicting_predicate = weak_cause	# new conflict
					return	# no recursive call
			# no weak cause
			trace(f"Failing to perform further abduction from {conflicting_pred}", 3)
			if not Negation:   # negation not tried yet
				CP = self.conflicting_predicate
				trace(f"Negating {CP}, considering {CP.opposedPredicate()}", 2)
				self.conflicting_predicate.setOpposite()
				Negation = True
				continue
			else:  # negation already tried
				self.giveUp()
				break
			return
	   
	def __str__(self):
		return '\n\n'.join([
				f'\npredicates: {self.predicates}',
				# f'incompatibilities: {self.incompatibilities}',
				# f'causalRules: {self.causalRules}',
		])
			
if __name__ == '__main__':
	# ------ setting trace level
	TraceLevel = 1
	trace(level=TraceLevel, set=True)
	# ------ loading world
	# W = World('rel_covid_vaccine.pl')
	W = World('rel_doors.pl')
	# ------ creating knowledge
	K = Knowledge(W)
	# ------ launching CAN
	print()
	print()
	K.CAN()


	
__author__ = 'Harith Proietti & jean-louis Dessalles'
