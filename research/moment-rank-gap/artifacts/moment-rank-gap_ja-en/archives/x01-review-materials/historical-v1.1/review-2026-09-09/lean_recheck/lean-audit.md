# Lean independent audit — 2026 09 09

## Result

**This audit did not execute a fresh Lean compilation.** The current workspace has no `lean`, `lake`, or `elan` on `PATH`. An attempt to access the official Lean 4.19.0 release archive stopped because the network approval was cancelled before a decision was returned. No alternate mirror, proxy, permission escalation, or access-control workaround was attempted.

This is an environment-preparation failure, not a rejected mathematical proof. The preserved `verification.json` still records an earlier successful compilation of all 14 declarations. That historical record must not be described as an independent rerun performed on 2026 09 09.

The source SHA-256 was independently recalculated and matches the preserved record:

`3f29d4e1daad5ed467c6ef2a832a067b03546a2ca35293983f3675e76e70c9fa`

There are 14 theorem declarations and 14 `#print axioms` commands; no `sorry`, `admit`, or new `axiom` declaration appears in the source. These are source and artifact-integrity checks, not a substitute for compilation.

## Mathlib tag resolved against the official repository

The following read-only Git query completed with exit code 0:

```text
git ls-remote https://github.com/leanprover-community/mathlib4.git refs/tags/v4.19.0
c44e0c8ee63ca166450922a373c7409c5d26b00b	refs/tags/v4.19.0
```

Therefore the claimed tag-to-commit correspondence was directly confirmed on 2026 09 09. Primary repository reference: [Mathlib v4.19.0](https://github.com/leanprover-community/mathlib4/tree/v4.19.0).

The web reader did not retrieve the GitHub release/tree pages, but this did not affect the successful direct Git ref query. The tag query does not establish a new Lean compilation or independently verify the old Lean executable's binary hash.

## Review suggestion D: the stronger partition statement is already formalized

Let the finite coordinate index set have at least two elements, let `I` be a nonempty proper subset, and suppose `0 ≤ xᵢ ≤ 1`. Write

\[
S=\sum_i x_i,\qquad D=\sum_i x_i(1-x_i),\qquad
u=\min_{i\in I}x_i,\quad v=\max_{j\notin I}x_j.
\]

Then

\[
2D+(S-|I|)^2+(u-v)^2\ge1.
\]

The existing theorem **`MomentIslands.rank_gap_partition` proves exactly this inequality with minimum and maximum witnesses supplied explicitly**. Its hypotheses are:

- `ha : a ∈ I` and `hb : b ∉ I`;
- `hbox : ∀ i, 0 ≤ x i ∧ x i ≤ 1`;
- `hmin : ∀ i ∈ I, x a ≤ x i`;
- `hmax : ∀ j ∉ I, x j ≤ x b`.

There is **no** assumption `x b ≤ x a` in that theorem. Witness membership implies the two parts are nonempty. Since the sets are finite, ordinary minimum/maximum attainment gives the mathematical formulation above; the Lean file takes those witnesses as inputs rather than proving their existence in a separate theorem.

The bridge `finite_rank_gap` likewise has no cross-order hypothesis. It proves the result even for two finite collections that are not assumed disjoint, with the corresponding double-counted totals. The partition theorem specializes this bridge to `I` and its complement and rewrites the totals.

Only the next theorem, **`rank_gap_partition_sqrt`**, adds

```lean
(hab : x b ≤ x a)
```

to choose the nonnegative square-root branch. Without that ordering, the natural consequence is an absolute-gap bound,

\[
\sqrt{\max\{1-2D-(S-|I|)^2,0\}}\le |u-v|,
\]

not a positive bound on the signed quantity `u-v`. The example `x=(0,1)`, `I={1}` has `D=0`, `S=|I|=1`, and `u-v=-1`: the squared inequality is exact while a positive signed-gap conclusion would be false.

**Editorial implication:** broaden the first theorem to the arbitrary-partition squared inequality, then specialize to the sorted top-`s` partition for the nonnegative rank gap. This needs no change to the previously compiled Lean source or to its SHA-256. A new separate Lean theorem for existence of the extremal witnesses has not been compiled in this audit.

## Suggested concise Japanese wording

> Fable 5.1 の指摘を受け、基本不等式を任意の非空な真部分集合に対する形へ拡張して記載した。この形は既存の Lean 定理 `rank_gap_partition` が既に証明しており、二つの集合をまたぐ順序の仮定は不要である。非負の順位間隔として平方根を取る段階では順序の仮定を用いる。
>
> 2026 09 09 に Mathlib の公式 Git リポジトリへ照会し、タグ v4.19.0 がコミット `c44e0c8ee63ca166450922a373c7409c5d26b00b` を指すことを確認した。Lean の新規実行環境は公式配布物の取得時にネットワーク承認が取り消されて準備できず、今回の独立再コンパイルは未実施である。前回の成功ログと今回のソース監査を区別して掲載する。

## Evidence files

- `recheck-record.json`: machine-readable scope, source hash, tag result, environment outcome.
- `environment-attempt.log`: command and tool outcomes transcribed from the execution session.
- The historical `round2_formal/verification.json` and `lean-check.log` are unchanged.
