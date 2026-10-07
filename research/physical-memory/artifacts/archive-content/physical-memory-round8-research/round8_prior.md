# Round 8 literature comparison and novelty assessment

Date: 2026 09 29. Scope: the completed global scalar minimum theorem for equal static edge budgets and the balanced finite-precision CP certificate, with comparison to the earlier edge-star subclass formula. This is a targeted prior-art audit, not a proof of historical priority.

## Updated assessment after the global theorem and independent audit

The completed `round8_window.md` and `round8_global_audit.md` supersede the earlier assessment that the result only covered edge stars. Under exact triangle-free static K with equal positive edge budgets, positive diagonal internal capacities, reciprocal nonnegative conductances, stable boundary-reachable components, and a nonnegative window kernel satisfying `3 q_* >= w_*`, the proof excludes **all admitted internally coupled networks** below a matching attainable state count. The current finite protocol `T=tau=h/10` meets that condition analytically. The optimization criterion is one scalar cross-edge sum, not the whole transfer function. The n=10, epsilon/c0=.05 count of 85 has an independent rational threshold certificate.

**Novelty judgment: a substantive, narrowly scoped theorem candidate; historical priority remains unconfirmed.** I located no identical fixed-K / positive grounded-capacity / finite-window / matching lower-and-upper minimum-order theorem in the primary texts inspected below. The strongest candidate contribution is the conjunction of an impossibility bound over the entire admitted physical class and a positive-element construction attaining it. This is materially stronger than an elementary top-r allocation in a preselected subclass. It still does not establish a general theory of physical coarse-graining.

Known ingredients must remain attributed: exact DC-preserving reduction; positivity versus unrestricted realization order; Kron-reduction clique fill-in; clique/CP-rank bounds on bipartite support; phase-type representations and phase-count extremal inequalities. Optimizing a single exponential rate, sorting budgets, and the elementary high-state expectation bound are not strong standalone novelty claims. The two-state density domination is an effective proof lemma; its novelty was not separately established.

Scope is especially important: unequal budgets or weights remain subclass results; arbitrary time protocols are covered only when the stated kernel-height condition holds; approximate K and same-side static leakage require the separate robust certificate; general passive realizations with negative synthesized elements, floating capacitances, or nonreciprocity are outside the physical class.

## Balanced leakage theorem: mathematical and literature audit

I checked `round8_leak.md` analytically. Its inequality

`S <= B_r + W_theta + sqrt(I_theta W_theta)`

passes the following checks: the row maximum is at least the squared row norm divided by its sum; each row chooses a dominant cross pair; repeated choices are jointly bounded by that pair's observed cap; at most r distinct choices lead to the sum of the top r caps; and Cauchy–Schwarz yields the stated balanced error term. Cases with one zero row sum cause no division issue because they are treated separately. Positive group rescaling preserves cross entries and factor count. The example `F=[I | J/n]` exactly attains the balanced bound and has CP-rank n by its identity block. Its V diagonal and within-V observations differ from the original target, so its n-state construction is only a counterexample for the declared retained observations.

The strongest novelty candidate here is **the explicit observable inequality with a linear leakage penalty at balance**, together with an experiment that measures the imbalance directly. Robust low-factor-count exclusion itself is established. The dominant-coordinate argument is elementary enough that rediscovery risk is material. No identical `B_r+W+sqrt(IW)` inequality was located in this search.

Closest checked precedents:

- Fawzi–Parrilo, *Lower bounds on nonnegative rank via nonnegative nuclear norms*, https://arxiv.org/pdf/1210.6970, §2.2 Theorem 3: quantitative lower bounds for all nonnegative matrices inside a Frobenius ball. Their certificate uses a copositive dual witness and norms of the full data/error. It already establishes robust approximate-rank certification; the new inequality instead uses CP symmetry, two specified groups, cross-entry caps, within-group leakage and a balanced quadratic observable. Neither source alone proves universal superiority over the other. A comparison requires the same data/uncertainty model. Relevant body re-read this round, tool refs turn33view0 and turn35view3.
- Korda–Laurent–Magron–Steenkamp, *Exploiting ideal-sparsity in the generalized moment problem with application to matrix factorization ranks*, https://arxiv.org/pdf/2209.09573, §4.2 Lemma 13, equation (51), Example 14: fractional clique-cover lower bounds and exact n² CP rank for a complete-bipartite supported family are already explicit. Those zero-support constraints do not themselves quantify the proposed balanced leakage correction. Body re-read, refs turn35view0/turn35view4. Use existing bibliography [70].
- Fawzi–Parrilo, *Self-scaled bounds for atomic cone ranks*, existing bibliography [41]: the project's earlier body audit/implementation of the arXiv v1 CP-rank SDP remains relevant. This round's fresh HTML/PDF retrieval failed, so no newly read section is claimed. The new inequality must not be advertised as stronger than the entire SDP hierarchy without a shared instance and certified comparison.

The O(log n) coded cut experiment is a useful acquisition design, but binary separating codes, Hamming distance, and union bounds are established tools. State it as an implementation consequence, not a new coding-theory result. Cross-entry caps remain independently required. The linear normalized-error regime depends on both leakage and imbalance being small; a fixed absolute per-entry uncertainty does not preserve quadratic counts for arbitrarily large n.

## Primary sources whose relevant body was read

### 1. Benvenuti and Farina, A Tutorial on the Positive Realization Problem (2004)

Open author manuscript: https://sites.math.rutgers.edu/~sussmann/papers/res-farina-tutorial-positive-realization.pdf

Read: §II formulation; §VII Theorems 15 and 16; surrounding examples and minimality discussion. This work treats exact positive realization of a prescribed discrete-time SISO transfer function. It distinguishes existence, minimum positive order, and generation of minimal positive realizations. Its pole-based lower bound can be far below the actual positive order even when all poles are real.

Overlap: a positivity restriction can force more states than an unrestricted realization. This is established background and cannot be claimed as the project’s discovery.

Difference: the new candidate allows only an approximate finite-time scalar measurement but exactly fixes a multiport static response and requires a reciprocal grounded-capacitor realization. No top-r DC-budget formula or fixed-K two-window theorem was found in the examined sections. The tutorial does not itself prove novelty in later literature.

Tool references: turn8view0; turn11view4.

### 2. Roxana Ionuțiu, Joost Rommes and Wil H. A. Schilders, SparseRC: Sparsity Preserving Model Reduction for RC Circuits With Many Terminals (2011)

Repository full text: https://pure.tue.nl/ws/portalfiles/portal/3597559/904284768535061.pdf

Read: §II-B, §III Theorem 1, §III-C1/C2. The reduced multiport model matches the zeroth and first admittance moments at DC. The congruence projection preserves passivity and stability. Crucially, §III-C2 explicitly permits negative capacitors in a passive synthesized netlist; with extra matching it may also produce negative resistors. It notes PartMOR as an alternative with positive-only elements.

Overlap: preserve DC response while reducing network dynamics; construct a smaller RC-type netlist; physical terminal interpretation and sparse graphs.

Difference: passive matrix realization does not imply a network of exclusively positive grounded capacities and positive resistors. Therefore its small model is not automatically a competitor in our physical model class. The paper gives an algorithm and matching guarantees, not a matching lower/upper formula for a fixed finite-window observable. Exact DC preservation by itself is not new.

DOI: https://doi.org/10.1109/TCAD.2011.2166075. Published IEEE TCAD 30(12), 1828–1841 (2011). Tool references: turn10view2, turn11view1, turn11view2, turn19view0. Bibliographic details verified against the repository cover and first printed page.

### 3. Martin Redmann, An L²_T-error bound for time-limited balanced truncation (2019)

Full preprint: https://arxiv.org/pdf/1907.05478

Read: §1 problem formulation, §2 Theorem 2.2 and Corollary 2.3, §3 heat-equation example. For stable LTI systems and zero initial conditions it derives finite-time L² output-error bounds based on truncated time-limited singular values, with constants involving the endpoint Gramians. The general time-limited method discussed does not preserve asymptotic stability automatically.

Overlap: reduce a heat-system model for a selected finite observation horizon and relate state count to error.

Difference: upper error guarantees for a particular projection method do not certify a universal minimum state count under exact K and elementwise physical sign conditions. Our two-window scalar observable is much weaker than the L² response objective. Do not compare numerical errors without converting the metrics.

Tool references: turn10view0, turn13view2.

### 4. Christian Grussler, Tobias Damm and Rodolphe Sepulchre, Balanced Truncation of k-Positive Systems (preprint 2020; v2 read, 2021)

Full preprint: https://arxiv.org/pdf/2006.13333

Read: §4 Theorem 1, Corollary 3 and Proposition 6, §5 Theorem 2. Hankel k-positivity gives conditions under which balanced truncation to order at most k is stable and Hankel totally positive; first-order internally positive MIMO approximations also receive a result.

Overlap: structure-preserving low-order approximation, sums of first-order lags, relation between positive realizations and Hankel structure.

Difference: Hankel total positivity is not the complete positivity/graph-supported boundary condition used here. No exact K or grounded-RC state-count tradeoff was found. This is relevant background but not an identified duplicate.

Tool references: turn10view1, turn11view3.

### 5. David Aldous and Larry Shepp, The least variable phase type distribution is Erlang (1987)

OA published scan: https://escholarship.org/content/qt7w51x4rb/qt7w51x4rb.pdf
DOI: https://doi.org/10.1080/15326348708807067

PDF recovered locally as round8_aldous_shepp.pdf. Text extraction only retrieves repository cover, so the original printed p.467 was rendered and read visually. The article proves the fixed-order Erlang chain minimizes the squared coefficient of variation among absorption times of finite-state continuous-time Markov chains. This is a statement about variability, not the maximum of every time-window functional.

Relevance: any attempt to optimize coupled component delay by treating it as a phase-type distribution must compare with known phase-count extremal inequalities. However, the triangular reward induced by the two-window functional is not globally convex or monotone. Hence a convex-order or least-variance theorem alone does not imply that Erlang, an exponential, or any chosen phase arrangement maximizes this reward.

Tool references: turn11view0 / turn12view0; original p.467 inspected locally.

### 6. Takayuki Osogami and Mor Harchol-Balter, Closed form solutions for mapping general distributions to quasi-minimal PH distributions (2006)

Open author PDF: https://www.cs.cmu.edu/~harchol/Papers/quasi-minimal-PH.pdf
DOI: https://doi.org/10.1016/j.peva.2005.06.002; Performance Evaluation 63, 524–552. Published online 2005, journal year 2006.

Read: §§1–3, especially Definitions 4/6 and Theorems 1–2. This paper characterizes the number of phases needed to match the first three moments and constructs an Erlang–Coxian distribution within one phase of the acyclic optimum. It explicitly distinguishes exact distribution representation from its term “well represented,” meaning only three-moment matching. Its acyclic-to-Coxian statement is attributed to Cumani (1982).

Overlap: experimental/statistical information can imply an exact or near-minimum number of positive Markov phases. Therefore “moments or observations force more states” is established in general. Difference: the paper does not impose a fixed multiport static graph or optimize the present compact finite-window reward. It also discusses acyclic rather than arbitrary cyclic optimality.

Citation caution: do not cite this paper as establishing every PH2 density's exact Coxian2 representation without an additional precise passage. That exact sentence was not found in the inspected version. The project's own two-eigenvalue mixture calculation makes the required lemma self-contained.

Tool refs turn31view0 and turn34view3. The related TOOLS 2003 papers are also openly available at https://www.cs.cmu.edu/~harchol/Papers/toolsa.pdf and https://www.cs.cmu.edu/~harchol/Papers/toolsb.pdf; use one representative citation in the HTML.

## Closely related sources located but not fully read

1. Bernard N. Sheehan, Realizable Reduction of RC Networks, IEEE TCAD 26(8), 1393–1407 (2007), DOI https://doi.org/10.1109/TCAD.2007.891374. Author/profile abstract available; full official or repository body not obtained. TICER removes small-time-constant, low-degree nodes and has a circuit-realizable output. Important comparison before publication; no conclusion about absent lower bounds based on the abstract.

2. Colm A. O’Cinneide, Phase-Type Distributions and Majorization, Annals of Applied Probability 1(2), 219–227 (1991), DOI https://doi.org/10.1214/aoap/1177005935. Bibliography and abstract identify a majorization strengthening of least-variable Erlang. Publisher full page did not expose the body in this session. Some aggregator dates incorrectly say 2007: use the actual 1991 journal date.

3. Qi-Ming He, Gábor Horváth, Illés Horváth and Miklós Telek, Moment bounds of PH distributions with infinite or finite support based on the steepest increase property, Advances in Applied Probability 51(1), 168–183 (2019), DOI https://doi.org/10.1017/apr.2019.7. Author PDF found at https://www.engineering.uwaterloo.ca/~q7he/Z_PDF_PS_Published/2019_AAP_PHD_Bounds.pdf but fetching failed. Abstract and author-posted opening sections accessible. It gives representation-size-dependent moment bounds using steepest increase. An abstract summary saying stochastic dominance by an Erlang must not be used without the rate normalization/parameters in the theorem.

4. R. J. Duffin and G. Knowles, Optimal thermal phase shift filters, Advances in Applied Mathematics 4(2), 197–211 (1983), DOI https://doi.org/10.1016/0196-8858(83)90010-6. Publisher author page labels the article open archive and gives its abstract. It optimizes capacitance in grounded-capacitor thermal filters to minimize attenuation at a specified phase shift. Body was not fetched. This is an older physical optimization precedent, not an established duplicate of the finite-window count theorem.

## Claim-by-claim rating

| Claim | Assessment |
|---|---|
| Positive constraints can increase minimal realization order | Established background |
| Exact DC preservation in model reduction | Established background |
| A scalar one-state exponential kernel has an optimal relaxation rate | Elementary derivation; weak novelty alone |
| Independent weighted DC budgets imply a top-r optimum | Elementary cardinality allocation; weak novelty alone |
| The exact formula is attained by positive edge stars plus residual direct conductances | Useful physical synthesis lemma; identical statement not located; priority unconfirmed |
| Cyclic regular subgraphs give an explicit fixed-K resource/error construction | Straightforward graph/spectral construction; valuable benchmark, do not oversell |
| Matching minimum for all admitted internally coupled networks, equal triangle-free K budgets and specified kernel condition | Analytic proof and independent audit now available; strongest specific theorem candidate; historical priority unconfirmed |
| Balanced leakage inequality and sharp construction | Analytically checked; meaningful explicit CP certificate; identical form not located |
| A new general theory of physical coarse-graining is completed | Not supported yet |

## Suggested safe wording

“We derive an exact minimum state count for a specified finite-time collective response while preserving the complete steady boundary conductance matrix. The theorem ranges over reciprocal networks with positive grounded capacities and nonnegative conductances, under equal triangle-free static edge budgets and a stated observation-kernel condition. A positive-element construction attains the lower bound. We also derive a separate finite-precision CP certificate whose leakage penalty is linear in the balanced case. Related principles are established in positive realization, RC reduction, phase-type distributions, and CP-rank theory; no identical statements were identified in the sources compared, but historical novelty is not established.”

## Minimal bibliography additions for the HTML

Retain existing [29] Redmann, [35] Benvenuti–Farina, [36] Grussler et al., [41]/[44] Fawzi–Parrilo, [69] Kron reduction, and [70] Korda et al. Add only three references if keeping the bibliography focused:

1. Ionuțiu, Rommes and Schilders (2011), *SparseRC*, DOI 10.1109/TCAD.2011.2166075, author/repository PDF above. Relevant body read: DC moments and negative synthesized capacitors.
2. Aldous and Shepp (1987), *The least variable phase type distribution is Erlang*, DOI 10.1080/15326348708807067. Original printed p.467 and theorem statement read visually; do not label the complete proof as read.
3. Osogami and Harchol-Balter (2006), *Closed form solutions for mapping general distributions to quasi-minimal PH distributions*, DOI 10.1016/j.peva.2005.06.002. Relevant body read: §§1–3 and precise meaning of moment matching.

## Search scope and limitations

Searched primary-paper leads using combinations of RC network, grounded capacitors, minimum realization/order, fixed DC gain, finite-time model reduction, thermal network, positive realization, phase-type, Erlang, majorization, and steepest increase. Both available engines were queried; some tightly quoted searches produced irrelevant or incomplete coverage. No claim of exhaustive database coverage is justified. Some recent broad search results were plainly irrelevant, so the main conclusions rest on the directly inspected primary texts and explicit problem comparisons, not search-result absence. The particular fixed-K / finite-window / all-positive grounded-capacity combination is a narrower and defensible contribution candidate, but old transformerless multiport synthesis and newer constrained approximation literature still need citation tracing before priority claims.
