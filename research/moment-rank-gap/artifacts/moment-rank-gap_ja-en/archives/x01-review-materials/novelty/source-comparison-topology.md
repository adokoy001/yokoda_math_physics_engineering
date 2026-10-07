# X01 位相部分の先行研究・新規性監査

調査日: 2026 09 09。対象: T6 の非整数和・成分分類、T8 の穴の具体例、T9 の広い帯の成分分類。これは公開前の限定的な一次資料照合であり、優先権の確定調査ではない。

## 判断

**T6・T9 を支えるグラフ還元は既知である。T9 の「劣位集合が大きくなる途中で新しい島が生まれ、成分数が増える」という現象も既知の文献に明示されている。** 今回、X01 と同一の箱帯・二次関数についての閾値と二項係数による閉形式は見つからなかった。しかしこれは新規性確認ではなく、同一陳述の先行文献未特定という状態である。

公開時の適切な地位は、**「既知の凸幾何の方法を具体的なモーメント制約へ適用し、閾値・成分数・一つの穴の変化を明示的に計算した研究ノート」**。独立した一般位相定理の発見とは呼ばない。

## 1. 最も近い既知の一般結果: Gorban

A. N. Gorban, *Thermodynamic Tree: The Space of Admissible Paths*, SIAM Journal on Applied Dynamical Systems 12(1), 246–278 (2013), DOI 10.1137/120866919。

- [出版社](https://epubs.siam.org/doi/abs/10.1137/120866919)
- [著者版 PDF: arXiv:1201.6315v3](https://arxiv.org/pdf/1201.6315)
- 以下のページは著者版 PDF の印刷ページ。版の公開日は 2012 07 24、出版年は 2013。

| 箇所 | 確認した内容 | X01 との関係 |
|---|---|---|
| Lemma 2.1, p.11 | 凸多面体から凸集合を除いた任意の点は、除外集合を避ける直線である頂点に到達できる | 頂点へのアクセスの一般原理は既知 |
| Proposition 2.4, p.13 | 凸集合と交わる頂点・辺を削除したグラフと、多面体の補集合の道連結成分が対応 | T6・T9 の直接の一般原理 |
| Lemma 3.2, pp.18–19 | 狭義凸関数の超位集合と等位集合の道連結成分が対応 | 固定和・固定二乗和の T6 で超位集合から等位集合へ移る部分 |
| §4.2, pp.26–27, Fig.4.5 | 閾値を下げて集合を増大させる途中で、辺につながらない新しい頂点が現れ成分数が再び増える具体例 | T9 の非単調性という現象自体にも先行例がある |

旧 HTML 引用の「Proposition 7」「Lemma 14」は平坦化された番号と考えられる。現在確認した原 PDF では **Proposition 2.4 / Lemma 3.2**。公開引用では原 PDF の番号とページを併記すると追跡しやすい。

原文の確認範囲: §2 の主要補題・命題、§3.1–3.3、§4 の例の陳述・図キャプション、導入の例を確認。全 PDF の cube / sphere / tetrahedron の文字列検索も実施し一致なし。§4 の具体例は化学組成の単体・台形・水素酸素系であり、X01 の箱帯の同一閉形式は確認できなかった。全文の全証明・参考文献までの完全精読ではない。

## 2. T9 の既知結果への還元と残る個別計算

対象は
\[
P=\{x\in[0,1]^n:s-\eta\le\textstyle\sum_i x_i\le s+\eta\},\qquad
F_\delta=\{x\in P:D(x)\le\delta\},\quad D(x)=\sum_i x_i(1-x_i),
\]
\(n\ge2,1\le s<n,1/2<\eta<1\)。ここで
\[
U=\{x\in P:D(x)>\delta\}
\]
は凸集合なので、Gorban の Proposition 2.4 がそのまま適用される。この同定は本監査で行った推論であり、Gorban がこの P,D を扱ったという意味ではない。

X01 で残る仕事は次の有限計算である。

1. 二値和 s の B 頂点、下側の L 頂点、上側の U 頂点を列挙する。
2. B の値は 0、L/U の値は \(k=\eta(1-\eta)\)。全頂点は \((n+1)\binom ns\) 個。
3. 頂点間の辺上で D の最大値を計算する。成分数に関係する値は \(c=(1-\eta^2)/2\)、\(h=1/4\)。より遅い辺はすでに全体が連結した後に現れる。
4. 各閾値区間のグラフを数える。

こうして得られる
\[
\binom ns\longrightarrow(n+1)\binom ns\longrightarrow
\begin{cases}
\binom n{s-1}+\binom ns+\binom n{s+1}&c<h,\\
\binom ns&h<c
\end{cases}
\longrightarrow1
\]
という閉形式は、今回の検索で同一の先行陳述を特定できなかった。

**新規性候補の範囲はこの明示計算・整理に限定する。** 「成分数の非単調性の初発見」「凸多面体から球を除く新理論」「一般次元で初めて位相を分類」といった文言は過大である。

## 3. T6 の非整数和の分類

\(S=m+r,0<r<1\) とし、\(P_S=\{x\in[0,1]^n:\sum_i x_i=S\}\)。\(Q=\sum_i x_i^2\) は狭義凸であり、\(Q\ge m+r^2-E\) の成分は同じグラフ原理で調べられる。等号集合へは上記 Lemma 3.2 が使える（最小 Q の退化点は別に扱う）。

頂点 \((1^m,r,0^{n-m-1})\) の順列は \(\binom nm(n-m)\) 個で、隣接する r と 0 の交換、1 と r の交換の二種類の辺があり、二乗和の損失はそれぞれ \(r^2/2\)、\((1-r)^2/2\)。この二種類を数えることから出る二項係数の段階分類についても、同一陳述の先行文献は今回未特定。

なお、この非整数切断多面体を、整数和の通常の hypersimplex と同一視してはいけない。頂点の座標に r があり、例えば n=4,m=1 は 12 頂点の切頂四面体になる。順列凸包という観点から multipermutohedron / generalized permutahedron も探索語に含めたが、同じ球面切断の位相分類を特定できなかった。

## 4. T8 の切頂四面体の穴

X01 の n=4,S=5/4 での
\[
12\text{点}\to4\text{円}\to4\text{点}\to\bigvee^3S^1\to S^2\to\text{点}
\]
というホモトピー型の列と、\(0,1/32,1/24,9/32,13/24,43/64\) の値は今回の検索で同一陳述を見つけていない。

ただし、凸多面体の面複体を利用すること、面ごとの二次関数の極値から段階的にセルが入ること、セルからホモロジーを求めることは既存の位相・凸幾何の枠内である。Gorban の Proposition 2.4 は成分数の結果なので、それだけを引用して高次ホモトピー型の全主張の出典とすることはできない。X01 独自に示した面複体への収縮・球面等位集合との対応・各セルの貼付けの証明が必要である。

近接する一次資料として、J. T. Harper, *Morse Matchings on a Hypersimplex* (2012) を確認した。[本文](https://arxiv.org/html/1211.6483v1)。Definition 2.4 は整数和の hypersimplex、Proposition 2.7 は面の記述、Theorem 6.11 は構成した Morse matching の非巡回性を扱う。X01 の二次関数による非整数断面フィルトレーションは陳述されていない。Introduction、§2、§3–4 の設定、Theorem 6.11 と説明を確認し、matching の証明全体は精読していない。引用される Harper 2011 博士論文は検索したが大学リポジトリの本文取得が失敗し、未読。

## 5. 新たに照合した近接分野

### 5.1 Power-sum map / Vandermonde fibers

J. Acevedo, G. Blekherman, S. Debus, C. Riener, *The Wonderful Geometry of the Vandermonde map*, Foundations of Computational Mathematics 26, 2005–2051 (2026), online 2025 09 22。[一次本文](https://link.springer.com/article/10.1007/s10208-025-09718-6)。

Lemma 2.12 は順序室 \(\mathcal W_n\) 内の power-sum fibers が空または連結であるという結果。Kostov・Givental・Arnold の研究を一般の非負座標へ発展させ、Theorem 2.4 は正規化したモーメント像の境界を少数の異なる座標値で特徴づける。

この論文は **順列を商として扱う順序室内の幾何**が中心であり、X01 の **座標ラベルを保つ箱帯全体**の道連結成分数と区別する必要がある。固定和・固定二乗和という対象の共通性は強いが、上限 1 の追加切断と帯を含む T9 の閉形式を直接与えるものとは確認できなかった。§2.1 の設定・Lemma 2.12–2.14・その証明、Theorem 2.4・2.27 の陳述と役割を確認。他節の全証明や同論文の全引用元は未読。

### 5.2 単体と球面の交わりの確率論

S. Chatterjee, *A note about the uniform distribution on the intersection of a simplex and a sphere*, arXiv:1011.4043v3 (2016; 初稿 2010)。[著者版](https://arxiv.org/pdf/1011.4043)。

§1、Theorems 1.1–1.3 は、正座標、固定一次・二次モーメントの集合上の一様分布を n→∞ で調べる。二次モーメントが大きい場合の最大座標への集中が主題。確率的な相転移であり、有限 n の全ての連結成分を数える X01 の分類とは区別する。PDF pp.1–4 の設定・主要定理を確認。全文で connected の文字列一致なし。全証明は未精読。

## 6. 検索の再現記録と限界

一般 Web 検索で、主に英語の次の組合せを使った（完全なデータベース検索ではない）。

- hypersimplex / sphere / connected components
- cube / sum of squares / connected components
- polytope / convex set / complement / topology
- thermodynamic tree
- power sums / fibers / topology / cube
- truncated tetrahedron / homotopy / sphere
- sphere / hypercube / intersection / sum coordinates
- hypersimplex / Morse
- polytope / ball / complement / deformation retract
- capped simplex / sphere / topology
- multipermutahedron および multipermutohedron / sphere / topology
- permutahedron / quadratic / Morse
- cube / slab / vertices / hypersimplex
- eta / 1/4 / connected components / cube
- sum / x_i(1-x_i) / components
- hypersimplex / r^2 / connected

候補のタイトル・スニペットだけで同一結果と認定していない。近接分野でも、球詰め・交叉体・複素 moment-angle manifold 等の異なる対象の結果は直接の先行定理から除外した。

未実施: MathSciNet / zbMATH / Scopus 等の包括的検索、非英語文献の網羅、Gorban 以前のロシア語文献・熱力学教科書の全追跡、Harper 博士論文の本文照合、最近の未索引原稿、専門家による優先権確認。したがって **「見つからない」を「存在しない」に変更しない**。

## 7. ブログへの説明例

> 本稿の位相解析は、凸多面体から凸集合を除いた領域の成分を辺グラフで調べる既知の方法に基づく。ここでは箱制約と一次・二次モーメント制約に適用し、閾値と成分数を明示的に計算する。広い平均許容帯では、領域を広げる途中で新しい成分が生まれる。こうした非単調性自体には既知の例がある。同一の閉形式を述べる先行文献は今回の限定調査で特定できておらず、新規性は未確定である。

この説明なら既知理論への帰属と今回の作業の具体的な内容を両立できる。
