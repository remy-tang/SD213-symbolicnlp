#!/usr/bin/env python3
""" @brief 	Rules are:
	- causal rules
	- incompatibilities
	here in basic form (predicates are just (name, sign) couples)
"""


###################################################################
# Telecom Paris - J-L. Dessalles 2022                             #
# Cognitive Approach to Natural Language Processing               #
#            http://teaching.dessalles.fr/CANLP                   #
###################################################################

class CausalRule:
	"""	A causal rule is represented with a consequence and a list of causes.
		Consequence and causes are tuples: (name of predicate, sign)
	"""
	def __init__(self, consequence, causes):
		self._consequence = consequence
		self._causes = causes

	def getCauses(self):	return self._causes

	def getConsequence(self):	return self._consequence

	def __str__(self):
		return f"{self._consequence} <=== {' + '.join(map(str, self._causes))}"

	__repr__ = __str__


class Incompatibility:
	"""	An incompatibility is a list of incompatible predicates
		where each predicate is represented in the form of a tuple (name of predicate, sign)
	"""
	def __init__(self, list):
		self.terms = list

	def getTerms(self):
		return self.terms
				
	def __str__(self):
		return f"[{', '.join(map(str, self.terms))}]"

	__repr__ = __str__


__author__ = 'Harith Proietti & jean-louis Dessalles'
