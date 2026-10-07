# X01 v1.1 — Fable5.1 の独立レビューへの応答

2026 09 09

横田さんから提供された `memo-to-astra_x01-review.html` を原文・証明ソースと照合した。レビューは手計算・ソース精読・Python再実行と、Lean再コンパイル未実施を区別している。この区別を維持し、以下を反映した。

| 指摘 | 対応 |
|---|---|
| A 適用域と行列中心の構成 | ほぼ二値の有効域と O(1/n) の分散条件を冒頭に明記。行列版はスペクトル定理による系として追加。全行列空間では固有ベクトルの回転が連続経路を増やすため、成分数の結論は固定座標のベクトル／対角モデルに属する。主定理全体を行列版へ置換しない。 |
| B 広い誤差帯 | 1/2<η<1、全 n≥2、1≤s<n、δ≥0 の道連結成分数をT9として証明。n=2の観察は正しく、η=.9の閾値は .09、.095、.25。二次元の穴も分類した。 |
| C 帰属 | 丸め評価の初等的直接証明を主とし、Rastegin (2023) を明示的な先行記述の一つとする。初出の断定はしない。 |
| D 分割形 | T1を任意分割の平方不等式で述べる。既存 rank_gap_partition と一致し、Leanソース変更なし。符号付き平方根下界には集合間の順序仮定が必要。 |
| E 補助例・合冊 | 14宣言に4変数の補助例2件が含まれることを明記。READMEにX04の別系統資料を含む合冊であることを追記。 |

T9の一般的な道具は、凸集合を除いた多面体を辺グラフへ還元する既知理論である。新しい一般原理とは数えず、今回の帯に対する明示的な式の優先権も未確定とする。

独立監査は活性制約の階数から辺を抽出し、60個の有理多面体・660条件ですべて一致した。別の補助検算も45多面体・444条件で一致したが、重複する条件を含むため合算して独立標本数とはしない。一般性は本文の証明に依拠し、有限検算は補助である。

Mathlib v4.19.0 のタグと commit c44e0c8ee63ca166450922a373c7409c5d26b00b の対応を公式Gitリポジトリで直接再確認した。2026 09 09のLean再コンパイルは、公式配布物の取得段階で環境のネットワーク承認が停止したため未実施。前回の成功ログとソースをそのまま保存し、今回の独立再実行とは扱わない。T9は未Lean形式化。

2008年の density-matrix purification 論文は実在と概要を確認したが全文照合は未完了。2013年の trace・Frobenius norm による固有値境界は具体的に照合した。同じ鋭い順位式を確認したとは主張せず、新規性も確定しない。

## English record

The supplied independent review was checked against the text and formal source. Version 1.1 clarifies the nearly binary regime, states the partition inequality exactly as proved in Lean, and presents the elementary rounding proof before the bibliographic comparison. Rastegin (2023) is an identified explicit prior statement, not an assertion of first discovery.

The matrix inequality is included as a spectral corollary. The vector component count is not transferred to the full matrix space: continuous rotations connect coordinate projections while preserving their spectrum, trace, and zero idempotency defect. The note therefore retains its vector formulation for the topology.

The reviewer’s wide-band observation led to T9, a complete path-component count for all n≥2, 1≤s<n, 1/2<η<1 and δ≥0. The proof enumerates all vertices and edges of the band polytope and applies convex-obstacle graph reduction. In dimension two, it also identifies the range with homotopy type S¹. This is an explicit application of prior general theory; priority of the particular formula is unresolved, and T9 is not Lean-formalized.

An independent exact-arithmetic graph audit passed 660 conditions on 60 rational polytopes. A separate check passed 444 conditions on 45 polytopes; overlapping coverage is not counted as independent samples. These finite checks support, but do not replace, the general proof.

The official Mathlib tag-to-commit mapping was verified. A fresh Lean compilation was not run: obtaining the official runtime stopped during environment preparation. The unchanged source and successful 2026 09 08 log remain historical evidence, clearly separated from this review’s source audit. The two auxiliary four-variable examples and the separate X04 branch are explicitly identified in the count and archive README.

The bilingual HTML contains five interactive figures and embedded proof, review, and audit materials. Mathematical typesetting and offline DOM/program behavior are checked. No browser viewport verification is claimed.
