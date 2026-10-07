# Round 8: exact collective-observable optimum in the edge-star subclass

Date: 2026 09 29. This is an independently derived mathematical result for a specified subclass. It does not establish historical novelty or global optimality among all passive thermal networks.

> Supersession notice (2026 09 29): the subclass theorem below remains valid. The later independent proof in `round8_window.md` and audit in `round8_global_audit.md` closes the 28-to-85 gap for equal triangle-free budgets and the stated kernel condition. Statements below that call this global extension open record the earlier stage of this round. Unequal weighted budgets remain a subclass-only claim.

## 1. Network and observable

Let the boundary steady-state response be a graph Laplacian

K = Σ_e κ_e (e_i−e_j)(e_i−e_j)^T,  κ_e>0.

Fix waiting time t≥0, window width h>0, and optional triangular-derivative ramp: each of the two uniform factors has width T≥0, so the full ramp ends at 2T and the subsequent wait is t. T=0 denotes an ideal step. For each chosen edge we may replace some amount 0<a_e≤κ_e of its direct conductance with a symmetric one-state star. Both spokes have conductance 2a_e and the capacity is C_e=4a_e/μ_e, with μ_e>0. The remaining direct edge conductance is κ_e−a_e. Edges not chosen remain entirely direct. This preserves the entire matrix K exactly.

One such star has

Y_e(s)=a_e (e_i−e_j)(e_i−e_j)^T + [s a_e/(s+μ_e)](e_i+e_j)(e_i+e_j)^T.

Thus its off-diagonal two-window entry is a_e q(μ_e), where

q(μ)=exp(−μt)(1−exp(−μh))²/μ × [(1−exp(−μT))/(μT)]².

The last factor is 1 if T=0. Define q_* = max_{μ>0}q(μ). For nonnegative edge weights w_e, use the scalar observable Z=Σ_e w_e D_ij. The special complete-bipartite collective experiment is w_e=1/n.

## 2. The scalar kernel has a unique maximizer

Write x=μh, a=t/h and b=T/h. Then q(μ)=h f(x), with

f(x)=exp(−a x)(1−exp(−x))²/x × [(1−exp(−b x))/(b x)]².

When b>0, the sign of f′(x) is the sign of

G(x)=2x/(exp(x)−1)+2bx/(exp(bx)−1)−3−a x.

The function z/(exp(z)−1) strictly decreases on z>0: its derivative has numerator exp(z)(1−z)−1<0. Therefore G strictly decreases, G(0+)=1, and G(∞)<0. It has exactly one positive zero x_*. Since f tends to zero at both ends, x_* is the unique global maximizer. If b=0, the same proof uses

G(x)=2x/(exp(x)−1)−1−a x.

Hence μ_*=x_*/h and q_*=h f(x_*). This gives a one-variable, monotone root problem rather than a nonconvex network search.

## 3. Exact count formula in this subclass

Sort the scores v_e=w_eκ_e in nonincreasing order, v_(1)≥…≥v_(m). Put W_r=Σ_{j=1}^{min(r,m)}v_(j), W_0=0.

**Theorem.** Among the edge-star models above with at most r internal states,

max Z = q_* W_r.

Furthermore every value of Z in [0,q_*W_r] is attainable with at most r states.

**Proof.** Every selected edge contributes w_e a_e q(μ_e)≤w_eκ_eq_*. Summing at most r selected edges gives the upper bound. Equality uses the top r edges, full a_e=κ_e, and the common rate μ_e=μ_*. To obtain any intermediate value, use full budgets on a prefix of the sorted edges and a partial budget on the next edge, all at μ_*. The leftover conductance remains direct and K is unchanged. If the required partial budget is zero, omit that state. □

Allowing several independent stars on the same edge does not improve the result: their budgets sum to at most κ_e, and one star at μ_* produces the largest possible scalar response for that total budget. This observation concerns independent parallel stars, not an internally connected multi-state component.

For target Z_*≥0 and scalar absolute error ε≥0, define L=(Z_*−ε)_+. The minimum number of states in the subclass is exactly

r_star = min { r∈{0,…,m} : q_*W_r ≥ L },

provided this set is nonempty. If L=0, r_star=0. If L>q_*W_m, this subclass cannot satisfy the request. The upper side Z≤Z_*+ε presents no problem because we construct Z=L.

This is not a global minimum over arbitrary thermal networks. It is also not a guarantee on every entry of D or on the full transfer function Y(s). Matching a scalar measurement leaves many aspects of the response unconstrained.

## 4. Specialization to the previous complete-bipartite family

For n ports on each side, κ_e=λc₀/n and w_e=1/n. The target has every edge at pole λ, so d_*=c₀α, where

α=exp(−λt)[(1−exp(−λT))/(λT)]²(1−exp(−λh))² = λq(λ).

The exact subclass count is therefore

r_star = ceil( n²(α−ε/c₀)_+ / (λq_*) ).

No truncation above n² is needed for this target, because q(λ)≤q_*; the zero case is interpreted as zero. Equality in the scalar tolerance is achieved with r_star−1 full stars and (unless the quotient is an integer) one partial star.

For the existing experiment t/h=T/h=0.1 and λh=1:

x_* = 0.9609333067794434,
q_*/h = 0.32764158598953086,
α = 0.32741819974556724,
q(λ)/q_* = 0.9993181993571147.

With n=10 and ε/c₀=0.05, the previous universal bound is 28, while the exact edge-star optimum is 85:

84 q_*/100 = 0.2752189322312059 < α−0.05 = 0.27741819974556725,
85 q_*/100 = 0.2784953480911012 > α−0.05.

Use 84 full stars and a 85th star with 0.671241871729805 of its original edge budget, all at μ=0.9609333067794434λ. The displayed decimals are ordinary double-precision numerical values; the theorem and integer characterization are analytic. At zero scalar error the continuous quotient is 0.9993181993571147n², so for sufficiently large n it can be slightly smaller than n². This does not contradict n² for exact reproduction of the entire transfer function.

For the ideal immediate step, t=T=0:

x_* = 1.2564312086261693,
q_*/h = 0.40726437758907374.

## 5. Constructive bound for the full transfer function, preserving K

A separate elementary construction retains the target rate μ=λ and a k-regular bipartite subgraph of K_{n,n}, where 0≤k≤n is an integer. Such a subgraph can be formed by taking k cyclic perfect matchings. Keep one original full-budget star on each retained edge and turn all n(n−k) omitted edges into direct conductances κ_e. Thus r=nk and K is exactly preserved.

Let H_omit be the signless Laplacian of the omitted graph divided by n. The target-minus-model difference is

Y(s)−Y_tilde(s) = [sλc₀/(s+λ)] H_omit.

The omitted graph is (n−k)-regular and bipartite, so its signless Laplacian has spectral norm 2(n−k). Hence

sup_{ω∈R} ||Y(iω)−Y_tilde(iω)||₂ = 2λc₀(1−k/n).

Also ||D−D_tilde||₂ = 2c₀α(1−k/n), and the collective error is exactly c₀α(1−k/n). Thus the full response has an explicit, linear resource-error construction under exact K. This is a constructive upper bound, not a general lower-bound match. The supremum at infinite frequency is a limit; the formula remains exact as a supremum.

In particular, for normalized full-frequency absolute tolerance δ∈[0,1] defined by E≤2λc₀δ, the construction takes k=ceil(n(1−δ)) and r=n ceil(n(1−δ)) states. No historical novelty is claimed for deleting star branches and replacing their static part with resistors.

## 6. Research significance and limits

The exact scalar edge-star formula gives a concrete benchmark for testing the universal lower bound. It also lets one distinguish a proof gap from a construction gap: for the current experiment the old universal estimate gives 28 states and an optimized 85-state construction meets the scalar error. Whether internally connected multi-state components can bridge that interval is a separate question. A universal theorem replacing h by q_* in the prior lower bound would close the gap; that assertion requires an independent proof and is not assumed here.

For arbitrary measurement weights and unequal edge budgets, the count is obtained from a sorted cumulative sum, rather than a continuous nonlinear optimization. The physical assumptions and exact-K requirement remain essential. The direct compensating edges are not counted as dynamic states but do consume static conductance resources.
