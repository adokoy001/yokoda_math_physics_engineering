# X01 第2回：新規性の独立照合

2026 09 08。第1版の第1〜8節を対象に、定理の名前が異なる文献も探索した。**査読による新規性認定ではなく、読めた一次資料と命題を対応づけた記録**である。

## 1. 今回の重要な更新

丸め評価

\[
\|x-z\|_1\le 1-\sqrt{1-2D},\qquad D=\sum_i x_i(1-x_i)<1/2
\]

について、**総和1の場合と一致する既知の鋭い不等式を発見した**。一般の整数総和の場合も、その既知不等式と初等的な集約による短い系として導ける。

該当資料は Alexey E. Rastegin, *Uncertainty relations in terms of generalized entropies derived from information diagrams*, 2023, Theorem 1, equations (30)–(31)。[arXiv 本文](https://arxiv.org/html/2305.18005v1)、[PDF](https://arxiv.org/pdf/2305.18005)。定理と証明を本文で照合した。

原論文の記号では、確率ベクトル \(P=(p_i)\) の二乗和 \(I(P)=\sum_i p_i^2\) と最大確率に対し、鋭い上下限を与える。高純度の枝 \(I(P)>1/2\) の下限は

\[
\max_i p_i\ge\frac{1+\sqrt{2I(P)-1}}2.
\]

したがって \(\sum_i x_i=1\) なら \(I=1-D\)、\(z=e_{\arg\max_i x_i}\) として、今回の丸め上限はまさにこの不等式の書換えとなる。原論文では全ての \(I\) について区分的な下限を与えており、今回必要な枝より広い。

## 2. 一般の整数総和を既知結果へ還元する

以下の還元は今回の監査で書いたものであり、Rastegin が整数総和の丸め定理を原論文に記載したという意味ではない。

前提は \(x_i\in[0,1]\)、\(\sum_i x_i=s\in\mathbb Z\)、\(D<1/2\)。最近整数丸め \(z\) を取る。\(d_i=\min(x_i,1-x_i)\) に対して \(d_i\le2x_i(1-x_i)\) だから \(\sum_i d_i<1\)。\(s-\sum_i z_i\) は絶対値1未満の整数なので0。丸めが総和を保存することが分かる。また \(x_i=1/2\) があると、その値の丸め方を変更した二つの丸めがともに総和を保存してしまうため矛盾し、一意である。

\[
\rho=\sum_{z_i=0}x_i=\sum_{z_i=1}(1-x_i)<1/2
\]

とおき、新たな確率ベクトル

\[
P=\bigl(1-\rho,\;(x_i)_{z_i=0}\bigr)
\]

を作る。\(\max P=1-\rho\) であり、

\[
\begin{aligned}
I(P)&=(1-\rho)^2+\sum_{z_i=0}x_i^2,\\
1-D&=1-2\rho+\sum_{z_i=0}x_i^2+\sum_{z_i=1}(1-x_i)^2.
\end{aligned}
\]

非負数の二乗和は和の二乗以下だから、\(I(P)\ge1-D>1/2\)。Rastegin の上記の枝を適用すると

\[
1-\rho\ge\frac{1+\sqrt{2I(P)-1}}2
\ge\frac{1+\sqrt{1-2D}}2.
\]

従って \(2\rho=\|x-z\|_1\le1-\sqrt{1-2D}\)。\(s=0,n\) は零誤差の自明例として分ける。\(D=0\) でも結論は直ちに成り立つ。

**判定：** s=1 については既知結果と同一。一般sの明示的な丸め解釈まで同じ形で出版されているかは未確認だが、既知結果からの短い系と分類するのが妥当である。「新しい鋭い不等式」として単独で主張する根拠は大幅に弱まった。

任意の部分集合 \(A\) に対する \(|\sum_{i\in A}(x_i-z_i)|\le\rho\) は、零和ベクトルの正部分・負部分の質量が等しいことから得られる標準的な関係である。この一般論を新規と数えることも避ける。

## 3. 部分和の完全可能集合に関する照合

今回の命題は

\[
\max(0,S-(n-k))\le t\le\min(k,S),\quad
\frac{t^2}{k}+\frac{(S-t)^2}{n-k}\le Q\le\phi(t)+\phi(S-t),
\quad \phi(u)=\lfloor u\rfloor+\{u\}^2.
\]

「固定ラベルk個の和t」の完全可能集合であり、最大k個の和、任意確率分布の条件付き期待値、与えられた固定配列の部分和問題とは区別した。

### 3.1 同じ下側境界の近接結果

Rastegin, *Entropic uncertainty relations for measurements assigned to a projective two-design*, APL Quantum **1**, 026111 (2024), Theorem 2 は、確率ベクトルについて最大2成分の和を二乗和から上界評価する。[一次本文](https://pubs.aip.org/aip/apq/article/1/2/026111/3294017/Entropic-uncertainty-relations-for-measurements)。Theorem 2 と証明を読んだ。

その計算は残り \(n-2\) 成分の Jensen 下限を使い、最適点で先頭2成分を等しくする。今回の \(S=1,k=2\) の \(q_0(t)\le Q\) を解いた上側端点に一致する。論文は \(I\ge1/2\) では2成分和の上界1が自明になる旨も述べる。

**この定理は固定ラベル部分和の穴を記述してはいない。** したがって今回の完全可能集合と同一だとは認定しない。一方で二次モーメントから部分確率和を制御する発想・下側二乗和の部品について、明確な近接先行研究である。

### 3.2 SPREAD 制約

Schaus, Deville, Dupont, Régin, *Simplification and Extension of the SPREAD Constraint* は平均・標準偏差・各変数の範囲から制約伝播を行う。2006年ワークショップ収録版を確認した。[CPAI 2006 proceedings、本文冊子pp.77–91／PDF pp.83–97](https://www.cril.univ-artois.fr/~lecoutre/compets/CPAI2006a.pdf)。同題資料が2007年扱いでも検索されるため、閲読版は2006年と明示する。

本文の定義は平均と標準偏差の値を結びつける。ただし提示アルゴリズムの中心は、分散上限を用いた領域削減と、最小分散・最大分散の境界計算である。§6 は異なる変数範囲についての最大分散の扱いを論じる。今回の共通範囲[0,1]、二つのブロック和固定、正確な二乗和という特殊化に、記載アルゴリズムがそのまま今回の区間の合併式を与えるとは確認できなかった。

後続の Schaus, *Bound-consistent spread constraint* (2014) は整数領域での bound consistency を扱う。[出版社の概要](https://link.springer.com/article/10.1007/s13675-013-0018-8)。**今回は概要のみ確認、全文未読。**

Ek, Schutt, Stuckey, Tack, *Explaining Propagation for Gini and Spread with Variable Mean*, CP 2022 は可変平均と分散上限の伝播器・説明生成を扱う。[公式概要と書誌](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CP.2022.21)。**概要を確認。全文PDFの取得は成功せず、定理一致の除外はしていない。**

### 3.3 区間データの統計量

Ferson et al., *Exact Bounds on Finite Populations of Interval Data*, Reliable Computing **11**, 207–233 (2005) は各データが別々の区間にある場合の分散範囲等を扱う。[出版社概要](https://link.springer.com/article/10.1007/s11155-005-3616-1)、[著者所属機関の書誌](https://scholarworks.utep.edu/cs_techrep/342/)。**概要のみ確認、全文未読。** 一般的な異種区間での分散最大化の難しさは既知であり、今回の等幅・等上限の特殊性を失う拡張は別問題となる。

Kamali, Longpré, Koshelev, *Estimating Mean under Interval Uncertainty and Variance Constraint*, UTEP report (2010) は、区間データと分散上限から平均の範囲を計算する。[原稿PDF](https://www.cs.utep.edu/vladik/2010/tr10-29.pdf)。要旨と問題設定を読んだ。固定分散等式の下で部分和に穴が開く問題とは、少なくとも明記されたモデルが異なる。

**現在の分類：** 完全可能集合は既知のブロックごとの二乗和最小・最大値と連続補間の組合せとして、既知結果の明示的な系である。同じ合併区間式の出版例は今回の検索では同定できなかった。「見つからない」ことを新規性の肯定には使わない。

## 4. 探索した別表現と保留

| 探索系列 | 狙い | 今回の状態 |
|---|---|---|
| fixed sum / sum of squares / subset / partial sum / mean variance feasible region | 直接の定式化 | 完全な同一定理を未同定 |
| SPREAD constraint / variance maximization / bound consistency | 制約プログラミング | 上記一次資料に到達。2014/2022本文の照合が残る |
| index of coincidence / maximum probability / min entropy / purity | 総和1への換言 | Rastegin 2023 Theorem 1 と丸め評価の一致を確認 |
| event probability / collision probability / partial probabilities | 固定部分和の換言 | Rastegin 2024 Theorem 2 と下側境界が対応 |
| hypersimplex / binary rounding / error bound | 整数総和の幾何 | 主丸め上限そのものの同一記載は未同定 |
| idempotency defect / trace norm / density matrix / Fantope | 固有値への換言 | 検索結果は多いが、今回の鋭い式と同一の一次定理は未同定 |
| finite populations / interval data / variance constraint | 不確実集計 | 一般的な先行研究を確認、全文照合の未完が残る |

別候補である不偏丸めの比較対象として、*Dimension-Free Correlated Sampling for the Hypersimplex* (ITCS 2026, arXiv:2511.13573) と *Constant-Stretch Rounding on the Hypersimplex* (arXiv:2606.00996) が見つかった。[前者の公式本文](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/html/LIPIcs.ITCS.2026.104/LIPIcs.ITCS.2026.104.html)、[後者書誌](https://arxiv.org/abs/2606.00996)。**今回の中心命題には用いておらず、後者は本文未読。** 全探索成果の不偏丸め部分を将来見直す際には照合対象に含める。

## 5. 第2版へ反映する推奨文言

> 部分和の完全可能集合を、既知の二乗和境界から構成的に導出した。丸めの鋭い上限については、総和1の場合が Rastegin (2023), Theorem 1 の高純度枝と一致し、一般の整数総和の場合も同定理と初等的な集約から得られることが判明した。従ってこれらを新規の独立不等式とは主張せず、既知理論の明示的な系・用途への具体化として扱う。非整数総和や頑健化などの追加結果は、それぞれ別個に新規性照合を要する。

この分類は数学的正しさの評価とは別である。Lean 等による証明が成功しても、その事実だけで学術的新規性を支持することにはならない。

## 6. 追加照合：非整数総和と順位間隔

追加対象は降順列 \(x_1\ge\cdots\ge x_n\in[0,1]\)、\(S=m+r\)、\(0<r<1\)、\(E=m+r^2-Q\) に関する候補

\[
x_m-x_{m+1}\ge\sqrt{\max\{(1-r)^2-2E,0\}},\qquad
x_{m+1}-x_{m+2}\ge\sqrt{\max\{r^2-2E,0\}}.
\]

それぞれ添字が存在する場合に限る。本節は文献上の対応に関する監査であり、全Eでの鋭さ・等号条件・頑健版の適用条件の独立証明監査は別担当とする。

### 6.1 新たに確認した最も近い決定論的統計文献

Agnieszka Goroncy and Tomasz Rychlik, *How deviant can you be? The complete solution*, Mathematical Inequalities & Applications **9** (2006), 633–647。[出版社PDF](https://files.ele-math.com/articles/mia-09-57.pdf)。§1、§2 Theorem 1 と定式化を本文確認した。

この論文は任意の実数標本の平均と絶対中心モーメントを用い、順序統計量の線形結合の鋭い決定論的境界を論じる。固定された外部の箱[0,1]を課したモデルではない。pp.636–637 は、標本全range以外の順位差について0という下限を一般には改善できない旨を先行研究 Fahmy–Proschan (1981) に帰属している。

**今回の公式と矛盾しない。** 箱制約がなければ分散をほかの座標へ逃がせる。共通箱と最大分散近傍を要求する今回の前提では、その自由がなくなる。したがって当該論文の一般性という題名だけから、今回の正の順位間隔を既知と認定してはいけない。一方で、決定論的な順位差をモーメントから制御する問題自体は十分な先行蓄積がある。

Fahmy–Proschan, *Bounds on Differences of Order Statistics*, American Statistician **35** (1981), 46–47, DOI [10.2307/2683585](https://doi.org/10.2307/2683585) は、今回、原論文の全文を取得していない。上記Goroncy–Rychlikが引用する先行研究として記録し、原論文の定理確認済みとは扱わない。

### 6.2 整数総和と端の非整数例は既知の系

整数総和s、D<1/2では、第2節の丸め評価から

\[
x_s-x_{s+1}\ge1-\|x-z\|_1\ge\sqrt{1-2D}
\]

が直ちに従う。第2節のRasteginへの還元を踏まえると、この整数総和の順位間隔も、独立した新規不等式としては扱わない。

\(m=0\)、\(S=r\) の場合は、\(p_i=x_i/r\) にRasteginの高純度枝を適用し、\(p_2\le1-p_1\) を使うだけで

\[
x_1-x_2\ge r\sqrt{\max\{2Q/r^2-1,0\}}
=\sqrt{\max\{r^2-2E,0\}}
\]

を得る。もう一方の端 \(m=n-1\) は補数 \(1-x_i\) を同様に正規化する。**非整数であっても、この端の2例は既知定理からの直接の系である。** 内部の一般mに対する2本の順位間隔を全て同じ方法で帰属したわけではない。

### 6.3 行列の近射影性からgapを推定する既存の実例

Emanuel H. Rubensson and Anders M. N. Niklasson, *Accelerated density matrix expansions for Born–Oppenheimer molecular dynamics*, arXiv:1302.7292v1 (2013), §5.1。[一次本文](https://arxiv.org/html/1302.7292v1)。§3〜5、特に固有値推定の式と条件を確認した。

密度行列の反復的なpurificationにおいて、\(v_i=\|X-X^2\|_F\) と \(w_i=\operatorname{Tr}(X-X^2)\) を利用し、0側・1側の固有値に \((1\pm\sqrt{1-4v_i})/2\) 型の境界を与えてHOMO/LUMOを推定する。所定の収束域条件と0.5のどちら側かという情報も用いる。

今回のEまたは \((D,|S-s|)\) から直接出す順位間隔の式とは異なる。この文献を『今回の鋭い式が既知』という根拠にはしていない。一方、**固有値分解をせずに近射影性を使って重要な順位境界を推定する用途は既に存在する**。行列版を応用として論じる際の、具体的な比較対象になる。

Wolkowicz–Styan, *Bounds for eigenvalues using traces* (1980), [出版社概要](https://www.sciencedirect.com/science/article/pii/002437958090258X) も近接分野である。今回は原著全文未読。後続 R. Sharma and M. Pal, *Note on bounds for eigenvalues using traces*, Operators and Matrices **16** (2022), 759–773, [出版社PDF](https://files.ele-math.com/articles/oam-16-54.pdf) の導入を確認したが、今回の床関数・箱制約を含む順位間隔との同一対応は確認していない。

### 6.4 今回の限定的な結論

追加照合では deterministic spacings、sample mean/variance、rank gap、majorization、purity/eigenvalue gap、idempotency error、density matrix purification の系列を調べた。確率的な順位差の期待値境界、ランダム行列のgap確率、物理的Hamiltonianのスペクトルギャップは、前提が異なるため直接の一致根拠には使わなかった。

一般内部mについての2本の平方根公式と、その正の域の最良性を同時に記した一次文献は、今回の時間を区切った探索では未同定である。**独立導出した具体的な系の候補として残し、新規性は未確定とする。** 頑健版 \(x_s-x_{s+1}\ge\sqrt{\max\{1-2\delta-\eta^2,0\}}\) も同じく未同定だが、\(\delta,\eta\) の実現可能域と等号条件が確定するまでは『全パラメータで鋭い』などと主張しない。
