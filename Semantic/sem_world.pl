/*---------------------------------------------------------------*/
/* Telecom Paris - J-L. Dessalles 2022                           */
/* Cognitive Approach to Natural Language Processing             */
/*            http://teaching.dessalles.fr/CANLP                 */
/*---------------------------------------------------------------*/


:- consult('sem_Chess.pl').

girl('Ann').
boy('John').
nice('Ann').
child('John').
child('Pat').
room('my_room').
daughter('Lisa', 'Ann').

dream(_, _) :- writeln('\n***** Continue to dream! *****\n').

% If X is a girl, then it is 'animate'
animate(X) :- girl(X).
animate(X) :- boy(X).

% Add contraints on the execution of talk: X and Y should both be animate
talk(X,Y,_Z) :- animate(X), animate(Y).

