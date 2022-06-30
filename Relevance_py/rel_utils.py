#!/usr/bin/env python3
""" @brief 
"""

###################################################################
# Telecom Paris - J-L. Dessalles 2022                             #
# Cognitive Approach to Natural Language Processing               #
#            http://teaching.dessalles.fr/CANLP                   #
###################################################################

# A set of useful functions that didn't belong to any special class
# In this file we also set the trace level (not done in another file 
# because otherwise there would be circular imports)

import sys

def trace(Msg='', level=0, set=False):
	"""	Prints only of level <= TraceLevel
	"""
	global TraceLevel
	try:	TraceLevel
	except NameError:	TraceLevel = 0
	if type(set) != bool:	raise Exception('Trace arguments misused')
	if set:	
		# if level > 0:	print(f'setting trace level to {level}')
		TraceLevel = level
	if level <= TraceLevel:	print(Msg)

def stop(level=0):
	"""	Stops display if level <= TraceLevel
	"""
	global TraceLevel
	if level <= TraceLevel:	
		if input('.'*50 + ' [enter] or "quit"').startswith('q'):	sys.exit(1)

def ask(question):
	return input('\n' + question + '\t')



__author__ = 'Harith Proietti & jean-louis Dessalles'
