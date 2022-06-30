/*---------------------------------------------------------------*/
/* Telecom Paris - J-L. Dessalles 2022                           */
/* Cognitive Approach to Natural Language Processing             */
/*            http://teaching.dessalles.fr/CANLP                 */
/*---------------------------------------------------------------*/


	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	% minimal implementation of aspect processing  %
	% Main file                                    %
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


:- assert(language(english)).
% :- assert(language(french)).
	
:- consult('asp_Util.pl').	% contains:  get_line str2wlist setTraceLevel wt

:-	(language(french), consult('asp_Lexique.pl'), consult('asp_Phrases.pl'), !); 
	(language(english), consult('asp_Lexicon.pl'), consult('asp_Sentences.pl')).

% get_rules converts DCG clauses into 'rule(Cat, RHS, HeadPosition)' 
% where RHS is a list representing the right-hand side of the clause.
% HeadPosition indicates whether the head of the rule (e.g. v in an vp phrase) comes first or second.
:- get_rules('asp_Grammar.pl').	% performs the conversion by asserting rule(vp, [v, dp], 1).

:- consult('asp_Merge.pl').	% semantic merge

:- setTraceLevel(3).	% controls the detail of tracing comments



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Syntax-driven processing, based on basic bottom-up parser
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

parse(PhraseType, [Phrase], FS) :-
	% success when one gets PhraseType after a sequence of transformations
	Phrase =.. [PhraseType, FS],
		wt(1, 'The sentence is correct'),
		wtln(3, [Phrase]), stop(3).
parse(PhraseType, Phrases, FS):-
		wtln(4, Phrases), stop(5),
	append(Pref, Rest, Phrases),   % P is split into three pieces 
	append(RHS, Suff, Rest), % P = Pref + RHS + Suff
	lexical_only(Suff),	% patch to avoid looping in some cases
	process_phrase(Head, RHS),	% bottom up parsing using rule: Head --> RHS. (RHS = right-hand side)
	append(Pref, [Head|Suff], NEWPhrases),  % RHS is replaced by X in P:  NEWP = Pref + X + Suff
	parse(PhraseType, NEWPhrases, FS).  % lateral recursive call

% finding a rule that matches the sentence portion 
process_phrase(Head, [Word]) :-
	lexicon(Word, Cat, FS),		% found Word in lexicon
	Head =.. [Cat, FS].		% lexicon('water', n, [vwp:g, im:water]) becomes n([vwp:g, im:water])
process_phrase(Head, RHS) :-	
	% looking for RHS as right-hand side of a rule.
	rule(Cat, LCat, HeadPosition),	% Cat --> elements of LCat.
	cats(RHS, LCat), 	% keeps only syntactic categories in RHS
	% Cat has been recognized
		% writeln((Cat, LCat, RHS)),
	merge(RHS, HeadPosition, FS1),
	rescue(Cat, FS1, FS),
	Head =.. [Cat, FS].

% checks that a list is made of words (atoms)
lexical_only([]).
lexical_only([W|WL]) :-
	atomic(W),
	lexical_only(WL).

% keeps only syntactic categories (functor names in a list of functors) 
% [d([blah, blah]), n([blah blah])] ---> [d,n]
cats([], []).
cats([X|XL], [XCat|XLCat]) :-
	X =.. [XCat|_],
	cats(XL, XLCat).
	
merge([H, C], 1, FS) :-
	matchPhrases(H, C, FS).
merge([C, H], 2, FS) :-
	matchPhrases(H, C, FS).
merge([H], _, FS) :-
	H =.. [_, FS].

matchPhrases(Head, Compl, FS) :-
	Head =.. [_, HeadFS],
	Compl =.. [_, ComplFS],
	matchFS(HeadFS, ComplFS, FS).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% various ways of running the programme
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

go :-
	go(2).

go(TraceLevel) :-
	setTraceLevel(TraceLevel),
	test1(FS),
	nl, write('== Ok. '), writeFS(0, FS), !,
	go(TraceLevel).
go(_) :-
	write('Ok').

test1(FS) :-
	nl, nl, write('Sentence --->  '),
	get_line(Sentence),
	parse(s, Sentence, FS).

test :-	% similar to 'go', but gives all solutions
	nl, nl, write('Sentence --->  '),
	get_line(Sentence),
	findall(FS, (parse(s, Sentence, FS), nl, write('== Ok. '), writeFS(0, FS), nl), _FSL).
	%member(FSi, FSL),
	%nl, write('== Ok. '), writeFS(0, FSi),
	%fail.
%test.


test(PhraseType) :-		% to test phrases instead of complete sentences
	nl, writef('Phrase of type %q --->  ', [PhraseType]),
	get_line(Phrase),
	parse(PhraseType, Phrase, FS),
	nl, write('== Ok. '), writeFS(0, FS).




tests :-
	% runs a series of tests on examples taken from a file
	example(_Correct, ExStr, _Comment),
	% writef('\n\n>>>>>>>  %d - %s - %d', [Correct, ExStr, Comment]), nl,
	% format('\n\n>>>>>>>  ~k - ~s - ~k', [Correct, ExStr, Comment]), nl,
	format('\n\n>>>>>>>  ~s', [ExStr]), nl,
	str2wlist(ExStr, Example),
	setof(SFS, (parse(s, Example, FS1), swriteFS(SFS, FS1)), FSl),
	member(FStr, FSl),
	%writef('\nCorrect! - %s - %q', [ ExStr, Comment]),
	nl, wt(0, '===> '),
	wt(0, FStr), nl,
	not(stop(2)),
	!.
tests.

tests0 :-
	setTraceLevel(0),
	tests,
	setTraceLevel(2).

tests00 :-
	tell('Trace0.txt'),
	tests0,
	told,
	write('File "Trace0.txt" created'), nl.

