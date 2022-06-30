#!/usr/bin/env python3
""" @brief  minimal implementation of aspectual processing  
"""

###################################################################
# Telecom Paris - J-L. Dessalles 2022                             #
# Cognitive Approach to Natural Language Processing               #
#            http://teaching.dessalles.fr/CANLP                   #
###################################################################

import re
import asp_Grammar
from syn_util import trace, Tree_, stop


class asp_parser(asp_Grammar.Grammar):
	"""	Syntax-driven processing, based on basic bottom-up parser
	"""
		
	def parse(self, Sentence, Target=None, Structure=None):
		"""	bottom-up parser.
		"""
		if Target is None:	Target = ('s',)		# non-terminal to be recognized
		if type(Target) != tuple:	Target = (Target,)
		trace(f'Analyzing: {Sentence}', 3); stop(4)
		
		if Structure is None:	
			Structure = tuple(map(lambda x: Tree_(x), Sentence))	# will become the parsing tree
		if Sentence == Target or len(Sentence) == 1:
			# ------ Sentence has been reduced to the target non-terminal
			trace('\nCorrect!', 1); trace(Structure, 3)
			for P in Structure:	
				self.ParseTrees.append(P)
				# trace(P, 3)
				P.print(level=3)	# printing parse tree
			trace(self.use(), 5)	# number of times grammar has been scanned
			stop(3)	# pause
		else:
			for splitpoint in range(len(Sentence)):
				for Rule in self:	# loops over grammar rules
					if len(Sentence) < splitpoint+len(Rule.RHS):	continue
					# ------ attempt to find rule's right-hand side (RHS) within sentence
					Chunk = Sentence[splitpoint:splitpoint+len(Rule.RHS)]
					Match = self.unifyList(Chunk, Rule.RHS)
					if Match is None:	continue
					# ------ Sentence includes Rule's right-hand side as a chunk
					if not all(map(self.lexical, Sentence[splitpoint+len(Rule.RHS):])):
						# ------ patch to avoid looping in some cases: all remaining tokens should be words
						continue
					trace(Rule, 4)
					# ------ merging the feature structures and propagating the result upwards
					if Rule.is_lexical():	
						LHSCandidates = [Rule.LHS] # lexical rule
					else:
						# ------ semantic_merge returns several possible LHSs, due to rescue operations
						LHSCandidates = self.semantic_merge(Rule.LHS, *Chunk)
					if LHSCandidates is None:
						nl = '\n\t'
						trace(f"Merging failure between:\n\t{nl.join(list(map(str,Chunk)))}", 3)
						continue
					for NewLHS in LHSCandidates:
						Sentence1 = Sentence[:splitpoint] + (NewLHS,) + Sentence[splitpoint+len(Rule.RHS):]
						Structure2 = Structure[:splitpoint]
						# ------ merging Right-hand side
						Structure2 += self.merge(NewLHS, *Structure[splitpoint:splitpoint+len(Rule.RHS)])
						Structure2 += Structure[splitpoint+len(Rule.RHS):]
						# ------ recursive call
						self.parse(Sentence1, Target=Target, Structure=Structure2)
			trace(f'no more rules for {Sentence}', 5)

if __name__ == "__main__":
	print(__doc__)
	TraceLevel = 2
	trace(level=TraceLevel, set=True)
	grammar = asp_parser()
	grammar.loadDCG('asp_Grammar.pl')
	# grammar.loadLexicon('asp_Lexique.pl')
	grammar.loadLexicon('asp_Lexicon.pl')
	trace(grammar, 3)
	# grammar.process('a dog', Target='np')
	# grammar.process('the dog barks')
	# grammar.process('the dog of the sister likes the sister of the cousin')
	while True:
		grammar.reinit()
		try:	
			grammar.process()	# will prompt for new sentence
			# for P in grammar.ParseTrees:	P.print()
			print(f'\n{len(grammar.ParseTrees)} interpretations found')
		except StopIteration: break


		
__author__ = 'Dessalles'



