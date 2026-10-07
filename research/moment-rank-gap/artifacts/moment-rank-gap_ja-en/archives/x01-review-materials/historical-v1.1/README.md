# 数学探索 第2回・再現資料

最初に `数学探索_第2回_順位間隔と形式証明.md` をお読みください。

## 内容

* round2_formal: Lean 4.19.0 / Mathlib の証明、実行ログ、版とハッシュ、再実行手順。
* round2_robust: 順位間隔、誤差帯、二線分の構成、丸め閾値、反例の完全証明と厳密検算。
* round2_topology: 非整数総和、一般凸スコア、穴の遷移の完全証明と厳密検算。
* round2_graph: 最少三角監査の一意性、行列式による誤差ギャップ、全設計の有限検査。
* round2_novelty: 一次文献との照合と、未読・未確定の範囲。

Python の検算は標準ライブラリのみを用います。各スクリプトは同じディレクトリの結果 JSON を再生成します。

```bash
python3 round2_robust/check_robust.py
python3 round2_topology/verify_noninteger_topology.py
python3 round2_topology/verify_higher_holes.py
python3 round2_graph/check_graph_round2.py
```

Lean の再実行にはインターネット接続と Lean / Mathlib の導入が必要です。`round2_formal/README.md` に通常環境の手順と、今回だけ必要になった実行場所の互換処理を記録しています。依存ライブラリ本体は同梱していません。

Lean 検証はソース中の個々の命題を対象とします。位相分類、鋭さの全達成配置、三角監査全体、新規性を形式検証したという意味ではありません。途中の Lean コンパイル失敗ログがある場合も削除せず収録しています。

`SHA256SUMS.json` はこの資料の各ファイルのハッシュです。


## 2026 09 09 / HTML edition 1.1

This is a combined reproducibility archive. The standalone bilingual HTML is the
current exposition; `bilingual-edition/article_ja.md` and `article_en.md` contain
its current source text. The older Round 2 report remains a historical record.

The main note concerns X01. `round2_graph` contains the separate X04 triangle-audit
branch, retained as historical material; it is not part of the X01 theorem claims.
The two `four_variable_*` Lean statements are auxiliary exploration examples,
included in the total of 14 checked statements, not two additional main X01 results.

`review-2026-09-09` records the supplied independent review, the response, the wide
band component classification, literature comparison, and a separate Lean recheck.
The original Lean source and successful 2026 09 08 logs are unchanged. A fresh
2026 09 09 compilation was NOT executed: runtime acquisition stopped during
environment preparation. The official Mathlib tag-to-commit mapping was verified.
The new T9 classification has a mathematical proof but is not Lean-formalized.

General polytope/convex-obstacle graph reduction is prior theory. Academic priority
of this explicit wide-band formula remains unresolved. The independent graph
enumeration is finite verification, not a substitute for the proof.

The SHA-256 manifest covers every archive entry except the manifest itself.
