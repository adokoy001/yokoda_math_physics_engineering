# Lean検証パッケージ：モーメントと順位ギャップ

2026 09 08。**Lean 4.19.0 / Mathlib v4.19.0で14定理の検証に成功。終了コード0。**

全14定理の公理依存は `propext, Classical.choice, Quot.sound` のみ。独自公理・証明穴・`sorryAx` はない。通常のMathlibの実数・古典論理を使った証明であり、公理が全くないという意味ではない。

## 主結果の正確な範囲

有限個の実数 `x_i∈[0,1]` を考える。添字集合Iの内部でaを最小値の添字、補集合でbを最大値の添字とし、`x_b≤x_a` を仮定する。Iの個数をs、全総和をS、全欠損を `D=Σx_i(1−x_i)` とすると、形式検証した結論は

\[
\boxed{x_a-x_b\ge\sqrt{1-2D-(S-s)^2}.}
\]

平方根の中身が正なら、上位s個とそれ以外の間に、明示的な正の差が保証される。**Sが整数という仮定はない。** Leanの実数平方根は負の入力を0とするので、式自体は中身が正でない場合にも意味を持つ。

これは数個の集約変数だけの補題に留まらず、任意の有限添字型、実際の全総和、実際の全欠損和からの証明である。Iの最小値・補集合の最大値という仮定、Iと補集合への所属、箱制約はLeanソースに全て明記した。降順への並べ替え処理そのものは形式化していない。

他に、4変数例の不可能な部分和、任意有限次元の平衡誤差の鋭い二次欠損評価とその平方根反転、平方和欠損による集中評価、順位ギャップの等号に近い場合の余剰質量評価を検証した。

**今回形式化していないもの：** 部分和の完全な必要十分条件、全実現集合の連結成分数と同相型、前回の最近0/1丸め定理の全工程。平衡誤差の定理は左右誤差の質量が等しいことを明示的に仮定する。形式証明の成功は新規性の証明ではない。

## 再現

通常のLean環境で、後掲の `lean-toolchain`、`lakefile.toml`、`MomentIslands.lean` を同じフォルダに保存し、次を実行する。

```bash
lake update
lake exe cache get
lake env lean MomentIslands.lean
```

実行環境ではLeanの自己実行ファイル検出とPID名前空間に互換性問題があり、後掲の短いCコードで `/proc/<getpid()>/exe` という**自プロセスの実行位置参照だけ**を `/proc/self/exe` に置換した。Lean本体・数学カーネル・証明検査・数学公理は変更していない。この対応は通常のLinux環境では不要。

## 版固定ファイル

`lean-toolchain`:

```text
leanprover/lean4:v4.19.0
```

`lakefile.toml`:

```toml
name = "moment_islands_proof"
version = "0.1.0"
defaultTargets = ["MomentIslands"]

[[require]]
name = "mathlib"
git = "https://github.com/leanprover-community/mathlib4.git"
rev = "v4.19.0"

[[lean_lib]]
name = "MomentIslands"
```

## 検証済みLeanソース全文

```lean
import Mathlib.Data.Real.Sqrt
import Mathlib.Algebra.Order.BigOperators.Ring.Finset
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

/-!
Formal algebraic core of the moment-islands exploration.
The ambient scalar type is `Real`; these are universal proofs, not grid tests.
The global topological classification is deliberately outside this file.
-/

open scoped BigOperators

namespace MomentIslands

/-- The sharp upper bound on the squared norm of a nonnegative pair. -/
theorem pair_square_upper (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    a ^ 2 + b ^ 2 ≤ (a + b) ^ 2 := by
  nlinarith [mul_nonneg ha hb]

/-- Applying the same fact to the distances from the upper endpoint. -/
theorem pair_square_upper_complement (a b : ℝ) (ha : a ≤ 1) (hb : b ≤ 1) :
    a ^ 2 + b ^ 2 ≤ 1 + (a + b - 1) ^ 2 := by
  nlinarith [mul_nonneg (sub_nonneg.mpr ha) (sub_nonneg.mpr hb)]

/-- The four-variable example: partial sum one half forces Q ≤ 3/2. -/
theorem four_variable_gap_bound (a b c d : ℝ)
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : c ≤ 1) (hd : d ≤ 1)
    (hs : a + b + c + d = 2) (ht : a + b = 1 / 2) :
    a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 ≤ 3 / 2 := by
  have hab := pair_square_upper a b ha hb
  have hcd := pair_square_upper_complement c d hc hd
  have hsum : c + d = 3 / 2 := by linarith
  rw [ht] at hab
  rw [hsum] at hcd
  nlinarith

/-- There is no real witness to the article's forbidden partial sum. -/
theorem four_variable_gap (a b c d : ℝ)
    (ha : 0 ≤ a) (hb : 0 ≤ b) (hc : c ≤ 1) (hd : d ≤ 1)
    (hs : a + b + c + d = 2) (ht : a + b = 1 / 2)
    (hq : a ^ 2 + b ^ 2 + c ^ 2 + d ^ 2 = 9 / 5) : False := by
  have h := four_variable_gap_bound a b c d ha hb hc hd hs ht
  linarith

/-- Finite nonnegative errors on two sides, each summing to rho, obey
the sharp quadratic defect bound D ≥ 2 rho (1-rho). No dimension is fixed. -/
theorem balanced_error_defect {ι κ : Type*} (I : Finset ι) (J : Finset κ)
    (u : ι → ℝ) (v : κ → ℝ) (rho : ℝ)
    (hu : ∀ i ∈ I, 0 ≤ u i) (hv : ∀ j ∈ J, 0 ≤ v j)
    (hsu : ∑ i ∈ I, u i = rho) (hsv : ∑ j ∈ J, v j = rho) :
    2 * rho * (1 - rho) ≤
      (∑ i ∈ I, u i * (1 - u i)) + ∑ j ∈ J, v j * (1 - v j) := by
  have hu2 := Finset.sum_sq_le_sq_sum_of_nonneg hu
  have hv2 := Finset.sum_sq_le_sq_sum_of_nonneg hv
  rw [hsu] at hu2
  rw [hsv] at hv2
  have eu : (∑ i ∈ I, u i * (1 - u i)) = rho - ∑ i ∈ I, (u i) ^ 2 := by
    calc
      _ = ∑ i ∈ I, (u i - (u i) ^ 2) := by
        apply Finset.sum_congr rfl
        intro i hi
        ring
      _ = _ := by rw [Finset.sum_sub_distrib, hsu]
  have ev : (∑ j ∈ J, v j * (1 - v j)) = rho - ∑ j ∈ J, (v j) ^ 2 := by
    calc
      _ = ∑ j ∈ J, (v j - (v j) ^ 2) := by
        apply Finset.sum_congr rfl
        intro j hj
        ring
      _ = _ := by rw [Finset.sum_sub_distrib, hsv]
  rw [eu, ev]
  nlinarith

/-- Inversion on the small-error branch. This is the square-root constant
used in the sharp rounding estimate. -/
theorem invert_defect_bound (rho D : ℝ) (hrho : rho ≤ 1 / 2)
    (hbound : 2 * rho * (1 - rho) ≤ D) :
    rho ≤ (1 - Real.sqrt (1 - 2 * D)) / 2 := by
  have hn : 0 ≤ 1 - 2 * rho := by linarith
  have hs : 1 - 2 * D ≤ (1 - 2 * rho) ^ 2 := by nlinarith
  have hroot : Real.sqrt (1 - 2 * D) ≤ 1 - 2 * rho :=
    (Real.sqrt_le_left hn).mpr hs
  linarith

/-- Arbitrary finite nonnegative balanced errors satisfy the sharp bound
whenever their common mass is at most one half. -/
theorem balanced_error_sharp_bound {ι κ : Type*} (I : Finset ι) (J : Finset κ)
    (u : ι → ℝ) (v : κ → ℝ) (rho D : ℝ)
    (hu : ∀ i ∈ I, 0 ≤ u i) (hv : ∀ j ∈ J, 0 ≤ v j)
    (hsu : ∑ i ∈ I, u i = rho) (hsv : ∑ j ∈ J, v j = rho)
    (hrho : rho ≤ 1 / 2)
    (hD : (∑ i ∈ I, u i * (1 - u i)) +
      (∑ j ∈ J, v j * (1 - v j)) = D) :
    rho ≤ (1 - Real.sqrt (1 - 2 * D)) / 2 := by
  apply invert_defect_bound rho D hrho
  rw [← hD]
  exact balanced_error_defect I J u v rho hu hv hsu hsv

/-- A quantitative near-equality certificate. If a nonnegative vector of
mass rho has a designated maximal entry m, then its missing squared norm
controls all mass outside that entry. -/
theorem concentration_from_square_deficit {ι : Type*} (I : Finset ι)
    (u : ι → ℝ) (rho m eps : ℝ)
    (hu : ∀ i ∈ I, 0 ≤ u i) (hm : ∀ i ∈ I, u i ≤ m)
    (hs : ∑ i ∈ I, u i = rho)
    (hgap : rho ^ 2 - ∑ i ∈ I, (u i) ^ 2 ≤ eps) :
    rho * (rho - m) ≤ eps := by
  have hsq : (∑ i ∈ I, (u i) ^ 2) ≤ m * rho := by
    calc
      _ ≤ ∑ i ∈ I, m * u i := by
        apply Finset.sum_le_sum
        intro i hi
        nlinarith [mul_nonneg (hu i hi) (sub_nonneg.mpr (hm i hi))]
      _ = _ := by rw [← Finset.mul_sum, hs]
  nlinarith

/-- Scalar rank-gap core. The hypotheses are aggregated mass and defect
bounds; no claim that they automatically describe a sorted vector is hidden. -/
theorem rank_gap_core (u v sigma rho D e g : ℝ)
    (hu : 0 ≤ u) (hv : v ≤ 1)
    (hsigma : 1 - u ≤ sigma) (hrho : v ≤ rho)
    (hD : u * sigma + (1 - v) * rho ≤ D)
    (he : e = rho - sigma) (hg : g = u - v) :
    1 ≤ 2 * D + e ^ 2 + g ^ 2 := by
  have hpA := mul_nonneg (sub_nonneg.mpr hv) (sub_nonneg.mpr hsigma)
  have hpB := mul_nonneg hu (sub_nonneg.mpr hrho)
  have hsq := sq_nonneg ((rho - v) - (sigma - (1 - u)))
  have hid : 2 * D + e ^ 2 + g ^ 2 - 1 =
      2 * (D - (u * sigma + (1 - v) * rho)) +
      2 * ((1 - v) * (sigma - (1 - u))) +
      2 * (u * (rho - v)) + ((rho - v) - (sigma - (1 - u))) ^ 2 := by
    rw [he, hg]
    ring
  nlinarith

/-- A square-root version, on the nonnegative gap branch. -/
theorem rank_gap_sqrt (D e g : ℝ) (hg : 0 ≤ g)
    (h : 1 ≤ 2 * D + e ^ 2 + g ^ 2) :
    Real.sqrt (1 - 2 * D - e ^ 2) ≤ g := by
  apply (Real.sqrt_le_left hg).mpr
  linarith

/-- Near equality forces the mass outside the two boundary coordinates
to be small, with the coefficients and all hypotheses left explicit. -/
theorem rank_gap_slack (u v sigma rho D e g : ℝ)
    (hu : 0 ≤ u) (hv : v ≤ 1)
    (hsigma : 1 - u ≤ sigma) (hrho : v ≤ rho)
    (hD : u * sigma + (1 - v) * rho ≤ D)
    (he : e = rho - sigma) (hg : g = u - v) :
    2 * (1 - v) * (sigma - (1 - u)) ≤ 2 * D + e ^ 2 + g ^ 2 - 1 ∧
    2 * u * (rho - v) ≤ 2 * D + e ^ 2 + g ^ 2 - 1 := by
  have hpA := mul_nonneg (sub_nonneg.mpr hv) (sub_nonneg.mpr hsigma)
  have hpB := mul_nonneg hu (sub_nonneg.mpr hrho)
  have hsq := sq_nonneg ((rho - v) - (sigma - (1 - u)))
  have hid : 2 * D + e ^ 2 + g ^ 2 - 1 =
      2 * (D - (u * sigma + (1 - v) * rho)) +
      2 * ((1 - v) * (sigma - (1 - u))) +
      2 * (u * (rho - v)) + ((rho - v) - (sigma - (1 - u))) ^ 2 := by
    rw [he, hg]
    ring
  constructor <;> nlinarith

/-- The rank-gap inequality for arbitrary finite top/rest collections.
`a` is a minimum of the top collection, `b` a maximum of the rest.
Disjointness is not needed for this algebraic statement; a sorted vector's
disjoint partition is a direct specialization. -/
theorem finite_rank_gap {ι : Type*} (I J : Finset ι) (x : ι → ℝ) (a b : ι)
    (ha : a ∈ I) (hb : b ∈ J)
    (hI : ∀ i ∈ I, 0 ≤ x i ∧ x i ≤ 1)
    (hJ : ∀ j ∈ J, 0 ≤ x j ∧ x j ≤ 1)
    (hmin : ∀ i ∈ I, x a ≤ x i) (hmax : ∀ j ∈ J, x j ≤ x b) :
    1 ≤ 2 * ((∑ i ∈ I, x i * (1 - x i)) +
      ∑ j ∈ J, x j * (1 - x j)) +
      ((∑ j ∈ J, x j) - (∑ i ∈ I, (1 - x i))) ^ 2 + (x a - x b) ^ 2 := by
  have hsigma : 1 - x a ≤ ∑ i ∈ I, (1 - x i) :=
    Finset.single_le_sum (fun i hi => sub_nonneg.mpr (hI i hi).2) ha
  have hrho : x b ≤ ∑ j ∈ J, x j :=
    Finset.single_le_sum (fun j hj => (hJ j hj).1) hb
  have htop : x a * (∑ i ∈ I, (1 - x i)) ≤
      ∑ i ∈ I, x i * (1 - x i) := by
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro i hi
    exact mul_le_mul_of_nonneg_right (hmin i hi) (sub_nonneg.mpr (hI i hi).2)
  have hrest : (1 - x b) * (∑ j ∈ J, x j) ≤
      ∑ j ∈ J, x j * (1 - x j) := by
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro j hj
    nlinarith [mul_nonneg (hJ j hj).1 (sub_nonneg.mpr (hmax j hj))]
  exact rank_gap_core (x a) (x b) _ _ _ _ _
    (hI a ha).1 (hJ b hb).2 hsigma hrho (add_le_add htop hrest) rfl rfl

/-- The same bound expressed using the actual total and defect of a finite
vector. For a top-s partition the cardinality of I is exactly s. -/
theorem rank_gap_partition {ι : Type*} [Fintype ι] [DecidableEq ι]
    (I : Finset ι) (x : ι → ℝ) (a b : ι)
    (ha : a ∈ I) (hb : b ∉ I)
    (hbox : ∀ i, 0 ≤ x i ∧ x i ≤ 1)
    (hmin : ∀ i ∈ I, x a ≤ x i) (hmax : ∀ j ∉ I, x j ≤ x b) :
    1 ≤ 2 * (∑ i, x i * (1 - x i)) +
      ((∑ i, x i) - (I.card : ℝ)) ^ 2 + (x a - x b) ^ 2 := by
  have hb' : b ∈ Iᶜ := by simpa using hb
  have hmax' : ∀ j ∈ Iᶜ, x j ≤ x b := by
    intro j hj
    exact hmax j (by simpa using hj)
  have h := finite_rank_gap I Iᶜ x a b ha hb'
    (fun i _ => hbox i) (fun j _ => hbox j) hmin hmax'
  have htot := I.sum_add_sum_compl x
  have hdef := I.sum_add_sum_compl (fun i => x i * (1 - x i))
  have hsigma : (∑ i ∈ I, (1 - x i)) = (I.card : ℝ) - ∑ i ∈ I, x i := by
    simp only [Finset.sum_sub_distrib, Finset.sum_const, nsmul_eq_mul, mul_one]
  have he : (∑ j ∈ Iᶜ, x j) - (∑ i ∈ I, (1 - x i)) =
      (∑ i, x i) - (I.card : ℝ) := by
    rw [hsigma]
    linarith
  rwa [hdef, he] at h

/-- The robust separation estimate for the actual finite-vector moments.
The ordering assumption chooses the nonnegative square-root branch. -/
theorem rank_gap_partition_sqrt {ι : Type*} [Fintype ι] [DecidableEq ι]
    (I : Finset ι) (x : ι → ℝ) (a b : ι)
    (ha : a ∈ I) (hb : b ∉ I)
    (hbox : ∀ i, 0 ≤ x i ∧ x i ≤ 1)
    (hmin : ∀ i ∈ I, x a ≤ x i) (hmax : ∀ j ∉ I, x j ≤ x b)
    (hab : x b ≤ x a) :
    Real.sqrt (1 - 2 * (∑ i, x i * (1 - x i)) -
      ((∑ i, x i) - (I.card : ℝ)) ^ 2) ≤ x a - x b := by
  exact rank_gap_sqrt _ _ _ (sub_nonneg.mpr hab)
    (rank_gap_partition I x a b ha hb hbox hmin hmax)

end MomentIslands

#print axioms MomentIslands.pair_square_upper
#print axioms MomentIslands.pair_square_upper_complement
#print axioms MomentIslands.four_variable_gap_bound
#print axioms MomentIslands.four_variable_gap
#print axioms MomentIslands.balanced_error_defect
#print axioms MomentIslands.invert_defect_bound
#print axioms MomentIslands.balanced_error_sharp_bound
#print axioms MomentIslands.concentration_from_square_deficit
#print axioms MomentIslands.rank_gap_core
#print axioms MomentIslands.rank_gap_sqrt
#print axioms MomentIslands.rank_gap_slack
#print axioms MomentIslands.finite_rank_gap
#print axioms MomentIslands.rank_gap_partition
#print axioms MomentIslands.rank_gap_partition_sqrt

#check MomentIslands.rank_gap_partition_sqrt
#check MomentIslands.balanced_error_sharp_bound
```

## 実行ログ

```text
'MomentIslands.pair_square_upper' depends on axioms: [propext, Classical.choice, Quot.sound]
'MomentIslands.pair_square_upper_complement' depends on axioms: [propext, Classical.choice, Quot.sound]
'MomentIslands.four_variable_gap_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'MomentIslands.four_variable_gap' depends on axioms: [propext, Classical.choice, Quot.sound]
'MomentIslands.balanced_error_defect' depends on axioms: [propext, Classical.choice, Quot.sound]
'MomentIslands.invert_defect_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'MomentIslands.balanced_error_sharp_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
'MomentIslands.concentration_from_square_deficit' depends on axioms: [propext, Classical.choice, Quot.sound]
'MomentIslands.rank_gap_core' depends on axioms: [propext, Classical.choice, Quot.sound]
'MomentIslands.rank_gap_sqrt' depends on axioms: [propext, Classical.choice, Quot.sound]
'MomentIslands.rank_gap_slack' depends on axioms: [propext, Classical.choice, Quot.sound]
'MomentIslands.finite_rank_gap' depends on axioms: [propext, Classical.choice, Quot.sound]
'MomentIslands.rank_gap_partition' depends on axioms: [propext, Classical.choice, Quot.sound]
'MomentIslands.rank_gap_partition_sqrt' depends on axioms: [propext, Classical.choice, Quot.sound]
MomentIslands.rank_gap_partition_sqrt.{u_1} {ι : Type u_1} [Fintype ι] [DecidableEq ι] (I : Finset ι) (x : ι → ℝ)
  (a b : ι) (ha : a ∈ I) (hb : b ∉ I) (hbox : ∀ (i : ι), 0 ≤ x i ∧ x i ≤ 1) (hmin : ∀ i ∈ I, x a ≤ x i)
  (hmax : ∀ j ∉ I, x j ≤ x b) (hab : x b ≤ x a) : √(1 - 2 * ∑ i, x i * (1 - x i) - (∑ i, x i - ↑I.card) ^ 2) ≤ x a - x b
MomentIslands.balanced_error_sharp_bound.{u_1, u_2} {ι : Type u_1} {κ : Type u_2} (I : Finset ι) (J : Finset κ)
  (u : ι → ℝ) (v : κ → ℝ) (rho D : ℝ) (hu : ∀ i ∈ I, 0 ≤ u i) (hv : ∀ j ∈ J, 0 ≤ v j) (hsu : ∑ i ∈ I, u i = rho)
  (hsv : ∑ j ∈ J, v j = rho) (hrho : rho ≤ 1 / 2) (hD : ∑ i ∈ I, u i * (1 - u i) + ∑ j ∈ J, v j * (1 - v j) = D) :
  rho ≤ (1 - √(1 - 2 * D)) / 2

Exit code: 0
```

## 実行場所検出の互換コード

```c
/* Runtime compatibility only. Lean 4.19 asks for /proc/<getpid()>/exe;
   this host virtualizes getpid independently of procfs. Resolve that one
   spelling through /proc/self/exe, the same process's executable.
   No Lean source, proof checker, mathematical primitive, or other pathname
   is changed. */
#define _GNU_SOURCE
#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>

ssize_t readlink(const char *path, char *buf, size_t bufsiz) {
    static ssize_t (*real_readlink)(const char *, char *, size_t) = NULL;
    if (!real_readlink) real_readlink = dlsym(RTLD_NEXT, "readlink");
    char current[64];
    snprintf(current, sizeof(current), "/proc/%d/exe", (int)getpid());
    if (strcmp(path, current) == 0)
        return real_readlink("/proc/self/exe", buf, bufsiz);
    return real_readlink(path, buf, bufsiz);
}
```

## 再実行・ログ記録スクリプト

```python
#!/usr/bin/env python3
"""Run the unmodified Lean kernel with a pinned Mathlib checkout.

Example for this workspace:
  python3 verify.py --lean-root ../formal_env/lean-4.19.0-linux \
    --mathlib-root ../formal_env/mathlib4 \
    --compat-library ../formal_env/proc_self_compat.so

On a standard Lean/Lake installation use the three commands in README.md.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--lean-root', type=Path, required=True)
p.add_argument('--mathlib-root', type=Path, required=True)
p.add_argument('--compat-library', type=Path)
args = p.parse_args()
out = Path(__file__).resolve().parent
source = out / 'MomentIslands.lean'
leanroot = args.lean_root.resolve()
mathlib = args.mathlib_root.resolve()
env = os.environ.copy()
env['PATH'] = str(leanroot / 'bin') + os.pathsep + env.get('PATH', '')
if args.compat_library:
    env['LD_PRELOAD'] = str(args.compat_library.resolve())

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(command, cwd):
    r = subprocess.run(command, cwd=cwd, env=env, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return {'command': [str(x) for x in command], 'cwd': str(cwd),
            'exit_code': r.returncode, 'output': r.stdout}

version = run([str(leanroot / 'bin/lean'), '--version'], out)
commit = run(['git', 'rev-parse', 'HEAD'], mathlib)
command = [str(leanroot / 'bin/lake'), 'env', 'lean', '--root=' + str(out),
           '-o', str(out / 'MomentIslands.olean'), str(source)]
result = run(command, mathlib)
source_text = source.read_text(encoding='utf-8')
axiom_audit = {
    'theorem_declarations': len(re.findall(r'^theorem\s+', source_text, re.M)),
    'axiom_print_commands': len(re.findall(r'^#print axioms\s+', source_text, re.M)),
    'sorry_axiom_in_output': 'sorryAx' in result['output'],
    'new_axiom_declarations': bool(re.search(r'^\s*axiom\s+', source_text, re.M)),
    'placeholder_tokens': bool(re.search(r'\b(?:sorry|admit)\b', source_text)),
}
passed = (result['exit_code'] == 0 and not axiom_audit['sorry_axiom_in_output']
          and not axiom_audit['new_axiom_declarations']
          and not axiom_audit['placeholder_tokens']
          and axiom_audit['theorem_declarations'] == axiom_audit['axiom_print_commands'])
attempt = len(list(out.glob('lean-attempt-*.log'))) + 1
log = out / f'lean-attempt-{attempt:02d}.log'
log.write_text(result['output'], encoding='utf-8')
(out / 'lean-check.log').write_text(result['output'], encoding='utf-8')
record = {
    'status': 'PASS' if passed else 'FAIL',
    'lean_version': version,
    'mathlib_commit': commit,
    'proof_check': result,
    'axiom_audit': axiom_audit,
    'source_sha256': sha(source),
    'lean_binary_sha256': sha(leanroot / 'bin/lean'),
    'lean_shared_library_sha256': sha(leanroot / 'lib/lean/libleanshared.so'),
    'runtime_compatibility': {
        'used': bool(args.compat_library),
        'scope': 'Only readlink(/proc/<getpid()>/exe) is resolved as /proc/self/exe.',
        'lean_kernel_modified': False,
        'source_sha256': sha(out / 'proc_self_compat.c')
    },
}
(out / 'verification.json').write_text(
    json.dumps(record, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(version['output'], end='')
print(result['output'], end='')
print('Exit code:', result['exit_code'])
sys.exit(0 if passed else 1)
```

## 検証記録

```json
{
  "status": "PASS",
  "lean_version": {
    "command": [
      "/workspace/scratch/969dff4f4f1c/formal_env/lean-4.19.0-linux/bin/lean",
      "--version"
    ],
    "cwd": "/workspace/scratch/969dff4f4f1c/round2_formal",
    "exit_code": 0,
    "output": "Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)\n"
  },
  "mathlib_commit": {
    "command": [
      "git",
      "rev-parse",
      "HEAD"
    ],
    "cwd": "/workspace/scratch/969dff4f4f1c/formal_env/mathlib4",
    "exit_code": 0,
    "output": "c44e0c8ee63ca166450922a373c7409c5d26b00b\n"
  },
  "proof_check": {
    "command": [
      "/workspace/scratch/969dff4f4f1c/formal_env/lean-4.19.0-linux/bin/lake",
      "env",
      "lean",
      "--root=/workspace/scratch/969dff4f4f1c/round2_formal",
      "-o",
      "/workspace/scratch/969dff4f4f1c/round2_formal/MomentIslands.olean",
      "/workspace/scratch/969dff4f4f1c/round2_formal/MomentIslands.lean"
    ],
    "cwd": "/workspace/scratch/969dff4f4f1c/formal_env/mathlib4",
    "exit_code": 0,
    "output": "'MomentIslands.pair_square_upper' depends on axioms: [propext, Classical.choice, Quot.sound]\n'MomentIslands.pair_square_upper_complement' depends on axioms: [propext, Classical.choice, Quot.sound]\n'MomentIslands.four_variable_gap_bound' depends on axioms: [propext, Classical.choice, Quot.sound]\n'MomentIslands.four_variable_gap' depends on axioms: [propext, Classical.choice, Quot.sound]\n'MomentIslands.balanced_error_defect' depends on axioms: [propext, Classical.choice, Quot.sound]\n'MomentIslands.invert_defect_bound' depends on axioms: [propext, Classical.choice, Quot.sound]\n'MomentIslands.balanced_error_sharp_bound' depends on axioms: [propext, Classical.choice, Quot.sound]\n'MomentIslands.concentration_from_square_deficit' depends on axioms: [propext, Classical.choice, Quot.sound]\n'MomentIslands.rank_gap_core' depends on axioms: [propext, Classical.choice, Quot.sound]\n'MomentIslands.rank_gap_sqrt' depends on axioms: [propext, Classical.choice, Quot.sound]\n'MomentIslands.rank_gap_slack' depends on axioms: [propext, Classical.choice, Quot.sound]\n'MomentIslands.finite_rank_gap' depends on axioms: [propext, Classical.choice, Quot.sound]\n'MomentIslands.rank_gap_partition' depends on axioms: [propext, Classical.choice, Quot.sound]\n'MomentIslands.rank_gap_partition_sqrt' depends on axioms: [propext, Classical.choice, Quot.sound]\nMomentIslands.rank_gap_partition_sqrt.{u_1} {ι : Type u_1} [Fintype ι] [DecidableEq ι] (I : Finset ι) (x : ι → ℝ)\n  (a b : ι) (ha : a ∈ I) (hb : b ∉ I) (hbox : ∀ (i : ι), 0 ≤ x i ∧ x i ≤ 1) (hmin : ∀ i ∈ I, x a ≤ x i)\n  (hmax : ∀ j ∉ I, x j ≤ x b) (hab : x b ≤ x a) : √(1 - 2 * ∑ i, x i * (1 - x i) - (∑ i, x i - ↑I.card) ^ 2) ≤ x a - x b\nMomentIslands.balanced_error_sharp_bound.{u_1, u_2} {ι : Type u_1} {κ : Type u_2} (I : Finset ι) (J : Finset κ)\n  (u : ι → ℝ) (v : κ → ℝ) (rho D : ℝ) (hu : ∀ i ∈ I, 0 ≤ u i) (hv : ∀ j ∈ J, 0 ≤ v j) (hsu : ∑ i ∈ I, u i = rho)\n  (hsv : ∑ j ∈ J, v j = rho) (hrho : rho ≤ 1 / 2) (hD : ∑ i ∈ I, u i * (1 - u i) + ∑ j ∈ J, v j * (1 - v j) = D) :\n  rho ≤ (1 - √(1 - 2 * D)) / 2\n"
  },
  "axiom_audit": {
    "theorem_declarations": 14,
    "axiom_print_commands": 14,
    "sorry_axiom_in_output": false,
    "new_axiom_declarations": false,
    "placeholder_tokens": false
  },
  "source_sha256": "3f29d4e1daad5ed467c6ef2a832a067b03546a2ca35293983f3675e76e70c9fa",
  "lean_binary_sha256": "92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023",
  "lean_shared_library_sha256": "2ab605c74c78f9ba4431a7b5305a4b28a9071d8a826f223eb14fe5530f78e14d",
  "runtime_compatibility": {
    "used": true,
    "scope": "Only readlink(/proc/<getpid()>/exe) is resolved as /proc/self/exe.",
    "lean_kernel_modified": false,
    "source_sha256": "2f3fe42f8e76de61473891406a97503891bc057dbfc68e37406a6b6c0f30ce12"
  }
}
```
