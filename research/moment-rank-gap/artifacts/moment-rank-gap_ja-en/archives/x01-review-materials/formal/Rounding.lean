import MomentIslands
import Packing
import Mathlib.Tactic

/-!
Finite-vector nearest-binary rounding.  No sortedness hypothesis and no
topological connectedness theorem are needed for the integer-total result.
-/

open scoped BigOperators

namespace MomentIslands

noncomputable def round01 (t : ℝ) : ℝ := by
  classical
  exact if 1 / 2 < t then 1 else 0

noncomputable def roundedOnes {ι : Type*} [Fintype ι] (x : ι → ℝ) : Finset ι := by
  classical
  exact Finset.univ.filter (fun i => 1 / 2 < x i)

theorem mem_roundedOnes {ι : Type*} [Fintype ι] (x : ι → ℝ) (i : ι) :
    i ∈ roundedOnes x ↔ 1 / 2 < x i := by
  classical
  simp [roundedOnes]

/-- The chosen rounded value is always binary. -/
theorem round01_binary (t : ℝ) : round01 t = 0 ∨ round01 t = 1 := by
  classical
  unfold round01
  split_ifs <;> simp

/-- The sum of rounded entries is exactly the cardinality of the ones set. -/
theorem sum_round01 {ι : Type*} [Fintype ι] [DecidableEq ι] (x : ι → ℝ) :
    (∑ i, round01 (x i)) = ((roundedOnes x).card : ℝ) := by
  classical
  let I := roundedOnes x
  have htop : (∑ i ∈ I, round01 (x i)) = (I.card : ℝ) := by
    calc
      _ = ∑ _i ∈ I, (1 : ℝ) := by
        apply Finset.sum_congr rfl
        intro i hi
        exact if_pos ((mem_roundedOnes x i).mp hi)
      _ = _ := by simp
  have hrest : (∑ i ∈ Iᶜ, round01 (x i)) = 0 := by
    apply Finset.sum_eq_zero
    intro i hi
    have hn : i ∉ roundedOnes x := by simpa [I] using hi
    exact if_neg (fun h => hn ((mem_roundedOnes x i).mpr h))
  have h := I.sum_add_sum_compl (fun i => round01 (x i))
  rw [htop, hrest, add_zero] at h
  exact h.symm

/-- Off the tie hyperplane, the nearer binary endpoint is unique. -/
theorem round01_unique_nearest (t b : ℝ) (ht : t ≠ 1 / 2)
    (hb : b = 0 ∨ b = 1) (hbest : |t - b| ≤ |t - round01 t|) :
    b = round01 t := by
  classical
  unfold round01 at *
  split_ifs at * with h
  · rcases hb with rfl | rfl
    · have ht0 : 0 ≤ t := by linarith
      rw [sub_zero, abs_of_nonneg ht0] at hbest
      have hab : |t - 1| < t := by
        apply abs_lt.mpr
        constructor <;> linarith
      linarith
    · rfl
  · have ht' : t < 1 / 2 := by
      rcases lt_or_eq_of_le (le_of_not_gt h) with hlt | heq
      · exact hlt
      · exact (ht heq).elim
    rcases hb with rfl | rfl
    · rfl
    · have ht1 : t - 1 ≤ 0 := by linarith
      rw [abs_of_nonpos ht1, sub_zero] at hbest
      have hab : |t| < 1 - t := by
        apply abs_lt.mpr
        constructor <;> linarith
      linarith

/-- The error of either nearest endpoint is at most twice the scalar defect. -/
theorem round01_error_le (t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    |t - round01 t| ≤ 2 * (t * (1 - t)) := by
  classical
  unfold round01
  split_ifs with h
  · rw [abs_of_nonpos (by linarith : t - 1 ≤ 0)]
    nlinarith [mul_nonneg (by linarith : 0 ≤ 1 - t) (by linarith : 0 ≤ 2 * t - 1)]
  · rw [sub_zero, abs_of_nonneg ht0]
    nlinarith [mul_nonneg ht0 (by linarith : 0 ≤ 1 - 2 * t)]

/-- Rounding minimizes distance among the two endpoints, including ties. -/
theorem round01_nearest (t b : ℝ) (hb : b = 0 ∨ b = 1) :
    |t - round01 t| ≤ |t - b| := by
  classical
  unfold round01
  split_ifs with h
  · rcases hb with rfl | rfl
    · rw [sub_zero, abs_of_nonneg (by linarith : 0 ≤ t)]
      apply abs_le.mpr
      constructor <;> linarith
    · exact le_rfl
  · rcases hb with rfl | rfl
    · exact le_rfl
    · rw [sub_zero, abs_of_nonpos (by linarith : t - 1 ≤ 0)]
      apply abs_le.mpr
      constructor <;> linarith

/-- Without half-valued coordinates the rounded vector is the unique global
l1 minimizer among all binary vectors; no prescribed rank is assumed. -/
theorem round01_l1_unique {ι : Type*} [Fintype ι]
    (x z : ι → ℝ) (ht : ∀ i, x i ≠ 1 / 2)
    (hz : ∀ i, z i = 0 ∨ z i = 1)
    (hbest : (∑ i, |x i - z i|) ≤ ∑ i, |x i - round01 (x i)|) :
    z = fun i => round01 (x i) := by
  classical
  have hd : ∀ i, 0 ≤ |x i - z i| - |x i - round01 (x i)| := by
    intro i
    exact sub_nonneg.mpr (round01_nearest (x i) (z i) (hz i))
  have hsum : (∑ i, (|x i - z i| - |x i - round01 (x i)|)) ≤ 0 := by
    rw [Finset.sum_sub_distrib]
    linarith
  funext i
  apply round01_unique_nearest (x i) (z i) (ht i) (hz i)
  have hi := Finset.single_le_sum (fun j _ => hd j) (Finset.mem_univ i)
  linarith

/-- Integer total below defect one half: rounding preserves the exact total,
has no ambiguous coordinate, and satisfies the sharp l1 error bound. -/
theorem integer_total_rounding {ι : Type*} [Fintype ι] [DecidableEq ι]
    (x : ι → ℝ) (s : ℕ)
    (hbox : ∀ i, 0 ≤ x i ∧ x i ≤ 1)
    (hs : ∑ i, x i = (s : ℝ))
    (hD : (∑ i, x i * (1 - x i)) < 1 / 2) :
    (roundedOnes x).card = s ∧
    (∀ i, x i ≠ 1 / 2) ∧
    (∑ i, |x i - round01 (x i)|) ≤
      1 - Real.sqrt (1 - 2 * ∑ i, x i * (1 - x i)) := by
  classical
  let I := roundedOnes x
  let sigma : ℝ := ∑ i ∈ I, (1 - x i)
  let rho : ℝ := ∑ i ∈ Iᶜ, x i
  let D : ℝ := ∑ i, x i * (1 - x i)
  have hI : ∀ i ∈ I, 1 / 2 < x i := by
    intro i hi
    exact (mem_roundedOnes x i).mp hi
  have hJ : ∀ i ∈ Iᶜ, x i ≤ 1 / 2 := by
    intro i hi
    have hn : i ∉ roundedOnes x := by simpa [I] using hi
    exact le_of_not_gt (fun h => hn ((mem_roundedOnes x i).mpr h))
  have hsigma0 : 0 ≤ sigma :=
    Finset.sum_nonneg (fun i _ => sub_nonneg.mpr (hbox i).2)
  have hrho0 : 0 ≤ rho := Finset.sum_nonneg (fun i _ => (hbox i).1)
  have hsigmadef : sigma = (I.card : ℝ) - ∑ i ∈ I, x i := by
    simp [sigma, Finset.sum_sub_distrib]
  have hmass : rho - sigma = (s : ℝ) - I.card := by
    have ht := I.sum_add_sum_compl x
    rw [hs] at ht
    rw [hsigmadef]
    dsimp [rho]
    linarith
  have herror : (∑ i, |x i - round01 (x i)|) = sigma + rho := by
    rw [← I.sum_add_sum_compl (fun i => |x i - round01 (x i)|)]
    apply congrArg₂ (· + ·)
    · apply Finset.sum_congr rfl
      intro i hi
      rw [round01, if_pos (hI i hi), abs_of_nonpos (by linarith [(hbox i).2])]
      ring
    · apply Finset.sum_congr rfl
      intro i hi
      rw [round01, if_neg (not_lt.mpr (hJ i hi)), sub_zero,
        abs_of_nonneg (hbox i).1]
  have herrorD : sigma + rho ≤ 2 * D := by
    rw [← herror, D, Finset.mul_sum]
    exact Finset.sum_le_sum (fun i _ => round01_error_le (x i) (hbox i).1 (hbox i).2)
  have herror1 : sigma + rho < 1 := by dsimp [D] at herrorD; linarith
  have hksR : (I.card : ℝ) < (s : ℝ) + 1 := by linarith
  have hskR : (s : ℝ) < (I.card : ℝ) + 1 := by linarith
  have hks : I.card < s + 1 := by exact_mod_cast hksR
  have hsk : s < I.card + 1 := by exact_mod_cast hskR
  have hcount : I.card = s := by omega
  have hbalanced : sigma = rho := by rw [hcount] at hmass; linarith
  have hrhohalf : rho < 1 / 2 := by linarith
  have hnotie : ∀ i, x i ≠ 1 / 2 := by
    intro i heq
    have hi : i ∈ Iᶜ := by
      simp only [Finset.mem_compl, I, mem_roundedOnes]
      rw [heq]
      exact lt_irrefl _
    have hsingle : x i ≤ rho := Finset.single_le_sum (fun j _ => (hbox j).1) hi
    linarith
  have hdef : (∑ i ∈ I, (1 - x i) * (1 - (1 - x i))) +
      (∑ i ∈ Iᶜ, x i * (1 - x i)) = D := by
    have h := I.sum_add_sum_compl (fun i => x i * (1 - x i))
    change _ = ∑ i, x i * (1 - x i)
    rw [← h]
    congr 1
    apply Finset.sum_congr rfl
    intro i hi
    ring
  have hsharp := balanced_error_sharp_bound I Iᶜ (fun i => 1 - x i) x rho D
    (fun i _ => sub_nonneg.mpr (hbox i).2) (fun i _ => (hbox i).1)
    hbalanced rfl (le_of_lt hrhohalf) hdef
  refine ⟨hcount, hnotie, ?_⟩
  rw [herror, hbalanced]
  change rho + rho ≤ 1 - Real.sqrt (1 - 2 * D)
  linarith

/-- In particular, the coordinatewise nearest binary vector is uniquely
specified by the nearest-endpoint inequalities. -/
theorem integer_total_rounding_unique {ι : Type*} [Fintype ι] [DecidableEq ι]
    (x z : ι → ℝ) (s : ℕ)
    (hbox : ∀ i, 0 ≤ x i ∧ x i ≤ 1)
    (hs : ∑ i, x i = (s : ℝ))
    (hD : (∑ i, x i * (1 - x i)) < 1 / 2)
    (hz : ∀ i, z i = 0 ∨ z i = 1)
    (hnear : ∀ i, |x i - z i| ≤ |x i - round01 (x i)|) :
    z = fun i => round01 (x i) := by
  funext i
  exact round01_unique_nearest (x i) (z i)
    ((integer_total_rounding x s hbox hs hD).2.1 i) (hz i) (hnear i)

/-- The previous theorem also gives uniqueness for a global l1 objective. -/
theorem integer_total_rounding_l1_unique {ι : Type*} [Fintype ι] [DecidableEq ι]
    (x z : ι → ℝ) (s : ℕ)
    (hbox : ∀ i, 0 ≤ x i ∧ x i ≤ 1)
    (hs : ∑ i, x i = (s : ℝ))
    (hD : (∑ i, x i * (1 - x i)) < 1 / 2)
    (hz : ∀ i, z i = 0 ∨ z i = 1)
    (hbest : (∑ i, |x i - z i|) ≤ ∑ i, |x i - round01 (x i)|) :
    z = fun i => round01 (x i) := by
  exact round01_l1_unique x z (integer_total_rounding x s hbox hs hD).2.1 hz hbest

/-- The robust rounding barrier (T4): an integer-centred total-error band
and defect strictly below 1/2-eta^2 force the nearest binary rank to be s.
This elementary proof uses the packing bound on errors in [0,1/2]. -/
theorem robust_total_rounding {ι : Type*} [Fintype ι] [DecidableEq ι]
    (x : ι → ℝ) (s : ℕ) (eta : ℝ)
    (hbox : ∀ i, 0 ≤ x i ∧ x i ≤ 1)
    (heta : 0 ≤ eta)
    (hmean : |(∑ i, x i) - (s : ℝ)| ≤ eta)
    (hD : (∑ i, x i * (1 - x i)) < 1 / 2 - eta ^ 2) :
    (roundedOnes x).card = s ∧ (∀ i, x i ≠ 1 / 2) := by
  classical
  let I := roundedOnes x
  let sigma : ℝ := ∑ i ∈ I, (1 - x i)
  let rho : ℝ := ∑ i ∈ Iᶜ, x i
  let D : ℝ := ∑ i, x i * (1 - x i)
  have hI : ∀ i ∈ I, 1 / 2 < x i := by
    intro i hi
    exact (mem_roundedOnes x i).mp hi
  have hJ : ∀ i ∈ Iᶜ, x i ≤ 1 / 2 := by
    intro i hi
    have hn : i ∉ roundedOnes x := by simpa [I] using hi
    exact le_of_not_gt (fun h => hn ((mem_roundedOnes x i).mpr h))
  have hsigma0 : 0 ≤ sigma :=
    Finset.sum_nonneg (fun i _ => sub_nonneg.mpr (hbox i).2)
  have hrho0 : 0 ≤ rho := Finset.sum_nonneg (fun i _ => (hbox i).1)
  have hsigmadef : sigma = (I.card : ℝ) - ∑ i ∈ I, x i := by
    simp [sigma, Finset.sum_sub_distrib]
  have hmass : rho - sigma = (∑ i, x i) - I.card := by
    have ht := I.sum_add_sum_compl x
    rw [hsigmadef]
    dsimp [rho]
    linarith
  have herror : (∑ i, |x i - round01 (x i)|) = sigma + rho := by
    rw [← I.sum_add_sum_compl (fun i => |x i - round01 (x i)|)]
    apply congrArg₂ (· + ·)
    · apply Finset.sum_congr rfl
      intro i hi
      rw [round01, if_pos (hI i hi), abs_of_nonpos (by linarith [(hbox i).2])]
      ring
    · apply Finset.sum_congr rfl
      intro i hi
      rw [round01, if_neg (not_lt.mpr (hJ i hi)), sub_zero,
        abs_of_nonneg (hbox i).1]
  have herrorD : sigma + rho ≤ 2 * D := by
    rw [← herror, D, Finset.mul_sum]
    exact Finset.sum_le_sum (fun i _ => round01_error_le (x i) (hbox i).1 (hbox i).2)
  have herror1 : sigma + rho < 1 := by
    dsimp [D] at herrorD
    nlinarith [sq_nonneg eta]
  have hdef := I.sum_add_sum_compl (fun i => x i * (1 - x i))
  have hdefI0 : 0 ≤ ∑ i ∈ I, x i * (1 - x i) :=
    Finset.sum_nonneg (fun i _ => mul_nonneg (hbox i).1 (sub_nonneg.mpr (hbox i).2))
  have hdefJ0 : 0 ≤ ∑ i ∈ Iᶜ, x i * (1 - x i) :=
    Finset.sum_nonneg (fun i _ => mul_nonneg (hbox i).1 (sub_nonneg.mpr (hbox i).2))
  have htopDef : (∑ i ∈ I, (1 - x i) * (1 - (1 - x i))) =
      ∑ i ∈ I, x i * (1 - x i) := by
    apply Finset.sum_congr rfl
    intro i hi
    ring
  have hcount : I.card = s := by
    rcases lt_trichotomy I.card s with hlt | heq | hgt
    · have hstep : I.card + 1 ≤ s := Nat.succ_le_of_lt hlt
      have hstepR : (I.card : ℝ) + 1 ≤ (s : ℝ) := by exact_mod_cast hstep
      have hlower : 1 - eta ≤ rho := by
        have hm := (abs_le.mp hmean).1
        linarith
      have hupper : rho ≤ 1 := by linarith
      have hpack := half_bounded_mass_defect Iᶜ x eta
        (fun i hi => ⟨(hbox i).1, hJ i hi⟩) heta hlower hupper
      exact False.elim (by linarith)
    · exact heq
    · have hstep : s + 1 ≤ I.card := Nat.succ_le_of_lt hgt
      have hstepR : (s : ℝ) + 1 ≤ (I.card : ℝ) := by exact_mod_cast hstep
      have hlower : 1 - eta ≤ sigma := by
        have hm := (abs_le.mp hmean).2
        linarith
      have hupper : sigma ≤ 1 := by linarith
      have hpack := half_bounded_mass_defect I (fun i => 1 - x i) eta
        (fun i hi => ⟨sub_nonneg.mpr (hbox i).2, by linarith [hI i hi]⟩)
        heta hlower hupper
      rw [htopDef] at hpack
      exact False.elim (by linarith)
  have hmean' : |(∑ i, x i) - ((s : ℤ) : ℝ)| ≤ eta := by simpa using hmean
  have hnotie := no_half_below_barrier Finset.univ x (s : ℤ) eta D
    (fun i _ => hbox i) hmean' (le_refl _) hD
  exact ⟨hcount, fun i => hnotie i (Finset.mem_univ i)⟩

/-- Under the robust barrier the global nearest binary vector is unique. -/
theorem robust_total_rounding_l1_unique {ι : Type*} [Fintype ι] [DecidableEq ι]
    (x z : ι → ℝ) (s : ℕ) (eta : ℝ)
    (hbox : ∀ i, 0 ≤ x i ∧ x i ≤ 1)
    (heta : 0 ≤ eta)
    (hmean : |(∑ i, x i) - (s : ℝ)| ≤ eta)
    (hD : (∑ i, x i * (1 - x i)) < 1 / 2 - eta ^ 2)
    (hz : ∀ i, z i = 0 ∨ z i = 1)
    (hbest : (∑ i, |x i - z i|) ≤ ∑ i, |x i - round01 (x i)|) :
    z = fun i => round01 (x i) := by
  exact round01_l1_unique x z (robust_total_rounding x s eta hbox heta hmean hD).2 hz hbest

end MomentIslands

#print axioms MomentIslands.round01_binary
#print axioms MomentIslands.sum_round01
#print axioms MomentIslands.round01_unique_nearest
#print axioms MomentIslands.round01_error_le
#print axioms MomentIslands.round01_nearest
#print axioms MomentIslands.round01_l1_unique
#print axioms MomentIslands.integer_total_rounding
#print axioms MomentIslands.integer_total_rounding_unique
#print axioms MomentIslands.integer_total_rounding_l1_unique
#print axioms MomentIslands.robust_total_rounding
#print axioms MomentIslands.robust_total_rounding_l1_unique
