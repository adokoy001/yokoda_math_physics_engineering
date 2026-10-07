# Connections to OpenAI's Mathematics Release

**English** · [日本語](openai-math-comparison-2026-10-07.md)

Checked: **2026 10 07**. This is a comparison with external research, not a result of this project.

Primary sources: [openai/math](https://github.com/openai/math), the [release announcement](https://openai.com/index/sharing-ai-progress-in-mathematics/), and the [results catalog](https://github.com/openai/math/blob/main/overview.tex). At the time of the check, the README listed 722 manuscripts and 372 result families. The following compares public claims and methods; it is not an audit of every proof or a rerun of the Lean code.

| Release entry | Connection | Possible direction for this project |
| --- | --- | --- |
| 330: approximation properties of Lipschitz-free spaces | A claimed separation between finite-rank approximability and approximation with uniformly bounded operator norms. The proof approach uses total variation of signed measures and test functions. | Can the physical-memory obstruction that capacity must diverge as accuracy improves be expressed using finitely many measurements? The objects, resources, and measures differ; direct applicability is not asserted. |
| 374: one-third stability of Brenier maps | A bound on transport-map error in terms of the target Wasserstein-2 distance, in the specified multidimensional setting of uniform probability measures on convex bodies. | Connect the selection of a representative distribution to an error bound for a transport map to it. This is not directly transplanted into the current one-dimensional center formula. |

See the manuscripts for [330](https://github.com/openai/math/blob/main/preprints/Failure-of-Bounded-Approximation-in-a-Lipschitz-Free-Space-over-a-Uniformly-Discrete-Metric-Space-September-26-2026/main.pdf) and [374](https://github.com/openai/math/blob/main/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/article.pdf). The latter concerns uniform probability measures on convex bodies; the word “uniform” describes the measure.

The [summary of the research process for π](https://github.com/openai/math/blob/main/reasoning_traces/irrationality-exponent-of-pi.pdf) suggests several methodological lessons: track improvements in approximation together with the cost of coefficients and denominators; check independence and nonvanishing separately; and apply an argument to known counterexamples to detect overgeneralization. A public process summary is distinct from a complete trial history.
