# 横田の数学・物理・工学探索

横田とAIが一緒に進めてきた探索研究の原稿、証明、計算実験、査読・訂正記録を集めたリポジトリです。

AIが候補の探索・定式化・反例探索・証明・文献照合を担い、人間が目的を伝え、方向性と結論を監査する。その過程で得た知識を、他の人が検証・応用・拡張できる形で残します。

初回集約：**2026 10 07**。数学的な証明の状態、形式検証の状態、学術的新規性は、それぞれ別に記録します。

## 入口

- **[研究目次と検証範囲](CATALOG.md)** — 何が分かり、何が未解決か。
- **[横断報告：何を守って、どこまで縮められるか](reports/research-deepening-2026-10-06.html)** — 2026 10 06の抽象化と4方向の追加研究。
- **[プロジェクトの出発点](project/initial-ledger-2026-09-08.md)** — 研究方針と最初の成果台帳。
- **[収録・再現・訂正の方針](ARCHIVE_NOTES.md)** — 原本、過去ログ、復元したコードの扱い。

## テーマ

| テーマ | 問い | 原稿と資料 |
| --- | --- | --- |
| 小回路の更新・P対NP探索 | 出力の一部を変えるには、何個のゲートを追加すればよいか | [incremental-circuits](research/incremental-circuits/) |
| Wasserstein中心 | 範囲・平均・分散だけが分かる分布族を、どの分布で代表するか | [wasserstein-center](research/wasserstein-center/) |
| モーメント・順位差・位相 | 平均と分散から、順位の間隔や許容集合の形をどこまで保証できるか | [moment-rank-gap](research/moment-rank-gap/) |
| 丸め・集計・比較監査 | 不偏丸めの代価、集計からの復元、最少の三角監査 | [rounding-aggregation-audit](research/rounding-aggregation-audit/) |
| ゲーム理論・監査設計 | 評価に共通誤差があるとき、改善の循環と監査の限界は何か | [game-theory](research/game-theory/) |
| 空間の観測と接続 | 雑音のある距離測定と、不確実な位置でのネットワーク設計 | [spatial](research/spatial/) |
| 一例外対称性 | 一つの例外を許した対称構造からゲーム値を決められるか | [one-exception-symmetry](research/one-exception-symmetry/) |
| 形式意味論・候補保持 | 圧縮して候補を捨てると、将来の選択肢をどこまで失うか | [formal-semantics](research/formal-semantics/) |
| 物理的記憶と縮約 | 熱・RC回路の内部状態を、応答と容量を守ってどこまで減らせるか | [physical-memory](research/physical-memory/) |

各フォルダの `report.html` または `report.md` が本文です。`notes/` は探索・導出、`reviews/` は査読と先行研究照合、`artifacts/` はHTMLから復元したコード等、`experiments/` は追加の検証コードと当時の結果、`archives/` は保存されていたZIPです。テーマにより収録物は異なります。

## 読み方と検証

HTMLはダウンロードしてブラウザで開けます。リポジトリ全体を取得した場合は、ルートで次を実行すると相対リンクを辿れます。

```bash
python3 -m http.server 8000
```

GitHub上ではMarkdownとソースコードを直接読めます。HTMLの数式・図解・操作部はブラウザで確認してください。一部の原稿は外部CDNを参照するため、通信が必要です。

収録ファイルのハッシュと新しい目次のリンクは、次で確認できます。

```bash
python3 tools/verify_archive.py
```

数学の検算には各テーマのコードと説明を参照してください。保存ログは当時の実行記録であり、今回の移設時に全計算を再実行した記録ではありません。X01のLeanについては、14宣言の過去の成功記録と、追加33宣言の未実行コードを区別しています。

## 更新

新しい結果には、正確な仮定・結論、証明、既知結果との関係、検証方法、残る問いを付けます。反例や訂正も保存し、旧稿は現行の結論と混同しない位置に置きます。成果の記録には [命題記録テンプレート](project/claim-template.md) を使えます。

第三者の研究は出典として参照します。OpenAIの `openai/math` に収録された原稿・Leanコードは、このリポジトリの成果には含めていません。

---

This repository preserves exploratory research by Yokoda and AI collaborators: manuscripts, proofs, computational checks, reviews, and corrections. Proof status, formal verification, and novelty are tracked separately. Most manuscripts are in Japanese; the moment/rank-gap report also includes English. See [CATALOG.md](CATALOG.md) for scope and limitations.
