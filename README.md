# Yokoda — Mathematics, Physics & Engineering

**English** · [日本語](README.ja.md)

Exploratory research by Yokoda and AI collaborators: manuscripts, mathematical proofs, computational experiments, reviews, and corrections.

AI collaborators explore candidates, formulate claims, search for counterexamples, develop proofs, and compare the literature. Human oversight sets the purpose and audits the direction and conclusions. We preserve the resulting work so that others can check, apply, and extend it.

First archive: **2026 10 07**. English editions are being added from **2026 10 08**, one theme at a time. Mathematical proof, formal verification, and research novelty are recorded separately.

## Start here

- [Research catalog and verification scope](CATALOG.md) — results, assumptions, open questions, and limitations.
- [Cross-disciplinary report: what must be preserved, and how far can a model be reduced?](reports/research-deepening-2026-10-06.html) — the original report from 2026 10 06.
- [Initial project charter and research ledger](project/initial-ledger-2026-09-08.md).
- [Archiving, reproduction, and corrections](ARCHIVE_NOTES.md).

English is the primary navigation language. Each theme links to its English edition when available and to the preserved Japanese original. Historical drafts, review records, code comments, and execution logs retain their original language. During this staged translation, some destinations still open the Japanese edition.

## Research themes

| Theme | Question | Reports and materials |
| --- | --- | --- |
| Circuit updates and P versus NP | How many gates must be added when only part of an output is changed? | [Incremental circuits](research/incremental-circuits/) |
| Wasserstein centers | How should a family of distributions with specified range, mean, and variance be represented by one distribution? | [Wasserstein center](research/wasserstein-center/) |
| Moments, rank gaps, and topology | What do the mean and variance guarantee about rank separation and the shape of the feasible set? | [Moment–rank gap](research/moment-rank-gap/) |
| Rounding, aggregation, and comparison audits | What are the costs of unbiased rounding, reconstruction from aggregates, and minimal triangle audits? | [Rounding and aggregation](research/rounding-aggregation-audit/) |
| Game theory and audit design | Under shared evaluation errors, when can improvement cycle, and what limits auditing? | [Game theory](research/game-theory/) |
| Spatial observation and connectivity | How do noisy distance measurements and uncertain positions constrain observation and network design? | [Spatial research](research/spatial/) |
| One-exception symmetry | Can a symmetry with one exception determine the value of a combinatorial game? | [One-exception symmetry](research/one-exception-symmetry/) |
| Formal semantics and candidate retention | When compression discards candidates, how much can it lose in future choices? | [Formal semantics](research/formal-semantics/) |
| Physical memory and model reduction | How far can internal states in thermal and RC circuits be reduced while preserving response and capacity? | [Physical memory](research/physical-memory/) |

Each theme's README is the entry point. English reports use `report.en.html` or `report.en.md`; the original `report.html` or `report.md` remains available as the Japanese source. `notes/` contains explorations and derivations, `reviews/` reviews and prior-art checks, `artifacts/` material recovered from HTML, `experiments/` additional checks and their recorded results, and `archives/` saved ZIP bundles. Contents vary by theme.

## Reading and verification

Download an HTML report and open it in a browser. To browse a local checkout with working relative links, run this command at the repository root:

```bash
python3 -m http.server 8000
```

GitHub displays Markdown and source code directly. Use a browser for HTML equations, diagrams, and interactive controls. Some original reports use external CDNs and require an internet connection.

Verify file hashes and navigation links with:

```bash
python3 tools/verify_archive.py
```

For mathematical checks, follow the code and instructions in the relevant theme. Saved logs record earlier runs; the archival and translation work does not rerun every experiment. For X01, the successful historical Lean check of 14 declarations is distinguished from 33 additional declarations that have not been compiled.

## Continuing the research

New results should state precise assumptions and conclusions, supply proofs, explain their relationship to known results, describe verification, and identify remaining questions. We preserve counterexamples and corrections and identify earlier drafts so they are not confused with current conclusions. Use the [claim template](project/claim-template.md) to record a result.

Third-party research is cited as prior work. Manuscripts and Lean code from OpenAI's `openai/math` repository are not included among this project's results.
