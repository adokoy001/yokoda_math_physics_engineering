# Review request for Fable: X01 integrated edition 1.2
Date: 2026 09 09

Please review this self-contained HTML before possible blog publication.
The labels T1–T9 are internal references, not certifications of novelty.

## Evidence status
- The original 14 declarations in MomentIslands.lean have a preserved successful run dated 2026 09 08; the source hash matches.
- The 33 added declarations in Packing.lean, BandSharp.lean, FiniteBand.lean and Rounding.lean are not compiled. Inspection against the pinned Mathlib APIs does not substitute for elaboration or kernel checking.
- If Lean is available, use version 4.19.0 and Mathlib commit c44e0c8ee63ca166450922a373c7409c5d26b00b with the included verify.py. Otherwise state that no execution occurred.
- Component and homotopy classifications have ordinary mathematical proofs and are outside the Lean-checked scope.
- Some exact prior statements remain unidentified; novelty is unconfirmed.

## Review priorities
1. Distinguish T1's arbitrary-partition squared inequality from the square-root version requiring boundary order. Check the nonnegative slack decomposition, equality conditions and stability assumptions.
2. Check all three branches of T2, including eta=0, eta=1/2 and both defect thresholds, as well as attaining configurations in arbitrary dimensions. Check quantifiers in the bridge from finite vectors to Lean partitions and from padded configurations to ranked gaps.
3. Check T4's preserved rounded count, uniqueness of the binary L1 minimizer, and the strict threshold. Inspect the topology-free argument in the added code.
4. Check the assumptions in the polytope/convex-obstacle reduction for T6–T9. T7 includes P itself among closed faces and uses relative boundaries. In T8, distinguish two retractions from a common complement from a direct retraction of the level set onto the face complex.
5. Check T9 at k=eta(1-eta), c=(1-eta^2)/2 and h=1/4, including c=h, boundary ranks and equality at every threshold.
6. Check attribution against the 2008 maximum-coordinate bound, the known integer-total and boundary-rank corollaries, and Gorban's example of nonmonotone component counts. Identify any overclaim or closer antecedent, with a precise source and theorem location.
7. Distinguish scalar eigenvalue bounds from topology of matrix spaces. Ensure finite numerical checks are not presented as proofs over an entire continuous space.
8. Check that assumptions, conclusions and evidence status agree between the Japanese and English versions.

## Requested response
For each finding, give the theorem/section, issue type, evidence or counterexample, and required correction.
Separate mathematical errors, omitted proof steps, Lean implementation errors, attribution, and editorial improvements.
For portions with no issue found, describe the scope actually checked. Do not call a reading review formal verification.
