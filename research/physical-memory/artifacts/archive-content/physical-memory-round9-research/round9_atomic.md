# Round 9 — Sharp stability of nonnegative latent structure under aggregate balance

Date: 2026 09 29. Analytic result proved below. Academic novelty remains unestablished; largest-coordinate rounding has explicit precedent in orthogonal NMF error-bound literature.

## 1. Main theorem

Let D=FᵀF be completely positive with F≥0 and at most r rows. Partition the N columns into k≥2 nonempty groups G₁,…,Gₖ, of arbitrary sizes. Put

W = Σ_g Σ_{i≠j in G_g} D_ij,

I = Σ_{g<h} (1_{G_g}−1_{G_h})ᵀD(1_{G_g}−1_{G_h}) ≥ 0.

Here within-group sums are ordered. Define ||E||_{entrywise 1}=Σ_ij |E_ij|.

There exists D₀=F₀ᵀF₀ such that:

1. F₀≥0 has at most r rows, so cp-rank(D₀)≤r.
2. Each row of F₀ has at most one nonzero coordinate in each group. Equivalently its support is a clique of the complete multipartite graph. In particular, D₀ has zero within-group offdiagonals.
3. 0≤D₀≤D **entrywise**.
4. The dimension-independent bound is

**||D−D₀||_{entrywise 1} ≤ (2k−1/2)W + 2√((k−1)IW).**

The constants 2k−1/2 and 2√(k−1) are individually optimal for universal inequalities of the displayed form that retain the factor budget and entrywise domination. Sharpness is already visible for r=1.

In particular, if D annihilates every group-difference vector, then I=0 and

**||D−D₀||_{entrywise 1} ≤ (2k−1/2)W.**

The constant does not depend on N, the number of factors, the group sizes, or the total signal amplitude. For two groups it is 7W/2. This is a statement about closeness of the entire Gram matrix, stronger in scope than a single scalar rank certificate.

### Balance is measurable, not an assumption on an unknown factor

Let A_g=1_{G_g}ᵀD1_{G_g}, and S=Σ_{g<h}1_{G_g}ᵀD1_{G_h}. Then

I=(k−1)Σ_g A_g−2S = kΣ_g A_g−1ᵀD1.

Moreover I=0 is equivalent to D(1_{G_g}−1_{G_h})=0 for every g,h, since D is PSD. It also implies that each nonnegative factor row has equal total mass in all groups. The theorem requires balance of group sums, not averages; weighted versions follow by applying it to P D P for a positive diagonal P.

## 2. Constructive proof

Take any admitted F, and in each row and each group retain only one largest coordinate. Call the resulting matrix F₀. Then 0≤F₀≤F, whence 0≤D₀≤D entrywise, and all structural and factor-count assertions hold.

For one factor row, let its subvector in group g have sum a_g, maximum m_g, and within-group leakage

w_g=a_g²−||f_g||₂².

All are nonnegative, and w_g≤a_g². Also

m_g≥||f_g||₂²/a_g=a_g−w_g/a_g

when a_g>0. The squared mass discarded from this group is at most w_g/2: each discarded coordinate x satisfies x²≤m_g x, whereas w_g includes twice every product of m_g and a discarded coordinate.

For two groups with sums a≥b>0, maxima m,l, and leakages u,v, multiply the lower bounds for maxima to obtain

ab−ml ≤ (b/a)u+(a/b)v−uv/(ab)
          ≤ u+v+(a−b)v/b
          ≤ u+v+(a−b)√v.

If a<b, interchange the groups; if ab=0, the cross loss is zero and the bound is immediate. Therefore the loss in an unordered cross block is bounded by the two leakages plus the difference of group sums times the square root of the leakage of the smaller-sum group.

Sum this inequality over all rows and unordered group pairs. The leakage terms sum to (k−1)W. By Cauchy–Schwarz, the imbalance terms are at most

√[ (Σ_rows Σ_{g<h}(a_g−a_h)²)
    (Σ_rows Σ_{g<h} w_{smaller-sum group}) ]
≤ √((k−1)IW),

because any w_g is selected at most k−1 times. Thus, writing S₀ for the total unordered cross mass of D₀,

**0≤S−S₀≤(k−1)W+√((k−1)IW).**

The full entrywise Gram loss consists of the discarded diagonal mass (at most W/2), all within-group offdiagonal mass (exactly W), and twice the unordered cross loss. Adding proves

||D−D₀||_{entrywise 1}≤W/2+W+2(k−1)W+2√((k−1)IW).

This is the claimed formula. □

## 3. Sharp constants

### Linear coefficient

Use one factor row. In k−1 groups the row has the single entry 1. In the final group it has two entries 1/2,1/2. Every group sum is 1, so I=0; W=1/2. The total sum of D is k².

Every entrywise dominated rank-one CP D₀ with multipartite support is ggᵀ, with at most one coordinate per group and g_i≤f_i by diagonal domination. Therefore its total entry sum is at most (k−1/2)². The minimal loss is

k²−(k−1/2)²=k−1/4=(2k−1/2)W.

Consequently no smaller coefficient than 2k−1/2 works even if one replaces our explicit rounding by the best admissible approximation.

### Square-root coefficient

Use k−1 singleton groups with entry A, and a final group of m equal entries b/m. Then

W=b²(1−1/m),
I=(k−1)(A−b)².

The best dominated rank-one approximation retains the singleton groups and one of the m entries. Its loss is

[(k−1)A+b]²−[(k−1)A+b/m]².

Let A/b→∞. Dividing the loss, less any fixed multiple of W, by √(IW) yields

2√(k−1)√(1−1/m).

Let m→∞. Thus 2√(k−1) is necessary as the coefficient of √(IW).

## 4. A robust clique-cover capacity corollary

Suppose upper bounds D_ij≤b_ij are known for intergroup pairs. Let C_r(b) be the largest total edge capacity in a union of at most r transversal cliques, counting each edge only once. Then

**S≤C_r(b)+(k−1)W+√((k−1)IW).**

Proof: D₀'s cross support lies in a union of at most r selected cliques, and D₀≤D≤b on the cross entries. Therefore S₀≤C_r(b). Combine with the cross-loss bound above.

For k=2, each transversal clique contains one edge; C_r is the sum of the largest min(r,|G₁||G₂|) caps. This recovers the Round 8 sorted-capacity certificate. For more groups, C_r is a combinatorial maximum-coverage quantity; this note does not claim an efficient exact algorithm. Uniform cap b yields the weaker explicit bound C_r≤r choose(k,2)b.

Both coefficients k−1 and √(k−1) in the cross-loss inequality are sharp by the same rank-one examples. The capacity corollary is also exact on their D-entry caps.

## 5. Distance characterization and limitations

Let δ_r(D) be the smallest entrywise-1 distance to a CP matrix with at most r factors, zero within-group offdiagonals, and entrywise dominated by D. The theorem gives

W≤δ_r(D)≤(2k−1/2)W+2√((k−1)IW).

The lower bound is immediate from the entries that must become zero. Under exact aggregate balance, leakage is therefore equivalent to distance from the multipartite support class, with dimension-independent constants, while preserving the number of latent factors.

The theorem is constructive **given a CP factorization**. It does not provide a generally efficient method to find one from D, or a polynomial-time CP-rank algorithm.

It gives **entrywise domination, not PSD/Loewner domination**. In general D−D₀ is indefinite: retaining one coordinate of a positive rank-one vector and dropping another produces a 2×2 error minor [[0,xy],[xy,y²]] with negative determinant. Nor does D₀ generally preserve the exact aggregate balance of D. It preserves the target zero pattern and factor budget.

Without balance, no bound δ_r(D)≤C W with universal C is possible. For two groups take f=(1 | ε/2,ε/2). Then W=ε²/2, while the minimal dominated rank-one Gram loss is ε+3ε²/4. The ratio diverges as ε→0. This shows why the imbalance term is structurally necessary.

The result applies directly to CP observation matrices produced by the existing admissible RC measurement protocols. Applying it to whole transfer functions, passive system realizations, arbitrary kernels, or non-CP data would require separate arguments. No such extension is asserted here.

## 6. Primary literature comparison and novelty status

The largest-entry-per-row rounding operation is already present in orthogonal nonnegative factorization error bounds. Chen, He and Zhang, *Tight Error Bounds for the Sign-Constrained Stiefel Manifold*, arXiv:2210.05164v7, §3.2 Lemma 7 and Remark 2, explicitly derive a squared factor-distance bound from offdiagonal Gram mass and attribute the same rounding to an earlier exact-penalty procedure. Their principal bounds concern factor distance to normalized nonnegative Stiefel constraints, with square-root behavior in the general case. Our candidate concerns the **Gram-matrix entrywise loss**, multiple groups, aggregate balance, the fixed factor budget, and sharp constants.

Primary full text checked: https://arxiv.org/html/2210.05164v7 (Lemma 7, lines 318–347 in retrieved text; Theorems 4–5 nearby). Search reference available to parent: turn62view0 / turn64view0. The parent should open the URL itself before citing in a final user response.

Fan and Zhou, *The CP-Matrix Approximation Problem* (2016; arXiv:1411.0795), treat projection onto CP matrices with linear constraints through semidefinite/moment methods. This is adjacent projection literature, not evidence that our fixed-factor-budget sharp stability estimate is new. Full PDF opened: https://arxiv.org/pdf/1411.0795 (turn62view2).

Korda, Laurent, Magron and Steenkamp, *Exploiting ideal-sparsity in the generalized moment problem with application to matrix factorization ranks* (2024), is already referenced in Round 7 and establishes the relevance of exact clique support to CP-rank bounds. The zero-leakage combinatorial structure is therefore established prior art.

Searches on 2026 09 29 did not identify our exact multipartite balanced Gram bound. This is only a bounded literature comparison, not a proof of novelty. Assessment: **a compact reusable lemma/theorem candidate worth recording; its central rounding mechanism is known, and academic novelty requires specialist review and deeper comparison.**

## 7. Verification performed

`round9_atomic_verify.py` is dependency-free. It checked 600 randomly generated CP factorizations (k=2,…,6; balanced and unbalanced groups; varying sparsity; coefficient range 10⁻³,…,10³), with explicit Gram matrices and direct computation of aggregate observables. Maximum normalized bound violation was 0. Eight exact sharpness cases k=2,…,9 were verified with rational arithmetic. Results are in `round9_atomic_verify.json`. These checks support implementation consistency; the proof above is the mathematical justification.

## 8. Conservation-preserving approximation under exact balance

The preceding sharp 2k−1/2 theorem preserves the zero pattern and factor budget but not the exact balance nullspace. If that conservation law must also survive, there is a second theorem with its own sharp coefficient.

Assume I=0. Then there exists a matrix D♭ satisfying all of the following:

- D♭ is CP with at most r factors.
- Every factor is a nonnegative multiple of the indicator vector of a transversal: exactly one chosen coordinate from each of the k groups (unless the factor is zero).
- 0≤D♭≤D entrywise.
- D♭(1_{G_g}−1_{G_h})=0 for every g,h; all group-balance conservation laws survive.
- **||D−D♭||_{entrywise 1}≤(3k²/2)W**, with the coefficient 3k²/2 optimal universally under the given factor budget and entrywise domination.

### Proof

For a factor row, exact aggregate balance forces its group sums all to equal some a≥0. Let m_g be the largest coordinate in group g and t=min_g m_g. Select one maximizing coordinate in each group, set all k selected amplitudes to t, and set all other coordinates to zero. This is componentwise at most the original row and is exactly balanced.

Choose a bottleneck group j with m_j=t. As in the first proof, its discarded squared mass is at most w_j/2, so

a²−t² = w_j+(||f_j||₂²−m_j²) ≤ 3w_j/2.

The entrywise Gram loss from this row is exactly

(ka)²−(kt)² = k²(a²−t²) ≤ (3k²/2)w_j ≤ (3k²/2)Σ_g w_g.

Summing over factor rows proves the assertion without increasing their number.

For sharpness use the same rank-one example: k−1 singleton groups with entry 1 and the final group with two entries 1/2,1/2. Any dominated rank-one balanced transversal core must use the same amplitude in every selected group, and this amplitude is at most 1/2. Its retained total Gram mass is at most k²/4; the lost mass is at least 3k²/4. Since W=1/2, the ratio is exactly 3k²/2. □

### Interpretation

An exactly balanced nonnegative latent Gram model with small within-group leakage is close to the Gram matrix of a **weighted k-partite hypergraph incidence matrix**, with no increase in the number of latent factors/hyperedges. Each hyperedge picks one coordinate from each group. For k=2 the core is a weighted bipartite signless Laplacian, i.e. a sum of atoms t²(e_i+e_j)(e_i+e_j)ᵀ. Its balance null vector has opposite signs on the two sides.

This is an abstract structural approximation theorem: conservation plus small forbidden interactions forces proximity to a combinatorial model. Its proof is elementary. It should not be described as an entirely new theory, and its exact novelty still requires comparison with CP-cone facial error bounds and normalized factor rounding.
