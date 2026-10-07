import MomentIslands

/-!
Sharp scalar optimization for the narrow moment band, 0 ≤ eta ≤ 1/2.
The vector-to-scalar reduction is deliberately supplied in a separate file.

Status: candidate Lean 4.19 / mathlib 4.19 source; this addition has NOT
been compiled in the present environment. No axiom or proof placeholder
is introduced. The `#print axioms` commands are instructions for the next
actual run, not a report that this run has already happened.
-/

namespace MomentIslands

/-- The proposed optimal adjacent-gap certificate for the narrow band. -/
noncomputable def bandGap (eta delta : ℝ) : ℝ :=
  if delta ≤ eta * (1 - eta) then (1 + Real.sqrt (1 - 4 * delta)) / 2
  else if delta ≤ (1 - eta ^ 2) / 2 then Real.sqrt (1 - 2 * delta - eta ^ 2)
  else 0

theorem band_small_lower (eta delta a D g : ℝ)
    (heta : 0 ≤ eta) (hetaHalf : eta ≤ 1 / 2) (hdelta : 0 ≤ delta)
    (ha : 0 ≤ a) (haeta : a ≤ eta)
    (hpacking : a * (1 - a) ≤ D) (hD : D ≤ delta)
    (hg : 0 ≤ g) (hcore : 1 ≤ 2 * D + a ^ 2 + g ^ 2)
    (hsmall : delta ≤ eta * (1 - eta)) :
    (1 + Real.sqrt (1 - 4 * delta)) / 2 ≤ g := by
  have hrad : 0 ≤ 1 - 4 * delta := by
    nlinarith [sq_nonneg (2 * eta - 1)]
  have hs := Real.sq_sqrt hrad
  have ht := Real.sqrt_nonneg (1 - 4 * delta)
  have htone : Real.sqrt (1 - 4 * delta) ≤ 1 := by
    apply (Real.sqrt_le_left (by norm_num : (0 : ℝ) ≤ 1)).mpr
    linarith
  have htbound : Real.sqrt (1 - 4 * delta) ≤ 1 - 2 * a := by
    apply (Real.sqrt_le_left (by linarith : 0 ≤ 1 - 2 * a)).mpr
    nlinarith
  have har : a ≤ (1 - Real.sqrt (1 - 4 * delta)) / 2 := by linarith
  have hprod := mul_nonneg (sub_nonneg.mpr har)
    (show 0 ≤ (1 - Real.sqrt (1 - 4 * delta)) / 2 + a by linarith)
  have hsq : ((1 + Real.sqrt (1 - 4 * delta)) / 2) ^ 2 ≤ g ^ 2 := by
    nlinarith
  exact (sq_le_sq₀ (by linarith) hg).mp hsq

theorem band_middle_lower (eta delta a D g : ℝ)
    (heta : 0 ≤ eta) (ha : 0 ≤ a) (haeta : a ≤ eta)
    (hD : D ≤ delta) (hg : 0 ≤ g)
    (hcore : 1 ≤ 2 * D + a ^ 2 + g ^ 2) :
    Real.sqrt (1 - 2 * delta - eta ^ 2) ≤ g := by
  apply (Real.sqrt_le_left hg).mpr
  have hprod := mul_nonneg (sub_nonneg.mpr haeta) (add_nonneg heta ha)
  nlinarith

/-- Universal scalar lower bound. The packing premise is a separate,
explicit obligation when this theorem is applied to finite vectors. -/
theorem band_gap_lower (eta delta a D g : ℝ)
    (heta : 0 ≤ eta) (hetaHalf : eta ≤ 1 / 2) (hdelta : 0 ≤ delta)
    (ha : 0 ≤ a) (haeta : a ≤ eta)
    (hpacking : a * (1 - a) ≤ D) (hD : D ≤ delta)
    (hg : 0 ≤ g) (hcore : 1 ≤ 2 * D + a ^ 2 + g ^ 2) :
    bandGap eta delta ≤ g := by
  by_cases hsmall : delta ≤ eta * (1 - eta)
  · simp only [bandGap, if_pos hsmall]
    exact band_small_lower eta delta a D g heta hetaHalf hdelta
      ha haeta hpacking hD hg hcore hsmall
  · by_cases hmiddle : delta ≤ (1 - eta ^ 2) / 2
    · simp only [bandGap, if_neg hsmall, if_pos hmiddle]
      exact band_middle_lower eta delta a D g heta ha haeta hD hg hcore
    · simpa only [bandGap, if_neg hsmall, if_neg hmiddle] using hg

/-- Two coordinates realize a prescribed error and gap whenever
the elementary box condition g ≤ 1-a holds. -/
theorem pair_realization (a g : ℝ) (ha : 0 ≤ a) (haone : a ≤ 1)
    (hg : 0 ≤ g) (hga : g ≤ 1 - a) :
    let u := (1 - a + g) / 2
    let v := (1 - a - g) / 2
    0 ≤ v ∧ v ≤ u ∧ u ≤ 1 ∧ u + v = 1 - a ∧ u - v = g ∧
      u * (1 - u) + v * (1 - v) = (1 - a ^ 2 - g ^ 2) / 2 := by
  dsimp
  constructor
  · linarith
  constructor
  · linarith
  constructor
  · linarith
  constructor
  · ring
  constructor
  · ring
  · ring

/-- In the first branch one fractional coordinate suffices, and the
defect constraint is attained exactly. -/
theorem band_small_witness (eta delta : ℝ)
    (heta : 0 ≤ eta) (hetaHalf : eta ≤ 1 / 2)
    (hdelta : 0 ≤ delta) (hsmall : delta ≤ eta * (1 - eta)) :
    let t := Real.sqrt (1 - 4 * delta)
    let a := (1 - t) / 2
    let u := (1 + t) / 2
    0 ≤ a ∧ a ≤ eta ∧ 0 ≤ u ∧ u ≤ 1 ∧
      u = 1 - a ∧ u * (1 - u) = delta ∧
      u = bandGap eta delta := by
  dsimp
  have hrad : 0 ≤ 1 - 4 * delta := by
    nlinarith [sq_nonneg (2 * eta - 1)]
  have hs := Real.sq_sqrt hrad
  have ht := Real.sqrt_nonneg (1 - 4 * delta)
  have htone : Real.sqrt (1 - 4 * delta) ≤ 1 := by
    apply (Real.sqrt_le_left (by norm_num : (0 : ℝ) ≤ 1)).mpr
    linarith
  have hleta : 1 - 2 * eta ≤ Real.sqrt (1 - 4 * delta) := by
    apply (sq_le_sq₀ (by linarith : 0 ≤ 1 - 2 * eta) ht).mp
    nlinarith
  refine ⟨by linarith, by linarith, by linarith, by linarith, by ring, ?_, ?_⟩
  · nlinarith
  · simp only [bandGap, if_pos hsmall]

/-- In the middle branch both the sum-band and defect constraints are
attained exactly by two fractional coordinates. -/
theorem band_middle_witness (eta delta : ℝ)
    (heta : 0 ≤ eta) (hetaHalf : eta ≤ 1 / 2)
    (hfirst : eta * (1 - eta) ≤ delta)
    (hmiddle : delta ≤ (1 - eta ^ 2) / 2) :
    let g := Real.sqrt (1 - 2 * delta - eta ^ 2)
    let u := (1 - eta + g) / 2
    let v := (1 - eta - g) / 2
    0 ≤ v ∧ v ≤ u ∧ u ≤ 1 ∧ u + v = 1 - eta ∧
      u - v = g ∧ u * (1 - u) + v * (1 - v) = delta := by
  have hrad : 0 ≤ 1 - 2 * delta - eta ^ 2 := by linarith
  have hs := Real.sq_sqrt hrad
  have hg := Real.sqrt_nonneg (1 - 2 * delta - eta ^ 2)
  have hga : Real.sqrt (1 - 2 * delta - eta ^ 2) ≤ 1 - eta := by
    apply (Real.sqrt_le_left (by linarith : 0 ≤ 1 - eta)).mpr
    nlinarith
  have hp := pair_realization eta (Real.sqrt (1 - 2 * delta - eta ^ 2))
    heta (by linarith) hg hga
  dsimp at hp ⊢
  refine ⟨hp.1, hp.2.1, hp.2.2.1, hp.2.2.2.1, hp.2.2.2.2.1, ?_⟩
  nlinarith [hp.2.2.2.2.2]

/-- The zero branch is attained already at its first threshold. -/
theorem band_zero_witness (eta delta : ℝ)
    (heta : 0 ≤ eta) (hetaHalf : eta ≤ 1 / 2)
    (hlarge : (1 - eta ^ 2) / 2 ≤ delta) :
    let u := (1 - eta) / 2
    0 ≤ u ∧ u ≤ 1 ∧ u + u = 1 - eta ∧
      u * (1 - u) + u * (1 - u) ≤ delta := by
  dsimp
  refine ⟨by linarith, by linarith, by ring, ?_⟩
  nlinarith

/-- Sharpness data for all branches, including every endpoint.
Append s-1 ones and n-s-1 zeroes to obtain an n-coordinate witness. -/
theorem band_gap_witness (eta delta : ℝ)
    (heta : 0 ≤ eta) (hetaHalf : eta ≤ 1 / 2) (hdelta : 0 ≤ delta) :
    ∃ a u v : ℝ, 0 ≤ a ∧ a ≤ eta ∧ 0 ≤ v ∧ v ≤ u ∧ u ≤ 1 ∧
      u + v = 1 - a ∧ u * (1 - u) + v * (1 - v) ≤ delta ∧
      u - v = bandGap eta delta := by
  by_cases hsmall : delta ≤ eta * (1 - eta)
  · have h := band_small_witness eta delta heta hetaHalf hdelta hsmall
    dsimp at h
    refine ⟨(1 - Real.sqrt (1 - 4 * delta)) / 2,
      (1 + Real.sqrt (1 - 4 * delta)) / 2, 0,
      h.1, h.2.1, le_rfl, h.2.2.1, h.2.2.2.1, ?_, ?_, ?_⟩
    · simpa using h.2.2.2.2.1
    · simpa using le_of_eq h.2.2.2.2.2.1
    · simpa using h.2.2.2.2.2.2
  · by_cases hmiddle : delta ≤ (1 - eta ^ 2) / 2
    · have h := band_middle_witness eta delta heta hetaHalf
        (le_of_lt (lt_of_not_ge hsmall)) hmiddle
      dsimp at h
      refine ⟨eta, (1 - eta + Real.sqrt (1 - 2 * delta - eta ^ 2)) / 2,
        (1 - eta - Real.sqrt (1 - 2 * delta - eta ^ 2)) / 2,
        heta, le_rfl, h.1, h.2.1, h.2.2.1, h.2.2.2.1,
        le_of_eq h.2.2.2.2.2, ?_⟩
      simpa only [bandGap, if_neg hsmall, if_pos hmiddle] using h.2.2.2.2.1
    · have h := band_zero_witness eta delta heta hetaHalf
        (le_of_lt (lt_of_not_ge hmiddle))
      dsimp at h
      refine ⟨eta, (1 - eta) / 2, (1 - eta) / 2,
        heta, le_rfl, h.1, le_rfl, h.2.1, h.2.2.1, h.2.2.2, ?_⟩
      simp only [sub_self, bandGap, if_neg hsmall, if_neg hmiddle]

end MomentIslands

#print axioms MomentIslands.band_gap_lower
#print axioms MomentIslands.band_gap_witness
