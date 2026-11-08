mult(0, _, 0).          % multiplying anything by 0 gives 0
mult(s(X), Y, Z) :-     % Z = (X+1)*Y if
    mult(X, Y, W),      %   W = X*Y
    add(W, Y, Z).       %   and Z = W + Y
