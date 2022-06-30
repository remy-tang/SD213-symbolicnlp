/*---------------------------------------------------------------*/
/* Telecom Paris - J-L. Dessalles 2022                           */
/* Cognitive Approach to Natural Language Processing             */
/*            http://teaching.dessalles.fr/CANLP                 */
/*---------------------------------------------------------------*/



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% merging of structures 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%-----------------------------------------

% When Syntax merges two phrases, 'matchFS' is called to merge the corresponding semantic structures
/*	Note:
	This program hesitates between using "feature structures" such as [vwp:f, det:u] that contain
	optional named features in any order vs. fixed "aspectual structures" (Vwp, Det, Occ, Im, Dur) */

	matchFS(HeadFS, ComplFS, _NFS) :-	% just for trace
		ground(ComplFS),
		wt(5, '\n. . . . . .  merging: '), writeFS(5, HeadFS), wt(5, 'with: '), 
		writeFS(5, ComplFS), stop(5),
		fail.
matchFS([], FS, FS) :- 	!.		 	% No feature left
matchFS(FS, [], FS) :- 	!.		 	% No feature left
matchFS(FS1, FS2, [F:V | NFS]) :-
	checkF(F:V1, FS1, R1),
	checkF(F:V2, FS2, R2),
	!,
	% V1 and V2 have to be merged as F-feature values
	merge_value(F, V1, V2, V), % calls specialized Merges
	matchFS(R1, R2, NFS).
matchFS(FS1, FS2, _) :-
	writeln(FS1), writeln(FS2), 
	wt(2, '\nEchec unif:   '), writeFS(2, FS1), writeFS(2, FS2), fail.

checkF(F:V, FS1, R) :-	% checks whether feature is possibly present
	select(F:V1, FS1, R),
	!, V = V1.
checkF(F:V, FS, [F:V|FS]).	% absent feature added

/*
checkFActual(F:V, FS1, R) :-	% checks that feature is actually present
	select(F:V1, FS1, R), 
	!, ground(V1), V = V1.
*/



%---------------------------------------------------------------------------------------------%
% merging of features. merge_value(F, V1, V2) : V1 and V2 are merged as features of type F    %
%---------------------------------------------------------------------------------------------%
merge_value(_, V, V, V) :- !.		% perfect merge - Nothing more to do
merge_value(im, Im1, Im2, Im) :-	% perceptive merge
	!,
	merge_picture(Im1, Im2, Im).
merge_value(dur, D1, D2, D) :-
	ground((D1, D2)),	% both durations are instantiated
	dcompare(D1, D2, D),	% checks whether both durations are compatible
	!.
merge_value(F, V1, V2, _) :-
	wt(4, ('\n************ Unification problem', F:V1, F:V2)),
	fail.
	
		

%---------------------------------------------------------%
% rescuing operations: zoom, slice, repeat, predication   %
%---------------------------------------------------------%

rescue(SCat, FSin, FSout) :-
		fs2as(FSin, AS0),
	rescue0(SCat, AS0, AS),	% optional operation: slice, predication or repeat
				wt(5, '===>'), writeAS(5, AS),
		as2fs(AS, FSout).	

rescue0(_SCat, AS, AS).			% no rescue0 by default
rescue0(dp, AS1, AS2) :-		
	zoom(AS1, AS2).				% zoom only named events
rescue0(pp, AS1, AS2) :-		% rescue0 by repetition
	slice(AS1, AS2).			% slice only temporal complements
rescue0(vpt, AS1, AS2) :-		% rescue0 by repetition
	repeat(AS1, AS3),			% repeat only actions
	rescue0(vpt, AS3, AS2).		% looping on rescuing vpt

rescue0(vpt, AS1, AS2) :-		% rescue0 by predication
	predicate(AS1, AS3),
	rescue0(vpt, AS3, AS2).		% looping on rescuing vpt

zoom(AS, AS1) :-
	AS = (f, Det, sing, Im, Dur),	
	number(Dur),	% real duration
		wt(5, '\nRescuing attempt by zooming'), writeAS(5, AS),
	merge_picture('zoom', Im, Im1), 
	AS1 = (g, Det, sing, Im1, Dur),
		wt(4, ('\nRescued       ', Im, 'by zooming')), writeAS(4, AS1).

slice(AS, AS1) :-
	% suppress this line to enable slicing
	AS = (_Vwp, Det, _Occ, Im, Dur),
	nonvar(Det), Det = d,
	number(Dur),	% duration is replaced by max(D)
		wt(5, '\nRescuing attempt by slicing'), writeAS(5, AS),
	% another constraint might be missing: that Im be derivable
	merge_picture('sliced', Im, Im1), 
	AS1 = (f, d, _, Im1, max(Dur)),
		wt(4, ('\n============ Rescued', Im, 'by slicing')), writeAS(4, AS1).

repeat(AS, AS1) :-
	AS = (f, _Det, sing, Im, Dur),	% only repeat figures
		wt(5, '\nRescuing attempt by repeating'), writeAS(5, AS),
	merge_picture('repeat', Im, Im1), 
	AS1 = (g, _, mult, Im1, min(Dur)),
		wt(4, ('\nRescued       ', Im, 'by repeating')), writeAS(4, AS1).

predicate(AS, AS1) :-
	AS = (_Vwp, _Det, Occ, Im, Dur),
	not(Dur = nil(_)),	% don't stack up predication
		wt(5, '\nRescuing attempt by pred:'), writeAS(5, AS),
	concrete(Im),	% conceptual predication
	merge_picture('!', Im, Im1), 
	AS1 = (f, d, Occ, Im1, nil(Dur)),
		wt(4, ('\nRescued', Im, 'by predicating')), writeAS(4, AS1).

concrete(Im) :-	% This can be implemented as a restriction on what can be predicated upon
	ground(Im), 
	Im \== ''.

/*
map(Op, AS, AS1) :-
	ground(Op), Op == sep,
	!,
		wt(5, '\nPerforming separation on:'), writeAS(5, AS),
	AS = (_Vwp, _Det, _Occ, Im, Dur),
	merge_picture(separate, Im, Im1), 
	AS1 = (f, d, _, Im1, nil(Dur)),
		wt(4, ('\nSeparate', Im)), writeAS(4, AS1).
map(_, AS, AS).
*/

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% interface with perception
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

merge_picture(Im1, Im2, Im) :-
	Im1 =.. ['!', _ | _],		% predication
	!,
	Im =.. [pred_, Im1, Im2	].	% mere embedding of image identifiers
merge_picture(Im1, Im2, Im) :-
	reify(Im1, Im1a),		% suppresses variables for display
	reify(Im2, Im2a),		% suppresses variables for display
	Im1a =.. [O | A],		% the functor is promoted
	Im =.. [O, Im2a | A	].	% mere embedding of image identifiers
	
	
reify(Im, '') :-
	% suppresses variables for display
	var(Im), !.
reify(op(O), O) :- 	!.
reify(Im, Im).	


%%%%%%%%%%%%%%%%%%%%%%%%%%
% duration compatibility %
%%%%%%%%%%%%%%%%%%%%%%%%%%

% slice		--> max
% repeat	--> min
% predicate	--> nil

% dcompare(D1, D2, D2) :-
	% write('comparing '), write(D1), write(' avec '), write(D2), nl, fail. 
dcompare(max(D1), nil(D2), max(D1)) :- 		% slice & predication
	!,
	duration_convert(max(D1), DD1),
	duration_convert(nil(D2), DD2),
	DD2 =< DD1.
dcompare(nil(D1), max(D2), D) :- 		% slice & predication
	!,
	dcompare(max(D2), nil(D1), D).
dcompare(D1, D2, D1) :- 
	number(D1),
	!,
	number(D2),
	abs(D1 - D2, G), 
	G < 1, !.	% less than one order of magnitude gap
dcompare(D1, D2, D1) :- 
	number(D2),
	!,
	dcompare(D2, D1, D2).
dcompare(D1, D2, D) :- 
	duration_convert(D1, DD1),
	duration_convert(D2, DD2),
	dcompare(DD1, DD2, D).

/*
dcompare(D1, min(D2), min(D2)) :- 	smaller(D2, D1, 2.5), !.
dcompare(min(D1), D2, min(D1)) :- 	smaller(D1, D2, 2.5), !.
dcompare(D1, max(D2), max(D2)) :- 	smaller(D1, D2, 1), !.
dcompare(max(D1), D2, max(D1)) :- 	smaller(D2, D1, 1), !.
% dcompare(nil(D1), max(D2), D) :-	dcompare(D1, D2, D), !.
% dcompare(max(D1), nil(D2), D) :-	dcompare(D1, D2, D), !.
% dcompare(min(D1), min(D2), min(D2)) :-	smaller(D1, D2), !.
% dcompare(min(D1), min(_D2), min(D1)) :- !.
% dcompare(max(D1), max(D2), max(D1)) :-	smaller(D1, D2), !.
% dcompare(max(_D1), max(D2), max(D2)) :- !.
dcompare(D1, D2, D2) :- 	% duration merge
	abs(D1 - D2, G), 
	G < 1, !.	% less than one order of magnitude gap
*/
% smaller(_, min(_)).
% smaller(max(_), _).
% % smaller(D1, D2, Gap) :- 	
	% % number(D1), number(D2), D1 + Gap =< D2.
% smaller(min(D1), D2) :-	smaller(D1, D2).
% smaller(D1, max(D2)) :-	smaller(D1, D2).
% smaller(D1, max(D2)) :-	smaller(D1, D2).
	
/*
increase(D1, D2) :-
	number(D1), D2 is D1 + 1.1.
increase(max(D1), D2) :- increase(D1, D2).
increase(min(D1), D2) :- increase(D1, D2).
increase(nil(D1), D2) :- increase(D1, D2).

duration(nil(D), D) :- !.
duration(min(D), D) :- !.
duration(max(D), D) :- !.
duration(D, D).
*/

duration_convert(nil(D), D1) :-
	!,
	duration_convert(D, D1).
duration_convert(min(D), D2) :-
	!,
	duration_convert(D, D1),
	D2 is D1 + 2.5.
duration_convert(max(D), D2) :-
	!,
	duration_convert(D, D1),
	D2 is D1 - 1.
duration_convert(D, D).



% ----------------------------
% conversion between FS and AS
% ----------------------------
fs2as(FS, (Vwp, Det, Occ, Im, Dur)) :-	% convert feature structure into aspectual structure
	checkF(vwp:Vwp, FS, _),		% viewpoint 
	checkF(det:Det, FS, _),		% determination 
	checkF(occ:Occ, FS, _),		% multiplicity 
	checkF(im:Im, FS, _),		% image
	checkF(dur:Dur, FS, _).		% duration

as2fs((Vwp, Det, Occ, Im, Dur), [vwp:Vwp, det:Det, occ:Occ, im:Im, dur:Dur]).



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Display feature structures 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

writeFS(TrLevel, FS) :-
	swriteFS(S, FS), 
	wt(TrLevel, S),
	fail.	% forces backtrack because swriteSF changes FS
writeFS(_, _).
	
swriteFS(S, FS) :-
	fs2as(FS, AS),
	swriteAS(S, AS).

writeAS(TrLevel, FS) :-
	swriteAS(S, FS), 
	wt(TrLevel, S),
	fail.	% forces backtrack because swriteSF changes FS
writeAS(_, _).

swriteAS(Str, (Vwp, Det, Occ, Im, Dur)) :-
	% swritef(Str1, "%d.%d.%d\t\t%t", [S, V, A, R5]),
	paraphrase(Im, StrIm),
	!,
	format(string(Str1), "~k.~k\t~p", [Vwp, Det, [occ:Occ, dur:Dur]]),
	string_concat(Str1, ' --->\t', Str2),
	string_concat(Str2, StrIm, Str3),
	string_concat(Str3, '\n', Str).
swriteAS('', (Vwp, Det, Occ, Im, Dur)) :-
	writeln('******************************  Display Error ********************************'),
	writeln((Vwp, Det, Occ, Im, Dur)).


paraphrase(Im, "...") :-
	var(Im),
	!.
% paraphrase(Im, StrIm) :-
	% Im =.. ['!', C1, C2], !,
	% paraphrase(C1, C1a),
	% paraphrase(C2, C2a),
	% % swritef(StrIm, "(%w)!", [C1]).	
	% format(string(StrIm), "(~w, ~w)!", [C2a, C1a]).	
paraphrase(Im, StrIm) :-
	Im =.. ['!', C], !,
	paraphrase(C, C1),
	% swritef(StrIm, "(%w)!", [C1]).	
	format(string(StrIm), "(~w)!", [C1]).	
paraphrase(Im, StrIm) :-
	Im =.. [V, S, C1, C2],
	rephrase(V, V1),
	paraphrase(S, S1),
	paraphrase(C1, C1a),
	paraphrase(C2, C2a),
	format(string(StrIm), "~w ~w ~w ~w", [V1, S1, C1a, C2a]).
paraphrase(Im, StrIm) :-
	Im =.. [V, S, C],
	rephrase(V, V1),
	paraphrase(S, S1),
	paraphrase(C, C1),
	format(string(StrIm), "~w ~w ~w", [V1, S1, C1]).
paraphrase(Im, StrIm) :-
	Im =.. [V, C],
	rephrase(V, V1),
	paraphrase(C, C1),
	% swritef(StrIm, "%w %w", [V, C1]).
	format(string(StrIm), "~w ~w", [V1, C1]).
paraphrase(N, StrIm) :-
	atomic(N),
	% swritef(StrIm, "%w", [N]).
	rephrase(N, N1),
	format(string(StrIm), "~w", [N1]).
paraphrase(X, X1) :-
	with_output_to(string(X1), write_term(X, [max_depth(0)])),
	!.
	