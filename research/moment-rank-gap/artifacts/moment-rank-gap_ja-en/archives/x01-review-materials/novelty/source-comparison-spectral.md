# X01 公開前監査：スペクトル・近似射影の先行研究

調査日：2026 09 09。担当範囲：指定順位ギャップ T1 と頑健帯の鋭い最小値 T2。検索による先行例未同定を新規性の確定としない。

## 判定

一般の内部順位についての

\[
2\operatorname{Tr}(X-X^2)+(\operatorname{Tr}X-s)^2+
(\lambda_s(X)-\lambda_{s+1}(X))^2\ge1,
\quad 0\preceq X\preceq I,
\]

および \(|\operatorname{Tr}X-s|\le\eta\le1/2\) を課した三分岐の最小ギャップについて、**今回照合した一次資料には同一の定理を同定できなかった**。ただし、その証明に使う凸性・集約・スカラー二次不等式は既知の道具である。独立した未知の原理や研究上の大きな新規性を示す根拠はない。

特に s=1 の T1 は \(g_1^2\ge 2Q-S^2\) に簡約する。親担当が確認した Rosenberg–Jakobsson (2008), Theorem 1(ii) の最大確率–同型接合度境界から直接導かれるため、この部分は新規候補から外す。一般内部順位・整数ずれを含む形の先行性とは分けて記す。

## 1. Wolkowicz–Styan (1980)：本文照合済み

Henry Wolkowicz and George P. H. Styan, *Bounds for eigenvalues using traces*, Linear Algebra and its Applications **29**, 471–506 (1980), DOI 10.1016/0024-3795(80)90258-X。

[著者の大学サイトにある全文 PDF](https://www.math.uwaterloo.ca/~hwolkowi/henry/reports/bndseigs80.pdf)

第2節の主要定理を直接照合した。

- Theorem 2.1, (2.2)–(2.3), pp.474–475：平均 \(m=\operatorname{Tr}A/n\) と固有値標準偏差から両端固有値を評価する。
- Theorem 2.2, (2.19), (2.22), pp.477–478：指定順位・順位区間平均の上下界。
- **Theorem 2.4, (2.40), p.482：\(\lambda_k-\lambda_l\) の上界。** 今回必要なのは小さい射影残差に基づく指定順位間の下界であり、方向・仮定が異なる。
- Theorem 2.5, pp.483–484：spread \(\lambda_1-\lambda_n\) の上下界。全幅の下界から特定の内部ギャップの下界は直接には得られない。

この論文を「同じ隣接ギャップ下界が既出」の根拠として引用することはできない。一方、「trace と trace-square から固有値情報を得る」一般的テーマの重要な先行研究である。

同年続編 *More bounds for eigenvalues using traces*, LAA **31**, 1–17, [著者配布全文](https://www.math.uwaterloo.ca/~hwolkowi/henry/reports/morebnds80.pdf) も確認。主として複素固有値の実部・虚部の二乗和評価を強める研究で、内部順位ギャップの T1・T2 と同じ主張を確認しなかった。

## 2. Sharma–Pal (2022)：本文照合済み

Rajesh Sharma and M. Pal, *Note on bounds for eigenvalues using traces*, Operators and Matrices **16**(3), 759–773 (2022), DOI 10.7153/oam-2022-16-54。

[出版社全文 PDF](https://files.ele-math.com/articles/oam-16-54.pdf)

Theorem 5, (3.3), p.767 は、昇順固有値と \(B=A-(\operatorname{Tr}A/n)I\) に対し

\[
\sum_{i=n-k+1}^{n}\lambda_i-
\sum_{i=1}^{k}\lambda_i
\ge 2\sqrt{\frac{k(n-k)}{(n-1)n}\operatorname{Tr}B^2}
\]

を与える。これは **上位 k 個の和と下位 k 個の和の差**であり、\(\lambda_s-\lambda_{s+1}\) の下界とは別。Theorem 2 と Corollary 1 は対応する部分集合平均の分散評価。その他の主要結果は trace-inverse 等を使う固有値評価である。T1・T2 と同一の公式は確認しなかった。

なお、同名の Sharma–Kumar–Saini (2014), [arXiv:1409.0096](https://arxiv.org/pdf/1409.0096) は別論文。Theorem 2.2, (2.11)–(2.13) と隣接差を扱う Corollary 2.3 は**上界**であり、2022 論文と混同しない。

## 3. Density-matrix purification 系列

### Rubensson–Rudberg–Sałek (2008)：依然として本文未照合

*Density matrix purification with rigorous error control*, J. Chem. Phys. **128**, 074106 (2008), DOI 10.1063/1.2826343。

[出版社](https://pubs.aip.org/aip/jcp/article/128/7/074106/921519/Density-matrix-purification-with-rigorous-error)、[PubMed](https://pubmed.ncbi.nlm.nih.gov/18298139/)、[研究グループ業績一覧](https://ergoscf.org/publications.php)。

出版社の本文 URL は今回のアクセスでは要旨と参考文献に転送された。大学機関リポジトリの論文記録と著者学位論文も検索したが、DiVA の自動アクセス確認画面等により論文全文を取得できなかった。**論文の存在・要旨は確認できたが、個々の式の一致／不一致は未判定。** 検索エンジンの断片に本文の記述があっても、全文を読んだとは扱わない。

### Rubensson–Niklasson (2013/2014)：比較対象が明確

[2013 プレプリント全文](https://arxiv.org/pdf/1302.7292)、研究グループ一覧では出版版を *Interior eigenvalues from density matrix expansions in quantum mechanical molecular dynamics*, SIAM J. Sci. Comput. **36**, B147 (2014) と記載している。

前回照合済みの §5.1、(13)–(16) は \(A=X-X^2\) の trace と Frobenius norm を使い、残差のスペクトルノルムを評価して中央の固有値のない区間を得る。この残差ノルムによる分離と、整数 s に対する trace のずれを入力とする T1・T2 は仮定が違う。

\(\|A\|_2\le v<1/4\) のスカラー帰結として確実なのは
\((\frac12-\sqrt{\frac14-v},\frac12+\sqrt{\frac14-v})\) という**開区間**の除外である。端点を含めた除外を自分の主張として転載しない。

### Kruchinina–Rudberg–Rubensson (2015/2016)

[Parameterless stopping criteria for recursive density matrix expansions](https://arxiv.org/html/1507.02087v3)、Theorem 1, (2.6)–(2.8)。行列関数の反復における射影残差ノルムの収束係数を扱う。指定順位の三分岐最小ギャップではない。近似射影からスペクトル情報を得る応用分野として引用できる。

## 4. 公開原稿への判定文案

> Trace と二次 trace から固有値を評価する先行研究、および density-matrix purification における残差による固有値評価がある。最大確率に関する部分は既知境界の系である。一方、今回照合した資料では、指定した内部順位と trace の整数ずれを同時に含む不等式、および trace 誤差帯での三分岐最小値と同一の記述は同定できなかった。これらを初等的な導出・最適定数の整理として提示するが、新規性・優先権は主張しない。2008 年の関連論文一本は本文の式照合が未完了である。

## 5. 検索範囲と限界

今回の担当では exact-title、eigenvalue gap / trace / positive semidefinite、HOMO/LUMO / trace bounds、idempotency / trace error、adjacent eigenvalues / lower bound、bounded moments / ordered gap などの英語検索を約40クエリ実施し、上記の一次資料を選別した。検索結果の件数は網羅性を保証しない。Wolkowicz–Styan と Sharma–Pal の具体的定理照合は進んだが、2008 purification の全文未取得という前回の限界は残った。追加の検索で同じ式が出なかったことだけを、未知定理が得られた積極的証拠にしてはいけない。
