# Fable レビュー後の文献照合：near-idempotency と順位ギャップ

調査日：2026 09 09。短時間の一次資料照合であり、網羅的な優先権調査ではない。

## 結論

Fable の「density-matrix purification の文献も調べるべき」という指摘は妥当。Tr(X−X²) やノルムを用いた固有値評価は明確な先行研究がある。一方、今回読めた箇所では、整数 s と e=Tr X−s を使う **2D+e²+g²≥1**、および **|e|≤η の下の三分岐の鋭い最小ギャップ**と同じ主張を確認していない。「未発見」は今回の探索結果にとどまり、新規性の証明にはならない。

## 1. Rubensson–Rudberg–Sałek 2008

Emanuel H. Rubensson, Elias Rudberg, Paweł Sałek, *Density matrix purification with rigorous error control*, Journal of Chemical Physics **128**, 074106 (2008), DOI **10.1063/1.2826343**。

- [出版社の論文ページ](https://pubs.aip.org/aip/jcp/article-abstract/128/7/074106/921519)
- [研究グループの業績一覧](https://ergoscf.org/publications.php)

実在と概要を確認。小さい行列要素の除去に伴う前進誤差を、固有値の誤差と占有不変部分空間の誤差に分け、後者を canonical angles で制御する研究。内部固有値の計算法も扱う。**本調査では全文を取得できず、個々の定理と今回の式の同一性は未判定。** 書誌の存在だけをもって、今回の式が既出とも新規とも判断しない。

## 2. Rubensson–Niklasson 2013：具体的に読めた関連式

Emanuel H. Rubensson, Anders M. N. Niklasson, *Accelerated density matrix expansions for Born-Oppenheimer molecular dynamics*, arXiv:1302.7292v1。

- [著者によるプレプリント本文](https://arxiv.org/pdf/1302.7292)
- [書誌・版情報](https://arxiv.org/abs/1302.7292)

本文 §5.1、印刷ページ 9–11（PDF の第9–11ページ）、式 (6)–(16) を照合した。A=X−X²、0≤X≤I とすると、式 (13) は

\[
\frac{\|A\|_F^2}{\operatorname{Tr}A}\leq\|A\|_2
\]

（分母非零の場合）。v=||A||F<1/4 なら、式 (14) は

\[
\left[\tfrac12-\sqrt{\tfrac14-v},\ \tfrac12+\sqrt{\tfrac14-v}\right]
\]

を固有値のない区間として記述する。端点の厳密な扱いは以下の注を参照。その後、反復中の HOMO/LUMO が 1/2 の両側にあることを保証する追加条件 (16) を使う。

**比較。** これは残差ノルムからの中央スペクトル分離であり、trace の整数ずれ e と指定順位 s を組み込む今回の最適化問題とは条件・入力が異なる。同じテーマの重要な関連先行例として追記するのが適切。

**本調査での数学的注。** v≥||A||2 だけから直接保証されるのは上式の**開区間**に固有値がないこと。例えば diag(λ,0) の λ(1−λ)=v なら端点に固有値がある。文献の閉区間表記を自分の定理として転載しない。今回の比較文では「中央の開区間を除外する評価」と書くのが安全。

## 3. Kruchinina–Rudberg–Rubensson 2015/2016

Anastasia Kruchinina, Elias Rudberg, Emanuel H. Rubensson, *Parameterless stopping criteria for recursive density matrix expansions*, arXiv:1507.02087v3（v1: 2015 07 08、v3: 2016 06 30）。

- [本文](https://arxiv.org/html/1507.02087v3)
- [版情報](https://arxiv.org/abs/1507.02087)

導入部は、Tr(X−X²) や行列ノルムを停止条件に使う既存研究を明示する。定理1（PDF 第8ページ、式 (2.6)–(2.8)）は、連続 f:[0,1]→[0,1] に対する ||f(X)−f(X)²||2 / ||X−X²||2^q の最適な係数をスカラー最適化から得るもの。今回の隣接順位ギャップの定理ではない。

この研究系列は用途の説明と「既知の near-idempotency 評価」を示す出典に使えるが、今回の全結果の先行性を一括して示す出典にはならない。

## 4. Rastegin 2023 の帰属

Alexey E. Rastegin, *Uncertainty relations in terms of generalized entropies derived from information diagrams*, arXiv:2305.18005v1。

- [定理1を含む本文](https://arxiv.org/html/2305.18005v1)
- [PDF](https://arxiv.org/pdf/2305.18005)

定理1・式 (30)(31)（PDF 第5ページ、証明は第6–7ページ）は、I=Σp_j² と p_max の鋭い上下界を明示する。I∈[1/2,1] の下側境界は

\[
p_{\max}\geq\frac{1+\sqrt{2I-1}}2.
\]

本文は右側の上界を既存文献 [38] に帰属し、左側を証明する。ただし高純度枝そのものの最初の発見者を、これだけから確定できない。従って本稿では **「Rastegin (2023), Theorem 1 に明示されている初等的な最大確率–純度境界」**または**「同定できた先行記述の一つ」**と書き、「Rastegin が初めて発見した」「Rastegin に全結果が帰着する」とは書かない。

高純度枝は、p=p_max、I≤p および I≤p²+(1−p)² から直接導けるため、元の順位ギャップ証明のうちこの枝だけを独創的な核心として扱うべきではない。

## 原稿への短い追記案

日本語：

> 近似射影行列の残差 Tr(X−X²) やそのノルムから固有値情報を得る研究は、density-matrix purification の分野に先行例がある。Rubensson–Niklasson (2013), §5.1 は trace と Frobenius norm を使った評価を具体的に与える。今回の調査では、trace の整数ずれを含む本稿の鋭い隣接順位ギャップ式および頑健な三分岐最小値と同一の記述を確認していないが、優先権は未確定である。Rubensson–Rudberg–Sałek (2008) は概要のみ照合でき、全文の確認が残る。

English:

> Earlier work on density-matrix purification extracts spectral information from the residual Tr(X−X²) and its norms. Rubensson–Niklasson (2013), §5.1 gives explicit trace and Frobenius-norm estimates. Our limited search has not identified the same sharp adjacent-rank inequality with an integer trace offset, or the same three-branch robust minimum; priority remains unresolved. We verified the abstract of Rubensson–Rudberg–Sałek (2008), but a full-text comparison remains outstanding.

## 検索範囲の記録

主要検索語：

- Rubensson Rudberg Salek 2008 purification error control eigenvalue bounds trace density matrix
- "Density matrix purification with rigorous error control"
- "idempotency" "trace" "eigenvalue bounds"
- "eigenvalue gap" "trace" "idempotent"
- "Tr(X-X" "gap" bound
- "2305.18005" Rastegin

関連性の低い検索結果は根拠に使わず、上記4本の著者原稿・出版社情報を中心に照合した。1990年代までの引用文献の全文追跡、数学の order statistics / bounded moment problem 全域の調査は行っていない。

## T9 に関する最小限の追加検索

一般分類の導出後、`hypercube slab "connected components" concave quadratic` と `"thermodynamic tree" "quadratic" polyhedron components` を追加検索した。同一の成分数公式を記す一次資料はこの2検索では同定できなかった。この小さい検索範囲では優先権判断はできず、T9は既知の凸障害物・多面体グラフ理論の明示的な系として扱う。
