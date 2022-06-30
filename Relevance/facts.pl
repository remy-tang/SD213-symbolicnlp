parent(marge, lisa).
parent(marge, bart).
parent(marge, maggie).
parent(homer, lisa).
parent(homer, bart).
parent(homer, maggie).
parent(abraham, homer).
parent(abraham, herb).
parent(mona, homer).
parent(jackie, marge).
parent(clancy, marge).
parent(jackie, patty).
parent(clancy, patty).
parent(jackie, selma).
parent(clancy, selma).
parent(selma, ling).

female(mona).
female(jackie).
female(marge).
female(ann).
female(patty).
female(selma).
female(ling).
female(lisa).
female(maggie).
male(abraham).
male(herb).
male(homer).
male(bart).
male(clancy).

gender(lisa, female).

female(X) :-
    gender(X, female).

children(X,Y) :-
    parent(Y,X).

mother(X,Y) :-
    parent(X,Y),
    female(X).

grandparent(X,Y) :-
    parent(X,Z), % note that the a variables scope is the clause
    parent(Z,Y). % variable Z keeps its value within the clause

sister(X,Y) :-
    parent(Z,X), % if X gets instantiated, Z gets instantiated as well
    parent(Z,Y),
    female(X),
    X \== Y. % can also be noted: not(X = Y).

ancestor(X,Y) :-
    parent(X,Y).
ancestor(X,Y) :-
    parent(X,Z),
    ancestor(Z,Y). % recursive call

aunt(X, Y) :-
    parent(Z, Y),
    sister(Z, X).