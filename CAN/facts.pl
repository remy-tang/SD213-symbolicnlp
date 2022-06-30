% spouse(X,Y) means X is a spouse of Y.
spouse(marla_maples,donald_trump).
spouse(melania_trump,donald_trump).

% children(X,Y) means Y is a child of X.
children(donald_trump,barron_trump).
children(mary_anne_macleod_trump,donald_trump).
children(mary_anne_macleod_trump,robert_trump).
children(marla_maples,tiffany_trump).
children(fred_trump,donald_trump).
children(fred_trump,robert_trump).
children(fred_trump,maryanne_trump_barry).
children(melania_trump,barron_trump).
children(don_cherry_trumpeter,eagle_eye_cherry).
children(donald_trump,tiffany_trump).
children(donald_trump,donald_trump_jr).
children(donald_trump,ivanka_trump).
children(donald_trump,eric_trump).

% parent(X,Y) means Y is a parent of X.
parent(eric_trump,ivana_trump).
parent(eric_trump,donald_trump).
parent(fred_trump,elizabeth_christ_trump).
parent(fred_trump,frederick_trump).
parent(eagle_eye_cherry,don_cherry_trumpeter).
parent(john_g_trump,elizabeth_christ_trump).
parent(john_g_trump,frederick_trump).
parent(donald_trump_jr,ivana_trump).
parent(donald_trump_jr,donald_trump).
parent(tiffany_trump,marla_maples).
parent(tiffany_trump,donald_trump).
parent(ivanka_trump,ivana_trump).
parent(ivanka_trump,donald_trump).
parent(donald_trump,mary_anne_macleod_trump).
parent(donald_trump,fred_trump).
parent(barron_trump,melania_trump).
parent(barron_trump,donald_trump).
parent(maryanne_trump_barry,mary_anne_macleod_trump).
parent(maryanne_trump_barry,fred_trump).
parent(robert_trump,mary_anne_macleod_trump).
parent(robert_trump,fred_trump).

grandparent(X,Y) :-
    parent(X,Z), % note that the a variables scope is the clause
    parent(Z,Y). % variable Z keeps its value within the clause

ancestor(X,Y) :-
    parent(X,Y).
ancestor(X,Y) :-
    parent(X,Z),
    ancestor(Z,Y). % recursive call
