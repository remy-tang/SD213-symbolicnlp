


% ================== MANUAL CHECK OF VALIDITY ================% 

% To check manually the correctness of the error detection

% % Missing spouse relation
% missing_spouse(X,Y) :-
% 	(parent(Z,X),children(Y,Z);
% 	parent(Z,Y),children(X,Z);
% 	parent(Z,X),parent(Z,Y)),
% 	X\=Y,
% 	not(spouse(X,Y);spouse(Y,X)).

% % Missing parent relation
% missing_parent(X,Y) :-
% 	children(Y,X),
% 	not(parent(X,Y)).

% % Missing children relation
% missing_children(X,Y) :-
% 	parent(X,Y),
% 	not(children(X,Y)).

% % Get the number of spouses of X
% num_spouses(X,Y) :-
% 	setof(Z, (spouse(Z,X); spouse(X,Z)), L),
% 	length(L, Y).

% ========================= CAN STARTS HERE ============================%

% Manually initialize facts to get the initial situation
% initial_situation(parent(donald_trump,mary_anne_macleod_trump)).
% initial_situation(parent(donald_trump,fred_trump)).
% initial_situation(children(fred_trump,donald_trump)).
% initial_situation(spouse(marla_maples,donald_trump)).
% initial_situation(spouse(melania_trump,donald_trump)).

% Sample of the knowledge base
parent(donald_trump,mary_anne_macleod_trump).
parent(donald_trump,fred_trump).
parent(barron_trump,melania_trump).
parent(barron_trump,donald_trump).
children(fred_trump,donald_trump).
spouse(marla_maples,donald_trump).
spouse(melania_trump,donald_trump).


init :-
	assert_init(_),
	two_spouses(_),
	missing_spouse(_,_),
	missing_children(_,_).
	
% Take the knowledge base and turn it into initial situation
assert_init(X) :-
	% consult('facts.pl'),
	assert_spouse(X),
	assert_parent(X),
	assert_children(X).

% Build the initial situation the predicates
assert_spouse(X):-
	spouse(X,Y),
	assert(initial_situation(spouse_(X,Y))).
assert_spouse(X):-
	spouse(Y,X),
	assert(initial_situation(spouse_(Y,X))).
assert_spouse(_) :-
	true. % continuer sans assertion
assert_parent(X):-
	parent(X,Y),
	assert(initial_situation(parent_(X,Y))).
assert_parent(X):-
	parent(Y,X),
	assert(initial_situation(parent_(Y,X))).
assert_parent(_) :-
	true. % continuer sans assertion
assert_children(X):-
	children(Y,X),
	assert(initial_situation(children_(Y,X))).
assert_children(X):-
	children(X,Y),
	assert(initial_situation(children_(X,Y))).
assert_children(_) :-
	true. % continuer sans assertion

% Define actions
action(add_missing_spouse(_Parent1, _Parent2)).
action(set_remarried(_Parent1)).
action(add_missing_children(_Parent,_Child)).

% % default predicates: these predicates are true unless proven false
% % defaults values represent the strength, or typicality, of the default
% default(-polygamous(_Person), 30). % a person cannot have multiple spouses by default

% logical clauses
% incompatible([physical(image)]).

% Define action consequences
-spouse_(Parent1,Parent2) <--- action(set_remarried(Parent1,Parent2)).
spouse_(Parent1,Parent2) <--- action(add_missing_spouse(Parent1, Parent2)).
children_(Parent, Child) <--- action(add_missing_children(Parent,Child)).

% Action prerequisites
set_remarried(Parent1,Parent3) <=== two_spouses(Parent1,_,Parent3).
add_missing_spouse(Parent1, Parent2) <=== missing_spouse(Parent1, Parent2).
add_missing_children(Parent, Child) <=== missing_children(Parent, Child).

% Database laws

% Check if Z has two spouses
two_spouses(Z) :-
	spouse(X,Z), % Equivalent to situation(spouse_(X,Z))
	spouse(Y,Z),
	X\=Y,
	assert(two_spouses(Z,X,Y) <=== spouse_(X,Z) + spouse_(Y,Z)),
	assert(situation(two_spouses(Z,X,Y))),
	assert(preference(two_spouses(Z,X,Y), -10)).

% Check if there should be spouse(X,Y) in the knowledge base
missing_spouse(X,Y) :-
	parent(Z,X),
	parent(Z,Y),
	X\=Y,
	not(spouse(X,Y);spouse(Y,X)),
	assert(initial_situation(-spouse_(X,Y))),
	assert(missing_spouse(X,Y) <=== parent_(Z,X) + parent_(Z,Y) + -spouse_(X,Y)),
	assert(preference(missing_spouse(X,Y), -10)).

% Check if there should be children(X,Y) in the knowledge base.
% parent(donald_trump,mary_anne_macleod_trump).

missing_children(X,Y) :-
	parent(Y,X),
	not(children(X,Y)),
	assert(initial_situation(-children_(X,Y))),
	assert(missing_children(X,Y) <=== parent_(Y,X) + -children_(X,Y)),
	assert(preference(missing_children(X,Y), -10)).

% ====================================================================
% % initial facts
% %initial_situation(on(books, desk)).

% Initiate the family situation from a person X from facts.pl
% e.g. initial_facts(donald_trump).
% initial_situation(parent()).

% initial_situation(-on(image, doors)).
% initial_situation(on(projector, shelves)).	% implies: on(image, doors)


% % actions
% action(remove(_Object,_From)).
% action(move(_Object,_To)).
% action(put_underneath(_Object1,_Object2)).
% action(tilt(_Object)).

% % default predicates: these predicates are true unless proven false
% % defaults values represent the strength, or typicality, of the default
% %default(-on(_Object,_Place), 30).
% default(horizontal(_), 30).
% default(stable(_), 30).
% default(clear(_Loc), 30).
% default(physical(_), 30).
% default(-distorted(_), 30).

% % logical clauses
% incompatible([physical(image)]).
% %incompatible([clear(L), on(_,L)]).

% % actions
% on(Object, To) <--- move(Object, To).
% -on(Object, From) <--- remove(Object, From).
% -horizontal(projector) <--- put_underneath(books,projector).
% -horizontal(P) <--- tilt(P).

% % prerequisites
% move(Object, To) <=== clear(To) + physical(Object).
% remove(Object, From) <=== on(Object, From).
% tilt(P) <=== horizontal(P).
% put_underneath(_, P) <=== horizontal(P).

% % physical laws
% -clear(desk) <=== on(books, desk).
% -stable(projector) <=== on(projector, shelves).
% on(image,door) <=== on(projector, shelves).
% on(image,door) <=== on(projector, desk).
% on(image,handle) <=== on(projector, desk) + horizontal(projector).
% distorted(image) <=== -horizontal(projector).
% -on(image,handle) <=== on(projector, shelves).

% % preferences (termes positifs seulement)
% preference(stable(projector), 40).
% preference(on(image,door), 30).
% preference(on(image,handle), -20).
% preference(distorted(image), -10).
