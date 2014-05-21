criminal(X) :- american(X), weapon(Y), nation(Z),
        hostile(Z), sells(X,Z,Y).
owns(nono,msl(nono)).
missile(msl(nono)).
sells(west,nono,M) :- owns(nono,M), missile(M).
weapon(W) :- missile(W).
hostile(H) :- enemy(H,america).
american(west).
nation(nono).
enemy(nono,america).
nation(america).
?- criminal(Who).
