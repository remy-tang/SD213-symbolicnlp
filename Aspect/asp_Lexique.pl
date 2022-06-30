%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% JL Dessalles -         2014 - www.dessalles.fr                                   %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% implementation minimale du modele temporel


:- encoding(utf8).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Lexicon
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% lexical entries : lexicon(<word>, <syntactic and semantic feature structure>)
% Feature structures are unterminated lists: [ Feature1:Value1, Feature2:Value2 | _ ]

lexicon(en, p, [vwp:f]).
lexicon(pendant, p, [vwp:g]).
lexicon(dans, p, [op:sep, im:after_now]).
lexicon(après, p, [op:sep]).
lexicon('à',p, _).

lexicon(',', sep, _).

lexicon('Marie', dp, [im:marie]).
lexicon('Pierre', dp, [im:pierre]).
lexicon('elle', dp, [im:elle]).
lexicon('il', dp, [im:il]).
lexicon(cantine,n, [im:cantine]).
lexicon('gâteau',n, [im:gateau]).
lexicon('voiture',n, [im:voiture]).

lexicon(an, n, [det:u, im:anDuree, dur:7.5]).
lexicon(heure, n, [det:u, im:heureDuree, dur:3.6]).
lexicon(minute, n, [det:u, im:minuteDuree, dur:1.8]).
lexicon(minutes, n, [det:u, im:minuteDuree, dur:2]).
lexicon('minute-là', n, [det:d, im:minute, dur:1.81, occ:sing]).
lexicon(seconde, n, [det:u, im:secondeDuree, dur:0]).
lexicon(spectacle, n, [det:d, im:spectacle, dur:3.8]).
lexicon(2010, dp, [det:d, im:'2010', dur:7.5]).
lexicon(2028, dp, [det:d, im:'2028', dur:7.5]). 


lexicon(aime, v, [vwp:g, im:aimer]).

lexicon(mange, vp, [vwp:f, im:déjeuner, dur:3.5]).
lexicon(mange, vp, [vwp:g, im:grignoter, dur:1.5, occ:mult]).
lexicon(mange, v, [vwp:f, im:ingérer, dur:1.4]).
lexicon(mange, v, [vwp:g, im:manger_de, dur:1]).

lexicon(ronfle, vp, [vwp:g, im:ronfler, dur:1]).
lexicon(conduire, v, [vwp:g, im:conduire]).



lexicon('_PP', t, [op:sep, vwp:f, det:d, im:past]).
lexicon('_IMP', t, [vwp:g, im:past]).
lexicon('_PR', t, [vwp:_, im:present]).
lexicon('_FUT', t, [op:sep, vwp:f, det:d, im:future]).

lexicon(un, d, [vwp:f, det:_, im:'1', occ:_]).	% quantity
lexicon(une, d, FS) :- lexicon(un, d, FS).
lexicon(dix, d, [vwp:f, det:_, im:'10', occ:_]).	
%lexicon(dix, d, [det:_, im:'10', occ:sing]).	% yes, singular
lexicon(le, d, FS) :-
	FS = [vwp:f, det:_, im:ce, occ:sing] .
lexicon(la, d, FS) :- lexicon(le, d, FS).
lexicon(cette, d, FS) :- lexicon(le, d, FS).
lexicon(ce, d, FS) :- lexicon(le, d, FS).
lexicon(du, d, [vwp:g]).	 


rephrase(future, 'dans le futur') :- !.
rephrase(past, 'dans le passé') :- !.
rephrase(sliced, 'à un moment de') :- !.
rephrase(cover, 'sur la durée de') :- !.
rephrase(repeat, répété) :- !.
rephrase(after, 'après') :- !.
rephrase(separate, separation) :- !.
rephrase(X,X).
