# Sharp state-count bound for a scalar two-window experiment

Date: 2026 09 29. Analytic derivation; academic novelty has not been established. This is a scalar observation theorem under exact static support and equal static edge budgets, not a claim about matching the whole transfer function.

## 1. A useful class of measurement kernels

For one connected internal component, let Q be a k-by-k symmetric positive definite Stieltjes matrix, and let u,v >= 0 be its two boundary coupling vectors. Define

M(t)=u^T Q^{-1} exp(-Qt) v, a=M(0).

If a=0 its cross response vanishes. If a>0, S(t)=M(t)/a is a survival function: S(0)=1, S(infinity)=0, and its density f(t)=u^T exp(-Qt)v/a is nonnegative. A two-window experiment can be expressed as

D=a integral_0^infinity w(t) f(t) dt.

The ideal-step, no-wait kernel is w(t)=psi_h(t), where psi_h(t)=max(0,h-|t-h|), a triangle on [0,2h]. With a temperature derivative equal to the convolution of two uniforms on [0,T], ramp completion at 2T, and wait tau >= 0, it is

w(t)=E[psi_h(t+V-2T-tau)],  V=U_1+U_2, U_i uniform[0,T].

The orientation is important: the absorption-time variable t is shifted to the right by the nonnegative age 2T+tau-V. This follows by integrating the survival against the positive/negative windows, or by Fubini with the survival-density relation.

For an exponential density of rate lambda,

q(lambda)=integral w(t) lambda exp(-lambda t) dt
 = exp(-lambda tau) [(1-exp(-lambda T))/(lambda T)]^2 (1-exp(-lambda h))^2/lambda.

Use the limiting expression at T=0. Define q_* = max_{lambda>0} q(lambda), and w_* = sup_{t>=0} w(t). For the protocols here the maximum q_* is attained, since q tends to zero at both endpoints.

## 2. Universal two-state lemma

For any nonnegative measurable w for which the following integrals exist,

k=1: D <= a q_*;
k=2: D <= 2 a q_*.

Proof of k=2. If Q has equal eigenvalues, symmetry gives Q=lambda I and the density is exponential. Otherwise write its eigenvalues as 0<a_1<a_2. The normalized survival is

S(t)=c_1 exp(-a_1 t)+(1-c_1) exp(-a_2 t).

S(t)>=0 at arbitrarily large t implies c_1>=0. The nonnegative density at t=0 gives a_1 c_1+a_2(1-c_1)>=0, hence c_1<=a_2/(a_2-a_1). Therefore S is a convex mixture, with weight theta=c_1(a_2-a_1)/a_2 in [0,1], of an Exp(a_2) survival and the survival of independent Exp(a_1)+Exp(a_2).

For 0<a<=b, the density p_{a,b} of the sum of the two independent exponentials obeys the POINTWISE domination

p_{a,b}(t) <= 2 g_{a/2}(t),  g_c(t)=c exp(-ct).

For a<b put p=2b/a-1>1 and z=at/2. Then

p_{a,b}(t)/(2 g_{a/2}(t))
 = (p+1)/(p-1) [exp(-z)-exp(-pz)]
 <= (p+1)/p * p^{-1/(p-1)} <= 1.

The first maximum follows by differentiation. For the last inequality,
log p >= (p-1)/p >= (p-1) log(1+1/p).
For a=b the ratio is 2z exp(-z)<=2/e<1. Thus any nonnegative w satisfies E w(Exp(a)+Exp(b))<=2q_*. The convex mixture above gives D/a<=(1-theta)q_*+2theta q_*<=2q_*. No complete-monotonicity assumption on M is used; the second exponential residue can be negative. Q being symmetric and two dimensional, plus positivity of survival and density, is enough.

## 3. Universal k-state theorem when 3 q_* >= w_*

Assume 3q_* >= w_*. For k>=3, the elementary probability bound D/a<=w_*<=kq_* applies. Combined with Section 2,

D <= k a q_*    for every k>=1.

For the ideal-step no-wait protocol, w_*=h and q_*=h gamma_*, with

gamma_*=max_{x>0}(1-exp(-x))^2/x = 0.4072643775890738... .

Its unique maximizing x>0 solves exp(x)=1+2x, approximately 1.2564312. Since gamma_*>1/3, the condition holds.

## 4. The EXISTING finite-ramp protocol also satisfies the condition rigorously

Take T=tau=h/10, exactly as in the current experiment. The kernel is a convolution of symmetric unimodal nonnegative triangles, translated to center h+T+tau. Such a convolution attains its maximum at its center: a layer-cake proof reduces this to the fact that the overlap of two centered intervals is largest when their centers coincide. Because T<=h, the triangle does not clip at this center, and

w_* = h-E|V-T| = h-T/3 = 29h/30.

At lambda=1/h,

q(1/h)/h = exp(-.1) [(1-exp(-.1))/.1]^2 (1-exp(-1))^2.

The elementary rational bounds exp(-.1)>.9, exp(-.1)<.905, exp(-1)<.37 imply

q_*/h >= q(1/h)/h > (9/10)(19/20)^2(63/100)^2
 = 12895281/40000000,

and therefore

3 q_*/h -29/30 > 57529/120000000 >0.

For completeness: exp(.1)>1+.1+.1^2/2=221/200>200/181 gives exp(-.1)<181/200=.905. The bound exp(-.1)>.9 is the tangent inequality exp(-x)>1-x. Also exp(1)>1+1+1/2+1/6+1/24=65/24>100/37.

Consequently D<=k a q_* is rigorous for the original finite ramp; it does not depend on numerical optimization proving 3q_*>w_*.

Numerically q_*/h=0.32764158598953064..., attained at lambda*h approximately 0.9609333. q(1/h)/h=0.3274181997455673, and their ratio is 0.9993181993571155.

The optimum is uniquely global. Put x=lambda h, A=T/h>0, B=tau/h>=0, and F(x)=x/(exp(x)-1). Then

x d(log(q/h))/dx = -Bx+2F(Ax)+2F(x)-3.

F is strictly decreasing on positive arguments. The right side decreases from 1 to a negative limit, so there is exactly one zero and q has exactly one maximum. Bisection is sufficient to locate it; no local optimizer assumption is necessary.

## 5. Sharp global scalar state complexity for triangle-free static coupling

Suppose the exact static boundary response K is the Laplacian of a triangle-free graph with m edges, each of the same conductance kappa>0. Boundary capacity/direct derivative terms are excluded by using post-ramp windows. Arbitrary nonnegative direct boundary conductances and positive diagonal internal capacities are allowed. All internal components are boundary reachable and stable. Count internal temperatures, not boundary states.

Any connected internal component has a boundary neighborhood that is a clique: its inverse internal Stieltjes block is strictly positive, so every two attached ports acquire positive Schur-complement coupling. Exact zero off-diagonal entries of K prohibit a component from attaching to a non-edge. Since the graph is triangle-free, each component touches at most two boundary ports. Components touching only one port make no cross-edge contribution.

For an edge e, write components c attached to that edge, with k_c internal states and a_c=M_c(0). The exact static budget gives sum_{c at e} a_c<=kappa. In particular each a_c<=kappa. Hence the observed unweighted total cross response S=sum_{edges}D_e satisfies

S <= sum_c k_c a_c q_* <= r kappa q_*.

This improves the old r*h*kappa bound by the protocol constant q_*/h.

The bound is attained up to and including every integer r<=m: put one optimal-rate star on each of r distinct edges. A star of static conductance sigma has two spokes 2sigma, internal capacity 4sigma/lambda_*, and contributes sigma q_* to S. On that edge add direct conductance kappa-sigma. Unused edges use direct conductance kappa. Thus exact K is preserved. Use full sigma=kappa on floor(S/(kappa q_*)) edges and one partial star if necessary. No internal state is counted for sigma=0.

Therefore, for any target scalar S_target in [0,m kappa q_*] and allowed absolute error epsilon>=0, the EXACT minimum number is

r_min = ceil( (S_target-epsilon)_+ / (kappa q_*) ).

The target may be matched at its lower permitted endpoint. This result concerns only the scalar cross-edge total and exact K. It does NOT assert that the constructed model matches diagonals, individual edge transients, or the whole transfer function. Unequal edge weights/budgets do not automatically admit the same exact formula; a multi-state component on a strong edge can compete with a one-state star on a weak edge.

## 6. Apply to the existing complete-bipartite family

There are m=n^2 cross edges, kappa=lambda_0 c0/n, h=1/lambda_0, T=tau=h/10. The normalized scalar is d=S/n and the target is d_*=c0 alpha, alpha=q(lambda_0)/h=0.3274181997455673.

For |d-d_*|<=epsilon, the exact scalar-only minimum is

r_min = ceil[ n^2 (alpha-epsilon/c0)_+ / gamma ],
gamma=q_*/h=0.32764158598953064... .

At zero scalar error the continuous fraction is approximately 0.9993181993571155*n^2; at epsilon/c0=.05 it is approximately 0.8467124187172987*n^2. The count is at most n^2 because alpha<gamma. Integer ceilings must be evaluated with sufficient precision near a threshold; floating display values are not proof certificates.

## Status / limits

The two-state density domination and the kernel-height condition give an analytic proof for ideal steps and the current finite ramp. The star construction matches its lower bound exactly for this scalar criterion and uniform triangle-free static budgets. This is substantially stronger than merely finding a lower bound, but academic priority still requires a separate literature comparison. General protocols failing 3q_*>=w_*, unequal edge budgets, allowed same-side static leakage, and full-response approximation remain outside this exact theorem.
