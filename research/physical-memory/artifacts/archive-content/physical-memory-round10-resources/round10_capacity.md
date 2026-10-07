# Round 10: finite total heat capacity / capacitance

Date: 2026 10 03. Analytic proofs below; independent numerical checks in `round10_capacity_check.py` and `.json`. Historical novelty is not established. The mean identity belongs to transition-path / network moment theory (the literature agent is identifying the precise primary source); these notes do not claim that identity as new.

## 1. Model and conventions

Two boundary ports L,R are fixed-temperature / fixed-voltage terminals. Internal capacities are diagonal C=diag(C_i), all C_i>0. Reciprocal internal conductances and boundary conductances b_L,b_R are nonnegative. No internal leakage to a third reservoir is allowed. The grounded internal conductance matrix L is positive definite, has nonpositive off-diagonals, and satisfies L1=b_L+b_R. Internal components attached only to one terminal may be included, though they cannot help the cross response.

Set Q=C^{-1/2}LC^{-1/2}, u=C^{-1/2}b_L, v=C^{-1/2}b_R. The delayed cross kernel is h(t)=u^T exp(-Qt)v>=0. Its static mass is a=integral h=u^T Q^{-1}v>0. A direct boundary conductor contributes an additional static conductance but is **not** included in h. Denote the total specified static conductance, including a direct conductor, by kappa>=a.

Let f=h/a, mu=integral t f, M=a mu, B=sum C_i. Let p=L^{-1}b_L; then 0<=p<=1 and L^{-1}b_R=1-p. Define z=C^{1/2}1 and y=C^{1/2}(2p-1). Then Qz=u+v and Qy=u-v.

## 2. Capacity identity and equality rigidity

M=u^T Q^{-2}v = p^T C(1-p), so

    B-4a mu = sum_i C_i(2p_i-1)^2 = ||y||^2 =: delta >=0.

Thus B>=4a mu. Equality holds iff p_i=1/2 at every capacitive node, equivalently b_L=b_R. In the equality case u=v and h(t)=u^T exp(-Qt)u is a nonnegative mixture of exponentials. Internal edges need not vanish, and equality does not force the physical circuit literally to be a collection of stars. It does force its scalar delayed cross response to have a balanced-star representation.

## 3. Universal capacity budget bound and an exact finite optimum

Let w>=0 be measurable and define

    q(lambda)=integral_0^infty w(t) lambda exp(-lambda t) dt,
    beta(w)=sup_{lambda>0} lambda q(lambda).

For all finite admissible networks,

    D_w=integral w h <= (B/4) beta(w).

Proof: spectral functional calculus gives the pointwise decomposition

    h=h_plus-h_minus,
    h_plus=1/4 z^T Q^2 exp(-Qt)z,
    h_minus=1/4 y^T Q^2 exp(-Qt)y.

Both h_plus,h_minus are nonnegative exponential sums. The positive matrix function Q^2 integral w exp(-Qt) has norm beta(w), so D_w <= integral w h_plus <= beta(w)||z||^2/4. This argument needs no state bound, no lower bound on capacities, and no upper bound on conductances. Infinite beta gives a vacuous bound, as happens for many windows touching time zero.

Suppose beta(w)<infinity is attained at lambda_star. Under a budget sum C_i<=B_max and fixed total static conductance kappa, if

    B_max lambda_star/4 <= kappa,

the exact global optimum over **all finite state counts and all topologies** is

    max D_w = B_max beta(w)/4.

A finite one-state circuit attains it: C=B_max, equal boundary conductances g_L=g_R=B_max lambda_star/2, and direct conductor g_direct=kappa-B_max lambda_star/4. Its delayed response is h(t)=B_max lambda_star^2 exp(-lambda_star t)/4. All required components are finite; g_direct may be zero. With at least one permitted internal state the optimum already holds. This does not assert the same formula in the complementary large-budget regime.

Consequently a requested scalar signal D_req certifies an absolute resource requirement B>=4D_req/beta(w), independent of the number of added nodes.

### Explicit late-window and pointwise corollaries

For w=1_[T,infinity), T>0, beta=1/(eT), uniquely optimized by lambda=1/T. Hence

    integral_T^infinity h(t)dt <= B/(4eT).

If B_max<=4kappa T, this is the exact optimum with fixed kappa and capacity budget. This improves the elementary Markov bound B/(4T), but historical novelty is unchecked.

Pointwise, maximizing lambda^2 exp(-lambda t) gives

    h(t)<=B/(e^2 t^2),  t>0,

sharp at lambda=2/t. This is an exact uniform bound over all state counts. It is attained with fixed kappa whenever B<=2kappa t.

### Finite observation interval [a,b], 0<a<b

beta=sup_lambda lambda(exp(-a lambda)-exp(-b lambda)). The unique optimizer solves

    (b lambda-1)/(a lambda-1)=exp((b-a)lambda), lambda>1/a.

The left side decreases from infinity to b/a, while the right side increases; uniqueness follows. The root lies in (2/b,2/a). For [0.9,1.1]:

    lambda_star = 2.013477252265762,
    beta       = 0.10899633216645743,
    beta/4     = 0.027249083041614358.

For kappa=1 and B_max=1, exact optimal signal is 0.027249083041614358. A finite attaining circuit is C=1, g_L=g_R=1.006738626132881, g_direct=0.4966306869335595. The exact small-budget branch extends through B_max=4/lambda_star approximately 1.9866129580052656. Decimal values illustrate the analytic theorem; no claim of interval-certified decimals is made.

### At a larger finite budget, two states can be useful

Keep kappa=1 and observation window [0.9,1.1], and allow total capacity at most B_max=5. A finite two-state serial path has C_1=C_2=5/2, left-to-node-1 and node-2-to-right conductances 15/4, internal conductance 15/8, and direct boundary conductance 1/16. Its normalized matrix is Q=[[9/4,-3/4],[-3/4,9/4]], with rates 3/2 and 3. The delayed cross kernel is exactly

    h(t)=(45/16)(exp(-3t/2)-exp(-3t)),
    a=15/16.

Thus the direct branch gives total static conductance exactly 1, and the capacity is exactly 5. Its finite-window signal is

    D_2=(15/8)q(3/2)-(15/16)q(3)
       =0.09755471129227979 (approximately).

For any one-state circuit with total static conductance 1, its dynamic static mass a<=1 and its response is a times an exponential density, so its signal is at most max_lambda q(lambda). For this window the maximizing rate is lambda_1=log(1.1/0.9)/0.2=1.0033534773107562, giving

    D_1,max=0.07369898721925505.

This one-state maximum is feasible under the same capacity budget: a balanced star with a=1 uses capacity 4/lambda_1=3.9866309236511768<5. Consequently the displayed finite two-state circuit has a **32.3691% larger signal than every permitted one-state circuit**. The example demonstrates that adding states is useless on the proved small-budget branch but can yield a concrete benefit with a larger finite budget. It does not assert that this two-state circuit is globally optimal among two-state or arbitrary-state networks.

If an exactly equal total capacity, rather than an upper budget, is desired for the one-state comparator, its same maximizing rate and a=1 can also be realized with C=5: choose g_L+g_R=5 lambda_1 and g_L g_R=5 lambda_1. Positive solutions exist because lambda_1>4/5. Thus the advantage is not caused by leaving capacity unused in the one-state comparison.

## 4. Near-minimum capacity controls deviation from exponential mixtures

Write b=integral h_minus=1/4 y^T Qy. Then integral h_plus=a+b. The density G=h_plus/(a+b) is a mixture of exponential densities, and

    G = a/(a+b) f + b/(a+b) H,

where H=h_minus/b when b>0. Therefore, using TV=1/2 integral absolute difference,

    TV(f,G)<=b/(a+b).

If lambda_max(Q)<=Lambda, then b<=Lambda delta/4 and

    TV(f,G)<=Lambda delta/(4a+Lambda delta),
    D_w<=a q_1(w) + Lambda delta q_1(w)/4

for nonnegative w with q_1(w)=sup_lambda q(lambda)<infinity. The second estimate follows from D_w<=integral w h_plus <=(a+b)q_1. It is generally a bound, not an optimal tradeoff. A spectral ceiling is essential to this particular ordinary-TV estimate.

There is also a ceiling-free statement in the natural first-moment-weighted metric. The length-biased cross density F_lb(t)=t h(t)/M has a comparison density G_lb(t)=4t h_plus(t)/B, which is a mixture of Erlang(shape 2) densities. Since integral t h_minus=delta/4,

    G_lb = (4M/B) F_lb + (delta/B) H_lb,
    TV(F_lb,G_lb)<=delta/B.

This is quantitatively stronger and cleaner than claiming an unweighted metric without a rate bound. It compares to shape-2 mixtures because length bias turns an exponential density into a shape-2 Erlang density. It does not say the original f is close to a shape-2 distribution.

## 5. A waveform-based capacity certificate: negative residues cost material

Suppose the full delayed scalar cross response is known as

    h(t)=sum_j r_j exp(-lambda_j t)

with distinct visible rates lambda_j>0. The coefficients r_j may have either sign even though h>=0. Let P_j be the spectral projection of Q at lambda_j. Then

    r_j = lambda_j^2 (||P_j z||^2-||P_j y||^2)/4.

Each positive r_j requires ||P_j z||^2>=4r_j/lambda_j^2. Each negative r_j requires ||P_j y||^2>=4(-r_j)/lambda_j^2. Summing orthogonal projections gives the realization-independent certificates

    B>=4 sum_j (r_j)_+/lambda_j^2,
    delta>=4 sum_j (r_j)_-/lambda_j^2.

Invisible modes do not invalidate the bound; they consume nonnegative additional norms. In particular the first inequality is stronger than B>=4M whenever negative residues occur.

For nonnegative exponential sums (all r_j>=0), the first bound is exact: a balanced star for each term with C_j=4r_j/lambda_j^2 and g_L,j=g_R,j=2r_j/lambda_j realizes it.

For the entire nonnegative two-exponential family

    h(t)=A exp(-alpha t)-B0 exp(-beta t),
    0<alpha<beta, A>=B0>0,

the exact minimum capacity over all allowed finite networks is

    B_min=4A/alpha^2.

An explicit attaining two-state circuit has equal capacities C_1=C_2=2A/alpha^2, internal conductance A(beta-alpha)/alpha^2, and boundary conductances

    g_L,1=(A+sqrt(A B0))/alpha,
    g_L,2=(A-sqrt(A B0))/alpha,
    g_R,1=g_L,2, g_R,2=g_L,1.

All are nonnegative; boundary zeros at A=B0 are allowed. In normalized coordinates Q has diagonal (alpha+beta)/2 and off-diagonal -(beta-alpha)/2; its symmetric and antisymmetric modes have eigenvalues alpha,beta and residues A,-B0. Static cross mass is a=A/alpha-B0/beta. If total static kappa>=a is prescribed, add direct conductance kappa-a. This is an exact minimum for the **entire scalar cross response**, not an assertion about fixing both diagonal entries of the full port transfer matrix.

Detailed verification: write e_plus=(1,1)/sqrt(2) and e_minus=(1,-1)/sqrt(2). Since sqrt(C_i)=sqrt(2A)/alpha, the normalized boundary vectors are u=sqrt(A)e_plus+sqrt(B0)e_minus and v=sqrt(A)e_plus-sqrt(B0)e_minus. Hence u^T exp(-Qt)v=A exp(-alpha t)-B0 exp(-beta t), directly proving the entire cross response. The total capacity equals 4A/alpha^2, which matches the previously proved lower bound, so it is globally minimal even among networks with arbitrarily many states. If kappa<a, no allowed realization with this unchanged h can have total static conductance kappa, because its direct conductance would have to be negative.

### Exact numerical example

For A=1, B0=1/4, alpha=1, beta=2, prescribe h(t)=exp(-t)-(1/4)exp(-2t) and total static kappa=1. The minimum-capacity circuit is

| Component | Exact value |
|---|---:|
| C_1, C_2 | 2, 2 |
| Internal g_12 | 1 |
| g_L1, g_L2 | 3/2, 1/2 |
| g_R1, g_R2 | 1/2, 3/2 |
| Direct g_LR | 1/8 |

Its dynamic static mass is a=7/8, so the direct branch fills the prescribed kappa exactly. Its first cross moment is M=15/16, mean delay mu=15/14, and capacity excess delta=1/4. The mean-only certificate gives C_total>=15/4; the full waveform certificate improves this to C_total>=4, and the displayed circuit attains 4 exactly. This finite example demonstrates a material cost caused by the negative spectral residue, while every physical part and the time-domain cross kernel remain nonnegative.

The same exactness extends constructively to

    h=A exp(-alpha t)-sum_j B_j exp(-beta_j t),
    beta_j>alpha, B_j>0, A>=sum_j B_j,

by parallel two-state realizations B_j(exp(-alpha t)-exp(-beta_j t)) plus the balanced star (A-sum B_j)exp(-alpha t). Their combined capacity is 4A/alpha^2. No general exact characterization is claimed when signed residues have arbitrary interlacing and coefficients.

## 6. Prior-art scope

The capacity first-moment identity is closely related to known transition-path occupancy identities and standard RC moment calculations. Root literature task should supply precise TPT references. A public primary research paper giving practical context is L. Vandenberghe, S. Boyd, and A. El Gamal, “Optimizing Dominant Time Constant in RC Circuits,” IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 17(2), February 1998, pp. 110–125: https://web.stanford.edu/~boyd/papers/pdf/rc_final.pdf (browser reference turn112view0). Its abstract and Sections II–V were read. It studies convex/quasiconvex optimization of dominant time constants, allows RC meshes and more general capacitance matrices, and discusses total-capacitance/power tradeoffs. This is contextual prior art and does not establish novelty of the inequalities here; its objectives and prescribed design variables differ from our cross-response and all-topology budget bounds.

Historical status for the sharp resource-only signal inequality, its exact finite small-budget branch, and residue-based capacity minimization remains **not verified**. They are elementary spectral consequences / explicit constructions, so familiarity to circuit-synthesis specialists is plausible. Their defensible immediate value is to prevent a misleading practical interpretation of unlimited-resource Erlang limit constructions.
