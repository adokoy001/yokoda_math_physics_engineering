# P vs NP 再始動：知識コンパイル・正規化の先行研究と旧経路監査

- 調査日：2026 09 05
- 対象：主ノート v0.24 の行 1–1605（§0–18.5）。後半は見出しと canonical／PH 関連の記述を検索した。
- 判定：旧経路の限定補題はおおむね妥当。ただし含意の反証ラベル、状態幅の定義、SSMS の変換仮定に修正が必要。
- 本文の「既知」は以下の一次論文で確認した範囲。新規性の否定／肯定を網羅的に認定するものではない。

## 1. 最も重要な整理

現在の研究は既に MCSP witness-carrying・proof analysis へ進んでいる。OBDD／HWB は再開地点そのものではなく、以後の主張を検査するための反例・型検査として維持するのがよい。

次の三つは別の量である。

1. 異なる残余意味の個数。
2. 一つの残余を表す記述の長さ。
3. 記述を構築・更新・比較する計算量。

N 個の残余クラスが必要でも、状態番号は ceil(log₂ N) ビットで表せる。さらに、番号の存在だけでは一様な更新器を与えない。ただし canonical 番号の更新だけを困難化しても、更新しやすい非 canonical な精密化を排除できない。この点は主ノート後半ですでに認識されており、旧章にも同じ尺度を適用すべきである。

## 2. 2026年の追加文献

### 2.1 TDD：正規化と Apply の両立は改善されたが、HWB はなお指数サイズ

Capelli, Choi, Mengel, Muñoz, Van den Broeck, *A Canonical Generalization of OBDD*, SAT 2026。

正式版の Theorem 11 は、vtree を尊重する幅 k の TDD を poly(k)|X| 時間で最小 canonical TDD にする。Theorem 16 は primal／incidence treewidth k の CNF を 2^{O(k)}mn 時間で TDD にコンパイルする。Theorem 21 は、7 の倍数 n について HWB_n が任意の TDD で 2^{Ω(n)} サイズを要することを示す。

したがって、TDD は正規化・合成の計算保証を改善する具体例だが、一般 P 計算を表す normal form には採用できない。小 treewidth での正のモデルと、HWB による負の監査を同じ論文で揃えられる点が本研究に有用。

出典：[SAT 2026 正式論文](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SAT.2026.10)。定理番号は arXiv v1 と異なるため正式版番号を使用する。

### 2.2 全解表現の下界を反駁過程へ移す、ただし弱化なし

Berkholz and Micun, *Proof Systems Based on Structured Circuits*, SAT 2026。

Theorem 13：n 変数 (k, log n)-CNF φ と C∈{OBDD, SDD, d-SDNNF} について、変換後の不充足式 Z(φ) にサイズ t の C(∧,r)-反駁があれば、φ はサイズ O(t² n^{2k²}) の C 表現を持つ。節幅 k を定数とすれば、表現下界をこの制限証明系の下界へ移せる。

決定的な制限は weakening を許さない点。Lemma 23 は、すべての Z(φ) に多項式サイズの Resolution 反駁があることを示す。最終関数が ⊥ になる問題を越えても、別の証明方式まで困難化したことにはならない。

出典：[SAT 2026 正式論文](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SAT.2026.6)。一般 SAT の下界や P≠NP を示す結果として扱わない。

## 3. 基礎文献との対応

| 文献 | 確認できた範囲と仮定 | 主ノートとの対応 |
|---|---|---|
| Bova & Slivovsky, *On Compiling Structured CNFs to OBDDs*, arXiv:1411.5494 | Theorem 1／Corollary 1 は constructive few subterms から polytime OBDD compilation。Theorem 7 は各節が正リテラル2個、各変数最大3出現でも指数 OBDD 下界。 | §2–4。subterm は構文的残余で、意味的残余数とは区別する。後者以下の数になるとは限らず、意味クラス数 ≤ 構文残余数。 |
| Bollig, Löbbing, Sauerhoff, Wegener, *On the Complexity of the Hidden Weighted Bit Function for Various BDD Models*, 1999 | HWB の OBDD 指数下界と、BDD モデルを変えた場合の挙動を扱う。 | HWB によるモデル制限の監査。通常計算の下界へ転用しない。 |
| Bova, *SDDs Are Exponentially More Succinct than OBDDs*, AAAI 2016 | HWB は O(n³) の非圧縮 SDD を持ち、OBDD は 2^{Ω(n)}。一般化 HWB により圧縮 SDD と OBDD も指数分離。 | §7 の SDD 拡張は既知。HWB 自体の結果と、一般化 HWB の canonical 結果を同一視しない。 |
| Darwiche & Marquis, *A Knowledge Compilation Map*, JAIR 2002 | 簡潔さ・問い合わせ・変換の組で対象言語を比較。DNNF の分解性や d-DNNF の決定性は、許される演算に固有の条件。 | §5, §14.2, §15 の CCP はこの研究方針と同系統。新しい名称だけでは新規結果にならない。 |
| Van den Broeck & Darwiche, *On the Role of Canonicity in Knowledge Compilation*, AAAI 2015 | 固定 vtree の reduced SDD では、正規化・二項 Apply・一変数の conditioning でも指数サイズ化し得る。非圧縮 SDD には polytime Apply。 | 「短い表現 vs 正規化／更新」の既知の明示例。固定 vtree と出力も reduced という仮定が不可欠。 |
| Amarilli, Capelli, Monet, Senellart, *Connecting Knowledge Compilation Classes and Width Parameters* | Theorem 4.2 は与えられた幅 k の tree decomposition から d-SDNNF を 2^{O(k)}×分解サイズ時間で構成。Theorem 8.3 は定数節幅・定数出現回数の単調 CNF に 2^{Ω(treewidth)} の DNNF 下界（complete 化の多項式係数に注意）。 | §3, §14.3, §18.5。単調 CNF は SAT 判定容易でも DNNF 表現が大きい。一般回路の下界ではない。 |
| Cadoli, Donini, Liberatore, Schaerf, *Space Efficiency of Propositional Knowledge Representation Formalisms*, JAIR 2000 | fixed part と online part を分け、poly-size 前処理は計算時間の制約と区別する。所定の compilability-hardness の下では poly-size compilation と P-time online query が PH collapse を含意する。 | §14.2, §15。任意の単発 SAT には適用できない。単発 Yes/No を非計算的に1ビット保存する例を排除するには online query の定義が必要。 |
| Fortnow & Grochow, *Complexity Classes of Equivalence Problems Revisited*, 2011 | LexEq ⊆ CF ⊆ Ker ⊆ PEq を区別。完全不変量、代表元、辞書順最初の代表は別問題。P=NP の世界ではこれらの P-time equivalence classes は一致する。 | canonical selector と任意 selector の差を形式化する参考。一般 CNF の論理同値は通常 PEq を仮定できないので、この階層に無条件で入れない。 |

一次出典：

- [Bova–Slivovsky](https://arxiv.org/abs/1411.5494)
- [HWB 原論文](https://www.numdam.org/item/ITA_1999__33_2_103_0.pdf)
- [Bova SDD 分離](https://ojs.aaai.org/index.php/AAAI/article/view/10107/9966)
- [Knowledge Compilation Map](https://arxiv.org/abs/1106.1819)
- [Canonicity](https://ojs.aaai.org/index.php/AAAI/article/view/9423/9282)
- [Width Parameters](https://arxiv.org/abs/1811.02944)
- [Space Efficiency](https://arxiv.org/abs/1106.0233)
- [Equivalence Problems](https://arxiv.org/abs/0907.4775)

## 4. 主ノート前半の独立監査

### A1. §6 Bridge-0 の「反証」ラベルは論理的に修正が必要【重要】

ノートは次の含意を「偽」と断定している。

    SAT ∈ P ⇒ 全 CNF に多項式状態の完全意味要約が存在する

「多項式状態」を OBDD の状態数と読むなら、後件 Q は既知の単調 CNF 下界により偽。一方、前件 P₀ は未解決。古典論理では ¬Q が既知のとき、(P₀⇒Q) は ¬P₀ と同値になる。したがってこの含意を無条件に反証すれば、逆に P₀、すなわち P=NP を示してしまう。

正しいラベルは「橋として未証明。この橋を証明すること自体が P≠NP を示す」。反証済みなのは「P で計算できる Boolean 関数なら poly-size OBDD を持つ」という一般変換原理である。§18.1 は既にこの点を正しく説明しており、§6 とラベルを統一する。

もし後件の「要約」が単に多項式ビットの任意 Boolean 式を意味するなら、量化消去のない CNF 全解集合については元の CNF 自体が短い表現となり、今度は後件を偽とする根拠が消える。後件の表現モデルと資源尺度を必ず固定する。

### A2. §2 の等式は「固定 cut の到達状態」に対して厳密化する【中】

同一状態なら全 continuation で同じ出力、という補題は正しい。最小の layered deterministic 状態数も残余クラス数と一致する。

ただし普通の reduced OBDD は変数を飛び越える。たとえば f(x₁,x₂)=x₂ では x₁ ラベルのノードはゼロ個だが、x₁ を読み終えた cut の残余は一個である。「既約 OBDD の各ラベル層のノード数」と「深さ i の残余数」が字義通り常に一致するとは書かず、layer-completed 表現または cut 上の残余ポインタ数（terminal を含む）と定義する。

### A3. §1–2 は存在量化の対象と最終出力を合わせる【中】

R_α(b)=∃u F(α,b,u) と定義した後、補題2.1では「元の Boolean 関数値」を最終状態から読むとする。投影ありなら終値は ∃u F(α,b,u) であり、u を与えた F の値ではない。読まれる変数集合、量化される固定集合 U、出力関数を一度固定すれば証明は成立する。

### A4. §5.1 の関数表現性と polytime 評価を分離する【中】

Cond を逐次適用して任意代入を評価できる、という表現性は正しい。ただし「一回の更新が現状態のサイズに対し多項式」だけでは、n 回の連鎖全体が初期入力長の多項式とは限らない。中間サイズが s→s²→s⁴ と増大し得るためである。効率まで主張する際は、全中間状態サイズが元入力長の多項式という不変条件と、uniform な演算器を追加する。

### A5. §8.2 の SSMS→SDD は forget のコストを仮定に含める【中】

葉が literal／constant、すべての内部ノードが同一 vtree の sentential decision という条件下で DAG を SDD に写す帰納証明は正しい。ただし SSMS の定義には forget=存在量化がある。任意 forget をマクロ一操作として数えたまま、各 merge だけが SDD 形だから全体も多項式 SDD になるとは言えない。

修正案：forget を禁止した構文定理にするか、forget の出力も既に合法な SDD として明示され、出力全サイズを資源に数えるという仮定を追加する。

### A6. §3 の著者名を修正する【書誌】

arXiv:1411.5494 の著者は Simone Bova と Friedrich Slivovsky の2名。ノートの Bova／Capelli／Mengel／Slivovsky の4名は別論文と混線している。

### A7. §7 は HWB の非圧縮 SDD と一般化 HWB を区別する【軽微】

HWB の O(n³) SDD 上界は正しい。ただし canonical compressed SDD の指数分離まで述べるときは、Bova の一般化 HWB へ切り替える。HWB そのものが同じ vtree の圧縮 SDD でも O(n³) だとは導けない。

### A8. §15.3 の再実行上界には入力型を明記する【軽微】

Comp が一般 Boolean 式を出力する場合、3-SAT 判定器 A へ渡す前の多項式 Tseitin／Cook–Levin 変換を明記する。文脈長が |F| の固定多項式で抑えられることも必要。これらを補えば上界は正しい。

### A9. §18.3 は正しい標準的系であり、新規な分離ではない【確定】

Good が固定 PH レベルで判定され、候補長に一つの多項式上界があり、全入力で候補が存在するなら、P=NP による PH collapse と prefix search で構築器が得られる。可変長の符号化もノートで処理されている。

正当性確認が非一様に各長さごと別述語で与えられる場合や、候補長の指数が入力ごと無制約に変わる場合にはこの系を適用しない。§18.4 の境界回路の正当性が Π₂^P に入る点も妥当。

### A10. §9, §11–13 は研究史の章として保存する【構成】

「現在の主経路」が前半の E-NF、後半の witness-carrying／proof analysis で重複している。前半を「v0.1–0.12 の研究史」、最新版の研究位置を冒頭に一箇所で定義する。削除する必要はないが、時点の違う主経路を同時に現行扱いしない。

## 5. 正規形についての追加の型検査

ここは文献の定理を装わず、有限符号化からの簡単な観察として置く。

一般 CNF F について、同じ固定変数 universe 上で F と論理同値な最短 CNF を取り、同長なら辞書順最初を選べば canonical representative canon(F) が集合論的に定まる。F 自身が候補なので |canon(F)|≤|F|。したがって短い canonical representative の存在自体は非常に弱い。

一方、F≡G iff h(F)=h(G) を満たす完全不変量 h が決定的多項式時間で計算できれば、h(F) と同じ universe の矛盾式 h(⊥) を比較して UNSAT を決められ、P=NP が従う。代表元を返す必要すらない。

ただし、この観察を境界投影 R_F(B)=∃X F(X,B) にそのまま適用してはいけない。出力言語を「量化なし B 上の CNF」に制限すると、元の F(X,B) は適格な候補ではない。内部変数を隠した投影表現を許すなら元式が短いが、B を与えた membership 自体が SAT 問い合わせとなる。ここでも「短い」の意味は出力言語と許される問い合わせに依存する。

## 6. 今回の結論と次に残す課題

この旧経路を新規な P≠NP 証明の芽として再始動する必要はない。現行 MCSP 経路の監査器として整理し、2026年の次の二例を追加するのが具体的な前進である。

1. **TDD**：最小 canonical 化と高速 Apply を両立しても、HWB の表現下界が残る。したがって操作の良さと一般計算の表現力を別々に検査する。
2. **Structured-circuit proofs**：表現下界から反駁下界へ移せても、weakening／Resolution が逃げ道になる。したがって「すべての許可された proof／selector／state refinement」を排除する量化が必要。

研究として残る価値は、特定の canonicalizer が遅いという事実ではなく、指定した資源内の**すべての一様な更新器・精密化・witness selector**に通用する障害の構築である。そのような障害はまだ得られていない。

