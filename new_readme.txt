https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/

//FLIGHT-NP-VIET[SEM=<?cnp,?whq>, VAR=?f] -> FLIGHT-CNP[SEM=?cnp, VAR=?v] WHICH-QUERY[SEM=?whq] 
S-VIET[SEM=<(WHQUERY(?vp(?v,?f),?np))>, VAR=?v, GAP=?f] -> FLIGHT-NP-VIET[SEM=?np, VAR=?f] FLIGHT-VP[SEM=?vp, VAR=?v]
FLIGHT-VP-VIET[SEM=<\r ?dest(?v) & f.?v(r,f,?time)>, VAR=?r] -> FLIGHT-V[SEM=?v, VAR=?r] FLIGHT-DEST[SEM=?dest] FLIGHT-TIME[SEM=?time]
