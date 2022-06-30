/*---------------------------------------------------------------*/
/* Telecom Paris - J-L. Dessalles 2022                           */
/* Cognitive Approach to Natural Language Processing             */
/*            http://teaching.dessalles.fr/CANLP                 */
/*---------------------------------------------------------------*/


% example(Correctness, Sentence, Comment...).


example(_, "Mary will drink the glass_of_wine", _).
example(_, "Mary will drink the glass_of_wine in ten second", _).
example(_, "Mary will drink the glass_of_wine in 2028", _).
example(_, "Mary will drink the glass_of_wine during one minute", _).
example(_, "Mary will drink the glass_of_wine during the show", _).
example(_, "Mary will drink water", _).
example(_, "Mary will drink water in one minute", _).
example(_, "Mary will drink water in 2028", _).
example(_, "Mary will drink water during one minute", _).
example(_, "Mary will drink water during the show", _).
example(_, "Mary will eat", _).
example(_, "Mary will eat in one minute", _).
example(_, "Mary will eat in one hour", _).
example(_, "Mary will eat in 2028", _).
example(_, "Mary will eat during 2028", _).
example(_, "Mary will eat during one hour", _).
example(_, "Mary will eat during one year", _).
example(_, "Mary will eat during the show", _).
example(_, "Mary _PRET snore", _).
example(_, "Mary _PRET snore in one minute", _).
example(_, "Mary _PRET snore in 2010", _).
example(_, "Mary _PRET snore during one minute", _).
example(_, "Mary _PRET snore during the show", _).
example(_, "Mary _PRET like the wine", _).
example(_, "Mary _PRET like the wine in 2010", _).
