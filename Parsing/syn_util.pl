/*---------------------------------------------------------------*/
/* Telecom Paris - J-L. Dessalles 2022                           */
/* Cognitive Approach to Natural Language Processing             */
/*            http://teaching.dessalles.fr/CANLP                 */
/*---------------------------------------------------------------*/


% Reading utf-8 files
:- set_prolog_flag(encoding, utf8).


/*
help :-
	write('verifier le fichier ''regles.txt''\n'),
	prompt1('>'),
	get0(_).
*/
help :-
	write('Bye...\n'),
	%prompt1('>'),
	sleep(1).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Reading sentences from input
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


get_line(Phrase) :-
        collect_wd(String), 
        str2wlist(Phrase, String).

collect_wd([C|R]) :-
        get0(C), C \== -1, C \== 10, C \== 13, !, 
        collect_wd(R).
collect_wd([]).

str2wlist(Phrase, Str) :-
	str2wlist([], Phrase, [], Str).
	
str2wlist(Phrase, [Mot|Phrase], Motcourant, []) :-
	reverse(Motcourant, Motcourant1),
        atom_codes(Mot, Motcourant1).
str2wlist(Phrasin, [Mot|Phrasout], Motcourant, [32|Str]) :-
	!,
	reverse(Motcourant, Motcourant1),
        atom_codes(Mot, Motcourant1),
	str2wlist(Phrasin, Phrasout, [], Str).
str2wlist(Phrasin, Phrasout, Motcourant, [C|Str]) :-
	str2wlist(Phrasin, Phrasout, [C|Motcourant], Str).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Converting grammar rules into predicate form: rule(Head, RHS)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

dcg2rules(GramFile) :-
	get_rules(GramFile).

get_rules(GramFile) :-
	retractall(rule(_, _)),
	see(GramFile),
	gather,
	seen.

gather :-
	%catch(read_clause(R), _, (write('Error in rules'), nl)),
	catch(read(R), _, (write('Error in rules'), nl)),	% reads next Prolog clause from input
	%write(R),
	R =.. [-->, T|Q],
	!,
	transform(T, Q, Q1),
	assert(rule(T, Q1)),
	gather.
gather.

transform(T, [A], L) :-
	!,
	transform(T, A, L).
transform(T, (A, B), [A|B1]) :-
	!,
	transform(T, B, B1).
transform(T, (A; B), B1) :-
	!,
	assert(rule(T, A)),
	transform(T, B, B1).
transform(_, A, [A]).




%%%%%%% predicats utilitaires
writel([]).
writel([M|Ml]) :-
	write(M), write(' '),
	writel(Ml).



% "display_tree" realise l'affichage de l'arbre syntaxique
% la variable "Indent" est une chaine de caratere qui,
% affichee en debut de ligne, reproduit le dessin des
% branches en fonction de la position dans l'arbre.  

display_tree(StructPhrase) :-
	nl,
	display_tree("         ", "         ", StructPhrase),
	nl, nl.

display_tree(_, _, StructPhrase) :-
	StructPhrase =.. [LibPhrase],
	/* il s'agit d'un terminal */
	!,
	ecris([" : ", LibPhrase]).
display_tree(Indent, Prefixe, StructPhrase) :-
	%StructPhrase =.. [LibPhrase, AttrPhrase|SousStruct],
	%nl, ecris([Prefixe, LibPhrase, AttrPhrase]),
	StructPhrase =.. [LibPhrase|SousStruct],
	nl, ecris([Prefixe, LibPhrase]),
	afficheFils(Indent, SousStruct).

afficheFils(_, []).
afficheFils(Indent, [SP]) :-
	% c'est le dernier fils, on ne dessine plus
	% la branche parente                        
	!,
	string_concat(Indent, "   ", NewIndent),
	string_concat(Indent, "  |__", IndentLoc),
	display_tree(NewIndent, IndentLoc, SP).
afficheFils(Indent, [SP|SPL]) :-
	string_concat(Indent, "  |", NewIndent),
	string_concat(Indent, "  |__", IndentLoc),
	display_tree(NewIndent, IndentLoc, SP),
	afficheFils(Indent, SPL).

ecris([]).
ecris([S|Sl]) :-
	% string_to_list(S1, S),
	!,
	write(S),
	ecris(Sl).

