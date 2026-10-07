# P vs NP 研究再始動：現在地、先行研究、今回の前進

作成日：2026 09 05  
状態：継続研究。P vs NP は未解決。本資料は解決の主張ではない。  
基礎資料：研究ノート v0.24、候補台帳 v0.16（ともに最終記載日 2026 08 14）。  
今回の更新：研究ノート v0.25、候補台帳 v0.17。

## 1. 今回、何が進んだか

過去の研究は、単に「3-SAT の分岐を圧縮できるか」という段階には留まっていなかった。最新版は、MCSP の逐次的な回路証人の保持、入力接頭辞への整合性、証明解析を使う証人抽出へ進んでいた。今回、その現在地を回収し、過去の主経路を時系列で分離した。

成果は次の四点である。

1. **論理の修正。** 「反証した」と「それを証明すること自体が未解決問題と同等」を区別した。Bridge-0、generic implicit-PAP、SAT 証人抽出の向きに訂正を加えた。
2. **一次文献の更新。** 2026 年の TDD、構造化回路による証明系、algebrization 障壁などを既存の論理地図へ接続した。新しい表現形式が、そのまま一般計算の下界を与えるわけではないことも確認した。
3. **構成的な補題の改善。** 辞書順の次の値を変更するための追加回路サイズを、旧 C23 の一般的な点変更より強く評価した。連続区間の変更にも線形の上界を得た。
4. **再現可能な検査。** 真理値表全数検査と、有限サイズの一般 DAG 回路の全数列挙を行った。新しい次ビット補題の二方向の境界が、それぞれ達成される小例も見つかった。

今回得た補題は初等的構成と既知結果の直接合成であり、学術的新規性は未確認である。通常計算に対する超多項式下界、P≠NP、P=NP のどれも証明していない。

## 2. 研究史と現行経路

| 段階 | 着想 | 残ったもの／止まった理由 |
|---|---|---|
| 意味的分岐圧縮 | 未来の振舞いが同じ探索履歴を合流する | 固定順・一回読みでは残余関数と OBDD の理論に対応。HWB や単調 CNF が、表現の難しさと一般計算の難しさを分離する。 |
| CCP・E-NF | 一般 P アルゴリズムから、下界を示せる表現へ正規化する | 一般 P 関数を表せないクラスへの無条件変換は失敗。SAT∈P を前提とする含意は、別途の未解決命題。 |
| MCSP 残余数 | 回路の小さい真理値表を逐次読み、状態数で下げる | YES 語が疎で、残余状態名は O(s log s) ビットで足りる。MREC は反証された。 |
| Search・WC | 各 live prefix に整合する小回路を保持・更新する | MMW の P=NP 仮定下の構成が使える。未証明なのは、通常の一様更新計算に対する下界。 |
| Prefix binding・PAP | 任意の小 completion 回路から元の SAT 証人を抽出する | 有力な還元・特徴づけの候補。ただし compiler 完成だけでは無条件の WC 下界にならない。 |

### 最小限の定義

n 変数の真理値表は、整数順と一致する辞書順で x₀,…,x₂ⁿ₋₁ と並べる。長さ i の接頭辞を u とする。回路サイズの閾値を s として、

\[
V_{n,s}(u)=\{C:|C|\le s,\ \forall j<i,\ C(x_j)=u_j\}
\]

を、u に整合する小回路の集合とする。V が空でなければ live、空なら dead と呼ぶ。

WC（witness-carrying system）は、過去の入力を再読せず状態を更新し、その状態から live 時には V 内の回路を取り出せる仕組みである。exact WC は dead 時も正しく失敗を返す。live-promise WC は live 時の正しさだけを要求するが、資源条件は別に明記する。

MMW の構成を一ビットずつ用いる旧 C20 は、固定した A∈PH と適切な s(n)≥n に対して、

\[
P=NP\Longrightarrow
\text{poly}(s)\text{ 資源の一様 exact WC が存在}
\]

を与える。保持する回路記述は O(s log s) ビットだが、更新中の総作業空間まで同じ上界とは言わない。通常計算における総作業空間・更新時間は poly(s) である。[MMW：Theorems 1.2–1.3, §2.1](https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf)

## 3. 今回の重要な訂正

### C33：Bridge-0 の条件文を反例と区別する

H を SAT∈P、Q を「全 3-CNF に、共通の多項式上界のサイズで全解集合を表す OBDD が存在する」とする。ここで 3-CNF は各節が高々 3 リテラルの式を指す。Q は既知の単調 2-CNF の下界により偽である。古典論理では、

\[
(H\Rightarrow Q)\ \Longleftrightarrow\ \neg H
\]

となる。したがって、この条件文の無条件反証を得たわけではない。この橋を証明できれば P≠NP が従い、橋を偽だと証明できれば逆に P=NP が従ってしまう。

反証済みとして維持するのは「P 時間で評価できる関数なら多項式サイズ OBDD を持つ」という一般原理である。SAT 判定器から全解表現を得るという説明の飛躍を指摘することと、SAT∈P を前件とする条件文を偽と決めることは異なる。[Bova–Slivovsky：Theorem 7](https://arxiv.org/abs/1411.5494)

**資源の型も必要。** Q を「多項式ビットの任意 CNF 表現がある」と読み替えると、元の CNF 自体が候補になり、Q が偽という議論は成立しなくなる。

### C34：NEXP の回路下界は P=NP と矛盾しないどころか、その帰結でもある

既知の easy-witness 定理は、

\[
NEXP\subseteq P/poly\Longrightarrow NEXP=MA
\]

を与える。P=NP なら PH=P、MA⊆PH より MA=P。ここに NEXP⊆P/poly を加えると NEXP=P となり、時間階層定理に矛盾する。したがって、

\[
\boxed{P=NP\Longrightarrow NEXP\not\subseteq P/poly.}
\]

これ自体は既知結果の直接合成である。NEXP⊄P/poly を得ただけで「P=NP に矛盾した」としてはならない。[Impagliazzo–Kabanets–Wigderson：§4.1](https://www2.cs.sfu.ca/~kabanets/papers/exp_journal.pdf)、[MA の PH 包含](https://www.wisdom.weizmann.ac.il/~oded/R1/bpp-ph.pdf)

さらに、

\[
\forall k\ \exists L_k\in NP:\ L_k\notin SIZE(n^k)
\]

と

\[
\exists L\in NP\ \forall k:\ L\notin SIZE(n^k)
\]

は違う。前者の言語は k ごとに変わってよい。Murray–Williams の定量的な NP 下界を、後者の NP⊄P/poly へ量化交換しない。[Murray–Williams：Theorem 1.1](https://people.csail.mit.edu/rrw/easy-witness-nqp.pdf)

### C38：証人抽出の完成と、P≠NP の証明は別の到達点

H=P=NP、W=同じ固定モデル・閾値関数における効率的な WC の存在、と置く。旧資料の NP-witness endgame は、次を目指している。

- SAT 式 φ だけから、n、閾値 s、prefix 長がすべて poly(|φ|) で、構築時間も poly(|φ|) の prefix を生成する。
- φ が SAT なら、所定サイズの completion が存在する。
- **任意の**そのサイズ内の completion 回路から、SAT 証人を poly(|φ|) 時間で抽出する。
- 入力回数、初期化、更新、取り出し、出力検証まで多項式時間に収める。

これが完成すれば、通常計算で実装された W を用いて SAT が解ける。つまり、

\[
W\Rightarrow H
\]

が得られる。しかし MMW は既に H⇒W を与えるので、同じ条件の下で得られるのは W⇔H という特徴づけである。矛盾は発生しない。

PAP compiler は、この還元を成立させる研究として価値がある。ただし compiler の完成を「WC 不存在の証明」と呼ぶことはできない。無条件の分離には、W を排除する別の正当な下界が必要である。

同様に旧 C31 の「generic implicit-PAP extractor が存在すれば P=NP」は条件付き結果として維持するが、extractor の無条件不存在を証明したとは扱わない。[Proof Analysis Problem：Theorem 1.1, Corollary 5.6](https://arxiv.org/abs/2506.16956)、[Provable Reductions in TFNP](https://arxiv.org/abs/2606.27931)

## 4. 先行研究の追加と再配置

ここでの「新しい」は、本研究への今回の追加・再照合を意味する。過去の研究時点より後に初めて発表されたものだけを指すわけではない。

| 一次資料 | 確認した内容 | 本研究への使い方 |
|---|---|---|
| [A Canonical Generalization of OBDD, SAT 2026](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SAT.2026.10) | TDD の canonical 最小化、Apply、幅を使ったコンパイル。正式版 Theorem 21 では HWB に指数サイズ下界。 | 操作が扱いやすくなっても、一般 P 関数を多項式サイズで表現できるとは限らない。旧 SSMS のモデル比較へ追加。 |
| [Proof Systems Based on Structured Circuits, SAT 2026](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SAT.2026.6) | 表現下界を、弱化なしの制限された反駁過程へ移す Theorem 13。構成された不充足式には多項式 Resolution 反駁もある。 | 最終出力が小さい場合にも過程下界を調べられる。ただし別の証明方式を排除していない。 |
| [On the Role of Canonicity in Knowledge Compilation, AAAI 2015](https://ojs.aaai.org/index.php/AAAI/article/view/9423/9282) | reduced SDD の正規化や更新での指数的なサイズ増大。固定 vtree と出力形式の条件付き。 | 「存在／更新」の隔たりを示す既知の具体例として扱う。 |
| [Complexity Classes of Equivalence Problems Revisited](https://arxiv.org/abs/0907.4775) | 完全不変量、代表元、辞書順最初の代表の差。 | canonical selector 一個の困難性から全 selector の困難性へ飛ばない。 |
| [On Oracles and Algorithmic Methods for Proving Lower Bounds：2024 訂正版](https://eccc.weizmann.ac.il/report/2024/113/) | 会議版の一定理に対する著者の erratum。 | アルゴリズムから下界への経路を、一律に非相対化と分類しない。定理と版を指定する。 |
| [New Algebrization Barriers…, ITCS 2026](https://arxiv.org/abs/2511.14038) | Missing-String の通信複雑性からの新しい障壁。 | range-avoidance を採用する場合の照合先。WC 全般を排除する定理ではない。 |

他に、知識コンパイルの Map、treewidth と DNNF、前処理とオンライン問い合わせ、HWB/SDD 分離を一次論文で照合した。詳細は同梱の literature_compilation.md と barriers_transfer.md にある。

**既存論文に対する過去の批判も再監査した。** TR26-128 について、ECCC、arXiv v1、正式 CCC 2026 版の該当記載と Appendix の推論を照合した。監査上、記載された外側指数は、提示された幅の不等式の合成からは導かれない。一方、旧 §30 の「幅は変数数以下だから即反証」という議論には、生成された Ref 式の UNSAT 性の確認が欠けていた。今回は「記載と導出に未解消の不整合」と分類し、定理そのものや主結果全体を反証したとは扱わない。詳細と適用範囲は同梱の tr26_128_width_recheck.md を参照する。[正式 CCC 2026 版](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2026.40)、[full version Appendix B](https://arxiv.org/html/2607.12331v1#A2)

## 5. C35：辞書順の次の一ビットは、少ないゲートで変更できる

### 命題と証明

基底を fan-in 2 の AND/OR、NOT は 1 ゲート、fan-out は無料とする。n≥1、1≤i<2ⁿ、長さ i の prefix u に整合する任意の回路 C を取る。i の二進表示における 1 の数を w=popcount(i) と置く。

\[
a_i(z)=\bigwedge_{\ell:\operatorname{bit}_\ell(i)=1}z_\ell.
\]

a_i(z)=1 なら入力 z の 1 ビット集合は i の 1 ビット集合を含むので、整数として z≥i である。したがって、

\[
a_i(x_j)=0\ (j<i),\qquad a_i(x_i)=1.
\]

そこで、

\[
C^{(1)}=C\lor a_i,\qquad
C^{(0)}=C\land\neg a_i
\]

とする。どちらも既読 prefix を完全に保存し、次の値をそれぞれ 1、0 にできる。a_i の構築には w−1 AND、接続にそれぞれ 1 ゲートまたは NOT と AND の 2 ゲートを使うので、

\[
|C^{(1)}|\le|C|+w,\qquad
|C^{(0)}|\le|C|+w+1.
\]

これは全長に対する記号的証明である。未読の他の点の値は変わってよい。旧 C23 の「指定した点以外をすべて保存する」構成より、この条件が弱いことが改善を可能にする。

### 強制ビットへの帰結

\[
\tau(u)=\min\{|C|:C\text{ が }u\text{ に整合}\}
\]

とする。Vₙ,ₛ(u) が非空で、

\[
\begin{aligned}
\text{次の値が全回路で 0}&\Rightarrow s-\tau(u)<w,\\
\text{次の値が全回路で 1}&\Rightarrow s-\tau(u)<w+1.
\end{aligned}
\]

従って s−τ(u)≥w+1 なら、両方の次の値が実現する。

| 切断位置 i | 必要な追加予算の安全上界（両値） |
|---|---|
| i=2ʳ | 2 ゲート |
| i=2ʳ−1 | r+1 ゲート |
| 一般 i | popcount(i)+1≤⌊log₂ i⌋+2 |

i=0 は空の接頭辞なので別処理する。定数入力を許さなくても、任意の入力変数 z を用いて z∧¬z と z∨¬z でそれぞれ 2 ゲートの定数回路が作れる。

**この命題が示さないこと。** 最小回路 τ(u) を効率的に求める方法ではない。変更を繰り返してもサイズを s 以下に保つ方法でもない。WC の更新時間下界や上界を解決していない。用途は、次ビット強制を利用する候補構成の検査である。

### 小さな鋭い例

2 入力、順序 00,01,10,11、閾値 s=3 とする。定数は無料、NOT は 1 ゲートという全数列挙モデルで、次の例が得られた。

| prefix u | τ(u) | 最小の整合回路 | 強制される次値 | 反対の値にした関数 |
|---|---:|---|---:|---|
| 011 | 1 | OR | 1 | XOR、最小 4 ゲート |
| 100 | 2 | NOR | 0 | XNOR、最小 4 ゲート |

この切断では w=2。前者の余裕は 2=w、後者は 1=w−1 で、二方向の厳密不等式の境界がそれぞれ達成される。任意の n,i で常に鋭いとまでは主張しない。

## 6. C36・C37：連続区間と自明な接頭辞補完

### C36：連続する k 点の変更

n≥1、1≤k≤2ⁿ とし、未読の連続区間 I=[a,a+k) を取る。任意のラベル α:I→{0,1} に対し、区間外で C を完全に保存し、区間内を α に置換する回路を、

\[
|C_\alpha|\le |C|+3k+3n-3
\]

で構成できる。基底は C35 と同じ。定数入力は不要。

**証明の要点。** 区間の二進 prefix trie を共有して各点の indicator を作る。深さ d の使用 prefix 数を N_d、T=Σ_{d=2}^n N_d とすると、全入力否定に n、共有 indicator に T、ラベル別 OR と接続に高々 k+1 の追加ゲートで足りる。連続性により各深さの片子ノードは高々二つで、T≤2k+2n−4。よって表示の上界を得る。n=k=1 も直接構成で含まれる。完全なゲート会計は同梱の ordered_patch.md を参照する。

旧 C23 の任意の散在した k 点に対する O(kn) 上界を、連続区間という仮定の下で O(k+n) に改善したものである。初等的な trie 共有であり、新規性は主張しない。

### C37：自明な補完を許す閾値では、抽出器自体が SAT を解いてしまう

明示的な長さ k≥1 の prefix u には、残りをすべて 0 とする completion 回路を、

\[
B(n,k)=3k+3n-3
\]

以下のゲート数で、u から多項式時間で構成できる。全 0 の場合は 2 ゲートでよい。この上界は最適とは主張しない。

次の候補還元を考える。

1. φ から n,k,s,uφ を poly(|φ|) 時間で生成し、n,k,s も poly(|φ|) である。
2. s≥B(n,k)。
3. 全入力で多項式時間に停止する E があり、φ が SAT なら、uφ に整合する**任意の**サイズ s 以下の回路から SAT 証人を返す。

このとき E が存在すれば P=NP。証明は、uφ の自明な completion を作って E に渡し、返された割当てを検証するだけである。WC は必要ない。

これは還元の不可能性を無条件に示す命題ではない。「その範囲の閾値では、予定していた難しさを completion に埋め込めておらず、抽出器が本丸を引き受けている」という条件付き監査結果である。s<B(n,k) でも、より小さい自明構成がある可能性をさらに調べる必要がある。

## 7. 計算検査と再現範囲

| 検査 | 範囲 | 結果 |
|---|---|---|
| 次ビット変更 | n=1〜4 の全 Boolean 関数、全非空 proper cut、両方の変更値 | 1,969,768 変更ケースで一致 |
| 連続区間変更 | n=1〜4 の全区間・全ラベル・全入力、元回路の出力の両値 | 263,172 回路、8,403,968 評価行で一致 |
| 区間変更の追加検査 | n=5,6,8,10 の境界例・固定 seed による標本 | 1,754 回路で一致 |
| 有限回路の正確列挙 | n=2・size≤4、n=3・size≤5、n=4・size≤4 | それぞれ 16、203、886 関数。調べた全 live prefix で C35 の不等式に違反なし |

正確列挙では、各段階で利用可能な真理値表集合を状態とし、AND/OR/NOT の出力を追加する BFS を行った。既にある wire と意味が等しい冗長なゲートは、任意の最小回路から除けるので省略できる。式木だけの列挙ではなく DAG の共有を許す。

n=2 では全 16 関数を覆った。n=3,4 は表示したサイズ上限内を完全に覆ったものであり、全 Boolean 関数を覆ったわけではない。

検査コードは標準 Python のみを使う。同梱ファイル：

- verify_nextbit_patch.py と nextbit_patch_verification.json
- verify_ordered_patch.py と ordered_patch_experiment.json
- tiny_wc_synthesis.py と tiny_wc_synthesis_n2/n3/n4.json
- verify_tiny_wc_synthesis.py と tiny_wc_verification.json
- 各担当の証明・先行文献監査メモ

有限回路台帳では全 7,493 live prefix・閾値組を保存した。n=2,3 の size≤3 については、重複・冗長ゲートを許す別の構文列挙とも比較し、最小サイズ分布が一致した。全 1,105 個の保存回路も再評価した。

有限検査は記号的証明の補助であり、漸近的な下界の証拠や新規性確認には使わない。複数担当も同じモデル系列と道具を共有するので、完全に独立した検証者とは扱わない。Lean 等による形式検証は今回は実施していない。

## 8. 次の実働単位

現時点では、状態数だけの下界や未証明の正規形を出し直すことより、**tight budget の prefix completion に残る構造**を調べる方が具体的である。

| 優先 | 作業 | 成功として認めるもの | 止める条件 |
|---|---|---|---|
| 1 | C35 の強制ビットが成立する tight 例を解析し、入力長にわたる族へ拡張する | 明示した基底・閾値・cut に対する構造補題 | 有限例の成長をそのまま超多項式下界と呼び始める |
| 2 | prefix generator と completion→証人抽出器を一組に固定する | 全 completion を対象にした正しい還元・特徴づけ | C37 の自明 completion、canonical 一個だけの検証、総入力時間の未会計 |
| 3 | PAP compiler を限定された認識可能な像で試す | 出力が明示 poly-size proof、または解析時間が保証された限定像 | 一般 implicit proof を無料で展開・解析する |
| 4 | 無条件 WC 下界の候補を定式化する | MMW の対偶と同じ量化・資源で、独立した困難性へ接続する | SAT が難しいことを前提にして P≠NP を結論する循環 |

次の命題カードには、入力長 |φ|、n、N=2ⁿ、prefix 長 k、閾値 s、最小補完サイズ τ、ゲート基底、oracle、全域停止条件、すべての多項式の依存先を同時に記す。

この段階では、PAP compiler を「P≠NP を解く直前の一つの補題」と表現しない。還元の完成と無条件分離を、二つの別目標として管理する。

## 確定した補題

- 旧 C20 の P=NP 仮定下の WC 構成は、一次本文と資源条件を照合して維持した。
- C33：既知に偽の後件 Q に対する (H⇒Q)↔¬H。Bridge-0 の判定を訂正した。
- C34：既知結果から P=NP⇒NEXP⊄P/poly。
- C35：辞書順の次ビット変更に追加 popcount(i) または popcount(i)+1 ゲート。
- C36：連続区間の任意変更に追加 3k+3n−3 ゲート以下。
- C37：表示した閾値・全 completion 抽出・全域多項式停止の条件下で P=NP。
- C38：prefix witness binding と WC の合成が与える含意は W⇒P=NP。単独で ¬W を与えない。

## 反証された橋

- P で評価できる関数なら小さい OBDD を持つ、という一般原理。
- MCSP の残余クラス数が、poly(s) を超える空間下界を強制するという MREC。
- 特定の canonical selector の下界から、任意の selector の下界への無条件移行。
- 「SAT 証人を WC から抽出できれば、それだけで WC の無条件下界が出る」という推論。

Bridge-0 という条件文そのものと、C31 の extractor の存在命題は、ここへ無条件反証として戻さない。過去の誤ラベルは履歴として残し、C33/C38 の訂正を優先する。

## 未証明命題

- P=NP、P≠NP のいずれも未証明。
- 所定の s,A について、すべての一様 WC 実装を排除する通常計算での poly(s) 資源下界。
- prefix witness binding、全小回路を対象とする PAP compiler、および必要な無条件 endgame。
- 母定理 M0 は未証明の複合仮説。本資料の数学的証明の前提には使っていない。
- 今回の初等補題の学術的新規性。人間の専門家による独立照合も未実施。

## 次の実験

有限回路台帳に現れた n=2 の鋭い二例から、固定した cut 族と閾値での prefix completion の構造を解析する。候補の最初の検査は C35 の少数ゲート変更と C37 の自明補完である。これらを通過した候補だけについて、全 completion からの証人抽出を検討する。

計算を大きくするだけで下界へ外挿せず、次は一つの入力長に閉じない構造命題を証明または反証する。
