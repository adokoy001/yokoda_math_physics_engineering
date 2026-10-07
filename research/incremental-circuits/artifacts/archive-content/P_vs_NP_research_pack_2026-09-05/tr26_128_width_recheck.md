# TR26-128 の width 記載：2026-09-05 現行版再照合

対象：Cavalar–de Rezende–Gray–Santhanam, *ETH-Hardness of Learning Monotone Circuits and Approximating Their Size*。旧主ノート §30.4 の指摘を、現行公開版の Theorem 3.5、Corollaries 3.6–3.7、Appendix B に限定して再監査した。元ノートは編集していない。

**結論：三つの公開版で外側指数の記載は残っている。Appendix B の提示された推論は、その外側指数を導かない。ただし、旧ノートの「width ≤ 変数数だから直ちに反証」という議論には、対象の Ref formula が UNSAT であるという追加前提が必要である。今回は headline theorem 全体の真偽を判定しない。**

## 1. 現行版の確認

| 公開先 | 2026-09-05 に確認できた版 | 限定照合結果 |
|---|---|---|
| [ECCC TR26-128](https://eccc.weizmann.ac.il/report/2026/128/) | 掲載記録 2026-07-22、公開 2026-07-26。別 revision の掲載なし。現行 download は 38 ページ | Theorem 3.5 と Corollaries 3.6–3.7 に外側指数。Appendix B は後述の線形幅の鎖 |
| [arXiv:2607.12331](https://arxiv.org/abs/2607.12331) | 提出履歴は 2026-07-14 の v1 のみ。PDF は 39 ページ | 同じ式。HTML の数式でも確認したため、PDF の文字抽出だけの誤りではない |
| [正式 CCC 2026 版](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2026.40) | LIPIcs 383, 40:1–40:25 | 40:15 の Theorem 3.5、40:16 の Corollary 3.6、40:17 の Corollary 3.7 に同じ外側指数。短縮版であり、Appendix B の詳細は full version と照合 |

「修正済みの版を旧ノートが見落としていた」という証拠は、これらの公開先では確認できなかった。未公開改訂や著者による補足の存在・不存在は判定していない。

## 2. 記載式と Appendix B の推論を分離する

以下で \(H=\mathsf{Ref}_d^G(F)\)。\(n\) は元の 3-CNF \(F\) の変数数であり、\(H\) の変数数ではない。

| 箇所 | 現行版の記載 | Appendix B の示す鎖から得られる下界 |
|---|---|---|
| Theorem 3.5(4) | \(2^{\Omega(r(c-1)/n)}\) | \(\Omega(r(c-1)/n)\) |
| Corollary 3.6(4)：complete bipartite graph | \(2^{\Omega(t/n)}\) | \(\Omega(t/n)\) |
| Corollary 3.7(4)：random expander | \(2^{2^{\Omega(n/d)}}\) | \(2^{\Omega(n/d)}/\operatorname{poly}(n)\) 型 |

上表の「記載」は [正式 CCC PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol383-ccc2026/LIPIcs.CCC.2026.40/LIPIcs.CCC.2026.40.pdf) と [arXiv HTML §3.2](https://arxiv.org/html/2607.12331v1#S3.SS2) による。右列は著者の改訂定理ではなく、以下の式からの監査上の帰結である。

[full version Appendix B](https://arxiv.org/html/2607.12331v1#A2) の三要素は次の通り。

\[
\mathsf{ResWidth}(\mathrm{rPHP}(G))\geq (c-1)r/2
\qquad\text{(Theorem B.1)},
\]

\[
F_0\leq_q H_0\ \Longrightarrow\
\mathsf{ResWidth}(F_0)\leq q\,\mathsf{ResWidth}(H_0)
\qquad\text{(Lemma B.3)},
\]

\[
\mathrm{rPHP}(G)\leq_{O(n)}H
\qquad\text{(equation (11), B.4)}.
\]

B.4 は出力ビットごとの decision-tree depth を \(O(n)\) と結論しており、幅の指数変換を追加していない。従ってこの鎖の合成は

\[
\frac{(c-1)r}{2}\leq Cn\,\mathsf{ResWidth}(H)
\quad\Longrightarrow\quad
\mathsf{ResWidth}(H)\geq\frac{(c-1)r}{2Cn}.
\]

外側に \(2^{(\cdot)}\) を付ける推論は存在しない。complete graph では \(r=t/2,c=2\)。random expander の使用では \(t=2^{n/d}\)、\(r=\Omega(\sqrt t)\) 型となり、同じ計算で右列の下界となる。この点について、旧 §30 の「記載された証明鎖が指数幅を支えない」という診断は維持される。

## 3. 旧監査側にも必要な修正：UNSAT 前提

\(V\) 変数の **UNSAT** CNF \(H\) については、Resolution の完全性から \(\mathsf{ResWidth}(H)\leq V\) である。しかし \(H\) が SAT なら refutation は存在しない。「すべての refutation は大きな幅を持つ」という文は空虚に真となり得る。幅を \(+\infty\) と拡張する流儀でも、上記の有限上界は適用されない。

元の \(F\) の UNSAT 性だけから \(\mathsf{Ref}_d^G(F)\) の UNSAT 性は一般には出ない。論文 §3 は Ref を指定構造の refutation の存在を表す式として構成している。例えば complete graph、\(d=1,t=2\)、\(F=(x_1)\land(\neg x_1)\) を考えると、各 root pointer をその assignment により偽になる単位節の leaf に向ければ、二つの leaf で Ref を満たす割当てを構成できる。leaf の summary と unlit をその単位節に合わせれば Ref-1–Ref-8 を満たし、3-CNF splitting は充足可能性を保存する。変数数は必要なら tautological padding で増やせる。この例は、対象 Ref の UNSAT 性を省略できないことを示す。

従って、旧 §30.4 の「後者は width ≤ V に反し、文字通りには偽」という一文と、「三つの定理を記載どおりは反証」と一括する分類は、今回の限定照合だけでは維持しない。厳密な反証には、該当 parameter で Ref が UNSAT になる入力族を明示し、その族における変数数上界と幅下界の矛盾まで示す必要がある。この追補ではそこまでの追加定理は証明していない。

一方、Appendix B が掲げた結論をその記載推論で導けていないという指摘は、この UNSAT 前提の補足とは独立に成立する。

## 4. 研究台帳に採用する状態

- **確定：** 2026-09-05 に取得した ECCC、arXiv v1、正式 CCC 版すべてに同じ外側指数がある。
- **確定：** Appendix B の B.1、B.3、(11) の合成が与えるのは線形の \(\Omega(r(c-1)/n)\) 下界である。記載された指数幅への推論は支持されない。
- **修正：** 変数数による直接反証には Ref の UNSAT 性を明記する。今回、それを全 parameter で証明したとは扱わない。
- **保留：** width の自然な修正で rETH / ETH の各 headline が完全に再証明できるか。今回の限定照合では、独立に再証明した定理として登録しない。
- **維持：** この論文は small monotone circuit から短い explicit Resolution proof を取り出す reverse compiler を与える、と解釈してはいけない。width 表記の修正があっても、その未証明 bridge は埋まらない。

推奨する短い台帳表現は「**現行公開三版で width 記載と Appendix の導出に未解消の不整合を再確認。主結果の反証とは区別して保留**」。著者への連絡・外部への誤り告知は行っていない。
