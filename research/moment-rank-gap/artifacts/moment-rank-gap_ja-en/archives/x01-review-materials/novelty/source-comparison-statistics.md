# X01 公開前照合：決定論的統計・制約最適化

調査日：2026 09 09。対象は T1（順位間隔の普遍不等式）と T2（総和誤差帯の三枝最適値）。これは限定的な一次文献照合であり、学術的新規性の認定ではない。

## 結論

**T1 の内部順位の一般形と T2 の三枝式をそのまま陳述した一次文献は、今回の検索では同定できなかった。** ただし、そのことから新規とは結論しない。T2 は T1 と既知の packed 二乗和境界を組み合わせた明示的な系として扱う。特に最大二乗和の床関数公式は既知であり、今回さらに、まったく同じ公式を明記する最近の統計論文を確認した。

前回未読だった SPREAD 2022 は今回公式 PDF を取得して、対象の定義と証明を確認した。これは可変平均下での分散**下限**を使う制約伝播の論文であり、X01 の大きな分散が強制する順位間隔の下限とは異なる。

## 1. 同一の部品を明示する一次文献：Ellis 2025

Jules L. Ellis, *The maximum variance of a finite dataset, given its mean, minimum, and maximum*, arXiv:2508.17525v2（2025 08 27）。[書誌と版](https://arxiv.org/abs/2508.17525)、[一次 PDF](https://arxiv.org/pdf/2508.17525)。全 7 頁の本文を確認した。

Theorem 1（PDF pp.4–5）は、\(y\in[0,1]^n\)、平均 \(c\)、\(a=\{nc\}\) に対し、

\[
\max\operatorname{var}(y)=c(1-c)-\frac{a(1-a)}n
\]

を与える。Example 2（p.6）は \(\sum x_i^2\le\sum x_i-a(1-a)\) を明記する。従って X01 の記号では

\[
Q_{\max}=\lfloor S\rfloor+\{S\}^2,
\qquad D\ge\{S\}(1-\{S\})
\]

と完全に同一。Lemma 1（p.3）の「最大化点で端点以外の成分は高々一つ」、Lemma 2（p.4）の「その成分は総和の小数部分」も一致する。

**帰属：既知の同一結果。** これ自体を新規成果に数えない。Rosenberg–Jakobsson (2008) の既存引用もあるため、Ellis を最初の発見者とする主張はしない。Ellis の論文に順位間隔や総和誤差帯の三枝式は記載されていない。

同題の *The American Mathematical Monthly* 論文が 2026 08 24 オンライン公開として出版社検索に掲載されている（DOI [10.1080/00029890.2026.2708352](https://doi.org/10.1080/00029890.2026.2708352)）。本調査で定理照合した版は上記 arXiv v2 であり、雑誌版本文は未確認。

## 2. SPREAD 2022：全文による問題の違いの確認

Alexander Ek, Andreas Schutt, Peter J. Stuckey, Guido Tack, *Explaining Propagation for Gini and Spread with Variable Mean*, CP 2022, LIPIcs 235, 21:1–21:16。前回の記録では PDF 未取得だったが、今回は [公式 PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol235-cp2022/LIPIcs.CP.2022.21/LIPIcs.CP.2022.21.pdf) を取得した。[公式書誌](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2022.21)。

- §2.3（21:4）：整数変数を実数区間へ緩和。Definition 2 は指定中心 \(\nu\) に最も近い区間内点を各成分に選ぶ。
- §3、式 (3)（21:4）：総和 \(M\) と分散の等式 \(n^2V=n\sum x_i^2-M^2\) がモデル。
- §3.1、Lemma 3–4（21:5）：中心に寄せた代入から分散の**下限**を計算する。
- §3.2、Algorithm 1、Lemma 5（21:6–7）：その下限を使う伝播器と説明節の正当性。

**帰属：関連する一般的問題設定・計算手法。同一命題ではない。** 分散上限に違反する領域を落とす問題であり、X01 の \(D\le\delta\)、つまり（総和固定なら）分散の下限を課す側とは方向が違う。本文に T1/T2 の式、指定された隣接順位間隔の最小値、三枝境界は見当たらない。SPREAD 文献全体に同種の式が存在しないとまで判定したわけではない。

## 3. 決定論的な順序統計量の既存理論

Agnieszka Goroncy and Tomasz Rychlik, *How deviant can you be? The complete solution*, Mathematical Inequalities & Applications 9 (2006), 633–647。[出版社 PDF](https://files.ele-math.com/articles/mia-09-57.pdf)。今回も定式化、Theorem 1、§3 Example 2 を本文で照合した。

§2（p.637）で最適化対象は全ての非定数実ベクトル \(X\subset\mathbb R^n\)。外から与えた共通箱 [0,1] は課さない。p.637 は、全 range 以外の順序統計量の差には一様な正の下限がないことを Fahmy–Proschan (1981) に帰属する。§3 Example 2（pp.642–643）はその理由を、他の端の座標を動かして中心モーメントを増大できる点から説明する。

**帰属：順位差をモーメントで制御する問題の先行研究。ただし X01 と前提が異なる。** 外部箱と最大分散近傍が本質なので、この論文の題名の「complete solution」だけで X01 が包含されるとは言えない。

Salwa Fahmy and Frank Proschan, *Bounds on Differences of Order Statistics*, The American Statistician 35(1) (1981), 46–47。出版社の PDF の所在 [10.1080/00031305.1981.10479304](https://www.tandfonline.com/doi/pdf/10.1080/00031305.1981.10479304) までは確認したが、本文取得は 403。**原論文全文は引き続き未読**であり、上記 2006 論文経由の帰属と区別する。

## 4. 残る文献と未読の明示

| 文献 | 確認したもの | 今回の扱い |
|---|---|---|
| Schaus–Régin, *Bound-consistent spread constraint* (2014), DOI 10.1007/s13675-013-0018-8 | [出版社概要](https://link.springer.com/article/10.1007/s13675-013-0018-8)・著者書誌 | 整数領域の二乗和最小化と伝播。全文未読。同一定理の完全除外はしない |
| Kvålseth, *Bounds on Sample Variation Measures Based on Majorization* (2015), DOI 10.1080/03610926.2013.844252 | Ellis の参考文献・概要 | majorization による分散等の境界。全文未読 |
| Kobayashi–Tanaka, *Unified relationship between mean, variance, and an arbitrary number of quantiles*, Metrika 88 (2025), 1051–1065 | [出版社概要](https://link.springer.com/article/10.1007/s00184-025-01001-6) | 任意個の分位数の可能領域。全文未読、指定箱を持つ有限標本の T1/T2 への還元を未確認 |
| Selim, *Bounds on Variance Based on Differences of Mass Points*, Advances and Applications in Statistics 47(3) (2015), 211–224 | [出版社概要](https://www.pphmj.com/abstract/9559.htm) | 質点差と質量による標本分散境界。PDF 所在はあるが本文取得 403、全文未読 |

## 5. 探索範囲と控えめな判定

今回の追加検索では、`fixed mean variance bounded sample`、`deterministic spacings`、`maximum variance order statistics`、`bounded sample variance order statistics`、`Bhatia-Davis order statistics`、`sum of squares bounded order statistics inequality`、`rank gap sum of squares`、`minimum gap sum squares inequality`、`maximum variance finite majorization` と、上記既知論文の題名・著者を照合した。確率的な spacings の分布・期待値・分散を論じる文献は、有限個の実数そのものに課す X01 の決定論的制約と区別した。

T1 の既知の特殊例については、親監査が Rosenberg–Jakobsson (2008), Theorem 1(ii) の高純度枝と照合している。本稿はその独立再読を行っていないため、正確な帰属は親監査の記録に従う。

**公開時に妥当な書き方：** 「既知の有限標本の最大分散公式などを基礎に、順位間隔と総和誤差帯について鋭い境界を独立導出した。一般内部順位の式と三枝の最適値を同じ形で記した文献は今回の限定検索では同定できておらず、新規性は未確定である。」

「未同定」と「既知理論から短く導けない」は別である。T1/T2 を既知命題へ短く還元できるかの数学的監査が優先される。

## ローカル閲読資料

- `novelty_work/sources/ellis2025.pdf` / `.txt`：arXiv v2、7 頁
- `novelty_work/sources/spread2022.pdf` / `.txt`：公式 CP 2022、16 頁

原文は照合用中間資料。ユーザー向け資料には必要な書誌・式・短い要約を引用する。
