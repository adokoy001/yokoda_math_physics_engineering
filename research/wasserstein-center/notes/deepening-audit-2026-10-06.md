# E02 deepening: audit-ready mathematical kernel
Date: 2026 10 06. Scratch research memo; not a user-facing saved artifact.

## Sources read and provenance

The attached 2026 09 08 project ledger was read. The full current E02 HTML was fetched from https://nikki.yokoda.okinawa/works/wasserstein-center/ using curl after the web retrieval service returned inaccessible. It is byte-identical (SHA256 e661f2a5f421372075d96f52de9bae33b78ae5046ae9e289b278213ef088a0b0) to root's Library download at `research_sources/wasserstein-center.html`. All three existing proofs were read.

Primary prior art newly opened:
- Tsang, Kwok, Cheung, “Very Large SVM Training using Core Vector Machines”, AISTATS 2005, https://proceedings.mlr.press/r5/tsang05a/tsang05a.pdf . Sections 3.1–3.2, equations (2)–(5), explicitly convert constant-diagonal-kernel minimum enclosing balls to minimum-norm convex combinations. Thus the abstract sphere/convex-hull reduction is established geometry, not a claimed discovery.
- Wang, Li, Yang, Ding, “Finding Wasserstein Ball Center: Efficient Algorithm and The Applications in Fairness”, ICML 2025, https://proceedings.mlr.press/v267/wang25be.html . Finite input-distribution minimax centers and fairness applications give concrete evidence of demand. Our infinite moment class and analytic constrained-variance formula are different problem data. No claim their paper solves our particular class.
- Existing E02 already cites Pass, Stoyan, Hürlimann etc.; their attributions are preserved, not claimed as new.

## 1. Abstract Hilbert kernel (known geometric principle; self-contained proof)

Let H be a real Hilbert space, A a nonempty subset of the sphere {a: ||a||=r}, r>0, and K=closed convex hull(A). Let p be the unique minimum-norm point of K, d=||p||. Then

(1) <p,a> >= d² for every a in A;
(2) inf_A <p,a> = d²;
(3) F(x):=sup_A ||x-a||² >= r²-d²+||x-p||²;
(4) F(p)=r²-d².

Proof: projection onto K gives (1). Linear functionals have the same infimum on A and K, giving (2). For any x, inf_A <x,a> <= <x,p>, because p∈K. Hence F(x)=r²+||x||²−2inf_A<x,a> >= r²+||x||²−2<x,p>, which is (3). At x=p, (2) gives (4). Thus p is the unique unconstrained center. No compactness of A or finite support for a barycentric measure is needed.

If d>0 and rho>0, the constrained problem ||x||=rho has unique center

x_rho = (rho/d) p,
R_rho² = r²+rho²−2rho*d.

For every ||x||=rho,

F(x)−R_rho² >= (d/rho)||x−x_rho||².

Indeed inf_A<x,a> <= <x,p> <= rho*d. At x_rho, projection inequality realizes equality in the lower bound. For the stability claim use ||x−x_rho||²=2rho²−2(rho/d)<x,p>. The farthest points at x_rho are exactly {a∈A:<p,a>=d²}, independent of rho>0. For rho=0 the feasible set is {0}; all a are farthest. If d=0, the normalized construction is undefined and is NOT asserted. Our E02 nondegenerate case has d>0.

## 2. New explicit consequence: representative with prescribed variance

Fix 0<mu<1 and 0<v<M:=mu(1−mu). Let A be the centered quantiles q=f_P−mu for all P supported on [0,1] with mean mu and variance v. Define

L=log(M/v), kappa=2/(2+L),
H(u)=min{mu*u,(1−mu)(1−u),sqrt(v*u*(1−u))}.

Existing E02 proves p=−kappa H', ||p||²=kappa*v, and p∈closed convex hull(A). The latter is explicit in its probability measure over two-point input quantiles. Also <p,q>≥kappa*v for every q∈A. These are the only substantive dependencies on the original E02 calculation.

For any prescribed representative variance w>0, among all real-line probability measures Q with mean mu and variance w, the unique minimax representative is

f_{Q_w}(u)=mu−sqrt(kappa*w/v) H'(u),
R_w² = v+w−2sqrt(kappa*v*w).

The centered function is nondecreasing, mean zero, and has norm sqrt(w), so it is a valid quantile even without a support constraint. Thus the abstract lower bound is attained in the actual quantile domain; relaxation to all Hilbert vectors loses nothing.

If 0<w<=v/kappa, the representative is supported in [0,1] too. This follows from −mu<=−H'<=1−mu and t:=sqrt(kappa*w/v)<=1: f_Q=mu+t(f_S−mu), with f_S=mu−H'. Hence the very same formula is optimal even when [0,1] support is required. For w>v/kappa the unconstrained-support formula remains valid, but this proof does NOT solve the bounded-support problem. v/kappa<M for nondegenerate v, since x(1−0.5log x)<1 for 0<x<1.

For w=0, the only mean-mu candidate is delta_mu, and R_0²=v. No farthest-point classification from the positive-w case is carried over to w=0.

### Principal solved extension: require Q itself to be an admissible input

Set w=v. The proposed representative D has

f_D=mu−sqrt(kappa)H',
Var(D)=v,
R_D²=2v(1−sqrt(kappa)).

It is supported in [0,1], so D∈K_{mu,v}. Therefore it uniquely solves the natural relative-center problem

min_{Q∈K_{mu,v}} max_{P∈K_{mu,v}} W2(P,Q)².

This closes one of the attached ledger's explicit open extensions. It is a new derivation within the project. Its broader literature novelty is NOT established. Best classification: “explicit corollary of the existing E02 theorem and standard Hilbert geometry; same specific formula not found in the limited search”.

For w>0, farthest distributions are unchanged from E02: all two-point admissible inputs, and all admissible distributions supported on {0,c,1}, and only those. For any Q with the required mean/variance,

max_P W2(P,Q)²−R_w² >= sqrt(kappa*v/w) W2(Q,Q_w)².

At w=v this coefficient is sqrt(kappa). In particular, excess squared risk epsilon gives W2(Q,D)<=kappa^(−1/4)*sqrt(epsilon).

The penalty for keeping the input variance is exact:

R_D²−R_C² = v(1−sqrt(kappa))²,
R_D²/R_C² = 2/(1+sqrt(kappa)) (nondegenerate case).

Thus keeping variance increases worst squared error by a factor strictly between 1 and 2, not more. Ratios at v=0 or M are undefined and should not be written as literal ratios there.

The full prescribed-variance tradeoff can be written

R_w² = v(1−kappa)+(sqrt(w)−sqrt(kappa*v))².

If representatives may have variance in an interval [wL,wU], the optimal w is the clipping of kappa*v to this interval. The displayed quantile solves the support-constrained problem as well when that selected w<=v/kappa. This is an exact variance-versus-robust-error design curve.

## 3. Moment uncertainty: independently proved usable outer-ball certificate

Write K_v for the above distribution family, now allowing v∈[0,M]. For any P∈K_s and target variance t∈[0,M], there exists Q∈K_t such that

W2(P,Q) <= { sqrt(s)−sqrt(t), if t<=s; sqrt(t−s), if t>=s }.

Proof when t<=s: for s>0 use Y=mu+sqrt(t/s)(X−mu). Its support stays in [0,1], mean is mu, variance t, and the coupling cost is (sqrt(s)−sqrt(t))². If s=t=0, take Q=P.

Proof when t>=s: for s<M let B|X be Bernoulli(X), and independently J be Bernoulli(lambda) with lambda=(t−s)/(M−s). Put Y=X when J=0 and Y=B when J=1. Then E[Y|X]=X, E Y=mu, Var(Y)=s+lambda(M−s)=t, and E(Y−X)²=lambda*E[X(1−X)]=t−s. If s=t=M take Q=P.

Consequently d_H^{W2}(K_s,K_t)<=sqrt(|s−t|). This is an elementary coupling consequence; no claim of sharpness for interior s,t, nor of literature novelty.

More usefully, if true variance is only known to lie in [a,b]⊂[0,M], then for any nominal v0∈[a,b], the EXACT E02 center C_{v0} yields the certified enclosure

union_{s∈[a,b]} K_s ⊂ B_W2(C_{v0}, R_{v0}+Delta(v0)),
Delta(v0)=max{sqrt(v0−a), sqrt(b)−sqrt(v0)}.

At v0=0 or M interpret C and R by the original degenerate formulas. The one-sided Delta is tighter than a symmetric sqrt(max(|v0−a|,|b−v0|)) bound. Proof: map every P to some Q∈K_{v0} by the preceding construction and apply triangle inequality. The scalar v0 can be numerically minimized for the tightest member of this family of certificates.

This is a guaranteed enclosure, NOT the exact Chebyshev center/radius for variance intervals. The exact interval problem remains a worthwhile next target. If the variance interval came from a valid statistical confidence statement, the enclosure inherits the same event; the construction itself does not estimate mean/variance or fabricate coverage.

For any Lipschitz loss ell with constant L_ell, this ball yields |E_P ell−E_C ell|<=L_ell*(R+Delta), using W1<=W2. This supplies a legitimate robust-expectation use. It does not show that choosing C gives the optimal action in an arbitrary downstream decision problem.

## 4. Ranking within E02

1. **Preserve representative variance / full variance tradeoff**: closed now with analytic proof; practical if a benchmark or simulator must preserve measured dispersion. Clear finite deliverable, moderate potential novelty as a specific corollary; abstract ingredient known.
2. **Input variance interval / finite-sample use**: greater practical need, exact solution still open in this project. We now have a certified outer ball with no optimization over distributions, which can be used immediately. Next compare with convex-optimization certificates and determine the exact interval center.
3. **Near-extremizer stability**: original note's deficit identity may quantify distance to the two/three-atom equality class. Likely mathematically more difficult and potentially interesting. Do not infer rate from qualitative compactness alone; boundary degeneracies matter.
4. **Higher-dimensional analogue**: demand exists, but 1D quantile Hilbert isometry fails and covariance does not determine transport geometry. Avoid advertising current formula as a multivariate result.

Suggested root-facing headline: “同じ平均・分散を保つ最適代表という未処理の問いは、既存結果を球面幾何として読み直すことで解けた。さらに分散に推定誤差を許す場合にも、証明付きの安全な包含半径を出せる。” Explicitly say this is a project-level solved extension, not a famous open problem or globally established new theorem.
