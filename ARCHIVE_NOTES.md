# Archiving, Reproduction, and Corrections

**English** · [日本語](ARCHIVE_NOTES.ja.md)

First archive: **2026 10 07**. English editions introduced: **2026 10 08**.

## Scope

This archive gathers the saved mathematics-exploration project and the related artifacts it references for P versus NP, Wasserstein centers, X01, and the three independent exploration branches. It includes manuscripts, separately saved reviews, exploration notes, ZIP bundles, and reproducibility materials embedded in HTML. The cross-disciplinary work of 2026 10 06 includes its combined HTML report and surviving derivation and verification notes.

The attached and saved copies of the initial ledger were identical, so they are represented by one file, `project/initial-ledger-2026-09-08.md`. This archive does not reconstruct every chat message, unsaved intermediate file, or lost execution environment.

## Languages and editions

English is the primary language of repository navigation and the translated current reports. Japanese navigation is available through `README.ja.md` and `CATALOG.ja.md`. English report filenames contain `.en`; Japanese source reports retain their original paths. Historical drafts, raw execution logs, code, downloadable bundles, and review records remain in their original language unless a separate English edition is provided.

Translations preserve the assumptions, conclusions, proof status, limitations, and corrections in the sources. Translation does not establish novelty or constitute a new mathematical verification. Original source bytes remain unchanged so that a reader can check an English edition against its Japanese source. Each completed translation is published as a small update.

## Originals and extracted materials

- `provenance/source-manifest.json` records original filenames, archive paths, sizes, and SHA-256 hashes. Source manuscripts are preserved unchanged.
- Extraction records in `provenance/` record HTML attachment keys and ZIP member names. Embedded data was recovered statically, without executing unknown JavaScript.
- A manuscript may duplicate the ZIP or code embedded inside it. Both are retained so the materials can be downloaded and reused independently; they are not counted as separate research results.
- Filenames, READMEs, and verification logs inside `artifacts/` preserve the historical materials. If they contain old working directories or links, use the theme's entry page and extraction records to locate the corresponding archived file.
- `sandbox:` links and working paths inside originals are historical references. When the target was recovered, use its counterpart in this repository.

## What the verification establishes

Archive checks establish the identity of recovered files, the integrity of extracted data, and reachability from the navigation pages. They do not mean that saved numerical results were freshly reproduced, that experts reviewed every proof, or that research novelty was established.

In particular, X01 has a historical successful Lean execution log for 14 declarations in `MomentIslands.lean`. Another 33 declarations have not been compiled. This is not a formalization of the entire manuscript and all its ordinary mathematical proofs. Consult [CATALOG.md](CATALOG.md) and the source reports for the exact scope.

When rerunning an experiment, record the Python or Lean version, dependency versions, inputs, random seed, execution date, and new outputs. Preserve the original result JSON and logs; run a working copy in a separate directory. Also check the instructions supplied with each ZIP and the output paths used by its code.

## Corrections and attribution

Attribution to known results, citations, and license notices inside the sources are retained. The source filename for one-exception symmetry includes `v5`, but the current report is the sixth edition and incorporates a counterexample to Conjecture K for general odd cliques. Read conjectures and novelty assessments in earlier notes together with later corrections.

OpenAI PDFs, Lean files, and catalog sources downloaded when studying third-party papers are not bundled here. The [related-work comparison](project/openai-math-comparison-2026-10-07.en.md) records the comparison and links to the original sources.
