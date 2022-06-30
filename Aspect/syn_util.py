#!/usr/bin/env python3
###################################################################
# Telecom Paris - J-L. Dessalles 2022                             #
# Cognitive Approach to Natural Language Processing               #
#            http://teaching.dessalles.fr/CANLP                   #
###################################################################

" i/o tools for parsing "

import sys

def trace(Msg='', level=0, set=False):
	global TraceLevel
	try:	TraceLevel
	except NameError:	TraceLevel = 0
	if type(set) != bool:	raise Exception('Trace arguments misused')
	if set:	
		# if level > 0:	print(f'setting trace level to {level}')
		TraceLevel = level
	if level <= TraceLevel:	print(Msg)

def stop(level=0):
	global TraceLevel
	if level <= TraceLevel:	
		if input('[enter or q]').startswith('q'):	sys.exit(1)
	


# ----------------------------------------------------------------#
# printing trees
# ----------------------------------------------------------------#
class Tree_:
	def __init__(self, head, children=()):
		self.head = head
		self.children = children
		# print('creating tree', head, children)

	def newchild(self, child):
		self.children += (child,)
		
	def print(self, depth=0, level=0, spaced=True):
		global TraceLevel
		try:	TraceLevel
		except NameError:	TraceLevel = 0
		if depth == 0 and len(repr(self)) > 140:	spaced = False
		if level <= TraceLevel or depth == 0:
			if spaced or depth < 3:	print(f"{'   |' * depth}")
			print(f"{'   |' * depth}__ {self.head}")
			for child in self.children:
				# print('|', end='')
				child.print(depth+1, level=level, spaced=spaced)
		if depth == 0:	print('\n')
	
	def __eq__(self, OtherTree):
		return self.head == OtherTree.head and self.children == OtherTree.children
	
	def __repr__(self):
		return str(self.head) + (repr(self.children) if self.children else '')
		
	def __str__(self):	
		# print(self.head, self.children)
		if len(self.children) > 0:
			# return f'T__{self.head}({",".join([str(c) for c in self.children])})'
			return f'{str(self.head)}({",".join([str(c) for c in self.children])})'
		# return f'T__{self.head}'
		return str(self.head)
	
	
	
def Treelist2Tree(TreeTuple):
	if TreeTuple:
		if type(TreeTuple[0]) != tuple:
			return Tree_(TreeTuple[0]), TreeTuple[1:]
		else:
			head, arity = TreeTuple[0]
			TreeTuple = TreeTuple[1:]
			children =  []
			for ichild in range(arity):
				child, TreeTuple = Treelist2Tree(TreeTuple)
				children.append(child)
			T = Tree_(head, children)
			return T, TreeTuple

