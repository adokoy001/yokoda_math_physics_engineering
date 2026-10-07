# Rank gaps and islands hidden in the mean and variance

**Research note · Version 1.1 · 2026 09 09 · Exploration candidate X01**

The principal finite-sample inequality has been verified in Lean. The sharp optimization formulas and topological classifications below have mathematical proofs, with independent exact-arithmetic checks; their complete formalization remains unfinished. The file contains 14 theorem declarations, including auxiliary lemmas and two earlier four-variable examples outside X01's main results. No claim of established academic novelty is made.

<a id="en-overview"></a>
## 1. What the two moments can reveal

> **Version 1.1: response to independent review (2026 09 09).** We checked the Fable5.1 review supplied by Yokota against the exposition and formal source. This edition clarifies the effective regime, attribution, and partition statement, and adds a matrix corollary with its topological limitation. Starting from the reviewer’s numerical observation, T9 proves the path-component count in every dimension for \(1/2<\eta<1\). T9 is not Lean-formalized, and its academic priority remains unresolved.

Let \(n\ge2\), let \(x=(x_1,\ldots,x_n)\in[0,1]^n\), and write its entries in decreasing order as \(x_{(1)}\ge\cdots\ge x_{(n)}\). Define

\[
S=\sum_i x_i,\qquad Q=\sum_i x_i^2,\qquad
D=S-Q=\sum_i x_i(1-x_i).
\]

The nonnegative quantity \(D\) is zero exactly at binary vectors. With mean \(\mu=S/n\) and variance \(V=n^{-1}\sum_i(x_i-\mu)^2\), it satisfies

\[
D=n\bigl[\mu(1-\mu)-V\bigr].
\]

Thus \(D\) measures the deficit from the endpoint variance bound \(\mu(1-\mu)\), multiplied by \(n\). For a fixed noninteger sum, that endpoint bound need not be attainable by a finite vector; Section 6 accounts for the resulting positive minimum of \(D\). The question is how much this aggregate information forces the individual entries to separate.

The useful regime is **nearly binary data**, with small total defect and a sum close to a specified integer \(1\le s<n\). Write \(e=S-s\). This is not a positive-gap guarantee for broadly distributed statistical data. More precisely, the positive certificate below satisfies

\[
2D+e^2<1\quad\Longleftrightarrow\quad
0\le\mu(1-\mu)-V<\frac{1-e^2}{2n}.
\]

Thus \(|e|<1\) is necessary, and the variance must lie within \(O(1/n)\) of the endpoint bound. For a fixed finite noninteger sum \(S=m+r\), \(0\le r<1\), the actual maximum variance is \(\mu(1-\mu)-r(1-r)/n\), as shown in Section 6. Nearly idempotent self-adjoint matrices are a natural application through their eigenvalues; Section 2 states that corollary and explains why the vector topology does not transfer to the full matrix space.

For an integer \(1\le s<n\), put \(e=S-s\) and \(g_s=x_{(s)}-x_{(s+1)}\). We prove

\[
\boxed{2D+e^2+g_s^2\ge1.}\tag{1}
\]

If \(2D+e^2<1\), the largest \(s\) entries are separated from the others by a positive gap. This also prevents the identity of that top group from changing along a continuous deformation that preserves the strict inequality. Aggregate statistics certify separation; they do not identify the labels of the largest entries without observing the vector.

The note develops this observation in three directions: an exact worst-case gap under uncertainty in the sum, a constructive classification of connected components, and a small example where holes appear and disappear. All component counts concern **labeled vectors**, not vectors modulo permutation and not one-dimensional projections onto a partial sum.

<!--DIAGRAM:rank-->

<a id="en-rank-gap"></a>
## 2. A universal rank inequality, its equality cases, and stability

### Theorem 1: the square inequality for an arbitrary finite partition

Assume \(x\in[0,1]^n\). Choose any nonempty proper subset \(I\) of the index set, put \(J=I^c\) and \(s=|I|\), and choose indices attaining the boundary extrema:

\[
u=\min_{i\in I}x_i=x_a,\quad
v=\max_{j\in J}x_j=x_b,\quad g_I=u-v.
\]

Here \(a\in I\), \(b\in J\), and \(g_I\) is signed. Then

\[
\boxed{2D+(S-s)^2+g_I^2\ge1.}
\]

Neither integrality of \(S\) nor cross-ordering \(u\ge v\) is assumed for this squared statement. If \(I\) is the set of the largest \(s\) entries, then \(g_I=g_s\ge0\), and it gives (1) and

\[
g_s\ge\sqrt{\max\{1-2D-(S-s)^2,0\}}.
\]

For an arbitrary partition, the squared inequality does not imply a positive signed gap. The square-root conclusion additionally requires \(u\ge v\).

**Proof.** Write \(g=g_I\), \(e=S-s\), and define

\[
\sigma=\sum_{i\in I}(1-x_i),\qquad
\rho=\sum_{j\in J}x_j,
\]
\[
A=\sigma-(1-u)=\sum_{i\in I\setminus\{a\}}(1-x_i),\qquad
B=\rho-v=\sum_{j\in J\setminus\{b\}}x_j.
\]

Empty sums are zero. In particular \(A,B\ge0\), and \(e=\rho-\sigma\). Define

\[
T=\sum_{i\in I}(x_i-u)(1-x_i)
 +\sum_{j\in J}(v-x_j)x_j.
\]

Every summand is nonnegative by the extremum condition on its own side and the box bounds; cross-ordering is not used. The following exact identity holds:

\[
\boxed{
2D+e^2+g^2-1
=2T+2(1-v)A+2uB+(B-A)^2.
}\tag{2}
\]

For \(i\in I\), write

\[
x_i(1-x_i)=u(1-x_i)+(x_i-u)(1-x_i).
\]

For \(i\in J\), write

\[
x_i(1-x_i)=(1-v)x_i+(v-x_i)x_i.
\]

Summing gives \(D=u\sigma+(1-v)\rho+T\). Substitute \(\sigma=1-u+A\), \(\rho=v+B\), \(e=u+v-1+B-A\), and \(g=u-v\). Expanding and collecting terms gives (2). Since \(0\le u\le1\) and \(0\le v\le1\), its right-hand side is nonnegative. This proves the partition statement and, by choosing a top set, (1). This is an identity for arbitrary finite vectors, not an inference from numerical samples. ∎

### Equality and quantitative stability

If \(g>0\), then \(u\ge g\) and \(1-v\ge g\). Hence, with \(R=2D+e^2+g^2-1\),

\[
R\ge2g(A+B),\qquad
\boxed{A+B\le\frac{R}{2g}.}\tag{3}
\]

Consequently, for \(g>0\), equality in (1) holds precisely for the sorted vectors

\[
(\underbrace{1,\ldots,1}_{s-1},u,v,
\underbrace{0,\ldots,0}_{n-s-1}).\tag{4}
\]

Indeed, \(R=0\) forces \(A=B=0\); nonnegative summands then force all the indicated entries to be endpoints. Conversely, (4) makes \(A=B=T=0\), so (2) gives equality.

More generally, \(g\ge\gamma>0\) and \(R\le\varepsilon\) force the total distance of all entries other than the boundary pair from their indicated endpoints to be at most \(\varepsilon/(2\gamma)\). This estimate degenerates as the gap approaches zero. Replacing those entries by endpoints does not necessarily preserve \(S\): the change in the sum is \(A-B\).

### Corollary: a spectral certificate for a Hermitian contraction

Let \(X\) be an \(n\times n\) self-adjoint matrix with \(0\le X\le I_n\) in the operator order, and let \(\lambda_1\ge\cdots\ge\lambda_n\) be its eigenvalues. For \(1\le s<n\),

\[
2\operatorname{Tr}(X-X^2)
 +(\operatorname{Tr}X-s)^2+(\lambda_s-\lambda_{s+1})^2\ge1,
\]
\[
\lambda_s-\lambda_{s+1}\ge
\sqrt{\max\{1-2\operatorname{Tr}(X-X^2)
 -(\operatorname{Tr}X-s)^2,0\}}.
\]

**Proof.** By the spectral theorem, \(\lambda_i\in[0,1]\), \(\operatorname{Tr}X=\sum_i\lambda_i\), and \(\operatorname{Tr}(X-X^2)=\sum_i\lambda_i(1-\lambda_i)\). Apply Theorem 1 and its rank corollary to the eigenvalue vector. ∎

This immediate transfer is a useful application, rather than an independent principal theorem. The gap formulas in Sections 3 and 6 transfer in the same way. The component and hole classifications require a different model: they concern labeled coordinates, equivalently diagonal matrices in a fixed basis. Eigenvectors may rotate in the full matrix space. For example,

\[
P_\theta=\begin{pmatrix}
\cos^2\theta&\cos\theta\sin\theta\\
\cos\theta\sin\theta&\sin^2\theta
\end{pmatrix},\qquad0\le\theta\le\frac\pi2,
\]

is a continuous path from \(\operatorname{diag}(1,0)\) to \(\operatorname{diag}(0,1)\), with \(P_\theta^2=P_\theta\), trace \(1\), and defect \(D=0\) throughout. More generally, complex orthogonal projections of the same rank are unitarily conjugate, and varying the eigenphases of a unitary matrix continuously supplies a connecting path. Hence the vector count \(\binom ns\) cannot be asserted for the full matrix space. Reframing the entire note around matrices would leave the gap formulas largely intact, but would require new topological questions and proofs for the component and hole sections.

<a id="en-robust-gap"></a>
## 3. The exact gap when the sum is uncertain

Fix \(1\le s<n\), \(0\le\eta\le1/2\), and \(\delta\ge0\). Consider

\[
P_{s,\eta}=\{x\in[0,1]^n:|S-s|\le\eta\},
\qquad
F_{s,\eta,\delta}=\{x\in P_{s,\eta}:D(x)\le\delta\}.
\]

Here \(\eta\) bounds the **sum error**; the corresponding mean error is \(\eta/n\). This is a joint constraint on \(S\) and \(D=S-Q\), not an arbitrary rectangular uncertainty set in the mean and variance.

Set

\[
\delta_0=\eta(1-\eta),\qquad
\delta_c=\frac{1-\eta^2}{2}.
\]

### Theorem 2: a sharp three-branch formula

\[
\boxed{
\min_{x\in F_{s,\eta,\delta}}g_s(x)=
\begin{cases}
\dfrac{1+\sqrt{1-4\delta}}2,&0\le\delta\le\delta_0,\\[5pt]
\sqrt{1-2\delta-\eta^2},&\delta_0\le\delta\le\delta_c,\\[3pt]
0,&\delta\ge\delta_c.
\end{cases}}\tag{5}
\]

The formulas agree at shared endpoints. When \(\eta=0\), the first branch consists only of \(\delta=0\). The set is nonempty because it contains all binary vectors with \(s\) ones; compactness and continuity also ensure the minimum exists.

<!--DIAGRAM:robust-->

### Lemma: the maximum squared sum at a fixed total

For \(y\in[0,1]^N\) with \(\sum_i y_i=t\),

\[
\sum_i y_i^2\le\phi(t):=\lfloor t\rfloor+\{t\}^2,
\qquad
\sum_i y_i(1-y_i)\ge\{t\}(1-\{t\}).\tag{6}
\]

**Proof.** If two entries satisfy \(0<a\le b<1\), set \(h=\min(a,1-b)>0\) and replace \((a,b)\) by \((a-h,b+h)\). The sum stays fixed, both entries remain in the box, and the squared sum increases by \(2h(b-a)+2h^2>0\). At least one of the two entries becomes an endpoint. Repeating this finite operation leaves at most one nonintegral entry. The resulting vector has \(\lfloor t\rfloor\) ones, one entry \(\{t\}\) if this is nonzero, and zeros elsewhere. Its squared sum is \(\phi(t)\), which proves both inequalities. ∎

This packed-vector extremum is classical; see Rosenberg–Jakobsson, Appendix Lemma 3, and the finite-data formulation by Ellis [R1–R2]. Its proof is included to make the optimization below self-contained.

### Proof of the lower bounds

Let \(a=|S-s|\le\eta\le1/2\). Equation (6) gives \(D\ge a(1-a)\), including either sign of \(S-s\).

If \(0\le\delta\le\delta_0\), define

\[
b=\frac{1-\sqrt{1-4\delta}}2.
\]

Since \(t(1-t)\) is increasing on \([0,1/2]\), we obtain \(a\le b\le\eta\). Theorem 1 now yields

\[
g_s^2\ge1-2D-e^2\ge1-2\delta-b^2=(1-b)^2.
\]

As \(g_s\ge0\), this proves the first branch. For \(\delta_0\le\delta\le\delta_c\), Theorem 1 directly gives \(g_s^2\ge1-2\delta-\eta^2\ge0\). The bound \(g_s\ge0\) proves the third branch's lower bound.

### Attainment in every branch

Use \(s-1\) initial ones and \(n-s-1\) final zeros, leaving exactly two boundary entries.

For the first branch, choose \((1-b,0)\). Then \(S=s-b\), \(D=b(1-b)=\delta\), and \(g_s=1-b\).

For the second branch, put \(h=\sqrt{1-2\delta-\eta^2}\) and choose

\[
\left(\frac{1-\eta+h}{2},\frac{1-\eta-h}{2}\right).\tag{7}
\]

The condition \(\delta\ge\delta_0\) is equivalent to \(h\le1-\eta\); hence both entries lie in \([0,1]\). Their sum is \(1-\eta\), their difference is \(h\), and their defect is \((1-\eta^2-h^2)/2=\delta\). Finally, for \(\delta\ge\delta_c\), the same construction at \(h=0\) has an exact tie and remains feasible. This proves all three branches and their sharpness. ∎

For example, \(n=6,s=2,\eta=0.1,\delta=0.2\) forces a gap of at least \(\sqrt{0.59}\approx0.7681146\). Equality is attained by

\[
(1,0.8340573\ldots,0.0659427\ldots,0,0,0).
\]

There is also stability of the optimizing configurations. If the value in (5) is \(q>0\), the preceding bounds imply \(2D+e^2\le1-q^2\). Therefore

\[
0\le R\le g_s^2-q^2,
\qquad A+B\le\frac{g_s^2-q^2}{2g_s}.
\]

A nearly minimal positive gap requires nearly all nonbinary mass to concentrate in the two boundary entries.

<a id="en-components"></a>
## 4. Components and a constructive path to a binary representative

### Theorem 3: the exact merging threshold

For the same parameter range,

\[
\boxed{
\#\pi_0(F_{s,\eta,\delta})=
\begin{cases}
\binom ns,&0\le\delta<\delta_c,\\
1,&\delta\ge\delta_c.
\end{cases}}\tag{8}
\]

Here \(\pi_0\) denotes path components. Below the threshold, a component is specified by the labels of the largest \(s\) entries. At equality the components have already merged. The result is an explicit consequence of the general polytope-complement theory of Gorban [R3], but the following proof is independent of that theory.

### Step 1: at most two line segments reach a binary vector

Take any \(x\in P_{s,\eta}\), sort its coordinates, and let \(z=(1^s,0^{n-s})\), where \(1^k\) means \(k\) consecutive ones. Define weights \(w_i=2x_i-1\). Choose an auxiliary point \(v\) as follows, with the first applicable case taking priority:

1. If \(x_s\le1/2\), choose \(v=(1^{s-1},1-\eta,0^{n-s})\).
2. Otherwise, if \(x_{s+1}\ge1/2\), choose \(v=(1^s,\eta,0^{n-s-1})\).
3. Otherwise choose \(v=z\).

All three candidates belong to the sum band. We claim

\[
c:=\sum_i w_i(v_i-x_i)\ge0.\tag{9}
\]

In the first case put \(\alpha=w_s\le0\) and write

\[
c=\sum_i(w_i-\alpha)(v_i-x_i)
 +\alpha\bigl[(s-\eta)-S\bigr].
\]

For \(i<s\), both factors of the summand are nonnegative. For \(i>s\), both are nonpositive. For \(i=s\), the first factor is zero. The final product is nonnegative because \(S\ge s-\eta\). This proves (9).

In the second case use \(\alpha=w_{s+1}\ge0\). For \(i\le s\), both factors are nonnegative; for \(i>s+1\), both are nonpositive; and the boundary summand vanishes. The final term is \(\alpha[(s+\eta)-S]\ge0\). In the third case, \(w_i\) and \(z_i-x_i\) have the same sign in each coordinate, proving (9) directly. These sign arguments also explain the greedy linear optimization behind the construction.

For \(0\le t\le1\), an exact expansion now gives

\[
D(x+t(v-x))
=D(x)-tc-t^2\|v-x\|_2^2\le D(x).\tag{10}
\]

The segment stays in \(P_{s,\eta}\) by convexity. Moreover, its defect is nonincreasing in \(t\). If \(v\ne z\), continue along the coordinate segment from \(v\) to \(z\). This moves \(\eta\) down to \(0\), or \(1-\eta\) up to \(1\). Since \(\eta\le1/2\), the function \(a(1-a)\) decreases along that segment. The sum stays in the band. Thus every \(x\in F_{s,\eta,\delta}\) reaches the binary representative of its chosen top group by at most two line segments, without increasing the defect.

This constructs a path for each starting point. The choice of the auxiliary vertex has not been proved continuous as the starting point varies; the construction therefore does not assert a deformation retraction of an entire component. Gorban's earlier vertex-access Lemma 4 is a related general result about reaching a polytope vertex by a segment avoiding a convex obstacle [R3]. The greedy choice and the binary endpoint used here are given explicitly by the sign proof above.

### Step 2: count the separated components

If \(\delta<\delta_c\), Theorem 2 gives \(g_s>0\) everywhere in \(F\). The top-\(s\) label set is consequently locally constant: strict separation persists in a sufficiently small coordinate neighborhood. It is therefore constant along a continuous path. Every \(s\)-element label set occurs at its binary representative. Conversely, all points with one such label set are connected to that same representative by Step 1. There are exactly \(\binom ns\) components.

### Step 3: connect all representatives at the threshold

Suppose \(\delta\ge\delta_c\). To exchange one selected label with one unselected label, keep the other \(s-1\) ones fixed and move the two relevant coordinates through

\[
(1,0)\longrightarrow(1-\eta,0)
\longrightarrow(0,1-\eta)\longrightarrow(0,1).
\]

The first and last segments have defect at most \(\delta_0\). On the middle segment the two entries have sum \(1-\eta\); their defect is largest when equal and is then \((1-\eta^2)/2=\delta_c\). The sum error never exceeds \(\eta\). Every two \(s\)-element subsets can be joined by a sequence of single-element exchanges, so all binary representatives are connected. Step 1 connects all other points to them. This proves (8), including \(\eta=0\). ∎

### Two limits of the statement

The two-segment construction cannot in general be replaced by a direct segment to \(z\). Let \(n=2,s=1,\eta=1/2\), and \(x=(3/8,1/8)\). Here \(D(x)=11/32<\delta_c=3/8\). Along the segment \(z+t(x-z)\), where \(z=(1,0)\),

\[
D=\frac{3t}{4}-\frac{13t^2}{32}.
\]

At \(t=12/13\) this equals \(9/26>11/32\). Thus the asserted components need not be star-shaped about their binary representatives.

The restriction \(\eta\le1/2\) is substantive. For \(n=2,s=1,\eta=0.9,\delta=0.1\), both \((0.1,0)\) and \((1,0)\) are feasible. Any continuous path between them makes the first coordinate equal \(1/2\), forcing \(D\ge1/4>0.1\). The set is disconnected even though \(0.1>(1-0.9^2)/2=0.095\). Formula (8) therefore does not extend to this larger error range.

### 4.1 Beyond a half-unit tolerance: the birth and merger of components

The restriction \(\eta\le1/2\) in the preceding result is essential. Nevertheless, for \(1/2<\eta<1\), a complete component count in every dimension follows by examining the vertices and edges of the band polytope. Let
\[
F_\delta=\left\{x\in[0,1]^n:\left|\sum_i x_i-s\right|\le\eta,
\quad D(x)=\sum_i x_i(1-x_i)\le\delta\right\}.
\]
Throughout this section, \(n\ge2\), \(1\le s<n\) are integers, \(1/2<\eta<1\), and \(\delta\ge0\).

**Theorem T9 (complete component count for a wide band).** Put
\[
a=1-\eta,\quad k=\eta(1-\eta),\quad
c=\frac{1-\eta^2}{2},\quad h=\frac14,\quad b=\binom ns.
\]
The number of path components of \(F_\delta\) is
\[
N_{n,s}(\eta,\delta)=
\begin{cases}
b,&0\le\delta<k,\\
(n+1)b,&k\le\delta<\min(c,h),\\
b+\binom n{s-1}+\binom n{s+1},&c\le\delta<h\quad(c<h),\\
b,&h\le\delta<c\quad(h<c),\\
1,&\delta\ge\max(c,h).
\end{cases}
\tag{T9}
\]
Rows with empty intervals are omitted. Equality \(c=h\) holds precisely when \(\eta=1/\sqrt2\); both intermediate rows then disappear. The displayed formula includes every threshold value with the indicated inequalities.

<!--DIAGRAM:wide-->

**A graph lemma for convex obstacles.** If \(P\) is a compact convex polytope and \(f\) is continuous and concave, the path components of \(X=\{f\le\delta\}\) correspond to the components of the graph retaining vertices with \(f(v)\le\delta\) and edges with \(\max_e f\le\delta\).

Here is a proof. The set \(U=\{f>\delta\}\) is relatively open and convex. Process the faces meeting \(U\) in decreasing dimension. In each such face choose \(z\in U\) in its relative interior; relative openness guarantees that this is possible. Move each point outside \(U\) outward along the ray from \(z\), until it reaches the face boundary. Convexity ensures that a ray cannot re-enter \(U\) after passing a point outside it. This continuous deformation fixes the boundary and therefore glues to the identity on the other remaining faces. After finitely many steps, \(X\) strongly deformation retracts onto the complex \(K\) of closed faces disjoint from \(U\). Each face has a connected edge graph, so the components of \(K\) are precisely those of its one-skeleton. That one-skeleton is the stated graph.

**All vertices.** Let \(P\) impose only the box and band constraints. Its vertices have exactly three types.

| Type | Coordinates | Count | \(D\) |
|---|---|---:|---:|
| \(B\) | \(s\) ones, all remaining entries zero | \(b\) | 0 |
| \(L\) | \(s-1\) ones, one entry \(a\), all others zero | \(sb\) | \(k\) |
| \(U\) | \(s\) ones, one entry \(\eta\), all others zero | \((n-s)b\) | \(k\) |

Indeed, a vertex away from the band boundaries must be a cube vertex, and \(s\) is the only allowed integer sum. At a band boundary, at least \(n-1\) coordinates must be fixed at zero or one. The sum constraint determines the remaining coordinate as \(a\) or \(\eta\). This proves completeness and the counts.

**All edges and their thresholds.** Edges inherited from the cube are exactly the segments \(L\leftrightarrow B\), with one coordinate ranging from \(a\) to 1, and \(B\leftrightarrow U\), with one coordinate ranging from 0 to \(\eta\). Both intervals contain \(1/2\), so their maximum deficit is \(h=1/4\). Each \(L\) or \(U\) vertex has exactly one edge of this kind, connecting it to a unique \(B\) vertex.

Edges within the band boundaries have the following four types. All coordinates other than the displayed pair are fixed at zero or one.

| Band boundary | Endpoints of the moving pair | Maximum \(D\) |
|---|---|---:|
| Lower, short edge | \((a,0)\leftrightarrow(0,a)\) | \(c\) |
| Lower, long edge | \((1,a)\leftrightarrow(a,1)\) | \(d=(1-a^2)/2\) |
| Upper, short edge | \((1,\eta)\leftrightarrow(\eta,1)\) | \(c\) |
| Upper, long edge | \((\eta,0)\leftrightarrow(0,\eta)\) | \(d\) |

A type is absent if its required coordinates do not fit the dimension or sum. At the relative interior of an edge, either no band boundary is active and \(n-1\) coordinates are fixed, or one band boundary is active and \(n-2\) coordinates are fixed. Thus the list is exhaustive. For a moving pair with fixed sum \(t\),
\[
y(1-y)+(t-y)(1-t+y)
=t-\frac{t^2}{2}-2(y-t/2)^2.
\]
The midpoint belongs to each listed segment, yielding the stated maxima. Moreover,
\[
c-k=\frac{(1-\eta)^2}{2}>0,\quad
h-k=(\eta-\tfrac12)^2>0,\quad
d>\max(c,h).
\]

**Counting the graph components.** For \(\delta<k\), only the \(B\) vertices are present. For \(k\le\delta<\min(c,h)\), all \((n+1)b\) vertices are present. No edges have yet appeared in either interval.

If \(c<h\) and \(c\le\delta<h\), the short band edges appear first. On the lower boundary, they connect each group with a fixed set of \(s-1\) one-coordinates; there are \(\binom n{s-1}\) such groups. On the upper boundary, they connect each group with a fixed positive support of size \(s+1\); there are \(\binom n{s+1}\) groups. The \(b\) binary vertices remain isolated. Adding these counts gives the third row of T9.

If \(h<c\) and \(h\le\delta<c\), the cube segments appear first. Each binary vertex is the center of a star whose leaves are its associated \(L\) and \(U\) vertices. Because every leaf has a unique binary neighbor, these are \(b\) disjoint stars.

Once \(\delta\ge\max(c,h)\), all binary vertices are connected. To see this, identify a binary vertex with its set \(I\) of \(s\) one-coordinates. If \(I'\) differs by exchanging one element, keep the common \(s-1\) ones fixed and use three edges: a cube segment, a short lower-boundary edge exchanging the position of \(a\), and another cube segment. Any two \(s\)-element subsets are related by successive single-element exchanges. Every \(L\) and \(U\) vertex also attaches to a binary vertex, so the entire graph is connected. This occurs before the long edges appear. No new vertices appear later, and adding edges preserves connectedness. The graph lemma now proves T9. □

**The reviewer's numerical example.** For \(n=2,s=1,\eta=0.9\),
\[
k=0.09,\qquad c=0.095,\qquad h=0.25.
\]
The component count therefore evolves as
\[
2\ \xrightarrow{\ \delta=0.09\ }\ 6\
\xrightarrow{\ \delta=0.095\ }\ 4\
\xrightarrow{\ \delta=0.25\ }\ 1.
\]
At each marked threshold the count on its right already applies. Thus the reviewer's observations \(6,4,4,1\) at \(\delta=0.09,0.10,0.20,0.26\), respectively, are correct. Although the sets grow with \(\delta\), their component count need not decrease monotonically: new components are born at new feasible vertices.

**Additional corollary: holes in dimension two.** For \(n=2,s=1\), put \(p=x_1+x_2-1\) and \(q=x_1-x_2\). The band polytope becomes the hexagon
\[
|p|+|q|\le1,\quad |p|\le\eta,
\qquad D=(1-p^2-q^2)/2.
\]
For \(\delta<1/2\), the origin is excluded. Radially expanding points from the origin to the hexagon boundary gives a strong deformation retraction onto the feasible boundary: the norm never decreases, so the deficit constraint is preserved. The boundary has four sloping edges with threshold \(h\) and two vertical edges with threshold \(c\). Therefore each component is contractible for \(\delta<\max(c,h)\); for \(\max(c,h)\le\delta<1/2\), the entire boundary is feasible and \(F_\delta\simeq S^1\). For \(\delta\ge1/2\), the full hexagon is feasible and contractible. Connectedness and the disappearance of the hole are different events.

**Status.** T9 is treated as an explicit corollary of [Gorban’s general theory of polytopes with convex obstacles](https://arxiv.org/html/1201.6315v3), notably Proposition 7. Priority for this particular band and component-count formula has not been established, and no novelty claim is confirmed. This section contains ordinary mathematical proofs and is outside the existing Lean verification scope.


<a id="en-rounding"></a>
## 5. Nearest binary rounding has an earlier threshold

Selecting the largest \(s\) entries and rounding each entry at \(1/2\) are different operations. For coordinatewise nearest rounding, the sharp threshold is

\[
\boxed{\delta_R=\frac12-\eta^2.}\tag{11}
\]

**Theorem 4.** If \(|S-s|\le\eta\le1/2\) and \(D<\delta_R\), every coordinate has a unique nearest value in \(\{0,1\}\), and the rounded vector has exactly \(s\) ones.

**Proof.** Suppose a coordinate equals \(1/2\). The remaining coordinates have sum \(s-1/2+e\), with \(|e|\le\eta\). The packed-square lemma, including the endpoint cases \(e=\pm1/2\), gives

\[
D\ge\frac14+\left(\frac12+e\right)
\left(\frac12-e\right)
=\frac12-e^2\ge\delta_R.
\]

Thus no coordinate can equal \(1/2\) under the strict defect bound. Follow the nonincreasing-defect path from Section 4 to a binary representative with \(s\) ones. No coordinate can cross \(1/2\) along this path, so its rounding remains unchanged and equals that representative. ∎

The threshold is sharp for the joint guarantee of uniqueness and sum preservation. The vector

\[
(1^{s-1},1/2,1/2-\eta,0^{n-s-1})
\]

has \(S=s-\eta\) and \(D=\delta_R\), but at least one rounding tie. When \(\eta>0\), the strict inequality \(\delta_R<\delta_c\) leaves a range in which a top group remains separated while nearest rounding may have the wrong number of ones. Replace the boundary pair by

\[
(1/2-\varepsilon,1/2-\eta+\varepsilon).
\]

For sufficiently small \(0<\varepsilon<\eta/2\), both are below \(1/2\), their gap remains positive, and

\[
D=\delta_R+2\eta\varepsilon-2\varepsilon^2
\quad\text{lies between }\delta_R\text{ and }\delta_c.
\]

For example, \(s=1,\eta=0.1,x=(0.49,0.41)\) gives \(D=0.4918<\delta_c=0.495\). The first entry is the unique largest entry, but both entries round to zero.

<a id="en-noninteger"></a>
## 6. An exact noninteger sum produces two merging events

Let \(S=m+r\), where \(m\in\{0,\ldots,n-1\}\) and \(0<r<1\). Define

\[
H_S=\{x\in[0,1]^n:\sum_i x_i=S\},\qquad M=m+r^2,
\]
\[
E=M-Q,\qquad E_{\max}=M-\frac{S^2}{n},
\qquad X_E=\{x\in H_S:Q=M-E\}.
\]

The feasible range is exactly \(0\le E\le E_{\max}\). The packed-square lemma gives the maximum \(Q=M\). The identity \(Q=S^2/n+\sum_i(x_i-S/n)^2\) gives the minimum \(S^2/n\), uniquely attained at \(c=(S/n,\ldots,S/n)\). Interpolation from \(c\) to a packed vertex attains every intermediate value.

The quantities \(D\) and \(E\) must not be confused:

\[
D=r(1-r)+E.\tag{12}
\]

### Theorem 5: both relevant rank gaps are sharp

For every feasible \(E\), and only when the stated rank exists,

\[
\boxed{
\min_{x\in X_E}(x_{(m)}-x_{(m+1)})
=\sqrt{\max\{(1-r)^2-2E,0\}}
}\quad(m\ge1),\tag{13}
\]
\[
\boxed{
\min_{x\in X_E}(x_{(m+1)}-x_{(m+2)})
=\sqrt{\max\{r^2-2E,0\}}
}\quad(m+1<n).\tag{14}
\]

**Proof of the lower bounds.** Apply Theorem 1 with \(s=m\), so \(e=r\), and substitute (12). This yields \(g_m^2\ge(1-r)^2-2E\). Apply it with \(s=m+1\), so \(e=r-1\), to get \(g_{m+1}^2\ge r^2-2E\). The gaps are nonnegative, giving the displayed bounds.

**Attainment before the thresholds.** Put \(b=(1-r)^2/2\). For \(0\le E\le b\), let \(d=\sqrt{(1-r)^2-2E}\) and choose

\[
w=(1^{m-1},(1+r+d)/2,(1+r-d)/2,0^{n-m-1}).
\]

Since \(0\le d\le1-r\), this is a sorted box vector with sum \(S\), gap \(d\), and squared sum \(M-E\). Similarly, put \(a=r^2/2\). For \(0\le E\le a\), the vector

\[
w=(1^m,(r+d)/2,(r-d)/2,0^{n-m-2}),
\qquad d=\sqrt{r^2-2E},
\]

attains (14). The assumed rank conditions make all multiplicities valid.

**Attainment after the thresholds.** In either construction, let \(y\) be the vector at its threshold \(t\), where \(t=b\) or \(a\), so the boundary pair is tied. Interpolate by \(x(\lambda)=(1-\lambda)y+\lambda c\), \(0\le\lambda\le1\). Sorting is preserved and the same pair remains tied. Orthogonality to the constant vector gives

\[
E(x(\lambda))=E_{\max}-(1-\lambda)^2(E_{\max}-t).
\]

Thus every \(E\in[t,E_{\max}]\) is attained with gap zero. If \(t=E_{\max}\), only the endpoint needs to be considered. ∎

<!--DIAGRAM:phases-->

### Theorem 6: component counts from a weighted edge graph

For the internal case \(1\le m\le n-2\), set

\[
a=r^2/2,\qquad b=(1-r)^2/2,\qquad
N=\binom nm(n-m).
\]

The following table gives the number of path components of \(X_E\). Empty intervals are ignored.

| Range of \(E\) | Number of components | Constant label within a component |
|---|---:|---|
| \(E<a\) and \(E<b\) | \(N\) | top-\(m\) set \(A\), together with the next label \(j\) |
| \(a\le E<b\) | \(\binom nm\) | top-\(m\) set \(A\) |
| \(b\le E<a\) | \(\binom n{m+1}\) | top-\((m+1)\) set |
| \(E\ge a\) and \(E\ge b\) | \(1\) | no separation into components |

We use the following known result explicitly. Gorban's *Thermodynamic Tree*, Proposition 7, identifies the path components of a convex polytope \(P\) minus a convex set \(U\) with those of the graph formed by vertices outside \(U\) and edges entirely outside \(U\). His Lemma 14 identifies the relevant components of a strictly convex level set with those of its superlevel set [R3]. In this quadratic setting the latter step also has the direct deformation retraction below.

**Vertices and edges.** A point of \(H_S\) with two entries strictly between \(0\) and \(1\) admits a nonzero perturbation of those entries with fixed sum, in both signs. Hence it is not a vertex. All vertices are therefore packed vectors: \(m\) ones, one \(r\), and zeros elsewhere. Conversely, fixing those \(n-1\) endpoint coordinates fixes the remaining coordinate, so each is a vertex. Label it \((A,j)\), with \(|A|=m\), \(j\notin A\).

Every edge has exactly two free coordinates in its relative interior. Indeed, fixing its endpoint coordinates leaves a cube slice of dimension one, so the number of free coordinates is two. Their sum must be \(r\) or \(1+r\). Thus there are only two edge types:

| Type | Moving coordinates | Maximum \(E\) on the edge |
|---|---|---:|
| L | \((r,0)\leftrightarrow(0,r)\) | \(a=r^2/2\) |
| U | \((1,r)\leftrightarrow(r,1)\) | \(b=(1-r)^2/2\) |

Each maximum occurs at the midpoint, by direct expansion of the squared sum. Define

\[
\Omega_E=\{x\in H_S:Q\ge M-E\},\qquad
U_E=\{x\in H_S:Q<M-E\}.
\]

The removed set \(U_E\) is relatively open and convex. An L edge is wholly in \(\Omega_E\) exactly when \(E\ge a\); a U edge is wholly there exactly when \(E\ge b\). The use of the strict inequality in \(U_E\) explains why merging is already complete at the threshold itself.

For \(E<E_{\max}\), put \(R_E=\sqrt{M-E-S^2/n}>0\). Every \(x\in\Omega_E\) has \(\|x-c\|\ge R_E\), and

\[
p_E(x)=c+\frac{R_E}{\|x-c\|}(x-c)
\]

belongs to \(X_E\). The homotopy

\[
c+\left[(1-t)+t\frac{R_E}{\|x-c\|}\right](x-c),
\qquad0\le t\le1,
\]

stays in \(H_S\) by convexity and has radius at least \(R_E\), so it remains in \(\Omega_E\). It fixes \(X_E\). Hence \(\Omega_E\) strongly deformation retracts onto \(X_E\). At \(E=E_{\max}\), \(X_E=\{c\}\) is handled directly.

**Count the surviving graph.** With neither edge type present, all \(N\) vertices are isolated. With only L edges, \(A\) is fixed and the \(n-m\) choices of \(j\) form a complete graph; this gives \(\binom nm\) components. With only U edges, \(B=A\cup\{j\}\) is fixed and its \(m+1\) choices of \(j\) form a complete graph; this gives \(\binom n{m+1}\) components. With both types present, the graph is connected. Explicitly, use an L move to designate a desired new element as the fractional coordinate, then a U move to exchange it with an element of \(A\). Repeated single-element exchanges connect all \(m\)-subsets, and L moves connect all fractional labels for each subset. Gorban's proposition and the retraction transfer these counts to \(X_E\).

Finally, (13) keeps the top-\(m\) label set fixed whenever \(E<b\), and (14) keeps the top-\((m+1)\) set fixed whenever \(E<a\). Each possible label is realized on the segment from its packed vertex toward \(c\). The number of labels equals the component count in each row, proving the stated labeling. ∎

For \(r<1/2\), the counts are \(N\to\binom nm\to1\); for \(r>1/2\), they are \(N\to\binom n{m+1}\to1\). When \(r=1/2\), both edge types enter at \(1/8\), and the intermediate stage disappears. For example, \(n=6,S=2.3\) gives \(60\to15\to1\) at \(E=0.045\) and \(0.245\).

At the boundaries, \(m=0\) has only L edges and only (14): \(n\) components merge into one at \(E=a\). The case \(m=n-1\) has only U edges and only (13), with merging at \(E=b\). For \(n=2\), the applicable threshold equals \(E_{\max}\), so two points meet at the uniform point. If one allows \(n=1\), the whole slice is already a single point.

<a id="en-holes"></a>
## 7. Beyond connectivity: holes appear and disappear

Take \(n=4,S=5/4\). Then \(m=1,r=1/4\), \(M=17/16\), and \(E_{\max}=43/64\). The component count is \(12\to4\to1\), but this does not describe all changes in shape.

### The homotopy sequence to be proved

| Range of \(E\) | Homotopy type of \(X_E\) | Betti numbers \((\beta_0,\beta_1,\beta_2)\) |
|---|---|---|
| \(0\le E<1/32\) | twelve points | \((12,0,0)\) |
| \(1/32\le E<1/24\) | four disjoint circles | \((4,4,0)\) |
| \(1/24\le E<9/32\) | four points | \((4,0,0)\) |
| \(9/32\le E<13/24\) | a wedge of three circles | \((1,3,0)\) |
| \(13/24\le E<43/64\) | the sphere \(S^2\) | \((1,0,1)\) |
| \(E=43/64\) | one point | \((1,0,0)\) |

Having the homotopy type of a point means being contractible; it does not mean the set literally consists of one point. Likewise, the other rows specify homotopy type rather than an exact embedding or homeomorphism. The Betti numbers displayed here agree over the integers and over \(\mathbb F_2\), as follows from the identified homotopy types.

<!--DIAGRAM:holes-->

### Theorem 7: retract a convex-set complement to uncut faces

Let \(P\) be a compact convex polytope, let \(U\subset P\) be relatively open and convex, and let \(K\) be the union of all closed faces of \(P\) disjoint from \(U\). Include \(P\) itself among its faces. Then \(P\setminus U\) strongly deformation retracts onto \(K\).

**Proof.** The assertion is immediate if \(U\) is empty. Otherwise process every positive-dimensional face \(F\) meeting \(U\), in decreasing dimension. Because \(U\) is relatively open in \(P\), a point in \(U\cap F\) can be perturbed within \(F\) into its relative interior while staying in \(U\). Choose \(c_F\in U\cap\operatorname{relint}(F)\).

For \(x\in F\setminus U\), let \(\rho_F(x)\) be the point where the ray from \(c_F\) through \(x\) meets \(\partial F\). The center is in the relative interior and does not belong to \(F\setminus U\), so this radial map is continuous on its domain; it fixes every boundary point. One can see continuity directly by representing \(F\) with finitely many affine inequalities: the distance to the boundary along a ray is the minimum of the positive intersection parameters with the supporting hyperplanes.

The entire segment \([x,\rho_F(x)]\) avoids \(U\). Otherwise, for some farther point \(y\in U\) on that ray, \(x\) would lie on the segment from \(c_F\in U\) to \(y\in U\), contradicting convexity of \(U\). Therefore

\[
H_F(x,t)=(1-t)x+t\rho_F(x)
\]

deforms \(F\setminus U\) into \(\partial F\setminus U\), staying outside \(U\) and fixing the boundary throughout.

At this stage, every higher-dimensional face meeting \(U\) has already been collapsed. A higher-dimensional face avoiding \(U\) cannot contain \(F\), since \(F\cap U\ne\varnothing\). Thus the currently remaining part of \(F\setminus U\) meets the rest of the remaining space only along its boundary. Extend \(H_F\) by the identity on that rest. The maps agree on the overlap, and the finite closed-face pasting property gives a continuous homotopy. After finitely many steps, only faces disjoint from \(U\) remain. Vertices in \(U\) were absent from the complement from the start. Every point of \(K\) is fixed during every step, so the resulting deformation retraction is strong. The empty-complement case is interpreted trivially. ∎

This is an explicit finite-dimensional geometric argument; it is not presented as a newly discovered general topological theorem.

### Compute the threshold for every face

Apply the lemma with \(P=H_S\) and \(U=U_E=\{Q<M-E\}\). A face has \(j\) coordinates fixed to \(1\), \(p\) free coordinates, and the rest fixed to \(0\), with \(0<S-j<p\). Its dimension is \(p-1\). On this face,

\[
Q=j+\sum_{\text{free }i}x_i^2
\ge j+\frac{(S-j)^2}{p},
\]

because the sum of squared deviations of the free entries from their mean is nonnegative. Equality is attained when all free entries equal \((S-j)/p\in(0,1)\). The face is entirely outside \(U_E\) exactly when

\[
\boxed{E\ge E_F:=M-j-\frac{(S-j)^2}{p}.}\tag{15}
\]

Let \(K_E\) contain precisely these faces. Theorem 7 gives \(H_S\setminus U_E\simeq K_E\), and Section 6 gives \(H_S\setminus U_E\simeq X_E\) for \(E<E_{\max}\). These are two deformation retractions from the common space \(\Omega_E=H_S\setminus U_E\). We do not claim a direct deformation retraction from \(X_E\) to \(K_E\): in general, \(K_E\) is not a subset of \(X_E\). At the endpoint, \(K_E=H_S\) and \(X_E=\{c\}\) are both contractible.

For \(n=4,S=5/4\), this polytope is combinatorially a truncated tetrahedron. Its complete face table is

| Face type | \(j\) | \(p\) | Count | Entry threshold \(E_F\) |
|---|---:|---:|---:|---:|
| vertex | 1 | 1 | 12 | \(0\) |
| L edge | 1 | 2 | 12 | \(1/32\) |
| triangular face | 1 | 3 | 4 | \(1/24\) |
| U edge | 0 | 2 | 6 | \(9/32\) |
| hexagonal face | 0 | 3 | 4 | \(13/24\) |
| full polytope | 0 | 4 | 1 | \(43/64\) |

For completeness, the counts follow by choosing the coordinate positions: vertices choose one fixed \(1\) and one fractional coordinate, giving \(4\cdot3=12\); L edges choose a fixed \(1\) and two free positions among the other three, giving \(4\binom32=12\); triangular faces choose their fixed \(1\), giving four; U edges choose their two free positions, giving \(\binom42=6\); hexagonal faces choose their fixed \(0\), giving four. No other possibilities satisfy \(0<5/4-j<p\) in the relevant dimension.

### Theorem 8: the six-stage homotopy classification

For \(n=4,S=5/4\), the six homotopy types and their exact parameter intervals are those stated at the start of this section.

**Proof.** Read the face complex \(K_E\) at each successive threshold.

Initially \(K_E\) consists of twelve isolated vertices. At \(E=1/32\), the twelve L edges form four disjoint triangular boundaries, one for each position of the fixed \(1\). At \(E=1/24\), the four triangular faces enter and fill these circles, giving four disjoint disks.

At \(E=9/32\), the six U edges enter. Each pair of triangular disks is joined by one such edge: the edge with free positions \(i,j\) connects the disk whose fixed \(1\) is at \(i\) to the one whose fixed \(1\) is at \(j\). In each triangle, choose one of its boundary edges. It is a free edge, because no other two-dimensional cell meets it. Collapse the triangle together with that edge onto the other two edges, keeping all three vertices and all joining edges. Each triangle has become a tree connecting its three attachment points. Contracting these four trees in the resulting graph gives the complete graph \(K_4\); these elementary collapses and graph-tree contractions preserve homotopy type. Finally, contract a spanning tree of \(K_4\). Its \(6-4+1=3\) remaining edges form a wedge of three circles.

At \(E=13/24\), all hexagonal faces enter, so \(K_E\) is the entire boundary of the three-dimensional convex polytope. Radial projection from any interior point identifies that boundary homeomorphically with \(S^2\). At \(E=43/64\), the whole polytope enters and is contractible. These arguments prove every row, including the equality conventions. ∎

Independent computation enumerated the faces and formed the cellular boundary matrices over \(\mathbb F_2\), verified that consecutive boundary maps compose to zero, and recovered the displayed Betti numbers. These finite calculations corroborate the result. The homotopy types themselves follow from the direct cell descriptions above, not from mod-2 homology alone.

<a id="en-formal"></a>
## 8. What Lean verified, and what it did not

The recorded run used **Lean 4.19.0** and **Mathlib v4.19.0**, at Mathlib commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`. It compiled all **14 theorem declarations** in `MomentIslands.lean`, with final exit code **0**. These are proofs over the real numbers and arbitrary finite index types, not numerical-grid checks.

That successful compilation was performed on **2026 09 08** and is recorded in the accompanying log. During the review response on **2026 09 09**, the official tag-to-commit mapping was checked again with `git ls-remote`. A fresh compilation on that date was not performed: fetching the official Lean distribution stopped at the environment's network approval. The earlier success record must not be read as a new successful compilation in this review pass.

The count of 14 is the number of theorem declarations in the file, not 14 independent principal results of X01. In particular, `four_variable_gap_bound` and `four_variable_gap` record an earlier four-variable impossibility example and lie outside the main results of this note.

| Formal theorem names | Verified scope |
|---|---|
| `rank_gap_partition`, `rank_gap_partition_sqrt` | Theorem 1 for an arbitrary finite partition with box bounds and attained extrema; the square-root form adds cross-ordering |
| `finite_rank_gap` | The bridge from finite sums and boundary hypotheses to the scalar rank certificate |
| `rank_gap_core`, `rank_gap_sqrt`, `rank_gap_slack` | Scalar algebraic rank inequalities and a quantitative slack bound |
| `balanced_error_defect`, `invert_defect_bound`, `balanced_error_sharp_bound` | The quadratic defect bound and its inversion for two nonnegative error families explicitly assumed to have the same mass |
| `pair_square_upper`, `pair_square_upper_complement` | Two elementary two-variable squared-sum bounds |
| `four_variable_gap_bound`, `four_variable_gap` | Total \(2\) and first-pair total \(1/2\) force \(Q\le3/2\), and hence exclude \(Q=9/5\); two auxiliary examples outside X01's main results |
| `concentration_from_square_deficit` | Concentration derived from a nonnegative vector's squared-sum deficit |

The formal theorem `rank_gap_partition` takes any nontrivial finite partition \(I,I^c\), an index \(a\in I\) attaining its minimum, and an index \(b\notin I\) attaining the maximum outside \(I\). It proves precisely the squared statement of Theorem 1, without requiring \(I\) to be a top set. The separate theorem `rank_gap_partition_sqrt` adds \(x_b\le x_a\) and proves

\[
\sqrt{1-2\sum_i x_i(1-x_i)
 -(\sum_i x_i-|I|)^2}\le x_a-x_b.
\]

Lean's real square root is zero on negative arguments. Thus the formal statement covers that case as well; a positive radicand is what provides a positive gap. Mathematical order-statistic notation specializes this interface by choosing a top set of size \(s\). The formal input explicitly supplies the partition and indices attaining its extrema. No sorting procedure is needed to state or prove this interface, and no unformalized sorting algorithm is required to fill a gap between the partition statement in this note and the formal theorem.

The file does **not** formalize the full equality classification, every extremizer in the three-branch formula, the two-segment paths, the nearest-rounding sum-preservation theorem, or any of the topological classifications. In particular, a lemma assuming equal error masses is not a formal proof that a particular rounding procedure produces those equal masses. The explicit nonnegative identity in Section 2 is proved in the text, and its aggregate algebraic identity appears inside `rank_gap_core`; the exact Lean coverage should be read from the theorem declarations rather than inferred from neighboring prose.

Each theorem was audited with `#print axioms`. Every output listed only `propext`, `Classical.choice`, and `Quot.sound`. There was no `sorryAx`, proof placeholder, or newly declared axiom. This means no unproved holes were added on top of the usual Lean/Mathlib foundations; it does not mean that the proofs are axiom-free.

The checked source has SHA-256

```text
3f29d4e1daad5ed467c6ef2a832a067b03546a2ca35293983f3675e76e70c9fa
```

During the 2026 09 08 run, the official Lean executable initially failed to locate itself because this host's process-ID namespace did not match its `/proc` view. A narrowly scoped compatibility shim maps only the current executable's `readlink(/proc/<getpid()>/exe)` lookup to `/proc/self/exe`. Lean's source, mathematical kernel, and proof checks were not changed. The reproduction material records the shim source, binary and source hashes, tool versions, failed intermediate attempts, and final successful log. The shim is unnecessary on a standard host.

With the supplied `lean-toolchain` and `lakefile.toml`, standard reproduction is

```bash
lake update
lake exe cache get
lake env lean MomentIslands.lean
```

### Independent exact-arithmetic checks

| Target | Recorded finite coverage | Result |
|---|---|---|
| Universal rank bound and nonnegative identity | 24,300 sorted grid vectors; 150,723 rank partitions | PASS |
| Robust formula and paths | 75,623 band checks and two-segment paths; 9,240 attaining configurations; 1,880 nearest-rounding checks | PASS |
| Sum-band edge graphs | 75 polytopes; 8,087 independently enumerated edges; 583 threshold checks | PASS |
| Noninteger rank gaps | 317,353 sorted grid vectors; 633,302 squared inequalities; 9,900 attaining configurations | PASS |
| Noninteger component counts | 1,695 weighted-graph levels | PASS |
| Wide-band edge graphs (T9) | 60 rational polytopes; 660 critical-value and midpoint checks | PASS (added in this review) |
| Hole transitions | Six face-complex stages; boundary matrices over \(\mathbb F_2\), including boundary-squared-zero checks | PASS |

The scripts use Python's standard-library integer and rational arithmetic. Different checks reuse some samples; these counts must not be added and reported as independent sample counts. Finite checks do not establish a theorem over a continuous domain. The generality comes from the mathematical proofs and, for the stated formal scope, the Lean proofs.

<a id="en-novelty"></a>
## 9. Novelty and attribution

Correctness, machine verification, and novelty are separate questions. Finding a proof of a statement does not establish that the statement is new, and a successful Lean run does not supply bibliographic evidence.

An additional limited search on **2026 09 08**, using six query families, did not identify a primary source stating the universal rank-gap inequality or the exact three-branch formula for a sum-error band. It rechecked the relevant statements in Rastegin, Gorban, Goroncy–Rychlik, and Rubensson–Niklasson, and inspected a further paper on stopping criteria for density-matrix expansions [R4, R3, R5, R6, R8]. This is a bounded literature update, not an exhaustive search or a priority determination.

| Result | Current attribution |
|---|---|
| Packed maximum squared sum at a fixed total | Classical extremal inequality; explicit sources include Rosenberg–Jakobsson and Ellis [R1–R2] |
| Sharp nearest-rounding bound for an integer total | An elementary direct consequence of the squared-sum bound on each error family; Rastegin (2023), Theorem 1 is one identified explicit prior statement of the corresponding probability bound, without a claim of first priority [R4] |
| Integer-total rank gap | A direct consequence of that rounding bound |
| Defect-nonincreasing path with at most two segments | Related to Gorban's vertex-access Lemma 4; an explicit greedy construction is proved here, without claiming a new general principle |
| Components for exact or uncertain totals | Explicit consequences of Gorban's general theory [R3]; a self-contained constructive proof is also given here for the uncertain-total case |
| Universal rank-gap identity and sharp three-branch uncertainty formula | No identical primary-source statement identified in the searches recorded so far; novelty remains unconfirmed |
| Interior noninteger rank formulas | Exact expressions derived here from elementary inequalities; identical prior publication not identified, with novelty unconfirmed |
| The six-stage hole example | Proved here by finite face geometry; higher-topology literature was not separately surveyed in this six-query update, and no claim of a new general topological theorem is made |

### An elementary direct proof, and its bibliographic correspondence

The earlier exploration obtained, for integer \(S=s\) and \(D<1/2\),

\[
\|x-z\|_1\le1-\sqrt{1-2D},\tag{16}
\]

where \(z\) is nearest binary rounding. This follows directly by applying the fact that the squared sum of nonnegative numbers dominates their sum of squares on both error families. For bibliographic comparison, Rastegin (2023), Theorem 1, equations (30)–(31), explicitly states, for a probability vector \(p\) with collision probability \(I=\sum_i p_i^2>1/2\),

\[
\max_i p_i\ge\frac{1+\sqrt{2I-1}}2.\tag{17}
\]

This is one identified explicit prior statement; we do not establish that this high-purity branch first appeared in that paper. When \(S=1\), (16) is precisely this branch, because \(I=1-D\) and the distance to the largest-coordinate unit vector is \(2(1-\max_i x_i)\).

First give the direct proof for every integer \(s\). Put \(d_i=\min(x_i,1-x_i)\). Since \(d_i\le2x_i(1-x_i)\), we have \(\sum_i d_i\le2D<1\). For any nearest rounding \(z\), the integer \(s-\sum_i z_i\) has absolute value at most \(\sum_i d_i<1\), and hence is zero. If some \(x_i=1/2\), changing only its rounding produces two nearest roundings with different sums, contradicting this conclusion. Thus rounding is unique and preserves the sum.

The two error masses are equal:

\[
\rho=\sum_{z_i=0}x_i=\sum_{z_i=1}(1-x_i),
\qquad2\rho=\sum_i d_i<1.
\]

Each error family is nonnegative and has mass \(\rho\), so its sum of squares is at most \(\rho^2\). Therefore

\[
D=2\rho-\sum_{z_i=0}x_i^2-\sum_{z_i=1}(1-x_i)^2
\ge2\rho(1-\rho).
\]

Equivalently, \((1-2\rho)^2\ge1-2D\). Since \(\rho<1/2\), taking the nonnegative square root gives

\[
1-2\rho\ge\sqrt{1-2D},\qquad
\|x-z\|_1=2\rho\le1-\sqrt{1-2D}.
\]

This proves (16) without using (17). The Lean lemmas `balanced_error_defect` and `balanced_error_sharp_bound` formalize this squared-sum argument and inversion under an explicit assumption of equal error masses. Cases \(s=0,n\) are the trivial binary vectors. The error in the sum over any subset of indices is at most \(\rho\), because both its positive and negative error mass are bounded by \(\rho\).

For the integer-total rank gap, the rounding has \(s\) ones, so

\[
x_{(s)}-x_{(s+1)}
=1-(1-x_{(s)})-x_{(s+1)}
\ge1-2\rho\ge\sqrt{1-2D}.
\]

**Aggregation as bibliographic correspondence.** Form the probability vector \(p=(1-\rho,(x_i)_{z_i=0})\). Its largest entry is \(1-\rho\), since each remaining entry is at most \(\rho<1/2\). Moreover,

\[
I(p)=(1-\rho)^2+\sum_{z_i=0}x_i^2,\qquad
I(p)-(1-D)=\rho^2-\sum_{z_i=1}(1-x_i)^2\ge0.
\]

Thus \(I(p)\ge1-D>1/2\), and (17) also gives

\[
1-\rho\ge\frac{1+\sqrt{2I(p)-1}}2
\ge\frac{1+\sqrt{1-2D}}2.
\]

This reduction explains the relation to an explicit prior inequality; it is not needed as a premise of the direct proof. We do not attribute this aggregation or the same rounding formulation to Rastegin's paper. The rounding and integer-total rank estimates are not counted as independently new inequalities.

The noninteger boundary case \(m=0\) also follows directly by applying (17) to \(p_i=x_i/r\) and using \(p_{(2)}\le1-p_{(1)}\). For a positive radicand this gives

\[
x_{(1)}-x_{(2)}\ge\sqrt{2Q-r^2}
=\sqrt{r^2-2E};
\]

otherwise the zero bound is immediate. The case \(m=n-1\) follows by complementing every coordinate. These boundary cases are therefore known consequences as well.

### Nearby results are not automatically identical results

Goroncy–Rychlik study sharp deterministic bounds for linear combinations of order statistics using central moments, without imposing a fixed external box \([0,1]\) [R5]. Their setting should not be silently substituted for this one. Rubensson–Niklasson use near-idempotency information in density-matrix purification to bound relevant eigenvalues and spectral gaps [R6]. This is an established application area, although the precise trace-and-squared-trace formulas above were not identified there in the previous check.

The matrix corollary in Section 2 is an immediate spectral transfer and is not counted as an independently new result. Earlier work on density-matrix purification extracts spectral information from the residual \(\operatorname{Tr}(X-X^2)\) and its norms. The recheck on **2026 09 09** confirmed explicit trace and Frobenius-norm estimates in Rubensson–Niklasson (2013), Section 5.1 [R6], including \(\|A\|_F^2/\operatorname{Tr}A\le\|A\|_2\) for \(A=X-X^2\) and nonzero denominator, and exclusion of a central open interval based on the residual norm. Our limited search has not identified the same sharp adjacent-rank inequality with a specified rank and integer trace offset, or the same three-branch robust minimum; priority remains unresolved.

We also verified the abstract of Rubensson–Rudberg–Sałek (2008), *Density matrix purification with rigorous error control* [R10]. It addresses errors in eigenvalues and occupied invariant subspaces, but a full-text theorem comparison remains outstanding. An abstract and bibliographic record cannot establish whether the present formula already appears there.

SPREAD-constraint work is another relevant comparison, especially when translating the exact feasible-set problem into constraint propagation. Its variable-mean and variance-bound models need theorem-by-theorem comparison rather than inference from an abstract or title [R7]. The additional stopping-criteria paper concerns convergence ratios for idempotency errors and discusses HOMO/LUMO bounds; its inspected parts were not identified as an exact match to the present formula [R8]. It was not checked theorem by theorem in full.

The six query families were: `eigenvalue gap trace idempotency inequality`, `order statistics bounded sum of squares gap inequality`, `hypersimplex connected components sphere`, `rank gap sum squares inequality`, `deterministic lower bounds spacings bounded sample mean variance order statistics`, and `idempotency error trace HOMO LUMO eigenvalue bounds Rubensson Niklasson`. Earlier incomplete readings, including Fahmy–Proschan (1981) and the 2014 SPREAD follow-up, remain incomplete. Alternate notation, books, non-English literature, and unindexed sources prevent any claim of comprehensive exclusion. The absence of an identical formula in this limited search does not establish novelty.

<a id="en-references"></a>
## 10. References and source roles

- **[R1]** N. A. Rosenberg and M. Jakobsson, *The Relationship Between Homozygosity and the Frequency of the Most Frequent Allele* (2008), Appendix Lemma 3. Source for the packed maximum of a squared sum. [Author-hosted PDF](https://web.stanford.edu/group/rosenberglab/papers/RosenbergJakobsson2008-Genetics.pdf).
- **[R2]** J. L. Ellis, *The maximum variance of a finite dataset, given its mean, minimum, and maximum* (2025 preprint). Finite-data maximum-variance formulation. [arXiv PDF](https://arxiv.org/pdf/2508.17525).
- **[R3]** A. N. Gorban, *Thermodynamic Tree: The Space of Admissible Paths* (2013), Lemma 4, Proposition 7, Lemma 14, and Section 3.3. Source for vertex access, the polytope-complement graph, and level-set component reduction. These statements and their relevant proofs were rechecked in the additional search. [Author's arXiv full text](https://arxiv.org/html/1201.6315v3).
- **[R4]** A. E. Rastegin, *Uncertainty relations in terms of generalized entropies derived from information diagrams* (2023), Theorem 1, equations (30)–(31). One identified explicit prior statement of the sharp maximum-probability bound at high collision probability; first priority for this branch is not established. [arXiv full text](https://arxiv.org/html/2305.18005v1).
- **[R5]** A. Goroncy and T. Rychlik, *How deviant can you be? The complete solution*, Mathematical Inequalities & Applications 9 (2006), 633–647. Comparison for deterministic order-statistic bounds; its hypotheses differ from the fixed-box setting here. [Publisher PDF](https://files.ele-math.com/articles/mia-09-57.pdf).
- **[R6]** E. H. Rubensson and A. M. N. Niklasson, *Accelerated density matrix expansions for Born–Oppenheimer molecular dynamics* (2013), Section 5.1. Comparison for near-idempotency and eigenvalue estimation. [arXiv full text](https://arxiv.org/html/1302.7292v1).
- **[R7]** A. Ek, A. Schutt, P. J. Stuckey, and G. Tack, *Explaining Propagation for Gini and Spread with Variable Mean*, CP 2022. Related constraint-propagation model; its exact theorem-level overlap requires further checking. [Official proceedings page](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2022.21).
- **[R8]** *Parameterless stopping criteria for recursive density matrix expansions*, arXiv:1507.02087v3. Additional comparison source: introduction, Theorem 1, and the HOMO/LUMO discussion in Section 6 were inspected; no complete theorem-by-theorem audit is claimed. [arXiv full text](https://arxiv.org/html/1507.02087v3).
- **[R9]** Lean 4.19.0 and Mathlib v4.19.0. Official version records for the proof environment: [Lean release](https://github.com/leanprover/lean4/releases/tag/v4.19.0) and [Mathlib tag](https://github.com/leanprover-community/mathlib4/tree/v4.19.0).
- **[R10]** E. H. Rubensson, E. Rudberg, and P. Sałek, *Density matrix purification with rigorous error control*, *Journal of Chemical Physics* 128, 074106 (2008), DOI 10.1063/1.2826343. Bibliography and abstract checked; full-text theorem comparison remains incomplete. [Publisher page](https://pubs.aip.org/aip/jcp/article-abstract/128/7/074106/921519).

<a id="en-next"></a>
## 11. Remaining proof and literature work

T9 now classifies the path components for every \(n,s\) when \(1/2<\eta<1\). Remaining mathematical questions include higher homotopy types in this regime and \(\eta\ge1\), when further integer-sum vertices enter the band.

The next formalization targets are the complete three-branch optimum with explicit attaining vectors, the two-segment construction, and the component classification. The next bibliographic targets are deterministic rank spacings under simultaneous box and moment constraints, sharp trace-based bounds for nearly idempotent matrices, and the full-dimensional face-complement reduction used in the hole example.

The current note records a useful collection of exact formulas, constructive proofs, and reproducible checks. It does not register an established new theorem or change the project's previously published E01/E02 ledger. The separate triangle-audit candidate X04 is outside this document's proof scope.
