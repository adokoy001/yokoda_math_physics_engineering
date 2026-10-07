# Independent audit of Round 9 abstract claims

Date: 2026 09 29. This audit checks mathematical validity and independent calculations. It does not establish academic priority.

## Verdict

Both main statements pass independent analytic audit:

1. For a normalized cross transient of a k-state symmetric positive definite Stieltjes system, one common probability mixture of exponentials dominates the density pointwise with the sharp universal multiplier

   C_k = k^k exp(1-k)/(k-1)!.

   Consequently every nonnegative measurement kernel obeys the same multiplier. The constant is optimal as a supremum even within physical two-terminal positive RC/thermal networks of any fixed positive static conductance.

2. For a completely positive Gram matrix with at most r factors and p column groups, largest-coordinate rounding gives a dominated Gram matrix with the same factor budget and zero within-group offdiagonals, with

   ||D-D0||_(entrywise 1) <= (2p-1/2) W + 2 sqrt((p-1) I W).

   Both displayed coefficients are separately sharp in the specified class. Its construction need not preserve balance and need not be realizable by an RC network. Its domination is entrywise, not Loewner order.

No correction to the two proof notes was required.

## Kernel theorem: audited proof dependencies

The principal dependency is genuinely a published theorem: Laurent Miclo, *On absorption times and Dirichlet eigenvalues*, ESAIM: Probability and Statistics 14 (2010), 117–150, Theorem 1.2, printed p.120; full proof in Section 5. Primary open-access full text:
https://www.numdam.org/item/10.1051/ps%3A2008037.pdf

It represents a reversible k-transient-state absorption time as a positive mixture of sums of at most k exponentials. The same source specifically warns that real eigenvalues alone do not ensure a representation using at most k phases for general nonreversible chains. Preserve the reversible hypothesis.

For irreducible Q, h=Q^-1 v is strictly positive. With H=diag(h), T=-H^-1 Q H, alpha_i=u_i h_i/a and beta_i=v_i/h_i, direct multiplication verifies:

- alpha is a probability vector;
- T has nonnegative offdiagonals and row sum -beta;
- h_i^2 T_ij=h_j^2 T_ji;
- alpha^T exp(Tt) beta=u^T exp(-Qt)v/a.

If Q is reducible, first separate its irreducible diagonal blocks. Blocks with zero cross normalization contribute zero, and the positive-normalization blocks are mixed with weights a_block/a. This removes the only potential h_i=0 division problem.

For j independent unit exponentials, their sum R and normalized proportions P are independent Gamma(j,1) and Dirichlet(1,...,1). Thus a sum of j possibly different-rate exponentials is a scale mixture of Gamma(j) laws. The ratio of Gamma(j,rho) density to Exp(rho/j) density is maximized at rho*t=j, where it equals C_j. Monotonicity follows from

C_(j+1)/C_j=(1+1/j)^(j+1)/e > 1.

The measure of exponential rates can be chosen independently of t and of the eventual kernel w. This matters: the conclusion is stronger than choosing a different best exponential at every observation time.

For sharpness, Q_epsilon=I-epsilon*A_path is symmetric positive definite for 0<epsilon<1/2. The endpoint exponential and resolvent entries have first nonzero order epsilon^(k-1), and their ratio tends to Gamma(k,1) density on compact time intervals. Every probability mixture of exponentials g satisfies g(k)<=1/(e*k); the limiting density therefore forces the multiplier C_k. Shrinking positive rectangle kernels gives sharpness for the integral inequality as well.

The physical construction with z=Q^-1(u+v), C_i=z_i^2, g_ij=-Q_ij z_i z_j, g_iL=z_i u_i, and g_iR=z_i v_i satisfies the exact internal Laplacian identity L_II=diag(z) Q diag(z). Its Schur-complement conductance is a=u^T Q^-1 v. Multiplying ALL conductances and capacities by kappa/a keeps Q and the normalized density unchanged while changing static conductance to kappa. Scaling conductances alone would not have preserved Q; the current proof correctly scales both.

## Multipartite Gram theorem: audited estimates

For one factor row and one group, sum a, maximum m, and leakage w=a^2-||f||_2^2 give m>=a-w/a. Also the discarded diagonal square mass is at most w/2, because every discarded coordinate x<=m and w includes twice m times every such coordinate.

For group sums a>=b>0 and corresponding leakages u,v,

ab-ml <= (b/a)u+(a/b)v-uv/(ab)
      <= u+v+(a-b)*v/b
      <= u+v+(a-b)*sqrt(v).

The final inequality uses v<=b^2. It is valid even for groups with arbitrarily many coordinates; zero-sum groups are handled separately. Cauchy–Schwarz across all factor rows and all unordered group pairs bounds the extra term by sqrt((p-1) I W). The factor p-1 arises because each group leakage can be chosen as the smaller group's leakage in at most p-1 pairs.

The full Gram loss equals the diagonal loss, plus W, plus twice the unordered cross-block loss. The coefficient therefore is 1/2+1+2(p-1)=2p-1/2. Ordered versus unordered sums are used consistently in the note.

The rank-one examples indeed force the coefficients even after optimizing over all admissible D0: entrywise diagonal domination forces the surviving factor coordinate to be no larger than its original coordinate; support constraints permit at most one coordinate per group. Hence largest-coordinate rounding is actually optimal in those examples.

## Independent reproducible checks

Run the standard-library-only file:

    python3 research_work/round9_audit_check.py

It writes `round9_audit_check.json` and passed:

- Exact Fraction arithmetic verifies the Doob transform, reversibility, physical Laplacian, both terminal static diagonal entries, and conductance normalization for path sizes 1 through 9.
- A 65-decimal-digit positive walk series independently checks endpoint densities, avoiding cancellation from small spectral residues. For k=2,3,5,8,12, epsilon decreasing from .2 to .001 approaches the predicted C_k; final ratio is above .999999 for every tested k.
- 1,200 exact-rational random multipartite Gram examples check the diagonal estimate and both cross/full loss estimates. The sample covers up to 7 groups, up to 5 factors, unequal group sizes, zeros and scales from 10^-3 to 10^3. In 128 examples the square-root term was needed to satisfy the displayed full estimate.
- Exact-rational equality examples verify the linear coefficient for p=2 through 12.
- Separate rank-one limits approach the square-root coefficient for p=2,3,5,10.
- Stable logarithmic evaluation checks the Gamma envelope over a wide time grid and C_k monotonicity for k up to 300.

Finite tests supplement the analytic proofs; they are not a proof of novelty, a formal proof assistant certificate, or evidence of a general signed-kernel/nonreversible extension.

## Final audit: exact fixed-kernel variational reduction

The later additions to `round9_kernel.md` and `round9_weighted.md`, Section 7, also pass.

For nonnegative measurable w, let q_j(w) be the supremum of its expectation under Gamma(j,rho), rho>0, and E_k=max_(1<=j<=k) q_j. Every normalized reversible cross density is a mixture of precisely this class, proving the upper bound E_k. The path Q_epsilon=rho(I-epsilon A_path,j) gives density tending pointwise to Gamma(j,rho). Fatou yields

integral w*p_(j,rho) <= liminf integral w*f_epsilon <= supremum_over_components integral w*f.

This works for unbounded w and extended-valued integrals; no interchange of an unjustified limit and integral is needed. If q_1 is finite, the already-proved universal C_j bound ensures every E_k is finite. If q_1=0, nonnegative w vanishes almost everywhere, and the problem is trivial. For bounded signed w, the positive density sequence has total mass one and converges pointwise to a density of total mass one, so Scheffe's lemma gives L1 convergence; the variational equality extends, while the nonnegative-kernel multiplicative estimate does not automatically extend.

For a fixed weighted triangle-free static graph, assigning k_e states to each edge produces the upper sum c_e E_(k_e), since the static shares of all components on that edge add to at most kappa_e and E is nondecreasing. There are finitely many allocations for a fixed total budget r. Approximating the Erlang envelope independently on each active edge proves that the maximum allocation value V_r is exactly the network supremum. A single component per active edge suffices in this limiting construction; there is no hidden increase in total state count.

For 0<S_req<V_r, choose an actual network with statistic S_actual>S_req, scale its dynamic capacities and conductances by theta=S_req/S_actual, and fill the resulting unused edge conductance budgets with direct conductors. The statistic scales by theta, the poles stay fixed, and the entire static boundary matrix stays fixed. For S_req=0 remove all dynamic components. At S_req=V_r, a finite realization need not exist. The notes correctly preserve this distinction. Dynamic programming gives an exact finite optimization characterization once the continuous rate suprema are known; it is not by itself a numerical certification of those continuous suprema.

## Final audit: retaining exact balance

The added `round9_atomic.md`, Section 8, also passes with its sharp coefficient 3p^2/2.

When I=0, every factor row has the same mass a in each group. Retain one maximum per group but lower all retained amplitudes to t=min_g m_g. A group attaining the minimum satisfies

a^2-t^2 = w_g + discarded_diagonal_mass <= 3w_g/2.

Hence the entire row Gram loss is p^2(a^2-t^2)<=3p^2*sum_g(w_g)/2. The construction preserves the factor count, entrywise domination, the required zero pattern, and all exact group-balance null vectors. The rank-one example of p-1 singleton groups of mass 1 and one two-coordinate group (1/2,1/2) forces t<=1/2, giving exact ratio 3p^2/2. Thus both validity and universal coefficient sharpness are justified.
