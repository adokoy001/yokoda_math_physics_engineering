import Packing
import BandSharp
import Mathlib

/-!
Draft extension, not compiled in the present environment.
The lower bound uses actual finite-vector moments.
The attainment theorem supplies arbitrarily many binary padding coordinates,
including explicit bounds identifying the two boundary values.
-/

open scoped BigOperators

namespace MomentIslands

theorem finite_band_gap {ι : Type*} [Fintype ι] [DecidableEq ι]
    (I : Finset ι) (x : ι → ℝ) (a b : ι) (eta delta : ℝ)
    (ha : a ∈ I) (hb : b ∉ I)
    (hbox : ∀ i, 0 ≤ x i ∧ x i ≤ 1)
    (hmin : ∀ i ∈ I, x a ≤ x i) (hmax : ∀ j ∉ I, x j ≤ x b)
    (hab : x b ≤ x a)
    (heta : 0 ≤ eta) (hetaHalf : eta ≤ 1 / 2) (hdelta : 0 ≤ delta)
    (hmean : |(∑ i, x i) - (I.card : ℝ)| ≤ eta)
    (hdefect : (∑ i, x i * (1 - x i)) ≤ delta) :
    bandGap eta delta ≤ x a - x b := by
  have hcore := rank_gap_partition I x a b ha hb hbox hmin hmax
  have hpacking := abs_integer_offset_defect Finset.univ x (I.card : ℤ)
    (fun i _ => hbox i)
  simp only [Int.cast_natCast] at hpacking
  apply band_gap_lower eta delta |(∑ i, x i) - (I.card : ℝ)|
    (∑ i, x i * (1 - x i)) (x a - x b)
    heta hetaHalf hdelta (abs_nonneg _) hmean hpacking hdefect
    (sub_nonneg.mpr hab)
  simpa only [sq_abs] using hcore

abbrev PaddedIndex (p q : ℕ) := (Fin p ⊕ Unit) ⊕ (Unit ⊕ Fin q)

def pairPadded (p q : ℕ) (u v : ℝ) : PaddedIndex p q → ℝ :=
  Sum.elim (Sum.elim (fun _ => 1) (fun _ => u))
    (Sum.elim (fun _ => v) (fun _ => 0))

theorem pairPadded_sum (p q : ℕ) (u v : ℝ) :
    (∑ i, pairPadded p q u v i) = (p : ℝ) + u + v := by
  simp [pairPadded, Fintype.sum_sum_type] <;> ring

theorem pairPadded_defect (p q : ℕ) (u v : ℝ) :
    (∑ i, pairPadded p q u v i * (1 - pairPadded p q u v i)) =
      u * (1 - u) + v * (1 - v) := by
  simp [pairPadded, Fintype.sum_sum_type]

theorem pairPadded_box (p q : ℕ) (u v : ℝ)
    (hv : 0 ≤ v) (hvu : v ≤ u) (hu : u ≤ 1) :
    ∀ i, 0 ≤ pairPadded p q u v i ∧ pairPadded p q u v i ≤ 1 := by
  intro i
  rcases i with (i | i) | (i | i)
  · simp [pairPadded]
  · exact ⟨le_trans hv hvu, hu⟩
  · exact ⟨hv, le_trans hvu hu⟩
  · simp [pairPadded]

/-- The top block has minimum u and the bottom block has maximum v.
The boundary coordinates themselves occur in the two Unit summands. -/
theorem pairPadded_boundaries (p q : ℕ) (u v : ℝ)
    (hv : 0 ≤ v) (hu : u ≤ 1) :
    (∀ i : Fin p ⊕ Unit, u ≤ pairPadded p q u v (Sum.inl i)) ∧
    (∀ i : Unit ⊕ Fin q, pairPadded p q u v (Sum.inr i) ≤ v) ∧
    pairPadded p q u v (Sum.inl (Sum.inr ())) = u ∧
    pairPadded p q u v (Sum.inr (Sum.inl ())) = v := by
  refine ⟨?_, ?_, rfl, rfl⟩
  · intro i
    cases i <;> simp [pairPadded, hu]
  · intro i
    cases i <;> simp [pairPadded, hv]

/-- Arbitrarily many ones and zeros can be appended to the two-coordinate
sharpness witness. The top block has p+1 coordinates and the bottom q+1.
No fixed dimension or finite numerical grid is assumed. -/
theorem finite_band_attainment (p q : ℕ) (eta delta : ℝ)
    (heta : 0 ≤ eta) (hetaHalf : eta ≤ 1 / 2) (hdelta : 0 ≤ delta) :
    ∃ u v : ℝ,
      let x := pairPadded p q u v
      (∀ i, 0 ≤ x i ∧ x i ≤ 1) ∧
      v ≤ u ∧
      |(∑ i, x i) - ((p : ℝ) + 1)| ≤ eta ∧
      (∑ i, x i * (1 - x i)) ≤ delta ∧
      (∀ i : Fin p ⊕ Unit, u ≤ x (Sum.inl i)) ∧
      (∀ i : Unit ⊕ Fin q, x (Sum.inr i) ≤ v) ∧
      x (Sum.inl (Sum.inr ())) = u ∧
      x (Sum.inr (Sum.inl ())) = v ∧
      u - v = bandGap eta delta := by
  obtain ⟨a, u, v, ha, haeta, hv, hvu, hu, hsum, hD, hgap⟩ :=
    band_gap_witness eta delta heta hetaHalf hdelta
  have hb := pairPadded_boundaries p q u v hv hu
  refine ⟨u, v, ?_⟩
  dsimp only
  refine ⟨pairPadded_box p q u v hv hvu hu, hvu, ?_, ?_,
    hb.1, hb.2.1, hb.2.2.1, hb.2.2.2, hgap⟩
  · rw [pairPadded_sum]
    have he : (p : ℝ) + u + v - ((p : ℝ) + 1) = -a := by linarith
    rw [he, abs_neg, abs_of_nonneg ha]
    exact haeta
  · rw [pairPadded_defect]
    exact hD

/-- At the rounding threshold a genuine half-valued coordinate is already
present. Binary padding gives this witness in every dimension p+q+2.
The total has offset -eta from the integer p+1. -/
theorem finite_rounding_barrier_attainment (p q : ℕ) (eta : ℝ)
    (heta : 0 ≤ eta) (hetaHalf : eta ≤ 1 / 2) :
    let x := pairPadded p q (1 / 2) (1 / 2 - eta)
    (∀ i, 0 ≤ x i ∧ x i ≤ 1) ∧
    |(∑ i, x i) - ((p : ℝ) + 1)| = eta ∧
    (∑ i, x i * (1 - x i)) = 1 / 2 - eta ^ 2 ∧
    x (Sum.inl (Sum.inr ())) = 1 / 2 := by
  dsimp only
  refine ⟨pairPadded_box p q (1 / 2) (1 / 2 - eta)
    (by linarith) (by linarith) (by norm_num), ?_, ?_, rfl⟩
  · rw [pairPadded_sum]
    have he : (p : ℝ) + 1 / 2 + (1 / 2 - eta) - ((p : ℝ) + 1) = -eta := by
      ring
    rw [he, abs_neg, abs_of_nonneg heta]
  · rw [pairPadded_defect]
    ring

end MomentIslands

#print axioms MomentIslands.finite_band_gap
#print axioms MomentIslands.pairPadded_sum
#print axioms MomentIslands.pairPadded_defect
#print axioms MomentIslands.pairPadded_box
#print axioms MomentIslands.pairPadded_boundaries
#print axioms MomentIslands.finite_band_attainment
#print axioms MomentIslands.finite_rounding_barrier_attainment
