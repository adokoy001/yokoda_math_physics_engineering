### Two bridges used in the additional code

These are ordinary mathematical derivations, not a report that the added Lean scripts compiled.

**From finite sums.** For every integer \(k\), with \(S=\sum x_i\) and \(D=\sum x_i(1-x_i)\), prove

\[
(S-k)(1-(S-k))\le D.
\]

Write \(F(S,D,k)=D-(S-k)(1-(S-k))\). Then

\[
F(S+t,D+t(1-t),k)=(1-t)F(S,D,k)+tF(S,D,k-1).
\]

The empty sequence gives \(F(0,0,k)=k(k+1)\ge0\). Both weights are nonnegative for \(0\le t\le1\), so finite induction proves the claim. This is a floor-free route to the classical packing bound.

**To the rounded count.** Assume \(0\le\eta\le1/2\), \(|S-s|\le\eta\), and \(D<1/2-\eta^2\). Round each coordinate to a nearest binary endpoint, with error \(d_i\le1/2\). Since \(d_i\le2x_i(1-x_i)\), the total error is less than one.

If the rounded count differs from \(s\), one side's error mass \(\rho\) is at least \(1-\eta\), while \(\rho<1\). Apply the finite-sum bound to \(2d_i\in[0,1]\) on that side, with integer offset \(k=1\). It gives

\[
\sum d_i^2\le\rho^2-\rho+\frac12,\qquad
\sum d_i(1-d_i)\ge\frac12-(1-\rho)^2\ge\frac12-\eta^2.
\]

This contradicts the total defect bound. A half-valued coordinate is excluded by applying packing to the remaining coordinates. This route makes the rounding proof independent of the topological classification.

Thirteen polynomial identities, including those used here, passed exact coefficient normalization. This does not check all inequality inferences, induction, square-root semantics or Lean types.
