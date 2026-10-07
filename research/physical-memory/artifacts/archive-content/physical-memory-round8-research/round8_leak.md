# Round 8 — Balanced finite-precision CP certificate

Date: 2026 09 29. Status: proved analytically below; numerical implementation checked; **academic novelty not established**. This strengthens the Round 7 leakage estimate in a useful near-balanced regime, but it is not uniformly stronger. The old and new certificates can be combined by taking the smaller justified penalty.

## 1. Main theorem: replace square-root trace sensitivity by a balanced collective measurement

Let `D=F^T F` with `F>=0` having `r` rows, and split its columns into nonempty groups `U,V`. Define

- `S = sum_{i in U,j in V} D_ij` (each cross pair once),
- `A_U=1_U^T D 1_U`, `A_V=1_V^T D 1_V`,
- `W_U=sum_{i!=j in U}D_ij`, `W_V=sum_{i!=j in V}D_ij` (ordered sums),
- given cross-entry upper bounds `D_ij<=b_ij`, `B_r` is the sum of the `min(r,|U||V|)` largest `b_ij`.

For any `theta>0`, put

`W_theta=theta W_U+theta^{-1}W_V`,

`I_theta=theta A_U+theta^{-1}A_V-2S = x_theta^T D x_theta >=0`,

where `x_theta=sqrt(theta)1_U-theta^{-1/2}1_V`.

Then

**`S <= B_r + W_theta + sqrt(I_theta W_theta)`.**

For a uniform cap `b`, the simpler consequence is `S<=r b+W_theta+sqrt(I_theta W_theta)`.

In particular, when `D(1_U-1_V)=0`, hence `I_1=0`,

**`S <= B_r + W_U+W_V`.**

The coefficient 1 multiplying `W_U+W_V` cannot be decreased universally, even in this balanced subclass.

### Proof

It suffices to prove the unscaled theorem after replacing the U columns by `sqrt(theta)` times those columns and V columns by `1/sqrt(theta)` times those columns. Cross entries and their caps do not change.

For one row write its U and V subvectors as `u,v>=0`, their sums as `a,b`, their maxima as `m,l`, and

`w_u=a^2-||u||^2`, `w_v=b^2-||v||^2`.

When `ab=0`, the row contributes zero to the cross sum and the desired inequality is immediate. Otherwise `m>=||u||^2/a=a-w_u/a`, and similarly `l>=b-w_v/b`. Therefore

`ab-ml <= (b/a)w_u+(a/b)w_v-w_u w_v/(ab)`.

If `a>=b`, this is at most `w_u+w_v+(a-b)w_v/b`, and `w_v/b<=sqrt(w_v)` because `0<=w_v<=b^2`. Exchanging the groups covers `a<b`. Thus

`ab <= ml+w_u+w_v+(a-b)_+ sqrt(w_v)+(b-a)_+ sqrt(w_u)`.

For every factor row choose a coordinate attaining each maximum and call their pair its dominant pair. At most r distinct dominant pairs occur. For any fixed pair `(i,j)`, the sum of `ml=F_ki F_kj` over rows assigned to that pair is at most `D_ij<=b_ij`. Consequently `sum_rows ml<=B_r`; repeated pairs do not cost additional capacity.

Sum the remainder over factor rows. By Cauchy–Schwarz, its last two terms together are at most

`sqrt( sum_rows(a-b)^2 * sum_rows[w_v 1_{a>b}+w_u 1_{b>a}] )`

`<= sqrt( I_1 (W_U+W_V) )`.

Also `sum_rows w_u=W_U`, `sum_rows w_v=W_V`. This proves the theorem. □

### Sharpness and relation to the old bound

Take one factor row with `u=(1,0,...)` and `v=(1/k,...,1/k,0,...)`. Then `a=b=1`, `S=1`, `B_1=1/k`, `W_U=0`, `W_V=1-1/k`, so equality holds. The old correction in this example is `sqrt(1-1/k)`, larger than the new `1-1/k`.

The coefficient 1 on the square-root correction is also dimension-uniformly optimal for this form: take `u=(a,0,...)`, `v=(b/k,...,b/k)`, with `a>b>0`. Writing `p=1-1/k`, the excess after subtracting `B_1+W` is `p b(a-b)`, while `sqrt(I W)=sqrt(p)b(a-b)`. Their ratio tends to 1 as k grows. This is a sharpness claim about these two universal coefficients, not a claim that the entire inequality is the best bound for every fixed dataset.

For nearly balanced data where normalized imbalance and leakage are both of size `eta`, the new penalty is `O(eta)`. The old bound generally contributes `O(sqrt(eta))` through the diagonal trace. If imbalance is large, the new bound may be worse, so there is no claim of uniform dominance.

Any positive boundary scaling `P D P` also preserves CP-rank; the same theorem then applies to weighted cross sums and weighted within sums. A useful finite family of scalings may improve a certificate. Claiming efficient global optimization over all scalings would need additional analysis. The two-group parameter theta can simply be tested at chosen positive values; every individual value is valid.

## 2. Direct finite-precision version

Suppose measurements/calibrations guarantee

`S>=S_low`, `W_theta<=W_up`, `I_theta<=I_up`, and `D_ij<=b_ij^up`.

Assume `W_up,I_up>=0`. Every r-state CP model consistent with the intervals obeys

**`B_r^up >= S_low-W_up-sqrt(I_up W_up)`.**

If the right side is positive, sort the cross caps and find the first cumulative sum at least that value. This gives an integer state lower bound. For a uniform `b_up>0`,

`r >= ceil( (S_low-W_up-sqrt(I_up W_up))_+ / b_up )`,

with interval/outward rounding when an integer threshold is nearly attained. If zero caps coexist with a strictly positive required cross contribution, this is inconsistency of the model class, not an infinite-state conclusion.

I can be measured directly: apply the signed group input `x_theta` around an equilibrium and take the same signed group output; apply the existing two-window functional. This measures `x_theta^T D x_theta`. **No separate diagonal-trace measurement is needed.** The signed thermal input is a small positive/negative deviation around an operating temperature, not a negative absolute temperature.

Alternatively, an upper bound is `theta A_U^up+theta^{-1}A_V^up-2 S_low`; a negative upper bound is incompatible with CP. The direct signed experiment avoids subtraction of several large independently measured quantities.

The existing measurement and sensor assumptions remain essential: same input profile, proper specimen initialization, valid sensor compensation/error bounds, and D's CP factorization under the admitted temporal protocol.

## 3. O(log n) group probes for the within-group leakage budget

This is a measurement construction, not a claim that all information for a certificate can be learned in logarithmically many experiments. **In particular the cross-entry caps must still be independently known or calibrated.**

Give the n boundaries of one group distinct binary codewords of length L and minimum Hamming distance `d_min>0`. For bit ell, let `A_ell` be the 0-bit boundaries and `B_ell` the 1-bit boundaries. Excite `A_ell`, read the total response on `B_ell`, and use the same two-window functional, obtaining

`c_ell=sum_{i in A_ell,j in B_ell}D_ij >=0`.

For an unordered pair, its contribution appears exactly its code Hamming distance times. Hence

**`W_group <= (2/d_min) sum_ell c_ell`.**

With observed intervals `c_ell<=c_ell^up`, the same upper bound uses their upper ends. An upper end below zero is an inconsistency with the assumed nonnegative model and error bounds.

Plain binary labels require `L=ceil(log2 n)` and `d_min>=1`, so the overcount is at most L. A binary code with `d_min>=L/4` gives a factor at most 4 relative to the true W, with L=O(log n). Existence is elementary: independent random binary codewords have pairwise distance Binomial(L,1/2); Hoeffding and a union bound give failure probability at most `n(n-1)/2 * exp(-L/8)`. Taking `L>=16 log(2n)` makes this less than 1. Generate once, check the exact minimum distance, and the subsequent certificate is deterministic. No unverified probabilistic claim about the specimen is needed.

If each normalized cut `c_ell/n` has additive error at most sigma, the resulting normalized leakage upper bound accumulates at most `2 L sigma/d_min<=8 sigma` of noise. Thus this particular aggregate noise overhead does not grow with n. Correlation of errors is allowed if the individual bounds are valid; no noise cancellation is assumed.

Repeat for U and V: `2L` cut experiments, one cross collective measurement for S, and one bipolar experiment for I. The existing independently established cross caps remain a separate requirement. Static conductance cuts may also be used, with `D_ij<=h(-K_ij)` inserting a factor h.

## 4. Scaling law for the physical complete-bipartite target

Use the Round 7 normalization: 2n boundaries, target cross signal `S*=n c0 alpha`, and candidates with cross steady caps

`-K_ij<=lambda c0 (1/n+beta)`.

Suppose the experiments/calibration imply

`S >= n c0 a`, `W_U+W_V <= n c0 w`, `I_1<=n c0 zeta`.

Then

**`r >= n^2 (a-w-sqrt(zeta w))_+ / [lambda h (1+n beta)]`.**

The integer version takes the ceiling. With `beta=O(1/n)` and positive numerator independent of n, the quadratic lower bound persists despite finite leakage and finite measurement errors. In the null-mode case `zeta=0`, the leakage correction is exactly linear in w.

For entrywise same-group static leakage bounded by `lambda c0 gamma/n` in both groups, one may take

`w=2 lambda h (1-1/n) gamma`.

This is a sufficient certificate, not a universal sharp threshold. It explicitly requires per-entry leakage of order 1/n as n grows when using such a uniform entrywise hypothesis; fixed absolute entrywise precision does not guarantee an n^2 lower bound for arbitrarily large n.

## 5. Matching order obstruction: 1/n leakage can permit n states

There is a simple physical construction showing why the leakage issue is substantive.

Take n internal nodes. Each internal node i connects to its unique U boundary with conductance `2 lambda c0` and to every V boundary with conductance `2 lambda c0/n`. Give every internal node capacity `4 c0`. There are no internal–internal edges or direct boundary edges. Then total capacity is `4 n c0`, and every boundary has total incident conductance `2 lambda c0`, the same resource scaling as the original n^2-state target.

Its single-pole factor is

`F=sqrt(c0)[I_n | J_n/n]`,

so

`H=c0 [[I,J/n],[J/n,J/n]]`,

`K=lambda c0 [[I,-J/n],[-J/n,2I-J/n]]`.

The full cross-block transfer function is **identical at every frequency** to the original n^2-state target. Also the bipolar transient observable is zero (`H(1_U-1_V)=0`). The U–U off-diagonal steady entries remain zero; V–V off-diagonal steady entries become `-lambda c0/n`.

For the two-window matrix `D=alpha H`,

`S=n c0 alpha`, `W_U=0`, `W_V=(n-1)c0 alpha`, `I=0`, `b=c0 alpha/n`, `B_n=c0 alpha`.

Thus the new CP inequality is exact:

`S=B_n+W_V`.

The candidate's cp-rank and physical state count are exactly n, since its U block has rank n. This construction shows that permitting same-group couplings of size 1/n can collapse n^2 to n **if the retained observations are cross response plus the balanced null mode**.

**Limitations:** This candidate does not preserve the V diagonal response or its V–V collective response. Its diagonal steady discrepancy is `lambda c0(1-1/n)` and its full operator discrepancy is not vanishing. It does not contradict a certificate which additionally constrains those observables tightly. It is not a matching upper construction for every error metric in Round 7.

## 6. Verification

`round8_leak_verify.py` checks 5000 random nonnegative factors with variable sizes, sparsity, large coefficient ranges, and positive group scalings. Maximum normalized excess of the left side over the right side was 1.12e-16. Five sharp examples and four physical transfer examples were also checked. Cross transfer errors were below 1.2e-16. The JSON is `round8_leak_verify.json`.

Finite numerical checks do not replace the analytic proof or determine novelty. Particularly relevant prior-art targets are CP-rank bounds for matrices near bipartite support, approximate nonnegative factorizations/rectangle covers, and coded group measurements of nonnegative quadratic forms. The dominant-coordinate proof is elementary enough that independent rediscovery is a material possibility.
