# Moment Islands — Lean 4 proof package

Status: **PASS**. All 14 theorem declarations were compiled by Lean 4.19.0, exit code 0. Every `#print axioms` result contains only `[propext, Classical.choice, Quot.sound]`. The source contains no proof placeholders or new axiom declarations. The authoritative machine-readable record is `verification.json`.

## Scope

`MomentIslands.lean` formalizes statements over `ℝ`, including arbitrary finite index types. These are universal mathematical proofs, not checks on a finite numeric grid.

The principal new formalization is `rank_gap_partition_sqrt`. Let `I` be a finite top collection, let `a` attain its minimum, and let `b` attain the maximum of its complement. Suppose every coordinate is in [0,1] and `x b ≤ x a`. The theorem proves

\[
\sqrt{1-2\sum_i x_i(1-x_i)-(\sum_i x_i-|I|)^2}\le x_a-x_b.
\]

The real square root is defined to be zero on negative inputs. Thus the theorem itself does not require the radicand to be positive. A strict positive radicand is the condition that makes its conclusion a positive separation guarantee.

The finite partition, box bounds, and minimum/maximum hypotheses are all explicit in the Lean statement. The preceding `finite_rank_gap` proves the finite-sum bridge from these hypotheses to the scalar algebraic certificate.

Other formalized results:

- Two-variable squared-norm upper bounds.
- The four-variable example: total 2 and first-pair total 1/2 force squared norm ≤3/2, hence exclude squared norm 9/5.
- Arbitrary finite nonnegative errors of equal mass ρ satisfy D≥2ρ(1−ρ).
- On ρ≤1/2 this implies the sharp square-root bound ρ≤(1−√(1−2D))/2.
- A concentration estimate from the deficit of a nonnegative vector's squared norm.
- Quantitative rank-gap slack bounds: near equality constrains the residual mass outside the two boundary entries.

The package does **not** formalize the full partial-sum necessary-and-sufficient criterion, the global component classification, the existence of a sorted enumeration, or the prior note's complete nearest-rounding theorem. In particular, the balanced-error theorem explicitly assumes the two masses are equal; it does not silently prove that a specified rounding produces this balance. Novelty and attribution are research questions outside proof checking.

## Standard reproduction

Install Lean using its official installation procedure. In this directory run:

```bash
lake update
lake exe cache get
lake env lean MomentIslands.lean
```

`lean-toolchain` pins Lean 4.19.0; `lakefile.toml` pins Mathlib v4.19.0. The Mathlib commit used in the recorded run is `c44e0c8ee63ca166450922a373c7409c5d26b00b`.

Each theorem is followed by `#print axioms`. The final output is saved as `lean-check.log`, and commands, exit codes, version, and source hashes are recorded in `verification.json`. Intermediate failed compilation logs, if any, are retained as `lean-attempt-NN.log`.

## This host's runtime compatibility

The official Lean 4.19.0 executable initially exited with `error: failed to locate application`. The reason was that this host's PID namespace and its procfs view disagreed. Lean's runtime (`src/runtime/io.cpp`, `lean_io_app_path`) spells the current executable as `/proc/<getpid()>/exe`; here that path was absent even though `/proc/self/exe` worked.

`proc_self_compat.c` is a narrowly scoped runtime compatibility shim. It rewrites only that exact process-self executable pathname to `/proc/self/exe` and forwards every other `readlink` call unchanged. It changes no Lean source, mathematical primitive, theorem, axiom, elaborator, or kernel check. The official executable and `libleanshared.so` are unmodified; their hashes are recorded.

Compile the shim if the same host problem occurs:

```bash
gcc -shared -fPIC -O2 -o proc_self_compat.so proc_self_compat.c -ldl
```

The exact workspace reproduction was:

```bash
python3 verify.py --lean-root ../formal_env/lean-4.19.0-linux \
  --mathlib-root ../formal_env/mathlib4 \
  --compat-library ../formal_env/proc_self_compat.so
```

The shim is unnecessary on a standard Linux host. Mathlib's cache archive extraction also needed the normal tar option `TAR_OPTIONS=--no-same-owner` because archive ownership IDs were unavailable here. No network proxy, alternate mirror, permission escalation, or access-control change was introduced.
