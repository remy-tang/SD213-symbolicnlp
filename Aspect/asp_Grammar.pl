/*---------------------------------------------------------------*/
/* Telecom Paris - J-L. Dessalles 2022                           */
/* Cognitive Approach to Natural Language Processing             */
/*            http://teaching.dessalles.fr/CANLP                 */
/*---------------------------------------------------------------*/



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Syntax
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

/*
	s   =  Mary will drink water during one minute in January
	ip  =  Mary will drink water during one minute
	dp  =  Mary / the show
	tp  =  will drink water during one minute
	t   =  will
	vpt =  drink water during one minute
	vp  =  drink water
	pp  =  during one minute
*/


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% head-first rules
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
s  --> ip, pp.		% time complement (time location)
s  --> ip.			% no time complement
tp  --> t, vpt.		% tense
vpt  --> vp, pp.	% internal time complement (duration...)
vpt  --> vp. 		% no time complement
vp  --> v, dp.		% internal complement 
vp  --> v. 			% no complement 
pp  --> p, dp.		% prepositional phrase
dp  --> d, n.		% determined noun

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% head-last rules (note the single hyphen sign ->)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ip  -> dp, tp.		% subject - tensed verb phrase

