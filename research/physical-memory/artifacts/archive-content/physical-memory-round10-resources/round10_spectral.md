# Round 10: spectral windows, finite paths, and their capacity cost

Date: 2026 10 03. Status: analytic derivation checked below; historical novelty not assessed. These are extensions/corollaries of the Round 9 reversible-phase-type argument, not a solution of general positive realization.

## 1. Exact scalar optimum under a nondegenerate spectral band

Let 0 < L < U < infinity. An admissible normalized component has

    f(t) = u^T exp(-Qt) v / a,  a = u^T Q^{-1} v > 0,

where Q is an at-most-k-dimensional symmetric positive-definite Stieltjes matrix, spec(Q) is contained in [L,U], and u,v are nonnegative. The following statement assumes that physical capacities and conductances may be any finite positive/nonnegative values; no uniform component-resource bound is imposed.

For nonnegative measurable w define

    q_j^[L,U](w) = sup_{rho in [L,U]} integral w(t) Erlang(j,rho)(t) dt,
    E_k^[L,U](w) = max_{1 <= j <= k} q_j^[L,U](w).

Then

    sup over admissible at-most-k-state components of integral w f
      = E_k^[L,U](w).

This is an equality of suprema, possibly infinite. It does not assert attainment.

### Upper bound

The h-transform and reversible absorption-time theorem used in Round 9 express f as a mixture of sums of j <= k independent exponentials whose rates lambda_i are eigenvalues of Q. The gamma/Dirichlet factorization expresses each such sum as a scale mixture of Erlang(j,rho), with

    rho = 1 / sum_i P_i/lambda_i.

Since each lambda_i is in [L,U], rho is in [L,U]. Integration against w >= 0 gives the claimed upper bound by Tonelli.

### Lower bound

For j <= k let A_j be the adjacency matrix of the j-vertex path. For j >= 2 take

    Q_epsilon = rho (I - epsilon A_j),  u=e_1, v=e_j.

Write beta_j = 2 cos(pi/(j+1)) = ||A_j||_2. The spectrum is inside [L,U] whenever

    rho epsilon beta_j <= min(rho-L, U-rho).

For every interior rho one may send epsilon down to zero, and the normalized density tends pointwise to Erlang(j,rho). Fatou proves that the supremum over finite admissible components is at least its w integral, even when w is merely nonnegative measurable or the integral is infinite. For endpoint rho, first choose interior rho_n tending to that endpoint, and positive epsilon_n tending to zero sufficiently fast to respect the spectral margin; the same pointwise convergence and Fatou argument applies. Shape j=1 is exactly realizable.

The physical realization is explicit. Set z=Q^{-1}(u+v)>0. Before static normalization choose C_i=z_i^2, internal conductances g_ij=-Q_ij z_i z_j, and port conductances g_iL=z_i u_i, g_iR=z_i v_i. Then multiply all capacities and conductances by kappa/a to fix the static two-terminal conductance to kappa. This keeps Q unchanged.

### Degenerate band is a genuine exception

If L=U=lambda, symmetric Q with that spectrum is lambda I. Every nonzero normalized cross response is exactly lambda exp(-lambda t). Thus the answer is q_1 at lambda, even if k>1. Substituting the degenerate interval into the nondegenerate-band formula is incorrect. The discontinuity is possible because the physical coefficients in the approximating path family become singular/unbounded as the spectral width collapses.

### The old C_k comparison requires an unrestricted exponential baseline

The gamma-to-exponential envelope in Round 9 uses rate mu=rho/j. This may lie outside [L,U]. No finite universal constant can compare this band's k>=2-state optimum with this same band's one-state optimum for every nonnegative w: for narrow windows near a large time T, an Erlang(2,L) limit has relative density L T compared to the best band-constrained exponential, which is L exp(-LT) once T>1/L. This ratio is unbounded with T. The Round 9 C_k bound remains valid if the reference one-state rate is unrestricted.

## 2. A finite effective state budget for bounded observation horizon

Suppose w >= 0 is supported in [0,T], T>0. Put J=max(1,ceil(U T)). Then

    E_k^[L,U](w) = E_min(k,J)^[L,U](w).

Indeed, at each rho<=U and t<=T,

    Erlang(j+1,rho)(t) / Erlang(j,rho)(t) = rho t/j <= U T/j.

For integer j>=J this is <=1, so q_(j+1)<=q_j. Consequently allowing more than J internal states cannot improve this single scalar observable's supremum. If UT<=1, one state already gives the optimal supremum over every finite state count. This is not a claim about reproducing the full transient curve or several observables simultaneously.

For w=indicator_[a,b] with 0<a<b, each shape's exact optimal rate is

    rho_j^* = clamp(j log(b/a)/(b-a), L, U).

The probability is the difference of Erlang survival functions. The formula follows by differentiating the interval probability; its derivative has the sign of b^j exp(-rho b)-a^j exp(-rho a).

## 3. A finite-path approximation certificate

Fix j>=2, rho>0, epsilon in (0,1/beta_j). Let D_j(epsilon)=det(I-epsilon A_j). The endpoint inverse identity gives

    a = epsilon^(j-1) / (rho D_j(epsilon)).

Expanding the matrix exponential and inverse in powers of epsilon gives the exact probability mixture

    f_epsilon(t) = sum_{m>=0} p_m Erlang(j+2m,rho)(t),
    p_m = D_j(epsilon) epsilon^(2m) (A_j^(j-1+2m))_(1j).

All coefficients are nonnegative, sum to one, and p_0=D_j(epsilon). Therefore, with total variation defined as sup_A |P(A)-Q(A)|,

    TV(f_epsilon, Erlang(j,rho)) <= 1-D_j(epsilon)
                                  <= (j-1) epsilon^2.

The second inequality uses paired path eigenvalues: D_j=product_{lambda_l>0}(1-epsilon^2 lambda_l^2), and sum_{lambda_l>0}lambda_l^2=j-1. Every factor belongs to (0,1].

Consequences:

* For 0<=w<=M, absolute observable error is at most M(1-D_j)<=M(j-1)epsilon^2.
* For arbitrary |w|<=M, the bound is 2M(1-D_j).
* For a CDF, 0<=F_Erlang(j,rho)(t)-F_epsilon(t)<=1-D_j for every t, since the other mixture terms have more exponential stages.
* These error statements are certificates for this constructed path, not lower bounds on all realizations.

## 4. Exact total capacity after fixing static conductance

Let s=e_1+e_j and y=(I-epsilon A_j)^{-1}s. The realized path's total capacity is exactly

    C_total = (kappa/a) ||Q^{-1}s||_2^2
            = kappa D_j(epsilon) ||y||_2^2
              / (rho epsilon^(j-1)).

This is computable from one tridiagonal solve and its determinant. The determinant recurrence is

    D_0=D_1=1,  D_n=D_(n-1)-epsilon^2 D_(n-2).

There is also an explicit capacity profile:

    y_i = [epsilon^(i-1) D_(j-i) + epsilon^(j-i) D_(i-1)] / D_j.

This follows from the inverse entries (M^{-1})_(i1)=epsilon^(i-1)D_(j-i)/D_j and its reflected counterpart.

For j>=2,

    C_total ~ 2 kappa / (rho epsilon^(j-1))  as epsilon -> 0.

A simple bound valid throughout the SPD range is

    C_total <= 2 kappa / [rho epsilon^(j-1) (1-epsilon beta_j)^2].

Thus the useful spectral-window theorem still permits severe capacity growth. If a target TV certificate delta is enforced by choosing epsilon=sqrt(delta/(j-1)), subject also to the spectral condition, then this path's capacity grows asymptotically as

    (2 kappa/rho) ((j-1)/delta)^((j-1)/2).

This is the cost of this sufficient construction, not a universal necessary resource law. A finite total-capacity cap invalidates the unrestricted sharpness construction and needs a separate optimization theorem.

## 5. Two-state path: all formulas elementary

For j=2,

    Q=rho [[1,-epsilon],[-epsilon,1]],  0<epsilon<1,
    D_2=1-epsilon^2,
    lambda_-=rho(1-epsilon), lambda_+=rho(1+epsilon),
    a=epsilon/[rho(1-epsilon^2)],
    z=(1,1)/[rho(1-epsilon)].

After fixing static conductance to kappa,

    C_1=C_2=kappa(1+epsilon)/[rho epsilon(1-epsilon)],
    g_L=g_R=kappa(1+epsilon)/epsilon,
    g_internal=kappa(1+epsilon)/(1-epsilon),
    C_total=2kappa(1+epsilon)/[rho epsilon(1-epsilon)].

Check: the three series conductances have reciprocal sum 1/kappa.

The normalized density and CDF are

    f_epsilon(t)=rho(1-epsilon^2)/(2epsilon)
                 [exp(-rho(1-epsilon)t)-exp(-rho(1+epsilon)t)],

    F_epsilon(t)=1-
       [(1+epsilon)exp(-rho(1-epsilon)t)
        -(1-epsilon)exp(-rho(1+epsilon)t)]/(2epsilon).

The exact mixture is

    f_epsilon=(1-epsilon^2) sum_{m>=0} epsilon^(2m) Erlang(2+2m,rho).

In particular

    0 <= [1-exp(-rho t)(1+rho t)] - F_epsilon(t) <= epsilon^2.

As epsilon -> 0, C_total ~2kappa/(rho epsilon), while the certified CDF/TV error is <=epsilon^2. Choosing epsilon=sqrt(delta) certifies error<=delta and gives the explicit sufficient capacity

    C_total=2kappa(1+sqrt(delta)) / [rho sqrt(delta)(1-sqrt(delta))].

This path's minimum total capacity over epsilon is (6+4sqrt(2))kappa/rho, attained at epsilon=sqrt(2)-1. For a fixed capacity budget B, write b=B rho/(2kappa). The path can fit the budget iff b>=3+2sqrt(2), with epsilon in the interval whose endpoints are

    [(b-1) +/- sqrt(b^2-6b+1)]/(2b).

A spectral-band constraint may further shrink that interval. These are family-specific feasibility statements, not an optimum across all two-state physical networks.
