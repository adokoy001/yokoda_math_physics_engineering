# P vs NP 研究パック

作成日：2026 09 05

最初に **P_vs_NP_restart_2026-09-05.md** を読む。過去ノートの研究史、今回の訂正、先行研究、構成的な補題、検査結果、次の命題がまとまっている。

## ファイル

| 場所 | 内容 |
|---|---|
| P_vs_NP_restart_2026-09-05.md | 今回の統合報告 |
| updated/ | 更新した研究ノート v0.25 と候補台帳 v0.17 |
| sources/ | 回収した旧ノート v0.24 と候補台帳 v0.16 の原本 |
| literature_compilation.md / literature_compilation_evidence.md | 知識コンパイルと2026年文献の監査 |
| barriers_transfer.md | MMW・IKW・量化・PAP・証明障壁の監査 |
| wc_audit.md | WC、live promise、次ビット修復の監査 |
| tr26_128_width_recheck.md | 過去に指摘した論文の現行版と、旧監査側の前提不足の再点検 |
| ordered_patch.md | 連続区間の構成と自明completionの監査 |
| tiny_wc_synthesis.md | 有限回路全数列挙と鋭い例 |
| *.py / 実験*.json相当の各JSON | 再現コードと計算結果 |
| source_checksums.json | 回収資料と更新資料のハッシュ、文書内の版番号 |

元ノート内の旧 experiments/FINDINGS.md などの相対参照は、当時の実験記録を指す。今回のパックは回収した2冊と今回の実験を収録しており、その旧実験フォルダ全体を復元したものではない。

外部論文は本文の一次資料リンクを参照する。論文PDFの複製は同梱していない。

## 再現

このディレクトリで標準 Python 3 を用いて実行する。外部ライブラリは不要。

~~~bash
python3 verify_nextbit_patch.py
python3 verify_ordered_patch.py
python3 tiny_wc_synthesis.py --n 2 --size 4 --out tiny_wc_synthesis_n2.json
python3 tiny_wc_synthesis.py --n 3 --size 5 --out tiny_wc_synthesis_n3.json
python3 tiny_wc_synthesis.py --n 4 --size 4 --out tiny_wc_synthesis_n4.json
python3 verify_tiny_wc_synthesis.py
~~~

測定秒数は実行環境で変わる。有限回路のBFSは一層あたり時間上限があり、途中で打ち切った層を完全列挙とは記録しない。大きな n への外挿はしない。

## このパックの範囲

- P=NP、P≠NP の証明ではない。
- 初等補題の記号的証明と有限検査は含むが、形式証明支援系での検証はしていない。
- 新規性確認済みの成果はない。文献の条件・版と、推論の向きの整理を含む。
- 複数の監査担当は同じモデル系列・道具を共有している。完全に独立した外部検証ではない。
