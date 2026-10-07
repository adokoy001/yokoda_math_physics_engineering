# X01 — formal proof development checkpoint / 形式証明の追加作業

Date / 日付: 2026 09 09

**New code status: NOT COMPILED. 追加した証明コードは Lean 実行未確認です。**

This package contains 33 new theorem statements with proof scripts, plus the
unchanged 14-theorem original module. The 14 original declarations have a
preserved successful run from 2026 09 08. That historical run does not cover the
new modules and is not a fresh run in this environment.

追加分について実施したのは数学的導出、独立の静的点検、13個の有理係数多項式恒等式の
正規化検査です。Lean の構文・型・タクティク・カーネル検査は実行できていません。
追加公理や証明の穴を宣言して穴埋めするコードは入れていませんが、それだけで
コンパイル成功や形式証明の完成を意味しません。

## Why execution is blocked / 実行できなかった理由

Lean, Lake and Elan are absent from the current environment.
An attempt to fetch the official Lean 4.19.0 release ended with:
"network approval was cancelled before a decision was returned".
No successful download or new Lean compilation was recorded.
No alternate mirror or access-control workaround was used.

After the user explicitly authorized a retry, the Lean release download
returned the same cancellation. The pinned Mathlib source checkout succeeded
and matches c44e0c8ee63ca166450922a373c7409c5d26b00b.
That source checkout enables API inspection, but supplies neither the Lean
runtime nor compiled dependencies. See retry-record.json.

明示的な再試行の許可後もLean取得は同じエラーで停止しました。
一方、Mathlibの固定版ソースは取得でき、使用APIとの照合に利用しました。
ソース取得をLean検証成功とは扱いません。

## Added scope / 追加した範囲

- Packing.lean: finite induction for the integer-offset defect bound;
  absolute integer offset; exclusion of half-valued coordinates; scaled packing.
- BandSharp.lean: all three scalar branches of T2 and their two-coordinate witnesses.
- FiniteBand.lean: actual finite-vector lower bound, arbitrary-dimensional padded
  attainment witnesses, and a half-valued witness at the T4 rounding threshold.
- Rounding.lean: nearest 0/1 rounding, cardinality preservation, unique global
  binary L1 minimizer, and the sharp integer-total L1 error estimate.

finite_band_gap makes the partition, attained extrema and their ordering explicit.
finite_band_attainment uses the index type
(Fin p ⊕ Unit) ⊕ (Unit ⊕ Fin q), with p+1 upper and q+1 lower coordinates.
It proves the box, moments and boundary ordering for arbitrary p and q.
Transport to a particular sorted Fin n enumeration is not implemented as an
additional sorting-algorithm theorem.

robust_total_rounding proves a sufficient condition with eta >= 0:
|S-s| <= eta and D < 1/2-eta^2 imply the rounded cardinality is s and no tie occurs.
The threshold witness assumes 0 <= eta <= 1/2. No optimal threshold for wider
eta is claimed.

Theorems about path components and higher homotopy (T3, T6–T9), the complete
equality classification and full stability statement are not newly formalized
in this package. Priority and novelty are not questions settled by Lean.

## Main mathematical step / 有限和をつなぐ核

For any finite x_i in [0,1] and any integer k, define S=sum x_i and
D=sum x_i(1-x_i). Then

    (S-k)(1-(S-k)) <= D.

Write F(S,D,k)=D-(S-k)(1-(S-k)).
For a new coordinate t in [0,1],

    F(S+t, D+t(1-t), k)
       = (1-t) F(S,D,k) + t F(S,D,k-1).

The empty-vector case is F(0,0,k)=k(k+1)>=0 for integer k.
Both weights are nonnegative, so finite induction gives the result.
This is a floor-free proof of a classical packing bound, not a novelty claim.

For rounding, an incorrect count forces an error mass rho >= 1-eta on one side.
Each error is in [0,1/2]; D<1/2-eta^2 implies rho<1.
The scaled packing inequality gives that side's defect >=1/2-(1-rho)^2
>=1/2-eta^2, a contradiction. This avoids a dependency on topology.

## Reproduce with a standard Lean installation / 再現手順

Use the [official Lean installation instructions](https://lean-lang.org/install/).

Then, in the directory containing these files:

    lake update
    lake exe cache get
    python3 verify.py

Lean is pinned to 4.19.0, and Mathlib to commit
c44e0c8ee63ca166450922a373c7409c5d26b00b.
The verifier checks both versions, runs lake build, queries every theorem's
axioms and records logs and source SHA-256 hashes in run-results/.
Only propext, Classical.choice and Quot.sound are allowed.
Missing runtime is BLOCKED, proof/build failure is FAIL, and only a completed
build plus axiom audit can produce PASS.

The included verification record is BLOCKED, because no Lean runtime exists.
The full Lean runner itself has not yet been exercised against a successful
installation; its setup/build steps may require ordinary corrections.

## Optional exact algebra check / 補助的な恒等式検査

    python3 algebra_check.py

This uses rational coefficient normalization without external Python packages.
It checks only the 13 listed polynomial identities.
It does not check all inequality inferences, finite induction, casts, square-root
semantics or Lean proofs, and is not a replacement proof assistant.

## Historical evidence / 過去の記録

historical/ contains the original verification JSON and Lean output for the
unchanged MomentIslands.lean, preserved separately from the current result.
They must not be presented as evidence that the extension compiled.
