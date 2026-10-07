import MomentIslands

open scoped BigOperators

namespace MomentIslands

/-- A floor-free form of the classical packing bound. It holds for every
integer offset, even when the offset is not the floor of the sum. -/
theorem integer_offset_defect {ι : Type*} (I : Finset ι) (x : ι → ℝ)
    (k : ℤ) (hbox : ∀ i ∈ I, 0 ≤ x i ∧ x i ≤ 1) :
    ((∑ i ∈ I, x i) - (k : ℝ)) *
        (1 - ((∑ i ∈ I, x i) - (k : ℝ))) ≤
      ∑ i ∈ I, x i * (1 - x i) := by
  classical
  revert hbox
  induction I using Finset.induction_on generalizing k with
  | empty =>
      intro hbox
      simp only [Finset.sum_empty]
      by_cases hk : 0 ≤ k
      · have hk' : (0 : ℝ) ≤ (k : ℝ) := by exact_mod_cast hk
        nlinarith [mul_nonneg hk' (show 0 ≤ (k : ℝ) + 1 by linarith)]
      · have hk1 : k + 1 ≤ 0 := Int.add_one_le_iff.mpr (lt_of_not_ge hk)
        have hk1' : (k : ℝ) + 1 ≤ 0 := by exact_mod_cast hk1
        nlinarith [mul_nonneg (show 0 ≤ -(k : ℝ) by linarith)
          (show 0 ≤ -(k : ℝ) - 1 by linarith)]
  | @insert a I ha ih =>
      intro hbox
      have hI : ∀ i ∈ I, 0 ≤ x i ∧ x i ≤ 1 := by
        intro i hi
        exact hbox i (Finset.mem_insert_of_mem hi)
      have ht := hbox a (Finset.mem_insert_self a I)
      have h0 := ih k hI
      have h1 := ih (k - 1) hI
      rw [Int.cast_sub, Int.cast_one] at h1
      have hw0 := mul_le_mul_of_nonneg_left h0 (sub_nonneg.mpr ht.2)
      have hw1 := mul_le_mul_of_nonneg_left h1 ht.1
      simp only [Finset.sum_insert ha]
      nlinarith [hw0, hw1]

/-- The usual sum-of-squares packing inequality, expressed at any integer
offset. Choosing the floor gives its sharp classical form. -/
theorem square_sum_integer_offset {ι : Type*} (I : Finset ι) (x : ι → ℝ)
    (k : ℤ) (hbox : ∀ i ∈ I, 0 ≤ x i ∧ x i ≤ 1) :
    (∑ i ∈ I, (x i) ^ 2) ≤
      (k : ℝ) + ((∑ i ∈ I, x i) - (k : ℝ)) ^ 2 := by
  have h := integer_offset_defect I x k hbox
  have hD : (∑ i ∈ I, x i * (1 - x i)) =
      (∑ i ∈ I, x i) - ∑ i ∈ I, (x i) ^ 2 := by
    rw [← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro i hi
    ring
  rw [hD] at h
  nlinarith

/-- The distance to any integer obeys the corresponding defect bound.
Only the range where this distance is at most one is informative. -/
theorem abs_integer_offset_defect {ι : Type*} (I : Finset ι) (x : ι → ℝ)
    (k : ℤ) (hbox : ∀ i ∈ I, 0 ≤ x i ∧ x i ≤ 1) :
    |(∑ i ∈ I, x i) - (k : ℝ)| *
        (1 - |(∑ i ∈ I, x i) - (k : ℝ)|) ≤
      ∑ i ∈ I, x i * (1 - x i) := by
  by_cases h : 0 ≤ (∑ i ∈ I, x i) - (k : ℝ)
  · rw [abs_of_nonneg h]
    exact integer_offset_defect I x k hbox
  · have hn : (∑ i ∈ I, x i) - (k : ℝ) ≤ 0 := le_of_not_ge h
    rw [abs_of_nonpos hn]
    have hbound := integer_offset_defect I x (k - 1) hbox
    rw [Int.cast_sub, Int.cast_one] at hbound
    nlinarith

/-- At a half-valued coordinate the defect has the sharp lower bound
1/2 minus the square of the total's offset from any integer. -/
theorem half_coordinate_defect {ι : Type*} [DecidableEq ι]
    (I : Finset ι) (x : ι → ℝ) (a : ι) (k : ℤ)
    (ha : a ∈ I) (hhalf : x a = 1 / 2)
    (hbox : ∀ i ∈ I, 0 ≤ x i ∧ x i ≤ 1) :
    1 / 2 - ((∑ i ∈ I, x i) - (k : ℝ)) ^ 2 ≤
      ∑ i ∈ I, x i * (1 - x i) := by
  have h := integer_offset_defect (I.erase a) x (k - 1)
    (fun i hi => hbox i (Finset.mem_of_mem_erase hi))
  rw [Int.cast_sub, Int.cast_one] at h
  have hS := Finset.sum_erase_add I x ha
  have hD := Finset.sum_erase_add I (fun i => x i * (1 - x i)) ha
  rw [hhalf] at hS hD
  nlinarith

/-- Below the half-coordinate barrier no coordinate can equal one half. -/
theorem no_half_below_barrier {ι : Type*} [DecidableEq ι]
    (I : Finset ι) (x : ι → ℝ) (k : ℤ) (eta delta : ℝ)
    (hbox : ∀ i ∈ I, 0 ≤ x i ∧ x i ≤ 1)
    (hmean : |(∑ i ∈ I, x i) - (k : ℝ)| ≤ eta)
    (hD : (∑ i ∈ I, x i * (1 - x i)) ≤ delta)
    (hdelta : delta < 1 / 2 - eta ^ 2) :
    ∀ a ∈ I, x a ≠ 1 / 2 := by
  intro a ha hhalf
  have h := half_coordinate_defect I x a k ha hhalf hbox
  have he : ((∑ i ∈ I, x i) - (k : ℝ)) ^ 2 ≤ eta ^ 2 := by
    have he0 := abs_nonneg ((∑ i ∈ I, x i) - (k : ℝ))
    have hp := mul_nonneg (sub_nonneg.mpr hmean)
      (show 0 ≤ eta + |(∑ i ∈ I, x i) - (k : ℝ)| by linarith)
    nlinarith [sq_abs ((∑ i ∈ I, x i) - (k : ℝ)), hp]
  linarith

/-- If entries lie in [0,1/2] and their total lies in [1-eta,1],
then their defect is at least 1/2-eta^2. This is the scaled packing
inequality used to rule out an incorrect nearest-integer count. -/
theorem half_bounded_mass_defect {ι : Type*} (I : Finset ι)
    (d : ι → ℝ) (eta : ℝ)
    (hbox : ∀ i ∈ I, 0 ≤ d i ∧ d i ≤ 1 / 2)
    (heta : 0 ≤ eta)
    (hlower : 1 - eta ≤ ∑ i ∈ I, d i)
    (hupper : (∑ i ∈ I, d i) ≤ 1) :
    1 / 2 - eta ^ 2 ≤ ∑ i ∈ I, d i * (1 - d i) := by
  have h := integer_offset_defect I (fun i => 2 * d i) 1 (by
    intro i hi
    constructor <;> nlinarith [(hbox i hi).1, (hbox i hi).2])
  have hS : (∑ i ∈ I, 2 * d i) = 2 * ∑ i ∈ I, d i := by
    rw [Finset.mul_sum]
  have hD : (∑ i ∈ I, (2 * d i) * (1 - 2 * d i)) =
      4 * (∑ i ∈ I, d i * (1 - d i)) - 2 * ∑ i ∈ I, d i := by
    rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_sub_distrib]
    apply Finset.sum_congr rfl
    intro i hi
    ring
  rw [hS, hD] at h
  norm_num only [Int.cast_one] at h
  have hsq : ((∑ i ∈ I, d i) - 1) ^ 2 ≤ eta ^ 2 := by
    nlinarith [mul_nonneg (show 0 ≤ eta + ((∑ i ∈ I, d i) - 1) by linarith)
      (show 0 ≤ eta - ((∑ i ∈ I, d i) - 1) by linarith)]
  nlinarith

end MomentIslands

#print axioms MomentIslands.integer_offset_defect
#print axioms MomentIslands.square_sum_integer_offset
#print axioms MomentIslands.abs_integer_offset_defect
#print axioms MomentIslands.half_coordinate_defect
#print axioms MomentIslands.no_half_below_barrier
#print axioms MomentIslands.half_bounded_mass_defect
