# Round 10 independent audit

Date: 2026 10 03. This audits the proposed statements mathematically; it does not establish historical novelty. No additional numerical experiment is needed for the conclusions below, which follow from explicit identities and inequalities.

## Verdict

All five proposed claims are correct with the qualifications stated below. The spectral-band variational equality requires a nondegenerate positive band `0 < l < b`. The capacity sharpness claim is conditional on the prescribed static budget. The total-variation convention is half the L1 distance, and the unbanded time-weighted comparison distribution is a mixture of Erlang distributions of shape 2.

## 1. Physical capacity, delay, and the sharp capacity envelope

Let C be the positive diagonal matrix of internal capacities, let L_II be the internal block of the reciprocal conductance Laplacian, and let g_L,g_R be the nonnegative coupling vectors to the two observed boundary ports. With no other port or conductance sink,

    L_II 1 = g_L + g_R.

Put

    Q = C^(-1/2) L_II C^(-1/2),
    u = C^(-1/2) g_L,   v = C^(-1/2) g_R,
    z = Q^(-1)(u+v) = C^(1/2) 1,
    y = Q^(-1)(u-v).

Assume Q is positive definite (each internal component is attached to a boundary) and a=u^T Q^(-1)v>0. Let

    h(t)=u^T exp(-Qt)v,   f=h/a,
    m=integral t h(t)dt=u^T Q^(-2)v,
    B=sum_i C_ii=||z||^2.

Since Q^(-1) is nonnegative, z+y=2Q^(-1)u>=0 and z-y=2Q^(-1)v>=0. In particular |y_i|<=z_i, and

    4m = ||z||^2 - ||y||^2,
    delta = B - 4a E_f[t] = ||y||^2 >= 0.

Thus total capacity is at least four times dynamic static coupling times mean delay. Equality is exactly y=0, equivalently u=v, for this no-other-port model. A direct L-R conductor contributes to total static conductance but not a, h, or B. It is essential to distinguish total static conductance kappa from the dynamic static contribution a<=kappa.

Because Q commutes with its exponential and is symmetric,

    h(t) = [z^T Q^2 exp(-Qt)z - y^T Q^2 exp(-Qt)y]/4.

Both quadratic forms on the right are nonnegative. Therefore, for every nonnegative measurable w,

    D_w = integral w(t)h(t)dt
        <= B/4 sup_(lambda>0) lambda^2 integral w(t)exp(-lambda t)dt.

This follows by pointwise domination and Tonelli; it remains an extended-valued inequality when the supremum is infinite. No subtraction of two infinite integrals is needed. In particular, for t>0,

    h(t) <= B/(e^2 t^2),

since max_lambda lambda^2 exp(-lambda t)=4/(e^2 t^2), attained at lambda=2/t.

Sharpness with an imposed total static kappa: if the kernel supremum is attained at lambda_* and kappa>=B lambda_*/4, take a balanced one-state star with

    capacity C=B,
    g_L=g_R=B lambda_*/2,
    direct g_LR=kappa-B lambda_*/4.

Then Q=lambda_*, h(t)=B lambda_*^2 exp(-lambda_*t)/4, dynamic a=B lambda_*/4, and equality holds. If kappa<B lambda_*/4, the bound is still valid but this sharpness construction is unavailable, and sharpness under that joint constraint is not established. If lambda_* is only a supremum, formulate sharpness as an approximating sequence, subject to the corresponding static constraint.

Useful scope note: when w is positive at times arbitrarily close to 0, the capacity-only kernel bound may be infinite; for example w=1_[0,T] makes the supremum infinite. This does not invalidate it, but delayed observation windows are a natural useful regime. The elementary static bound D_w<=a||w||_infinity<=kappa||w||_infinity remains available for bounded w.

## 2. Stronger applicability of the capacity inequality

The exact identity with physical B assumes there are no unobserved ports or conductance sinks. The capacity UPPER BOUND needs less.

With other nonnegative boundary/sink couplings, write

    Q z_phys = u+v+r,  r>=0,
    z_phys=C^(1/2)1,
    z_eff=Q^(-1)(u+v)<=z_phys.

Then B_eff=||z_eff||^2<=B_phys. The same spectral identity using z_eff gives

    D_w <= B_phys/4 sup_lambda lambda^2 integral w exp(-lambda t),
    h(t) <= B_phys/(e^2 t^2).

Thus the pairwise signal envelope holds in general reciprocal thermal/grounded-capacitor networks with other ports held at the reference value, provided Q remains SPD. The exact delay equality becomes B_eff-4m=||y||^2; with B_phys it is an inequality. Do not normalize t h_+ by B_phys unless B_eff=B_phys.

## 3. Spectral-band Erlang optimization

Assume 0<l<b and every eigenvalue of Q lies in [l,b]. For fixed nonnegative measurable w define

    q_j^[l,b](w)=sup_(rho in [l,b]) integral w(t) p_(j,rho)(t)dt,
    E_k^[l,b](w)=max_(1<=j<=k) q_j^[l,b](w).

The exact supremum over normalized reversible positive cross densities with at most k states and spectrum in [l,b] is E_k^[l,b](w).

Upper bound: the previously audited Miclo decomposition uses spectral rates lambda_i in [l,b]. The gamma-Dirichlet representation has rate rho=1/(sum P_i/lambda_i), a weighted harmonic mean, so rho remains in [l,b]. Taking expectations against w gives the bound.

Lower bound: for each j and each rho strictly inside the band, Q_epsilon=rho(I-epsilon A_path,j) is admissible for sufficiently small epsilon and its normalized endpoint density converges pointwise to Erlang(j,rho). For rho=l or b, first adjust rho_epsilon inward by O(epsilon), so the entire spectrum remains in the band and rho_epsilon tends to the desired endpoint. Fatou's lemma gives the lower bound for arbitrary nonnegative w. Physical realization and rescaling to a fixed positive dynamic static conductance leave Q and its spectral band unchanged.

This remains an equality of suprema, not a general finite-network attainment statement. Resource budgets are not included in this equality: the path realization may require divergent physical capacities as epsilon tends to zero.

Degenerate exception: if l=b=lambda, symmetry implies Q=lambda I, hence every nonzero normalized cross response is exactly lambda exp(-lambda t), regardless of the allowed state count. Erlang shapes j>1 must not be inserted into a zero-width-band formula.

## 4. Exact finite-horizon saturation

If w>=0 is supported in [0,T], then

    p_(j+1,rho)(t)/p_(j,rho)(t)=rho t/j<=bT/j.

For every integer j>=bT the ratio is at most one on the observation support. Therefore q_(j+1)^[l,b]<=q_j^[l,b] for all j>=ceil(bT), and

    E_k^[l,b](w)=E_J^[l,b](w)
    for all k>=J=max(1,ceil(bT)).

This is a saturation of the performance SUPREMUM for this scalar observation. It does not assert that every such bound is attained by a finite J-state physical circuit. If T=0 and w is a Lebesgue-measurable function, the integral is zero; the formula remains harmless.

## 5. No universal C_k factor relative to a band-restricted exponential

The original C_k envelope chooses exponential rate rho/j, which can be smaller than l. The same coefficient cannot in general be used when the one-state comparison is restricted to [l,b]. Indeed, there is no finite factor depending only on k,l,b for all nonnegative kernels when k>=2.

For w=1_[T,T+eta], fixed eta>0 and T>=1/l, the best exponential rate in [l,b] is l. The ratio of the Erlang(2,l) expectation to that exponential expectation is exactly

    lT + 1 - l eta/(exp(l eta)-1),

which tends to infinity with T. Erlang(2,l) is approachable inside the band by the preceding path construction. An explicit admissible two-state matrix is

    Q_d=[[l+d,-d],[-d,l+d]], 0<2d<=b-l,
    u=e_1, v=e_2,

whose spectrum is {l,l+2d} and normalized density is

    f_d(t)=l(l+2d)/(2d) [exp(-lt)-exp(-(l+2d)t)].

As d tends to zero, f_d tends to l^2 t exp(-lt). Thus the counterexample uses valid reciprocal positive systems, not merely an abstract Erlang law outside the finite physical class.

## 6. Quantitative near-balance statements

Set

    h_+(t)=z^T Q^2 exp(-Qt)z/4,
    h_-(t)=y^T Q^2 exp(-Qt)y/4,
    beta=integral h_-=y^T Qy/4.

Then h=h_+-h_->=0, integral h_+=a+beta, and h_+/(a+beta) is a probability mixture of exponential densities. If lambda_max(Q)<=Lambda,

    TV(h/a, h_+/(a+beta))
      <= beta/(a+beta)
      <= Lambda delta/(4a+Lambda delta).

Here TV is one half of the L1 distance. Proof: h_+/(a+beta) is the convex combination of h/a and h_-/beta with mixture weight beta/(a+beta) on the latter. The zero-beta case is equality of the two densities. The eigenvalue inequality beta<=Lambda||y||^2/4 then gives the stated bound.

Without a spectral upper bound, let

    F_time(t)=t h(t)/m,
    G_time(t)=4t h_+(t)/B.

These are probability densities, and

    TV(F_time,G_time)<=delta/B.

Indeed integral t h_+=B/4 and integral t h_-=delta/4, so the same convex-mixture argument applies. In an eigenbasis of Q,

    G_time(t)=sum_i (z_tilde_i^2/B) lambda_i^2 t exp(-lambda_i t),

which is a mixture of Erlang(2,lambda_i) densities, not a mixture of exponentials. Time weighting is essential here. Equality delta=0 implies h/a itself is an exponential mixture.

With unobserved ports or sinks, these statements hold using B_eff and delta_eff=B_eff-4m. They also imply the looser numerical upper bound delta_phys/B_phys=1-4m/B_phys for the time-weighted TV, but G_time must still be normalized with B_eff.

## Reporting recommendations

- Emphasize that the capacity inequality does not depend on a guessed number of hidden states, and applies to cross responses of a measured pair even in a larger positive reciprocal network.
- Separate fixed-capacity, fixed-static, and fixed-band assumptions. The unconstrained path construction is not a resource-feasible construction under a fixed capacity budget.
- State the static condition explicitly whenever calling the capacity bound sharp.
- Describe the finite-horizon result as saturation of an observation's supremum, retaining the distinction between a limiting law and an attained finite circuit.
- The underlying spectral identities are elementary. The spectral-band optimization imports the previously cited reversible absorption decomposition. Neither claim should be presented as a resolved classical open problem or as historically new without a separate literature comparison.

## 7. Additional audit: a residue capacity certificate and an attained two-pole optimum

The proposed new lower bound and finite construction are correct. This section treats a FIXED SCALAR CROSS RESPONSE, not a prescribed full two-port transfer matrix.

### 7.1 General residue bound

Suppose the cross response is written in its canonical distinct-rate form

    h(t)=sum_j r_j exp(-lambda_j t),   lambda_j>0.

Combine equal-rate coefficients before taking positive parts; do not arbitrarily split one residue into positive and negative terms. A reciprocal finite thermal/grounded-capacitor realization has such a form because its Q is real symmetric and hence diagonalizable.

For every distinct eigenvalue lambda of a realization, let P_lambda be its orthogonal spectral projector, including eigenvalues whose net residue is zero. Set

    Z_lambda=||P_lambda z||^2,
    Y_lambda=||P_lambda y||^2.

The spectral identity gives the cross residue

    r_lambda=lambda^2 (Z_lambda-Y_lambda)/4.

Consequently

    Ctot=||z||^2=sum_lambda Z_lambda
        >=4 sum_j max(r_j,0)/lambda_j^2.

The lower bound is invariant under repeated eigenvalues because it uses their whole spectral projectors. Invisible additional states cannot evade it. More exactly, in the two-port no-leakage model,

    Ctot - 4 sum_(r_lambda>0) r_lambda/lambda^2
      = sum_(r_lambda>0) Y_lambda
        + sum_(r_lambda<=0) Z_lambda >=0.

Equality therefore requires P_lambda y=0 at every positive-residue eigenvalue, and P_lambda z=0 at every nonpositive-residue eigenvalue, including any invisible one. This is an equality characterization for a realization, not a general guarantee that every admissible target attains the lower bound.

With other ports or nonnegative leakage, use z_eff in the projector argument. Since ||z_eff||^2<=Ctot, exactly the same residue LOWER BOUND for physical total capacity remains valid. A leak-free construction attaining it is therefore also optimal within the larger class allowing such leakage.

### 7.2 Exact two-exponential result

Let

    h(t)=A exp(-alpha t)-B exp(-beta t),
    A>0, 0<=B<=A, 0<alpha<beta.

The condition A>=B is necessary for a positive-system cross response, since h(0)=A-B must be nonnegative. For this target it is also sufficient for the construction below. The residue certificate gives

    Ctot >= 4A/alpha^2.

Take two internal nodes with equal capacities

    C_1=C_2=2A/alpha^2,

internal conductance

    g_12=A(beta-alpha)/alpha^2,

and four boundary conductances arranged as

    g_(1,L)=(A+sqrt(AB))/alpha,
    g_(1,R)=(A-sqrt(AB))/alpha,
    g_(2,L)=(A-sqrt(AB))/alpha,
    g_(2,R)=(A+sqrt(AB))/alpha.

All capacities are strictly positive and all listed conductances are nonnegative; g_12 is strictly positive. When A=B, the two minus-sign conductances are zero, which is allowed in the nonnegative-conductance model.

The internal normalized matrix is exactly

    Q = [[(alpha+beta)/2, -(beta-alpha)/2],
         [-(beta-alpha)/2, (alpha+beta)/2]].

Its symmetric eigenvector (1,1)/sqrt(2) has eigenvalue alpha, while its antisymmetric eigenvector (1,-1)/sqrt(2) has eigenvalue beta. The normalized port vectors are

    u=[(sqrt(A)+sqrt(B))/sqrt(2),
       (sqrt(A)-sqrt(B))/sqrt(2)]^T,
    v=[(sqrt(A)-sqrt(B))/sqrt(2),
       (sqrt(A)+sqrt(B))/sqrt(2)]^T.

Their symmetric eigen-coordinates are both sqrt(A), and their antisymmetric coordinates are sqrt(B) and -sqrt(B). Therefore

    u^T exp(-Qt)v=A exp(-alpha t)-B exp(-beta t)

for every t>=0, exactly, with no limiting argument. The total internal capacity is exactly 4A/alpha^2, so the lower bound is attained.

Its dynamic static cross conductance is

    a=integral h(t)dt=A/alpha-B/beta>0.

If total two-terminal static conductance kappa is prescribed, the necessary condition is kappa>=a: the total cross conductance is the sum of nonnegative direct conductance and a. It is also sufficient here: add a direct L-R conductor of size

    g_LR=kappa-a.

This does not change Q, h, or the capacity optimum. The complete two-port diagonal dynamic responses are whatever this construction induces; they were not fixed by the scalar cross target.

An additional internal check is the delay/capacity defect:

    m=A/alpha^2-B/beta^2,
    Ctot-4m=4B/beta^2=||y||^2,
    z=(sqrt(2A)/alpha)(1,1),
    y=(sqrt(2B)/beta)(1,-1).

This agrees with the general identity and with the equality conditions for the positive-residue bound.

If B>0, the scalar response has two distinct nonzero poles, so at least two states are necessary even without positivity constraints; the construction also has the minimum state count. If B=0, the same capacity minimum can be attained by one balanced star, and the two-node construction is capacity-optimal but not state-minimal. The trivial A=B=0 target has capacity minimum zero and should be handled separately rather than assigning zero capacity to a purported positive-capacity node.

The result is an attained capacity optimum for a complete scalar waveform under stated component constraints. It strengthens a single-observation certificate, but it does not solve general positive realization, general two-port realization, or the arbitrary signed-residue capacity problem. Historical novelty is unestablished.
