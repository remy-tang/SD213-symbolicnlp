#!/usr/bin/env python3
###################################################################
# Telecom Paris - J-L. Dessalles 2022                             #
# Cognitive Approach to Natural Language Processing               #
#            http://teaching.dessalles.fr/CANLP                   #
###################################################################

" Reads DCG file and translates into Python structures "

import re
import syn_Grammar
from syn_util import trace, stop
import asp_Lexicon


class HFRule(syn_Grammar.Rule):
	"""	Head-first rule
	"""
	def __init__(self, LHS, RHS, Pgm='', lexical=False):
		super().__init__(LHS, RHS, Pgm=Pgm, lexical=lexical)
		self.HeadPosition = 1
		
class HLRule(syn_Grammar.Rule):
	"""	Head-last rule
	"""
	def __init__(self, LHS, RHS, Pgm='', lexical=False):
		super().__init__(LHS, RHS, Pgm=Pgm, lexical=lexical)
		self.HeadPosition = 2


class Grammar(syn_Grammar.Grammar):
	""" List of grammar rules distinguishing head position.
	
		Here, rules can be head-first (-->) or head-last (->)
	"""
	
	def __init__(self, *args):
		super().__init__(*args)
		self. Lexicon = None
	
	def loadDCG(self, DCGFileName):
		"""	Retrieve grammar as DCG rules.
		"""
		super().loadDCG(DCGFileName, RuleClass=HFRule, ProductionSign='-->')
		super().loadDCG(DCGFileName, RuleClass=HLRule, ProductionSign='->')
						 
	def loadLexicon(self, LexiconFileName):
		self.Lexicon = asp_Lexicon.Lexicon(LexiconFileName)
		for word in self.Lexicon:
			# LHS, RHS, PGM, lexical = self.processRule(word.cat, f"[{word.word.lower()}]")
			LHS = word
			RHS = (f"[{word.word.lower()}]",)
			self.Rules.append(self.RuleClass(LHS, RHS, lexical=True))			
			# checking of rule already exists, as words may differ just by feature structures
			# New = True
			# for R in self.Rules:
				# if R.lexical and R.LHS == word.cat and R.RHS == RHS:	New = False
			# if New: 
				# self.Rules.append(self.RuleClass(word.cat, RHS, lexical=True))
	
	def match(self, W1, W2):
		"""	perform unification between feature structures
		"""
		trace(f'unifying {W1}  and  {W2}', 6)
		if type(W1) == str:
			# real word, should match RHS of lexical rule
			return super().match(W1, W2)
		# W1 is supposed to be a feature structure
		return (W1.cat == W2) or None

	def unifyList(self, L1, L2):
		"""	find a substitution that allows two lists to match termwise.
		"""
		if L1 != ():
			if L2 == (): return None
			# trying all matching entries for the two first words
			if not self.match(L1[0], L2[0]):	return None
			# trace(f'\tMatch {L1[0], L2[0]} ok', 4)
			return self.unifyList(L1[1:], L2[1:])
		elif L2 == (): return True
		return None

	def semantic_merge(self, Cat, Phrase1, Phrase2=None):
		"""	Merging feature structures
		"""
		trace(f'Merging {Phrase1} and {Phrase2} under {Cat}', 5)
		return Phrase1.semantic_merge(Cat, Phrase2)

if __name__ == "__main__":
	print(__doc__)
	grammar = Grammar()
	grammar.loadDCG('syn_Grammar.pl')
	trace(grammar)
	grammar.parse(grammar.ask())

__author__ = 'Dessalles'

