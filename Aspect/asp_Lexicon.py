#!/usr/bin/env python3
###################################################################
# Telecom Paris - J-L. Dessalles 2022                             #
# Cognitive Approach to Natural Language Processing               #
#            http://teaching.dessalles.fr/CANLP                   #
###################################################################

" Reads Prolog lexixon file "

import re
from syn_util import trace

Correction___ = 0

class Feature:
	"""	Defines an aspectual feature
	"""
	def __init__(self, feature, value):
		self.name = feature
		if self.name == 'dur' and value != '_': 
				self.value = Duration(value)
		else:	self.value = value

	def val(self, newval=None):	
		if newval is not None:
			self.value = newval
		return self.value
		
	def type_(self):
		if self.name == 'dur':
			if self.value == '_':	return D.Unspecified
			else:	return self.value.type_
		raise ValueError
	
	def merge(self, other):
		if (self.name != other.name):	
			raise Exception(f'Error: comparing two different features: {self.name} and {other.name}')
		if self.value == '_':	return other
		if other.value == '_':	return self
		if self.name in ['vwp', 'det', 'occ']:
			if self.value == other.value:	return self
			return None
		if self.name == 'dur':
			durationCompatibility = self.value.compare(other.value)
			if durationCompatibility is not None:
				return Feature(self.name, durationCompatibility)
			else:	return None
		if self.name == 'im':
			return Feature(self.name, f"{self.value}_{other.value}")
		return self
	
	def __str__(self):	return f"{self.name}:{self.value}"
	# def __repr__(self):	return f"{self.name}:{self.value}"
	__repr__ = __str__
	
class FeatureStructure(dict):
	"""	Defines an aspectual feature structure
	"""
	def __init__(self, FeatureStringOrFS=''):
		"""	Creates a feature structure with aspectual features
		"""
		dict.__init__(self)
		if type(FeatureStringOrFS) == str:
			for F in ['vwp', 'det', 'occ', 'op', 'im', 'dur']:	self[F] = Feature(F, '_')
			if FeatureStringOrFS.strip() != '':
				for Fstring in FeatureStringOrFS.split(','):
					F, V = Fstring.strip().split(':')
					if V != '_':	self[F] = Feature(F, V)
		else:	# receiving a ready-to-use feature structure
			self.update(FeatureStringOrFS)

	def val(self, slot, Val=None, **args):
		if Val is not None:
			if slot == 'dur':
				if Val != '_':
					self[slot] = Feature('dur', Duration(Val.duration, **args))
				else:	self[slot] = Feature('dur', '_')
			else:	self[slot] = Feature(slot, Val)
		return self[slot]
		
	def merge(self, other):
		"""	Attempt to merge with another feature structure
		"""
		trace(f'merging {self} and {other}', 6)
		Merge = {F:self[F].merge(other[F]) for F in self}
		if None in Merge.values():	
			trace(f"{self} and {other} cannot be unified", 5)
			return None
		return FeatureStructure(Merge)
	
	def __str__(self):	return f"({', '.join([str(self[F]) for F in self if self[F].value != '_'])})"
	# def __repr__(self):	return f"({','.join([str(F) for F in self if self[F].value != '_'])})"
	
	# __repr__ = __str__
	
	
class WordEntry(FeatureStructure):
	"""	Word, and its associated feature structure
	"""
	def __init__(self, Word, SyntacticCat, FeatureStringStructure=''):
		self.word = Word
		self.cat = SyntacticCat
		super().__init__(FeatureStringStructure)
	
	def semantic_merge(self, Cat, Word=None):
		"""	Merging self with Word into Cat
		"""
		# ------ should return various merging solutions
		if Word is None:
			# ------ copying self's feature structure into Cat
			# return [WordEntry(Cat, Cat, self)]
			MergeStructure = FeatureStructure(self)
		else:	
			MergeStructure = self.merge(Word)
		if MergeStructure is not None:
			# return WordEntry(Cat, Cat, MergeStructure)
			return self.rescue(Cat, MergeStructure)	# rescue loops over all rescue possibilities
		return None
	
	def rescue(self, Cat, MergeStructure):
		def idendity(x, y):	return [y]
		trace(f'Rescuing attempt on {Cat}:{MergeStructure}', 4)
		# vvvvvvvv  To be changed vvvvvvvv
		# You should add operators to the list of rescue operations
		Operations = [idendity, self.zoom, self.repeat]
		# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
		for RescueOperation in Operations:
			Rescue = RescueOperation(Cat, MergeStructure)
			if Rescue is not None:
				for rescuedMS in Rescue:
					if rescuedMS is not None:
						if RescueOperation != idendity:
							trace(f'yielding rescued {Cat} though {RescueOperation.__name__}: {rescuedMS}', 3)
						yield WordEntry(Cat, Cat, rescuedMS)
	
	def zoom(self, Cat, FS):
		"""	Attempt to zoom event described by feature structure FS
		"""
		if Cat != 'dp':	return None	# zoom only dp (named events)
		if FS.val('occ').value == 'mult':	
			return None	# don't zoom repeated events
		if FS.val('vwp').value != 'f':
			return None	# only zoom figures 
		try:
			if FS['dur'].type_() != D.Normal:
				return None 			# zoom only into extented periods
		except AttributeError:
			print(Cat, FS)
			raise AttributeError
		NewFS = FeatureStructure(FS)
		NewFS.val('im', f"{FS['im'].value}_zoomed")
		NewFS.val('vwp', 'g')
		return [NewFS]
		
	def slice(self, Cat, FS):
		"""	Attempt to slice event described by feature structure FS
		"""
		if Cat != 'pp':	return None	# slice only pp (temporal complements)
		if FS.val('det').value != 'd':	
			return None	# slice only determined periods
		if FS['dur'].type_() != D.Normal:
			return None 			# slice only extented periods
		NewFS = FeatureStructure(FS)
		NewFS.val('im', f"{FS['im'].value}_sliced")
		NewFS.val('vwp', 'f')
		NewFS.val('occ', '_')	# erasing occurrence
		NewFS.val('dur', FS['dur'].value, type_=D.Max)
		return [NewFS]
		
	def repeat(self, Cat, FS):
		"""	Attempt to repeat event described by feature structure FS
		"""
		if Cat != 'vpt':	return None	# repeat only actions
		if FS['occ'].value == 'mult':	
			return None	# don't zoom repeated events
		if FS.val('vwp').value != 'f':	
			return None	# only zoom figures 
		NewFS = FeatureStructure(FS)
		NewFS.val('im', f"{FS['im'].value}_repeat")
		NewFS.val('vwp', 'g')
		NewFS.val('occ', 'mult')
		NewFS.val('dur', FS['dur'].value, type_=D.Min)
		return self.rescue(Cat, NewFS)		# looping on rescuing vpt
		
	def predication(self, Cat, FS):
		"""	Attempt to predicate on event described by feature structure FS
		"""
		if Cat != 'vpt':	return None	# repeat only actions
		if FS.val('dur').type_() == D.Nil:
			return None 			# don't stack up predication
		NewFS = FeatureStructure(FS)
		NewFS.val('im', f"{FS['im'].value}!")
		NewFS.val('vwp', 'f')
		NewFS.val('det', 'd')
		NewFS.val('dur', FS['dur'].value, type_=D.Nil)
		return self.rescue(Cat, NewFS)	# looping on rescuing vpt
		
	
	def __str__(self): return f'{self.word}({self.cat}): {FeatureStructure.__str__(self)}'
	
	def __repr__(self): return f'{self.word}({self.cat})'

class Lexicon:
	"""	Retrives lexion from a Prolog file
	"""
	def __init__(self, PrologLexiconFile):
		self.Words = []
		self.loadLexicon(PrologLexiconFile)
		
	def loadLexicon(self,PrologLexiconFile):
		LexiconTxt = open(PrologLexiconFile).read()
		Entries = re.findall(r"^lexicon\('?([^,]+?)'?,\s*(\w+),\s*\[(.*?)\]\)", LexiconTxt, flags=re.M)
		if Entries is not None:
			for E in Entries:
				self.Words.append(WordEntry(*E))
		trace(self, 4); trace(f'{len(self)} words found in {PrologLexiconFile}\n', 1)

	def __iter__(self):	return iter(self.Words)
	
	def __getitem__(self, word):
		"""	returns possibly several entries for one given word
		"""
		# print([wordEntry for wordEntry in self.Words if wordEntry.word.lower() == word.lower()])
		return [wordEntry for wordEntry in self.Words if wordEntry.word.lower() == word.lower()]
		
	def __len__(self): 	return len(self.Words)

	def __str__(self): return '\n'.join(map(str, self.Words))


class D:
	Unspecified, Nil, Normal, Min, Max  = 0, 1, 2, 3, 4
	type_s = ['_', 'Nil', 'Normal', 'Min', 'Max']
	@classmethod
	def type_(self, T):	return D.type_s[T]
	
class Duration:
	"""	defines duration in log10(seconds)
	"""
	def __init__(self, duration, type_=None):
			try:	
				self.duration = float(duration)
				self.type_ = type_ if type_ is not None else D.Normal
			except (TypeError, ValueError):	
				# input is str or already Duration
				if type(duration) == str:
					self.duration = duration
					self.type_ = D.Unspecified
				else:
					self.duration = duration.duration
					self.type_ = duration.type_
				if type_ is not None: self.type_ = type_
			# if type_ is not None: print('>>>>', self)

	def compare(self, other):
		"""	Comparison of durations based on their order of magnitude
		"""
		if self.type_ == D.Max and other.type_ == D.Nil:
			if self.convert() >= other.convert():
				return self
			return None
		if self.type_ == D.Nil and other.type_ == D.Max:
			return other.compare(self)
		if self.type_ == D.Normal and other.type_ == D.Normal:
			if abs(self.duration - other.duration) < 1:  
				return self
			return None
		return Duration(self.convert()).compare(Duration(other.convert()))
		
	def convert(self):
		"""	effect of repetition or slice on duration
		"""
		d = self.duration if type(self.duration) == float else self.duration.convert()
		if self.type_ == D.Nil:	return d
		if self.type_ == D.Min:	return d + 2.5
		if self.type_ == D.Max:	return d - 1
		return self.duration
		
	def __str__(self):	
		if self.type_ != D.Normal:	return f"{D.type_(self.type_)}({self.duration})"
		return str(self.duration)

if __name__ == "__main__":
	print(__doc__)
	# print(Lexicon('asp_lexicon.pl'))
	# print(Lexicon('asp_lexicon.pl'))
	print(Lexicon('asp_lexique.pl'))


__author__ = 'Dessalles'

