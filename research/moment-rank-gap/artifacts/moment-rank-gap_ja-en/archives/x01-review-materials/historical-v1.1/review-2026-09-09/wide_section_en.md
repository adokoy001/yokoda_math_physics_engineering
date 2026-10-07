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

**Status.** T9 is treated as an explicit corollary of Gorban's general theory of polytopes with convex obstacles. Priority for this particular band and component-count formula has not been established, and no novelty claim is confirmed. This section contains ordinary mathematical proofs and is outside the existing Lean verification scope.
