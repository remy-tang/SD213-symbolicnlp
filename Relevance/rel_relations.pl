
	% :- consult('facts.pl').

	% Get contradiction from database
	missing_spouse(X,Y) :-
		parent(X, Z),
		children(X, Z),
		children(Y, Z),
		X \= Y,
		not(spouse(X, Y)),
		not(spouse(Y, X)).

	multiple_spouses(X,Y) :-
		spouse(X, Z),
		spouse(Y, Z),
		X \= Y,
		X \= Z,
		Y \= Z.
	
	% initial facts
    initial_situation(parent(donald_trump, X)).
    initial_situation(children(marc, jean)).

	% actions
    action(add_missing_spouse(_Parent1, _Parent2)).
    action(set_remarried_spouse(_Parent1, _Parent2)).

	% default predicates: these predicates are true unless proven false
	% defaults values represent the strength, or typicality, of the default
	%default(-on(_Object,_Place), 30).
    default(-polygamous(_Person), 30). % a person cannot have multiple spouses by default
	
	% logical clauses
	% incompatible([physical(image)]).
	
	% actions
	-missing_spouse(_Parent1, _Parent2) <--- action(add_missing_spouse(_Parent1, _Parent2)).
	remarried_spouse(_Parent1, _Parent2) <--- action(set_remarried_spouse(_Parent1, _Parent2)).

	% prerequisites
	add_missing_spouse(_Parent1, _Parent2) <=== missing_spouse(_Parent1, _Parent2).
	missing_spouse(_Parent1, _Parent2) <=== children(_Child, _Parent1) + children(_Child, _Parent2) + -spouse(_Parent1, _Parent2).

	set_remarried_spouse(_Parent1, _Parent2) <=== spouse(_Parent1, _Parent2).

	
	% physical laws
	-nice_database <=== missing_spouse(_Parent1, _Parent2).
	


	% preferences (termes positifs seulement)
	preference(nice_database, 40).
	preference(-missing_spouse(_Parent1, _Parent2), 20).

	