/*---------------------------------------------------------------*/
/* Telecom Paris - J-L. Dessalles 2022                           */
/* Cognitive Approach to Natural Language Processing             */
/*            http://teaching.dessalles.fr/CANLP                 */
/*---------------------------------------------------------------*/


% Coding chess piece locations for a famous chess play
% https://i.ytimg.com/vi/dhSY_ChdGvI/hqdefault.jpg
% https://www.youtube.com/watch?v=dhSY_ChdGvI

loc(black, bishop, (1, 8)).
loc(black, rook, (4, 8)).
loc(black, rook, (8, 8)).
loc(black, king, (1, 8)).
loc(black, queen, (5, 7)).
loc(black, pawn, (6, 7)).
loc(black, pawn, (8, 7)).
loc(black, pawn, (1, 6)).
loc(black, knight, (2, 6)).
loc(black, knight, (6, 6)).
loc(black, pawn, (7, 6)).
loc(black, pawn, (2, 5)).
loc(black, pawn, (3, 5)).
loc(black, pawn, (4, 4)).

loc(white, knight, (1, 5)).
loc(white, knight, (4, 5)).
loc(white, pawn, (5, 4)).
loc(white, queen, (6, 4)).
loc(white, pawn, (1, 3)).
loc(white, pawn, (6, 3)).
loc(white, pawn, (7, 3)).
loc(white, bishop, (8, 3)).
loc(white, pawn, (2, 2)).
loc(white, pawn, (3, 2)).
loc(white, pawn, (8, 2)).
loc(white, king, (2, 1)).
loc(white, rook, (4, 1)).
loc(white, rook, (5, 1)).

% Meanings
% Creating predicates for actual pieces by asserting predicates such as knight(white, (1,5))
:- findall(_, (loc(Color, Piece, Loc), P =.. [Piece, Color, Loc], assert(P)), _).

black(black).	
white(white).


% coding relations
left((HP1, VP), (HP0, VP)) :-			% HP1 is to the left of HP0
	nonvar(HP0),
	HP1 is HP0 - 1.
left(Loc, Piece0) :-	% metonymic use: replacing Piece0 by its location
	nonvar(Piece0),
	Piece0 =.. [_, _, Loc0],
	left(Loc, Loc0).

right((HP1, VP), (HP0, VP)) :-			% HP1 is to the right of HP0
	nonvar(HP0),	%%%%%% Change this
	HP1 is HP0 +1.	
right(Loc, Piece0) :-	% metonymic use: replacing Piece0 by its location
	nonvar(Piece0),
	Piece0 =.. [_, _, Loc0],
	right(Loc, Loc0). 	

        