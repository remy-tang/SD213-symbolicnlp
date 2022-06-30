#!/usr/bin/env python3
###################################################################
# Telecom Paris - J-L. Dessalles 2022                             #
# Cognitive Approach to Natural Language Processing               #
#            http://teaching.dessalles.fr/CANLP                   #
###################################################################

" Reads DCG file and translates into Python structures "

import re
from syn_util import trace, Tree_, stop

class Rule:
	"""	defines a context-free rule 
	"""
	def __init__(self, LHS, RHS, Pgm='', lexical=False):
		self.LHS = LHS
		self.RHS = RHS	
		self.Pgm = Pgm
		self.lexical = lexical

	def is_lexical(self):	return self.lexical
		# return len(self.RHS) == 1 and re.match(r'\[(.*?)\]', self.RHS[0]) is not None
	
	def __str__(self):
		# return f'''{self.LHS} --> {", ".join(self.RHS)}.{'    (lexical rule)' * self.lexical}'''
		return f'''{self.LHS} --> {", ".join(self.RHS)}.'''
		

class Grammar:
	"""	List of grammar rules 
	"""
	def __init__(self):
		self.Rules = []
		self.WordPattern = '[%s]'	# default representation of words
		self.reinit()
		self.RuleClass = Rule
		
	def reinit(self):
		self.Count = 0	# counts the number of times rules are scanned
		self.ParseTrees = []	# stores parse trees found
		
	def loadDCG(self, DCGFileName, LexicalRuleInputPattern=None, WordPattern=None, 
				ProductionSign='-->', RuleClass=None):
		"""	Retrieve grammar as DCG rules.
		"""
		if RuleClass is not None:	self.RuleClass = RuleClass
		if LexicalRuleInputPattern is None:	LexicalRuleInputPattern = r'\[(.*?)\]'	# identifies how words appears in rules
		if WordPattern is not None:	self.WordPattern = WordPattern	# identifies how words appears in stored rules
		" reads a file with DCG rules with Prolog syntax and translates into Python structures "
		DCGTxt = open(DCGFileName).read()	# grammar in one string
		# np --> det, n.
		RuleTuples =  re.findall(	r'^([a-z]+)\s+' + ProductionSign + r'\s+([^\.\{]+)()\.', 
									DCGTxt, re.M|re.S)
		# np --> det, n, {some instructions}.
		RuleTuples += re.findall(	r'^([a-z]+)\s+' + ProductionSign + r'\s+([^\.\{]+)\{(.*?)\}\.',
									DCGTxt, re.M|re.S)
		# np(Number, pers3) --> det(Number), n(Number).
		RuleTuples += re.findall(	r'^([a-z]+\([^\-]*\))\s+' + ProductionSign + r'\s+([^\.\{]+?)()\.',
									DCGTxt, re.M|re.S)
		# np(Number, pers3) --> det(Number), n(Number), {some instructions}.
		RuleTuples += re.findall(	r'^([a-z]+\([^\-]*\))\s+' + ProductionSign + r'\s+([^\.\{]+?)\{(.*?)\}\.', 
									DCGTxt, re.M|re.S)
		for R in RuleTuples:
			for RHSstr in R[1].split('|'):
				# processing and storing rules
				LHS, RHS, PGM, lexical = self.processRule(R[0], RHSstr, R[2], 
						LexicalRuleInputPattern=LexicalRuleInputPattern)
				self.Rules.append(self.RuleClass(LHS, RHS, PGM, lexical=lexical))
		trace(self, 4); trace(f'{len(RuleTuples)} rules found in {DCGFileName}\n', 1)

	def processRule(self, LHSstr, RHSstr, PGMstr='', LexicalRuleInputPattern=None):
		"""	converts grammar rule from string into formal representation.
		"""
		RHS, lexical = self.processRHS(RHSstr, LexicalRuleInputPattern=LexicalRuleInputPattern)
		return LHSstr, RHS, PGMstr, lexical
		
	def processRHS(self, RHSstr, LexicalRuleInputPattern):
		"""	reading right-hand side of rules.
		"""
		RHS = ()
		lexical = False
		for G in RHSstr.split(','):
			if G.strip() == '': continue
			if LexicalRuleInputPattern:
				LR = re.match(LexicalRuleInputPattern, G)	# lexical rule
			else:	LR = None
			if LR: 
				lexical = True
				RHS += (self.WordPattern % LR[1].strip(),)
			else:	RHS += (G.strip(),)
		return RHS, lexical
		
	def ask(self, Sentence=None, Prompt='\nSentence > '):
		"""	ask for a sentence to analyze.
		"""
		if Sentence is None:	Sentence = input(Prompt)
		else:	print(f'{Prompt}{Sentence}')
		if Sentence == '':	raise StopIteration
		return tuple(self.WordPattern % w for w in Sentence.strip().split())

	def process(self, Sentence=None, Target=None):
		self.parse(self.ask(Sentence), Target=Target)

	def __iter__(self):
		self.Count += 1
		return iter(self.Rules)
	
	def ruleLHS(self, LHS):	
		"""	find rules whose left-hand side matches LHS.
		"""
		self.Count += 1
		for R in self.Rules:	
			if R.LHS == LHS:	yield R, None	# Rule and match structure
	
	def use(self):
		"""	display Count.
		"""
		return f'\nRules have been scanned {self.Count} times\n'

	def merge(self, Head, *Phrases):
		"""	merging of phrases - build a tree by default.
		"""
		return (Tree_(Head, Phrases),)

	def match(self, W1, W2):
		"check (non)-terminal equality "
		# important to return None instead of False
		return (W1.lower() == W2.lower()) or None	
		
	def unifyList(self, L1, L2):
		"""	check whether elements of L1 and L2 match.
		"""
		# important to return None instead of False
		return all(map(lambda x: self.match(*x), zip(L1, L2))) or None
		
	def update(self, Input, Match):
		return Input	# default behaviour
	
	def parse(self, *args, **argv):
		"""	to be overloaded.
		"""
		print('Parser has not been defined')

	def lexical(self, W):
		"""	checks that a symbol is a word.
		"""
		MatchPattern = self.WordPattern.replace('%s', '.*?').replace('(', r'\(').replace(')', r'\)').replace('[', r'\[').replace(']', r'\]')
		# LR = re.match(r'\[(.*?)\]$', W)
		LR = re.match(MatchPattern + '$', str(W))
		return LR is not None
	
	def __str__(self):
		return '\n'.join([str(R) for R in self.Rules]) + '\n'
		
if __name__ == "__main__":
	print(__doc__)
	grammar = Grammar()
	grammar.loadDCG('syn_Grammar.pl')
	trace(grammar)
	grammar.parse(grammar.ask())


__author__ = 'Dessalles'

