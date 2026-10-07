# Round 10 focused primary-literature audit

Audit date: 2026 10 03. Scope: capacity budgets, cross-port transient first moments, sharp response envelopes; comparison with earlier positive-realization claims. This is a bounded literature search, not a claim of exhaustive novelty clearance.

## Main result of the audit

The identity `a E[T] = sum_i C_i p_i(1-p_i)` is exactly in the orbit of established transition path theory (TPT), not a promising claim of a new fundamental identity. TPT explicitly connects committors to resistor-network voltages. The lower bound `C_total >= 4 a E[T]` then follows immediately from `p(1-p) <= 1/4`. The deficit identity and the capacity-only response envelope are useful further deductions, but their short derivation from spectral positivity means the honest framing is a sharp corollary/application pending wider novelty checks.

## OA primary bodies actually read

### 1. Metzner, Schütte, Vanden-Eijnden (2009)

Title: Transition Path Theory for Markov Jump Processes.
Multiscale Modeling & Simulation 7(3), 1192–1219.
DOI: https://doi.org/10.1137/070699500
Full published PDF retrieved via web: https://publications.imp.fu-berlin.de/43/1/MeScVE09.pdf
Repository metadata: https://publications.imp.fu-berlin.de/43/
Tool refs: turn99view0 / turn101view1 / turn101view2.

Exact locations: Theorem 2.9, Eq. (2.17), p.1197: reactive occupation mass equals `pi_i q_i^+ q_i^-`. Remark 2.10, Eq. (2.21), p.1198: reversibility gives `pi_i q_i(1-q_i)`. Theorem 2.15, Eq. (2.30), p.1200: reactive transition rate equals boundary flux. Eq. (2.35), p.1200: reversible flux is the Dirichlet energy. Section 2.6, Eqs. (2.36)–(2.40), p.1201: conductance `c_ij=pi_i l_ij`; committor equals the voltage with boundary values 0 and 1. This is already an explicit electrical-network connection.

Mapping worked out here: extend an RC/thermal graph to two boundary states with arbitrary positive stationary weights and symmetric conductances. Interior generator is `l_ij=g_ij/C_i`; normalized stationary measure is `pi_i=C_i/Z`. No direct boundary edge gives reactive rate `a/Z` and occupation mass `sum C_i p_i(1-p_i)/Z`. Their ratio equals the duration of the reactive path. A direct boundary conductor adds zero-duration reactive paths and changes the total flux; if our normalized density excludes that feedthrough, apply the mapping to the dynamic subnetwork, not indiscriminately to total K.

### 2. Roux (2022)

Title: Transition rate theory, spectral analysis, and reactive paths.
Journal of Chemical Physics 156, 134111.
DOI: https://doi.org/10.1063/5.0084209
Public full-text landing page: https://pmc.ncbi.nlm.nih.gov/articles/PMC11373612/ (direct open produced a reCAPTCHA, but indexed full text is searchable).
Full article PDF actually retrieved: https://pdfs.semanticscholar.org/2c90/c99529b02343ba59a12e8e514a3f5fd5bcbb.pdf
Tool refs: turn103view0 / turn104view0.

Exact location: page 134111-5, immediately following Eq. (24), before subsection III.C.2. The paper explicitly writes `mean reactive transit time = <q(1-q)>/J_AB`, citing earlier work in its refs.13 and20. It also notes directional equality of the mean under reversibility. This independently confirms that the duration/occupation/flux identity is not new.

### 3. Hughes (2018)

Title: On the internal signature and minimal electric network realizations of reciprocal behaviors.
Systems & Control Letters 119, 16–22.
DOI: https://doi.org/10.1016/j.sysconle.2018.06.007
OA full text: https://arxiv.org/pdf/1804.01489
Tool ref: turn97view2.

IMPORTANT SCOPE CORRECTION: this paper is NOT limited to scalar transfer functions. It treats n×n polynomial matrices and multiport reciprocal behaviors. Theorems 8–9, printed p.3 in the arXiv PDF, bound even/odd state counts and capacitors/inductors using Bezoutian inertia plus uncontrollable modes. Remark 10 states that earlier RLCT constructions attain these bounds. The allowed class includes resistors, inductors, capacitors and transformers; it does not impose our nonnegative grounded-capacitor network geometry. It does not establish cp-rank characterization for our class. Thus distinguish allowed components, positivity/grounding restrictions and invariant (inertia versus cp-rank), not scalar versus multiport.

## Capacity envelope and stability: exact overlap not located

Candidate communicated by the derivation agent:

`h(t) <= C_total/(e^2 t^2)` for t>0, and, for w>=0,
`integral w(t) h(t) dt <= (C_total/4) sup_{lambda>0} [lambda q_lambda(w)]`,
where `q_lambda(w)=integral w(t) lambda exp(-lambda t) dt`.

The proof uses the polarization identity with `s=u+v=Qz`, `d=u-v`:
`4 h = z^T Q^2 exp(-tQ)z - d^T exp(-tQ)d`,
followed by the spectral theorem and `||z||^2=C_total` in the physical realization. Since `sup lambda^2 exp(-lambda t)=4/(e^2 t^2)`, the coefficient is elementary and a balanced one-state construction saturates at a chosen t. This is structurally a sharp self-adjoint semigroup estimate plus the physical capacity identity. The search did not locate this exact cross-port/capacity envelope, nor the proposed TV stability estimate with spectral ceiling, in the accessed bodies. This absence is not evidence that the result is historically new.

For saturation, retain the feasibility condition: a one-state star with capacity C and rate lambda requires dynamic static conductance C lambda /4; with fixed total static coupling kappa, direct-conductor completion is possible only if C lambda/4 <= kappa. Capacity-only envelope can otherwise be strict for the fixed-K class.

The deficit `delta=C_total-4a E[T]=sum_i C_i (2p_i-1)^2` is an elementary exact variance identity once TPT is known. It identifies the departure from equipotential midpoint balance and may support useful approximation certificates. Do not call delta itself a new physical law.

Focused queries used: transition path theory + committor / reactive duration / capacity; reversible absorption-time density upper bound; RC total capacitance upper bound; impulse response e^2; heat-content second derivative; minimum total capacitance RC realization; grounded capacitors multiport synthesis. Search noise is substantial for generic heat-kernel terms; no exact resource-envelope match found in this pass.

## Older capacity-synthesis literature: leads requiring further body comparison

These are valuable novelty-risk leads; their full texts were NOT obtained in this pass, so no technical conclusion is based on them.

1. J. D. Hagopian and I. T. Frisch, “Capacitance and resistance minimization in one-port RC networks,” IEEE Trans. Circuit Theory CT-17, 386–392 (1970), DOI https://doi.org/10.1109/TCT.1970.1083139 . Search-indexed abstract describes topological characterization of minimum total capacitance/resistance for an entire driving-point impedance and Foster canonical minimizers. Primary DOI fetch failed.
2. F. T. Boesch and J. D. Hagopian, “Minimum total capacitance RC realizations,” IEEE Trans. Circuit Theory CT-18(2), 286–288 (1971). Exact bibliographic entry verified in the references of the primary paper https://onlinelibrary.wiley.com/doi/abs/10.1002/cta.456 (ref.42). A public university scan of p.288 is indexed at https://scholar.cu.edu.eg/sites/default/files/ams/files/1-march_1971.pdf but timed out on web retrieval; shell download was blocked by network policy. The indexed fragment mentions transformerless resistor n-ports, a capacitance inequality via congruent transformations, and Cauer/Foster synthesis. Do not infer its complete theorem from the fragment.
3. J. D. Hagopian and I. T. Frisch, “Capacitance and resistance minimization in n-port RC networks,” IEEE Trans. Circuit Theory CT-19, 87–89 (1972). Bibliographic lead in an author thesis: https://mspace.lib.umanitoba.ca/bitstream/1993/13712/1/Ali_Some_new.pdf . Not body-verified.
4. E. N. Protonotarios, “Optimal transfer-function synthesis of RC ladders—Lumped and distributed,” IEEE Trans. Circuits and Systems CAS-21, 49–56 (1974). Same thesis bibliographic lead. Not body-verified.

Do not conflate active grounded-capacitor realizations (Bickart–Melvin1972, current-feedback amplifier/filter papers, nullor constructions) with our passive nonnegative-resistor class: those can use amplifiers to match the algebraic degree and evade our positivity/geometric constraints.

## Recommended claim language

“既知の遷移経路理論と対称半群の評価を、総容量を制約した熱／RC回路に適用し、測定値から必要容量を下から保証する証明と、条件付きで限界を達成する構成を得た。数式の成立と実装上の価値は検証できるが、学術的新規性は、古典的な容量最小化合成との照合を含めて未確定。”
