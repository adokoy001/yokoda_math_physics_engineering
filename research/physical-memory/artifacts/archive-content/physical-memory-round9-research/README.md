# Round 9 research and reproduction package

2026 09 29

This package contains analytic notes, bounded literature comparisons, and reproducibility checks.
Academic priority is not established. Known decomposition theorems and the classical Gamma
rejection-envelope constant are credited in the notes. Supremum and finite attainment are distinct.

Main notes:
- round9_kernel.md: reversible positive semigroup envelope; exact fixed-kernel supremum.
- round9_weighted.md: fixed triangle-free static graph, exact state-allocation reduction.
- round9_atomic.md: multipartite CP Gram stability and balance-preserving approximation.
- round9_audit.md: independent proof audit, including the exact-supremum additions.
- round9_phase_prior.md: checked literature and limitations of novelty assessment.
- round9_finite_example.md: finite 3-state construction and a rigorous 2-state exclusion.

Python 3, standard library only:
  python3 round9_atomic_verify.py
  python3 round9_audit_check.py
  python3 round9_weighted_rectangle.py
  python3 round9_finite_example.py

Each writes results to the same-basename .json file next to the script.
Optional additional check requires NumPy and SciPy:
  python3 round9_weighted_check.py

The rectangular-window optimizer has an analytic global optimal rate; its displayed DP values
use floating arithmetic. The separate finite-example script uses exact rational Taylor bounds
for its strict inequality. The minimum of 3 states is also proved analytically.

No external paper or book PDF is distributed here. Source URLs are in the notes and HTML.
Checks corroborate algebra and implementation; the proofs, not random trials, justify the claims.
