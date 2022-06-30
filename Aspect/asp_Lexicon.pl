/*---------------------------------------------------------------*/
/* Telecom Paris - J-L. Dessalles 2022                           */
/* Cognitive Approach to Natural Language Processing             */
/*            http://teaching.dessalles.fr/CANLP                 */
/*---------------------------------------------------------------*/




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Lexicon
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% lexical entries : lexicon(<word>, <syntactic and semantic feature structure>)
% Feature structures are non-exhaustive lists: [ Feature1:Value1, Feature2:Value2]

lexicon(in, p, [vwp:f]).
% lexicon(in, p, [op:sep, im:this-time_after]).	% ne fonctionne pas
lexicon(during, p, [vwp:g]).
lexicon('at', p, []).
lexicon('after', p, [op:sep]).

lexicon(', ', sep, []).

lexicon('Mary', dp, [im:'Mary']).
lexicon('Peter', dp, [im:'Peter']).
lexicon('she', dp, [im:she]).
lexicon('he', dp, [im:he]).
lexicon(cafeteria, n, [im:cafeteria]).
lexicon('cake', n, [im:cake]).
lexicon('water', dp, [vwp:g, im:water]).
lexicon('glass_of_wine', n, [vwp:f, im:glass_of_wine]).
lexicon('car', n, [im:car]).
lexicon('wine', n, [im:wine]).

lexicon(year, n, [det:u, im:year, dur:7.5]).
lexicon(hour, n, [det:u, im:hour, dur:3.6]).
lexicon(minute, n, [det:u, im:minute, dur:1.8]).
lexicon(minutes, n, [det:u, im:minute, dur:2]).
lexicon(second, n, [det:u, im:second, dur:0]).
% lexicon(hour, n, [vwp:f, det:d, im:hour_from_now, dur:3.6]).
% lexicon(minute, n, [vwp:f, det:d, im:minute_from_now, dur:1.8]).
% lexicon(minutes, n, [vwp:f, det:d, im:minute_from_now, dur:2]).
% lexicon(second, n, [vwp:f, det:d, im:second_from_now, dur:0]).
lexicon(show, n, [det:d, im:show, dur:3.8]).
lexicon(2028, dp, [det:d, im:'2028', dur:7.5]).
lexicon(2010, dp, [det:d, im:'2010', dur:7.5]).

lexicon(like, v, [vwp:g, im:like]).

lexicon(eat, vp, [vwp:f, im:eat_meal, dur:3.5]).
lexicon(eat, v, [vwp:f, im:ingest, dur:1.4]).
lexicon(eat, v, [vwp:g, im:eat_from, dur:1]).
lexicon(drink, v, [vwp:f, im:ingest, dur:0.9]).
lexicon(drink, v, [vwp:g, im:drink_some, dur:0.9]).
lexicon(draw, v, [vwp:f, im:draw_circle, dur:0.7]).
lexicon(draw, vp, [vwp:g, im:drawing, dur:7.5]).

lexicon(snore, vp, [vwp:g, im:snore, dur:1]).
lexicon(drive, vp, [vwp:g, im:drive, dur:2.6]).

lexicon('_PP', t, [op:sep, vwp:f, det:d, im:past]).
lexicon('_PRET', t, [op:sep, vwp:_, det:d, im:past]).
lexicon('_PRES', t, [vwp:g]).
lexicon('_FUT', t, [op:sep, vwp:f, det:d, im:future]).
lexicon('will', t, [op:sep, vwp:f, det:d, im:future]).

lexicon(a, d, [vwp:f, det:_, im:'1', occ:_]).	% quantity
lexicon(one, d, [vwp:f, im:'1', occ:_]).	% quantity
lexicon(ten, d, [vwp:f, im:'10', occ:_]).
lexicon(the, d, [vwp:f, im:this, occ:sing]).
lexicon(this, d, [vwp:f, im:this, occ:sing]).
% lexicon(this, Cat, FS) :- lexicon(the, Cat, FS).
lexicon(some, d, [vwp:g, det:_]).	 


	
rephrase(future, 'in the future') :- !.
rephrase(past, 'in the past') :- !.
rephrase(sliced, 'at some moment in') :- !.
rephrase(repeat, repeated) :- !.
rephrase(separate, separated) :- !.
rephrase(pred_, '') :- !.
rephrase(X, X).
