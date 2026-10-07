# OpenAI数学公開物との接点

確認日：2026 10 07。外部研究の比較メモであり、このプロジェクトの成果ではありません。

原出典：[openai/math](https://github.com/openai/math)、[公開説明](https://openai.com/index/sharing-ai-progress-in-mathematics/)、[結果カタログ](https://github.com/openai/math/blob/main/overview.tex)。確認時のREADMEは722原稿・372結果群と記載しています。以下は公開主張と手法の接点の整理で、全証明の監査やLeanの再実行は実施していません。

| 公開資料の番号 | 接点 | このプロジェクトでの検討候補 |
| --- | --- | --- |
| 330：Lipschitz-free空間の近似性 | 有限ランク近似可能性と、作用素ノルムを一様に抑えた近似可能性を分離する主張。本文の証明方針は符号付き測度の総変動とテスト関数を使う | 物理的記憶の「精度を上げるには容量が発散する」という障害を、有限個の測定で表せるか。対象・資源・測度が異なるため、そのまま適用できるとはしていない |
| 374：Brenier写像の1/3乗安定性 | 指定された多次元・一様凸体分布の設定で、標的のW₂距離から輸送写像の誤差を評価する主張 | 分布の代表を選ぶ問題と、その分布へ輸送する写像の誤差評価を接続する。現在の一次元の中心公式へ直接移植しない |

330の[本文](https://github.com/openai/math/blob/main/preprints/Failure-of-Bounded-Approximation-in-a-Lipschitz-Free-Space-over-a-Uniformly-Discrete-Metric-Space-September-26-2026/main.pdf)、374の[本文](https://github.com/openai/math/blob/main/preprints/Sharp-One-Third-Stability-of-Brenier-Maps-September-25-2026/article.pdf)を参照してください。374の「一様凸体分布」は、凸体上の一様確率測度という意味です。

[πの研究過程要約](https://github.com/openai/math/blob/main/reasoning_traces/irrationality-exponent-of-pi.pdf)からは、近似改善と係数・分母の費用を同時に追うこと、独立性や非消滅性を別に検査すること、既知の反例へ議論を適用して過剰一般化を検出することを方法上の参考にしています。公開要約と完全な試行履歴は区別します。
