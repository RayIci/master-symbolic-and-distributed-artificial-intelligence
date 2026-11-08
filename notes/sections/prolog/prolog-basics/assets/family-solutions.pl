% 1. Dad is the father of Kid if Dad is a parent of Kid and Dad is male
father(Dad, Kid) :-
    parent(Dad, Kid),
    male(Dad).

% 2. Adult is a great-grandparent of Child if Adult is a parent
%    of some X and X is a grandparent of Child
greatgrandparent(Adult, Child) :-
    parent(Adult, X),
    grandparent(X, Child).
