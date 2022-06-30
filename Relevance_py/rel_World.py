#!/usr/bin/env python3
""" @brief 	World processing
"""

###################################################################
# Telecom Paris - J-L. Dessalles 2022                             #
# Cognitive Approach to Natural Language Processing               #
#            http://teaching.dessalles.fr/CANLP                   #
###################################################################

import re

from rel_Predicate import WPredicate, sPredicate, WPredicates
from rel_Rules import CausalRule, Incompatibility
from rel_utils import trace

signedPredicate = lambda T: (T.strip('-'), "-" if T[0] == '-' else "+")

class KnowledgeBase:
	"""	Reads a text file to extraxt all input knowledge
	"""
	def __init__(self, knowledgeFile):
		self.wpredicates = WPredicates()	# all world-predicates
		self.incompatibilities = []
		self.causalRules = []
		self.beliefs = []	
		self.preferences = []
		self.retrieveKnowledge(knowledgeFile)
		self.update()
		trace(str(self), 3)	# print initial state of the world

		
	def retrieveKnowledge(self, knowledgeFile):
		"""	Reads a knowledge text file to retrieve:
			- actions	(used in both World and Knowledge)
			- ideas	(used in both World and Knowledge)
			- defaults	(used in World)
			- necessities	(used in Knowledge)
			- initial values	(used in World)
			- incompatibilities	(used in both World and Knowledge)
			- causal rules	(used in both World and Knowledge)
		"""
		knowledgeTxt = open(knowledgeFile).read()
		
		# ------ actions
		for A in re.findall(r'^\s*action\((\w+)\)', knowledgeTxt, flags=re.M):
			self.wpredicates.add(WPredicate(A, state='False', type='action'))
		trace(f'{len(self.wpredicates)} actions found', 4)
		
		# ------ defaults
		defaultsTxt = re.findall(r'^\s*default\((-?\w+)(?:[,_ ]*)\)', knowledgeTxt, flags=re.M)
		# ------ no Boolean value, but the strings "True", "False", "Unknown" instead
		for D in defaultsTxt:
			predStr = D.strip('-')
			predSign = ("False" if D[0] == '-' else "True")
			self.wpredicates.add(WPredicate(predStr, state=predSign, origin='default'))
		
		# ------ beliefs and preferences (will be used by Knowledge)
		self.beliefs = re.findall(r'^\s*belief\((\w+),\s*([-+]?\d+)\)', knowledgeTxt, flags=re.M)
		self.preferences = re.findall(r'^\s*preference\((\w+),\s*([-+]?\d+)\)', knowledgeTxt, flags=re.M)
		for B in self.beliefs:
			self.wpredicates.add(WPredicate(B[0], origin='beliefs'))
		for P in self.preferences:
			self.wpredicates.add(WPredicate(P[0], origin='preference'))

		# ------ initials
		initialsTxt = re.findall(r'^\s*initial_situation\((-?\w+)\)', knowledgeTxt, flags=re.M)
		for I in initialsTxt:	
			predStr = I.strip('-')
			predState = ("False" if I[0] == '-' else "True")
			# ------ priority over defaults and preferences
			trace(f'Setting {predStr} to {predState}', 5)
			self.wpredicates.add(WPredicate(predStr, state=predState))
		
		# ------ incompatibilities
		incompatibilitiesTxt = re.findall(r'^\s*incompatible\(([\,\-\w ]+)\)', knowledgeTxt, flags=re.M)
		for incompatibilityStr in incompatibilitiesTxt:
			terms = re.split(r',\s*', incompatibilityStr)
			Incompatibility_terms = []
			for T in terms:
				Tstr, Tsign = signedPredicate(T)
				self.wpredicates.add(WPredicate(Tstr))
				Incompatibility_terms.append(sPredicate(self.wpredicates[Tstr], sign=Tsign))
			self.incompatibilities.append(Incompatibility(Incompatibility_terms))
		trace(f'{len(self.incompatibilities)} incompatibility rules found', 4)
		
		# ------ causal rules
		causalrulesTxt = re.findall(r'^\s*(-?\w+)\s*<===\s*([^\.]*?)\.?\s*$', knowledgeTxt, flags=re.M)
		for causalRule in causalrulesTxt:
			consequenceStr, consSign = signedPredicate(causalRule[0])
			self.wpredicates.add(WPredicate(consequenceStr))
			consequence = sPredicate(self.wpredicates[consequenceStr], sign=consSign)
			terms = re.split(r'\s*\+\s*', causalRule[1])
			causes = []
			for T in terms:
				Tstr, Tsign = signedPredicate(T)
				self.wpredicates.add(WPredicate(Tstr))
				causes.append(sPredicate(self.wpredicates[Tstr], sign=Tsign))
			self.causalRules.append(CausalRule(consequence, causes))
		trace(f'{len(self.causalRules)} causal rules found', 4)

	# ------ interface with Knowledge - reveal predicates only through their names
	def getWPredicates(self):
		# ------ only return wpredicate labels
		return self.wpredicates.keys()
	
	def getCausalRules(self):
		for CR in self.causalRules:
			yield (CR.getConsequence().signature(), ((P.signature()) for P in CR.getCauses()))	# signature = (name, sign)
		
	def getIncompatibilities(self):
		for I in self.incompatibilities:
			yield ((P.signature()) for P in I.getTerms())	# signature = (name, sign)
		
	def observe(self, predicateName):
		try:	return self.wpredicates[predicateName].getState()
		except KeyError:
			raise KeyError('Error: unknown predicate')

	def setState(self, predicateName, state, force=False):
		try:	return self.wpredicates[predicateName].setState(state, force=force)
		except KeyError:
			raise KeyError('Error: unknown predicate')
	# ------
	
	def __str__(self):
		predicatesStr = "\n\t".join(sorted(map(str, self.wpredicates.values())))
		return '\n\n'.join([
				f'{len(self.wpredicates)} predicates: \n\t{predicatesStr}',
				# f'incompatibilities: {self.incompatibilities}',
				# f'causalRules: {self.causalRules}',
		])
		

class World(KnowledgeBase):
	"""
		This class handles the state of the world.
		This is where all concrete modification of predicates are done.
		In the world, predicates are represented by their string name
		which is coincides with the attribute "name" of the predicates available in knowledge.
		This class is also the one which allows to update the state of the world 
		according to the causal rules and incompatibilities.
	"""
		

	def infer_states_from_causalRules(self):
		"""	infer states using causal rules
		"""
		newInferencesCount = 0
		for CRule in self.causalRules:
			validRule = True
			for cause in CRule.getCauses():
				# consequence is not its 'good state' if at least one of the causes doesn't have the "good" state
				if cause.getState() != "True":
					# ------ this rule is not active
					validRule = False
					break
			if validRule:
				csq = CRule.getConsequence()
				if csq.getState() != "True":
					newInferencesCount += 1
					trace(f"Inferring {csq} (through causal rules)", 2)
					csq.setState("True", force=True, origin='inferred')
		return newInferencesCount

	def infer_states_from_incompatibilities(self):
		"""	infer states using incompatibilities
		"""
		newInferencesCount = 0
		for inc in self.incompatibilities:
			validRule = True
			csq = None
			for pred in inc.getTerms():
				# consequence is not in 'good state' if at least one of the causes doesn't have the "good" state 
				# having the 'good state' means that the predicate is True if it appears in its positive form ('+'), or False if it appears in its negative form ('-')
				if pred.getState() != "True":
					if csq is not None:
						# ------ more than one not valid predicate - rule is useless
						validRule = False
					csq = pred
			if validRule and csq is not None:	# only one not valid predicate
				# all predicates are in 'good state' except one which is unknown: 
				# only case where we can update with incompatibilities
				consequence = csq.opposedPredicate()
				if consequence.getState() != "True":
					newInferencesCount += 1
					trace(f"Inferring {consequence} (through incompatibility rules)", 2)
					consequence.setState("True", force=True, origin='inferred')
		return newInferencesCount

	def update(self):
		"""	Updates the world by drawing all consequences from true facts
		"""
		# forgetting about previously inferred facts
		for P in self.wpredicates:	self.wpredicates[P].reset()
		while True:
			newInferencesCount = self.infer_states_from_causalRules() + \
					self.infer_states_from_incompatibilities()
			if newInferencesCount == 0:	break
			trace(f"{newInferencesCount} new inferences", 3)
		
if __name__ == '__main__':
	TraceLevel = 3
	trace(level=TraceLevel, set=True)
	# W = World('covid_vaccine.txt')
	W = World('rel_doors_00.pl')
	W.update()
	print()
	print(W)

__author__ = 'Harith Proietti & jean-louis Dessalles'
