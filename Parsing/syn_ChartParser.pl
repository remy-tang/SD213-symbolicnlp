/*---------------------------------------------------------------*/
/* Telecom Paris - J-L. Dessalles 2022                           */
/* Cognitive Approach to Natural Language Processing             */
/*            http://teaching.dessalles.fr/CANLP                 */
/*---------------------------------------------------------------*/



:- consult('syn_util.pl').	% input / output facilities
:- dynamic(rule/2).	% 'rule' can be asserted and retracted
:- dynamic(edge/7).	% 'edge' can be asserted and retracted

tracing :-
			% fail,	% comment to print messages
			true.

/*	'ask' loads the grammar, then asks for a sentence and calls 'parse' */
ask(GramFile) :-
	% 'get_rules' converts DCG clauses into 'rule(Cat, RHS)' where RHS is a list representing the right-hand side of the clause.
	get_rules(GramFile),	% note:  allows for hot changes in grammar
	nl, prompt1('Sentence to parse: '), get_line(L),	% returns a list of words
	L \== [''],
	parse(L), 
	!,
	ask(GramFile).
ask(_).

go :-
	ask('syn_Grammar.pl').
	
	
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Chart parser
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

/*
	edge(StartPos, EndPos, Cat, Done, Rest, T, Comment)
	This indicates that a candidate phrase of type 'Cat' may start from 'StartPos'
		StartPos:	Position in input of the first word of the candidate phrase
		EndPos:	Position in input of the last recognized word for the candidate phrase
		Cat:			left hand side of the candidate rule
		Done:		list of categories in the right-hand side of the candidate rule that have been recognized
		Rest:		list of categories in the right-hand side of the candidate rule that are not yet recognized
		T:				tree for display
		Comment: comment for trace
*/
parse(L) :-
	retractall(edge(_, _, _, _, _, _, _)),
	add_lexical_edges(L, 1, N),	% creates lexical edges - instantiates N as the length of L
	nl, write('Parsed sentence: '), writel(L),
	edge(1, N, s, _, [], T, _),	% total inactive edge - sentence fully recognized
	display_tree(T),
	write('The sentence is correct.'), nl,
	fail. 	% to force backtracking and find out futher interpretations if any
parse(_).


/* ------------------------
add_lexical_edges gathers all categories that match words in the input sentence
and creates lexical edges such as edge(1, 2, det, [the], [], det(the), 'Lexical')
   -------------------------*/
add_lexical_edges([], EndPos, EndPos).	% instantiates sentence length
add_lexical_edges([W|_], StartPos, _) :-	
	rule(Cat, [W]),	% gets a lexical rule that matches W. 
	Cat =.. [C|_],	% keeping only category name for tree
	T =.. [C, W],	% tree
	StartPos1 is StartPos + 1,
	add_edge(StartPos, StartPos1, Cat, [W], [], T, 'Lexical'),
	fail.	% forces backtracking
add_lexical_edges([_|WL], StartPos, EndPos) :-	
	StartPos1 is StartPos + 1,
	add_lexical_edges(WL, StartPos1, EndPos).


add_edge(StartPos, EndPos, Cat, Done, Rest, T, _) :-
	edge(StartPos, EndPos, Cat, Done, Rest, T, _),	% edge already exists !
	!.
add_edge(StartPos, EndPos, Cat, Done, Rest, T, Comment) :-
	assert(edge(StartPos, EndPos, Cat, Done, Rest, T, Comment)),
	trace_edge(StartPos, EndPos, Cat, Done, Rest, T, Comment), 
	fail.	% forces backtracking - Note that assert is not canceled when  backtracking 
add_edge(StartPos, _, Cat, _, [], _, _) :-	% Generation
	% about to add an inactive edge
	% Generating active edges starting from Cat
	rule(Cat1, [Cat|Rest]),
	T = Cat1,		% processing tree
	% ADD APPROPRIATE EDGE HERE using 'add_edge' recursively 
	add_edge(StartPos, StartPos, Cat1, [], [Cat|Rest], T, 'Generated'),
	fail.	% forces backtracking
add_edge(StartPos, EndPos, Cat, _, [], T, _) :-	% extension
	% about to add an inactive edge
	% Extending active edges
	edge(StartPos1, StartPos,Cat1, Done, [Cat|Rest], T1,_),
	append(Done, [Cat], Done1),
	% . . .
	T1 =.. [H|L],		% processing tree
	append(L, [T], L1),
	T2 =.. [H|L1],	% new tree for the edge about to be added
	% ADD APPROPRIATE EDGE HERE using 'add_edge' recursively - you may also call 'trace_edge'
	add_edge(StartPos1, EndPos, Cat1, Done1, Rest, T2, 'Extension'),
	fail.	% forces backtracking
% Here we need yet another 'add_edge' clause to extend the inactive edge we are adding
% using an existing edge (and, by doing so, leveraging memory to speed up parsing)
add_edge(StartPos1, StartPos,Cat1, Done, [Cat|Rest], T1,_) :-	% extension
	% about to add an inactive edge
	% Extending active edges
	edge(StartPos, EndPos, Cat, _, [], T, _),
	append(Done, [Cat], Done1),
	% . . .
	T1 =.. [H|L],		% processing tree
	append(L, [T], L1),
	T2 =.. [H|L1],	% new tree for the edge about to be added
	add_edge(StartPos1, EndPos, Cat1, Done1, Rest, T2, 'Extension'),
	fail.	% forces backtracking
add_edge(_, _, _, _, _, _).	% catch-up clause: always succeeds


trace_edge(StartPos, EndPos, Cat, Done, Rest, T, Comment) :-
	tracing, !,
	write('Adding edge:\t'), write(':\t'), write(StartPos), write('->'), write(EndPos),
	write('\t\t'), write(Cat), write(' --> '), writel(Done), write(' . '),
	writel(Rest), write('\t'), write(T), write('\t'), write(Comment), nl,
	true.
trace_edge(_, _, _, _, _, _, _).

