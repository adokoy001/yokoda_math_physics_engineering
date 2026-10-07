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
