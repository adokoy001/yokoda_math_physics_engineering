# Independent adversarial audit of the Round 8 scalar minimum theorem

Date: 2026-09-29. Scope: mathematics and model consistency, not academic priority.

## Verdict

**The exact scalar minimum theorem passes this independent audit.** I found no proof gap in `round8_window.md` under its explicit assumptions: positive diagonal internal capacity; nonnegative reciprocal conductances; stable, boundary-reachable internal components; the complete static boundary matrix K fixed exactly; triangle-free support with equal positive edge budgets; post-ramp two-window measurement; and only the specified scalar response required to lie within tolerance. The finite protocol T=tau=h/10 satisfies the needed kernel-height condition analytically.

The example with n=10, lambda0*h=1, and epsilon/c0=0.05 has **minimum 85 internal states over all networks in this model class**, not merely over independent edge stars. This is not a statement about approximating the whole transfer matrix with 85 states.

## Decisive proof checks

1. **Measurement kernel and normalization.** Starting from M(t)=u^T Q^-1 exp(-Qt)v and a=M(0)>0, the normalized density is f(t)=u^T exp(-Qt)v/a. It integrates to one. With ramp derivative rho equal to two convolved uniforms and measurement start 2T+tau, Fubini gives D/a=E[w(X)], where w(s)=E[psi_h(s+V-2T-tau)]. The shift and the factor 1/lambda in the exponential benchmark q(lambda) are correct. Direct boundary conductance cancels between equally long windows. Boundary capacitance contributes only during the ramp and is absent from these post-ramp windows.

2. **Two-state mixture.** For distinct rates a1<a2, write the normalized survival as c exp(-a1 t)+(1-c)exp(-a2 t). Nonnegative survival at large time forces c>=0; nonnegative density at zero forces c<=a2/(a2-a1). These are exactly the bounds for the stated convex mixture of Exp(a2) and Exp(a1)+Exp(a2). A negative fast residue is allowed and does not invalidate the proof. For repeated eigenvalues a symmetric Q is a scalar matrix, so the exponential case applies.

3. **Pointwise density domination.** Substitution p=2b/a-1 and z=at/2 yields the stated ratio (p+1)/(p-1)(exp(-z)-exp(-pz)). Its maximum is (1+1/p)p^(-1/(p-1)), at most one because log(p)/(p-1)>=1/p>=log(1+1/p). Thus the factor 2 is rigorously valid. It need not be sharp to prove the global minimum.

4. **Three or more states.** The convolution of the centered nonnegative triangular kernels attains its maximum at their common center. For T<=h, w*=h-T/3. The rational elementary lower bound for 3q* at T=tau=h/10 exceeds 29h/30. Hence the trivial expectation bound D/a<=w* yields D<=k a q* for all k>=3. No unproved higher-dimensional phase-type extremal theorem is needed.

5. **Static graph reduction.** Every connected internal component has strictly positive inverse internal Stieltjes block. It therefore creates positive static coupling between every pair of boundary ports it touches. Nonnegative direct conductors cannot cancel such coupling. Exact triangle-free K forces each component to touch at most two boundary ports. Its static cross budget a_c is nonnegative and, for the corresponding edge, sum_c a_c<=kappa. Consequently sum_c k_c a_c<=kappa sum_c k_c<=kappa r. Single-port components contribute no measured cross response, but still cost states.

6. **Attainability.** A one-state star with spokes 2sigma and capacity 4sigma/lambda* contributes static conductance sigma and scalar window response sigma q*. A direct edge of conductance kappa-sigma preserves K. Distinct equal-budget edges attain the r kappa q* upper bound for every integer r<=m. A partial final star attains the lower allowed target endpoint exactly. The stated target range [0,m kappa q*] guarantees that no construction with r>m is needed.

## Independent certified threshold and numerical stress test

The separate reproducible script `round8_global_audit_check.py` uses exact `Fraction` arithmetic and alternating exponential series to bracket the unique optimal root and q*. Its strict rational comparisons certify the integer 85 without trusting printed floating-point decimals:

- root x*: [0.96093330677944, 0.96093330677945];
- q*/h: [0.3276415859895202, 0.3276415859895413] (displayed bounds rounded for readability; comparisons use exact rationals);
- every 84-state candidate: d/c0 <= 0.2752189322312147;
- required lower endpoint: d/c0 >= 0.2774181997455673;
- available 85-star upper response: d/c0 >= 0.27849534809109217, with continuous partial-budget adjustment to the required endpoint.

The same script checks 3,200 random physically assembled connected RC components with 1 through 8 states, arbitrary positive capacities, dense internal conductance graphs, and both dense and disjoint endpoint attachment. All satisfy D<=k a q*. Many have negative spectral residues, so this test does not silently restrict M to a positive exponential mixture. This numerical test is supporting evidence, not the proof.

An informative negative check: sampled two-state components reach D/(a q*) approximately 1.269. Therefore the stronger component claim D<=a q* is false. The factor k is essential to this proof. It also explains why the sorted top-r edge-star formula for unequal edge budgets must **not** be presented as a global theorem.

## Scope that must stay explicit in the HTML

- Exact K includes exact same-side zero static coupling. This is not a robust theorem for unknown leakage or approximate K.
- Edge conductance budgets are equal for the global exact count. The weighted/unequal-budget result remains an edge-star subclass result.
- The fit criterion is one scalar window statistic, plus exact K. Other entries, diagonals, early-time behavior, high-frequency response, and full transfer accuracy are unconstrained.
- Dynamic states mean internal temperatures. Direct conductors and prescribed boundary temperatures are not counted as dynamic states.
- Arbitrarily small positive component values are allowed. A manufacturing lower bound on capacity or conductance could change attainability.
- Nonreciprocal dynamics, floating/mutual capacitance, general positive systems, and nonlinear finite-amplitude models are outside this theorem.
- If adding ground conductance is considered, exact graph-Laplacian K and nonnegative conductances rule out any boundary-reachable ground loss. A grounded capacitor is not a grounded conductance.
- Mathematical validity does not establish novelty. A separate primary literature comparison is still required.

No corrective theorem change is required. The older construction note's statement that the 28-to-85 interval remains open is now historically superseded by `round8_window.md` and should be labeled or updated before presentation.
