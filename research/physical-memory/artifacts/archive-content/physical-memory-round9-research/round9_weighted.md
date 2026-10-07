# Unequal static budgets: a concave resource bound

Date: 2026 09 29. Proof note; academic priority is not established.

This note assumes the Round 9 kernel lemma supplied by the kernel task:

> For a connected reversible positive component with k internal states, static cross conductance a, and any nonnegative measurable observation kernel w, its cross statistic obeys D <= a C_k q, where q = sup_(lambda>0) integral w(t) lambda exp(-lambda t) dt and C_k = k^k exp(1-k)/(k-1)!.

The kernel lemma is independent of the choice of w. If W = sup w < infinity, the additional elementary bound is D <= a W. Define C_0 = 0 and d_k = min(q C_k, W), including d_0 = 0. The case q = 0 is trivial for these absolutely continuous component laws; below q > 0.

## 1. The constants are increasing and strictly concave

The real-variable extension

    C(x) = x^x exp(1-x) / Gamma(x), x > 0,

is strictly increasing and strictly concave, and extends continuously to C(0) = 0.

Proof. Let A(x) = d(log C(x))/dx = log x - psi(x). The standard convergent integral identity is

    A(x) = integral_0^infinity exp(-xt) phi(t) dt,
    phi(t) = 1/(1-exp(-t)) - 1/t.

For t > 0, phi increases strictly from 1/2 to 1, since

    phi'(t) = 1/t^2 - 1/[4 sinh(t/2)^2] > 0.

Thus A > 0. The convolution identity and differentiation under the integral give

    A(x)^2 = integral_0^infinity exp(-xt)
                  [integral_0^t phi(u) phi(t-u) du] dt,
    -A'(x) = integral_0^infinity exp(-xt) t phi(t) dt.

For 0 < u < t, phi(u) phi(t-u) < phi(t), because phi(u) < 1 and phi(t-u) < phi(t). Consequently A^2 < -A', and

    C''(x)/C(x) = A^2 + A' < 0.

Finally Gamma(x) ~ 1/x and x^x -> 1 as x decreases to zero, so C(x) ~ e x. This proves the continuous extension. In particular C_1 = 1, C_k <= k, and the increments C_k-C_(k-1) decrease strictly. Truncating an increasing concave sequence at a constant preserves nonincreasing nonnegative increments. Therefore d_k is discretely concave.

The first constants are 1, 4/e, 27/(2e^2), 256/(6e^3), ... . The bound C_k <= k is now a consequence of concavity, rather than a separate estimate.

## 2. Graph theorem with unequal budgets and arbitrary nonnegative weights

Let the fixed static boundary matrix be the Laplacian of a triangle-free graph G=(V,E), with positive edge conductances kappa_e. Let eta_e >= 0 be arbitrary observation weights, and set

    S = sum_e eta_e D_e,       c_e = eta_e kappa_e.

All measured entries use the same kernel w. The physical model has positive diagonal internal capacities, nonnegative reciprocal conductances, boundary-reachable stable internal components, and no uncancelled ground loss. Count internal states; prescribed boundary temperatures are not states.

Every connected internal component touches at most two boundary ports, by the static Schur-complement clique property and triangle-free support. Components touching only one port contribute nothing to S. If edge e receives components with state counts k_(e,j) and static contributions a_(e,j), then

    sum_j a_(e,j) <= kappa_e.

Put k_e = sum_j k_(e,j). Since d is increasing,

    D_e <= sum_j a_(e,j) d_(k_(e,j))
        <= kappa_e d_(k_e).

Therefore every network with at most r internal states satisfies

    S <= B_r := max { sum_e c_e d_(k_e) :
                     k_e nonnegative integers, sum_e k_e <= r }.

This is an explicit relaxation with a closed scalar coefficient sequence. It is not being claimed that every relaxed edge value kappa_e d_k is achievable for the fixed w.

## 3. B_r is computed by sorting marginal gains

For every edge form the sequence

    g_(e,k) = c_e [d_k - d_(k-1)], k = 1,2,... .

Every sequence is nonnegative and nonincreasing. B_r equals the sum of the r largest gains across all edges, with zeros appended if necessary. To prove this, a feasible allocation chooses a prefix of each edge sequence. Conversely, the r globally largest gains can be chosen with all predecessor gains included, resolving equal-value ties in predecessor order. This gives a feasible prefix allocation and attains the unconstrained largest-r sum.

Thus a target S_target with absolute scalar tolerance epsilon requires

    r >= min { j >= 0 : B_j >= max(S_target-epsilon,0) }.

If W is finite, only finitely many gains are positive: stop each sequence when C_k q >= W. For the existing ramp T=tau=h/10, q/h = 0.32764158598953... and W/h = 29/30; there are eight potentially positive gains per edge. In units of h, the d_k values are approximately

    k:       1          2          3          4          5          6          7          8
    d_k/h: .327642    .482130    .598610    .695992    .781376    .858327    .928936    .966667

This is much stronger for unequal budgets than replacing every c_e by max c_e. It also corrects the tempting but false extension that simply uses the r largest distinct edge budgets: additional states on one strong edge can outperform a new state on a weak edge.

## 4. Exact uniform-budget result follows for every nonnegative kernel

If all c_e = c and there are m measured edges, then for r <= m, all first marginal gains cq precede all later gains, so B_r = r c q. One optimal-rate star on each of r distinct edges attains this value if the exponential supremum q is attained. A partial final star continuously adjusts its static budget while a direct conductor fills the remaining fixed static budget. Hence, for targets in [0, m c q],

    r_min = ceil( max(S_target-epsilon,0) / (c q) ).

This is the Round 8 exact count with its protocol restriction removed by the Round 9 kernel lemma. If q is only a supremum and not attained, all strict interior targets below r c q remain achievable, but threshold equality may fail; distinguish an infimum statement from an attained minimum at that endpoint.

For r = m ell + s, 0 <= s < m, the relaxed bound for any r is

    B_r = c [(m-s) d_ell + s d_(ell+1)].

For r > m this is generally an upper bound, not an exact physical optimum for a fixed kernel.

## 5. A simple square-root bound and a quadratic state lower bound

The classical strict lower Stirling bound Gamma(k) > sqrt(2 pi) k^(k-1/2) exp(-k) gives

    C_k < e sqrt(k/(2 pi)).

Cauchy-Schwarz therefore yields, for r > 0,

    S <= [e/sqrt(2 pi)] q sqrt(r sum_e c_e^2).

Equivalently a nonzero required statistic S_req=max(S_target-epsilon,0) imposes

    r >= [2 pi/e^2] S_req^2 / [q^2 sum_e c_e^2].

One also retains r >= S_req/(q max_e c_e). The sorted marginal certificate B_r dominates these simpler bounds. In the equal-budget case the quadratic expression is

    r >= [2 pi/e^2] m [S_req/(m c q)]^2.

This expresses the extra state cost of concentrating a reversible response into an observation window more strongly than one exponential mode can. It is meaningful for targets above the one-star-per-edge range; for targets in that range the exact linear formula is preferable.

## 6. Explicit counterexample to a distinct-edge top-r formula

Use the original dimensionless ramp h=1, T=tau=0.1. Take a triangle-free graph with one edge of static conductance 1 and another of conductance 0.1. Observe the sum of their cross statistics.

On the strong edge, use a two-internal-state path with capacities C_1=C_2=4, boundary spokes of conductance 4 at opposite ends, and internal link conductance 2. Then

    Q = [[1.5,-0.5],[-0.5,1.5]],

whose rates are 1 and 2. Its static conductance is 1 and its normalized cross-density is that of Exp(1)+Exp(2). Thus its statistic is

    H(1,2) = 2 q(1) - q(2) = 0.40341927619090... .

Make the weak edge a direct conductor, consuming no state. Two one-state stars could contribute at most

    (1+0.1) q = 0.36040574458848...,

strictly less than this two-state path. The graph may be two disconnected edges, or a path of two edges sharing one boundary vertex. The static matrix is preserved in either case. The count of states is two in both comparisons.

## 7. Stronger result: the exact fixed-kernel supremum is a finite resource problem

The kernel task has established the following stronger consequence of the reversible phase-type and Dirichlet-mixture representations. Define

    q_j(w) = sup_(rho>0) integral_0^infinity
                 w(t) rho^j t^(j-1) exp(-rho t)/(j-1)! dt,
    E_0(w) = 0,
    E_k(w) = max_(1<=j<=k) q_j(w).

Then E_k(w) is exactly the supremum of D/a over all allowable two-terminal connected components with at most k internal states. This holds for every nonnegative measurable w; assume q_1(w) is finite for a finite-valued optimization. The bound q_j <= C_j q_1 implies all entries are finite.

The upper bound follows because every relevant reversible phase-type law is a mixture of hypoexponential laws with at most k phases, and each j-phase hypoexponential law is a scale mixture of Erlang laws of shape j. For the lower bound, a symmetric near-diagonal path Q_epsilon with endpoint input/output vectors has normalized cross-density converging pointwise to the Erlang density of any selected shape j <= k and rate rho. Fatou's lemma applies directly to nonnegative w; continuity of w is not required. The phase-type mixture proof and physical path realization are recorded by the kernel task.

Consequently the EXACT supremum over all physical networks with at most r states and the fixed weighted triangle-free static graph is

    V_r = max { sum_e c_e E_(k_e)(w) :
                 k_e nonnegative integers, sum_e k_e <= r }.

Proof of the global upper bound uses the same static decomposition as Section 2, replacing d_k by E_k. For the lower bound, select a maximizing integer allocation (there are finitely many). On each active edge choose a component whose normalized statistic is arbitrarily close to E_(k_e), using its entire static budget kappa_e. Such edge components are independent and together preserve the exact static matrix. Their finite weighted sum approaches the allocation value. Hence the network supremum is V_r.

This is a genuine reduction: optimization over arbitrary internal topologies, capacities, conductances and numbers of connected components becomes (i) one-dimensional rate optimization for each integer Erlang shape j <= r, and (ii) a finite integer allocation problem. It is not just a new name for the original network optimization.

Unlike the universal coefficient envelope d_k, the sequence E_k has not been proved discretely concave for arbitrary w. Therefore V_r is obtained by dynamic programming, not automatically by sorting marginal gains:

    V_(0,s) = 0,
    V_(ell,s) = max_(0<=k<=s) [V_(ell-1,s-k) + c_ell E_k],

for edges ell = 1,...,m and state budgets s = 0,...,r. This costs O(m r^2) scalar operations after the Erlang envelope values are supplied. Because q_j are continuous-rate suprema, this is an exact mathematical characterization; evaluating them numerically requires separate certified one-dimensional optimization if one wants certified integer thresholds.

### Supremum versus attained minimum

For any required lower endpoint S_req >= 0:

* If S_req > V_r, r states are impossible.
* If 0 <= S_req < V_r, r states suffice. Choose a network with statistic above S_req, scale all its dynamic components' conductances and capacities by the same positive factor to reach S_req exactly, and replace the unused static edge budgets by direct conductors. This leaves the pole locations unchanged and preserves K. S_req = 0 uses direct conductors only.
* At S_req = V_r, attainability requires separate analysis. A repeated-pole Erlang limit is generally not itself a finite symmetric realization. Do not silently replace a supremum by a maximum.

Thus away from exact endpoint ties, V_r identifies the exact minimum state count. The uniform low-target case in Section 4 has an explicit attaining star construction and therefore has no such gap when q is attained.

## 8. Portable demonstration with a rectangular observation window

Take w = 1_[a,b], 0 < a < b. For an Erlang law of shape j and rate rho, the derivative of the interval probability has the sign of

    b^j exp(-rho b) - a^j exp(-rho a).

It changes from positive to negative exactly once, at

    rho_j = j log(b/a)/(b-a).

Thus q_j has an explicit globally optimizing rate. Its value is the difference of two elementary integer-Gamma survival functions,

    q_j = exp(-rho_j a) sum_(ell=0)^(j-1) (rho_j a)^ell/ell!
        - exp(-rho_j b) sum_(ell=0)^(j-1) (rho_j b)^ell/ell!.

The standard-library-only script `round9_weighted_rectangle.py` implements this formula, the exact supremum dynamic program, and the concave universal bound. For [a,b]=[0.9,1.1] and c=(1,0.5,0.1), representative results are:

| State budget | Optimal Erlang-envelope allocation | Exact physical supremum V_r | Universal upper B_r | Attainable distinct-star value |
|---:|:---:|---:|---:|---:|
| 1 | (1,0,0) | 0.0736989872 | 0.0736989872 | 0.0736989872 |
| 2 | (1,1,0) | 0.1105484808 | 0.1105484808 | 0.1105484808 |
| 3 | (2,1,0) | 0.1451174779 | 0.1452988625 | 0.1179183796 |
| 4 | (3,1,0) | 0.1710497495 | 0.1714994833 | 0.1179183796 |
| 5 | (4,1,0) | 0.1926212728 | 0.1934044383 | 0.1179183796 |
| 6 | (5,1,0) | 0.2114398729 | 0.2126104358 | 0.1179183796 |
| 7 | (5,2,0) | 0.2287243715 | 0.2299856267 | 0.1179183796 |
| 8 | (6,2,0) | 0.2455993557 | 0.2472949378 | 0.1179183796 |

The table evaluates the analytically defined quantities with floating arithmetic, not certified interval arithmetic. In this example, a required scalar value 0.14 needs exactly 3 states: V_2 is strictly below 0.14, while V_3 is strictly above 0.14 and every strict interior value is attainable by scaling a near-optimal component. This threshold has a wide numerical margin, although a fully machine-certified version would enclose the exponentials and logarithm by intervals.

The third state is best assigned to the strongest edge, not to the remaining weakest edge. This concretely demonstrates why the all-network problem is an allocation over Erlang shapes rather than a distinct-edge selection problem.

## Status

The concavity proof and sorting reduction are analytic. The resulting certificate is explicit for every finite graph and every supplied q,W, but its edge envelope need not be sharp for a particular observation kernel. The separate Erlang-envelope dynamic program gives the exact supremum for a fixed kernel. The exact uniform low-target theorem is sharp and attained when the exponential optimum is attained. The Gamma/phase-type kernel lemma and academic novelty assessment belong to separate notes.
