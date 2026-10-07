# P vs NP 再開監査：C16–C27 と lex 次ビット修復

監査日：2026 09 05。対象：研究ノート §§25–27、候補台帳 C16–C27。元資料は変更していない。以下の「維持」は今回の独立した行監査で反例や証明の欠落を発見しなかったという意味であり、形式検証済みや専門家査読済みという意味ではない。

## 1. 結論

C20 の条件付き分離基準は維持できる。MMW の Circuit-Min-Merge を一ビット更新へ変更する証明に、現時点で致命的な穴は見つからない。特に、更新後の回路は旧回路の**全入力での意味**を保持する必要はなく、既読 prefix 上だけで一致すればよい。この区別が成功の理由である。

一方、tight-budget prefix rigidity が実際の計算時間下界を与えるという部分は未証明である。C23 の shattering は「十分な余裕があるとラベル強制できない」という必要条件を与えるだけである。今回、固定 lex 順を使ってその必要条件を強める初等的な補題を得た。prefix 長 i > 0 の次ビットは、現在の整合回路へ高々 popcount(i) + 1 gates を追加すれば、どちらのラベルにも変更できる。

## 2. 一次資料の照合

1. McKay–Murray–Williams, *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*, STOC 2019。Theorems 1.2–1.3、§2.1、§4 を確認した。[著者版 PDF](https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf)
2. Ren–Santhanam, *A Relativization Perspective on Meta-Complexity*。Theorem 3.4 と §2 の回路サイズ規約、§3.1 の脚注 5 を確認した。[ECCC 全文](https://eccc.weizmann.ac.il/report/2021/089/download)
3. Ilango, *Constant Depth Formula and Partial Function Versions of MCSP are Hard*。Theorem 11 の reduction と冒頭の回路サイズ規約を確認した。[ECCC 全文](https://eccc.weizmann.ac.il/report/2020/183/download)

引用の結論を本文と同一視しないため、MMW の主定理、そこからの一ビット改変、今回の独立補題を以下で分離する。

## 3. C20 の行監査

### 3.1 記述長と回路サイズ

n 入力、サイズ予算 s、s >= n とし、回路記述長が L = O(s log s) となる符号化を明示的に固定する。通常の fan-in 2 回路では問題ない。oracle 回路では oracle 入力配線も予算へ課金するなど、長い oracle query を一ゲートの定数コストで無制限に隠せない規約が必要である。

MMW の §2.1 自体が出力記述長を定数倍の s log s とする。本ノートの oracle 回路版でも、これと互換な符号化・サイズ規約を採用する旨を定義へ明記すべきである。ゲート数、配線数、NOT 無料を exact threshold で混ぜることはできない。

### 3.2 意味的不変条件

u の長さを i とし、現在の整合回路を C とする。候補 D に対し

\[
\operatorname{Ext}(D;C,i,b)
\iff \operatorname{Valid}_{n,s}(D)
\land \forall j<i\,[D^A(x_j)=C^A(x_j)]
\land D^A(x_i)=b
\]

とする。このとき C が u に整合する限り、

\[
\{D:\operatorname{Ext}(D;C,i,b)\}=V^A_{n,s}(ub).
\]

両包含は定義から従う。この等式は C の未読領域での挙動に依存しない。現在の C 自身が次ビットへ延長できる必要もない。D を全面的に書き換えてよい。

ub が live なら候補が存在する。dead なら存在しない。一旦 dead になると以後 live へ戻れないため、吸収状態が妥当である。i = 0 は空 prefix 用の固定小回路から始め、有限の小サイズ境界は別処理する。

### 3.3 PH 量化

固定長の valid encoding だけを候補とし、G(D,x) を妥当性と該当位置での整合性の述語とする。候補順はサイズ、次いで符号化の辞書順とする。第 k ビットの条件は

\[
\exists D\bigl[D_k=1\land\forall x\,G(D,x)
\land\forall E\prec D\,\exists y\,\neg G(E,y)\bigr]
\]

で記述できる。無効な E は G(E,y) を偽にすることで排除できる。順序比較に失敗した E の場合は後件を真にする。従って共通の形式

\[
\exists D\,\forall(x,E)\,\exists y\ R^A(D,x,E,y)
\]

へ変形できる。n <= s なので入力点、位置、候補記述はすべて poly(s) 長である。成功 flag は候補の存在だけなので Σ2^A で足りる。Σ3^A への上界は安全であり、最適性は主張しない。

P = NP と固定 A ∈ PH の下では、これらの判定と全出力ビットの生成は一様な poly(s) 時間で実装できる。指数や定数は固定した A と採用する機械に依存してよい。

### 3.4 資源

| 資源 | この構成の保証 | 監査 |
|---|---:|---|
| 更新間に残す state | O(s log s) bits | 回路、位置、flag |
| 更新中を含む総作業空間 | poly(s) | PH collapse 後の判定器が余分な作業領域を使う |
| 一ビット更新の最悪時間 | poly(s) | 出力長分の bit 計算を含む |
| 任意 prefix の decode | O(s log s) | 保持回路の複写 |
| 最終 report | O(s log s) | 同上、出力書出しを課金 |
| 初期化 | poly(s) | 最初の update に課金 |

MMW の streaming モデルも最終 reporting を update 上限へ含める。公開パラメータとして i を渡しても、i 自体を算出・保持する O(n) のコストを消してはならない。今回の上界には吸収される。

MMW の blockwise Algorithm 1 をそのまま every-prefix decoder と呼ぶのは不正確だが、ノートはその誤りを修正済みである。一ビットの Circuit-Min-Merge 呼出しへの変更が必要であり、その変更後も上記の多項式資源は維持される。

### 3.5 対偶の量化

必要なのは、ある固定 s と A ∈ PH について

\[
\forall M\ \forall k\ \forall n_0\ \exists n\ge n_0
\]

で、ある到達 prefix の正しさまたはいずれかの poly(s) 資源保証が破れることである。M は同じ一機械を全 n で使う。有限個の例外は固定記述へ埋め込める。定数倍は s >= n -> infinity と指数増加で吸収できる。

この結論は「一つの canonical selector が難しい」ではなく「効率的な exact WC が一つもない」へ量化する。canonical PME 自体の無条件多項式時間下界が得られた場合にも直接 P ≠ NP は導けるが、それは search relation 全体の下界と同じ命題ではない。

## 4. Live-promise と clock の明確化

live-promise WC は live prefix でだけ正しい witness を要求する。promise 外で必ず停止するという条件まで定義に含めるかどうかは分離すべきである。

ただし C25 と C26 の検証付き reduction は、live prefix 上での一様な多項式時間上界だけからも修復できる。仮定した機械の上界 p(s) を固定し、初期化、各 update、decode に個別の clock を付け、時間切れなら棄却する。YES 入力の全途中 prefix は live なので時間切れは起きない。NO 入力で機械が停止せず、無効な値を返し、あるいは誤った小回路を返しても、clock と最終的な元データ上の検証で棄却できる。

この clock の存在は hypothetical polynomial-time machine から得られ、具体的な未知の多項式を研究者が計算可能に推定する主張ではない。仮定した一機械とその上界を reduction の記述へ固定すればよい。

なお、live-WC から exact-WC が自動的に得られるという話ではない。prefix を再読せず任意長で past-consistency を検証するには別の仕事が必要である。

## 5. C16–C27 の台帳判定

| 候補 | 判定 | 読み違えてはいけない点 |
|---|---|---|
| C16 | 維持 | final-output の全内部状態を記録するモデル同値。更新の一様性と一時作業空間も資源へ数える。 |
| C17 | 維持 | 同じ回路記述が異なる全真理値表を計算できないことから live prefix ごとの残余が分離。state 数上界は更新計算時間上界ではない。 |
| C18 | 維持 | lex-min のみ Equality を解く反例が正しい。全 selector の下界を表す例ではない。 |
| C19 | 維持 | n >= 3 の chain、all-one transcript、未照会 hole の議論は正しい。構文を読めるモデルの下界ではない。 |
| C20 | 維持 | 条件付き分離基準。下界本体は未証明。 |
| C21 | 維持、モデル限定 | typed same-length permutation oracle の separation。普通の unrestricted oracle access と同一視しない。 |
| C22 | 一次資料と整合 | source-native の配線サイズと NOT 無料を明記する。terminal search 自体も難しい world。 |
| C23 | 維持、強化可能 | gate 会計は安全。任意 future set の shattering。lex 次点については §7 の方が強い。 |
| C24 | 維持 | multi-output の出力 source 指定を含む計数が必要。すべての arbitrary mask を覆う permutation-only 案に限定。 |
| C25 | 条件付きで維持 | size bound に収まる PRF のみ排除。promise 外は clock と検証で処理。 |
| C26 | 条件付きで維持 | 任意 address 版。source の exact size 規約と fixed-prefix 版との違いが重要。 |
| C27 | 維持 | oracle の定義へ問題の解を入れた飽和構成。既知の全 locality barrier と同一視しない。 |

### C22 の exact parameter

Ren–Santhanam Theorem 3.4 の c = 2 から、配線サイズ 8n 以下の YES 表に対し、サイズ N/(4n) 以下の回路出力を N^2 時間機械が失敗する world が得られる。脚注 5 は各機械を無限回列挙すると明記しており、「任意に大きい長さ」の使用も支持される。

poly(n) update を N ビットへ適用する総時間は N poly(log N) であり、十分大きい N では N^2 未満になる。小さい長さを処理した clocked machine で矛盾が得られる。定数 8 と配線サイズを、NOT 課金ゲートサイズの定数としてそのまま使わないこと。

### C26 の size convention を保持する修復

Ilango の一般回路は fan-in 2 AND/OR と NOT、サイズは AND/OR gates 数である。Theorem 11 の hard family の入力次元 m は 6r、threshold は m - 1。YES の明示回路は NOT を含まない monotone read-once formula なので、NOT も課金する版でも同じ m - 1 以内である。一方、NOT 課金で size <= m - 1 の回路は、NOT 無料でも size <= m - 1 である。従って NO も保たれる。この挟み込みで C26 を C23 と同じ total-gate basis へ移せる。

s = m - 1 は C20 の表示 s >= m を一つ下回るが、n = O(s) の範囲へ C20 の直接証明を拡張すれば記述長も資源も維持される。とはいえ fixed-prefix 化の未証明問題は一切解決しない。

### C27 の one-round

各 output bit の query を旧 C、i、b から作るため、一 update 内ではすべて非適応である。この意味で batch / truth-table access の 1 round。逐次 oracle machine が一回しか query しないという意味ではない。L 個の長さ O(L) query を書くので時間 O(L^2)、逐次生成時は一時空間 O(L) で十分である。stream 全体は前 update の結果へ依存するので O(N) の逐次段を持つ。

## 6. Prefix rigidity の量化修正

live prefix u の minimum completion size を

\[
\tau_{n,A}(u)=\min\{|C|: C^A\text{ is consistent with }u\}
\]

とする。予算 s 内に存在する場合だけ考える。

C23 から next-bit forcing に必要なのは正確には

\[
\tau_{n,A}(u)>s-(2n+1).
\]

すなわち、**一つでも**十分な slack を持つ整合回路があれば forced next bit は成立しない。現在の selector が偶然保持している C のサイズだけを見て slack が少ないと判断するのは不十分である。

またこの必要条件は forced-next-bit / unique semantic completion gadget への条件であり、一般の witness-binding、canonical syntax の困難性、計算時間下界の必要条件ではない。下界がすべて dead detection に由来しないことも、この補題だけでは証明されない。

## 7. 追加補題 C35 案：Lexicographic Upper-Cone Next-Bit Repair

### 定義

通常の n 入力回路を fan-in 2 AND/OR と unary NOT で数え、各 gate のコストを 1、fan-out は無料とする。x_0,...,x_(2^n-1) は整数値の昇順、すなわち通常の lex 順に並ぶ。

1 <= i < 2^n に対し、i の binary 表示で 1 となる座標集合を H_i、その要素数を h(i) = popcount(i) とする。

\[
a_i(x)=\bigwedge_{j\in H_i}x_j.
\]

i > 0 のため H_i は空でない。h(i) = 1 の場合は a_i が一入力線そのもので、内部 gate は 0 個である。

### 命題

長さ i の prefix u に整合する任意の回路 C から、u と次ラベル 1 に整合する回路 C_1 および u と次ラベル 0 に整合する回路 C_0 を構成でき、

\[
|C_1|\le |C|+h(i),\qquad
|C_0|\le |C|+h(i)+1.
\]

従って

\[
\tau_{n,A}(u)\le s-h(i)-1
\quad\Longrightarrow\quad
V^A_{n,s}(u0)\ne\varnothing
\ \land\ V^A_{n,s}(u1)\ne\varnothing.
\]

ここで A-oracle 回路の場合も、追加する普通の AND/OR/NOT gates の課金が同じなら成立する。source-native の wire-size に適用する場合は追加 wire 数で再計算する。

### 証明

まず a_i(x_i) = 1。任意の入力 x が a_i(x) = 1 を満たすなら、i で 1 の全座標が x でも 1 であり、整数値として x >= i である。よって j < i なら a_i(x_j) = 0。

\[
C_1=C\lor a_i,\qquad
C_0=C\land\neg a_i
\]

と置く。既読点では a_i = 0 なので C_1 = C_0 = C。新しい点 x_i では C_1 = 1、C_0 = 0 になる。

a_i は h(i) - 1 個の AND gates で作れる。C_1 は最後の OR を 1 個追加するので h(i) 個。C_0 は a_i の NOT と最後の AND を追加するので h(i) + 1 個である。元回路 C の入力否定を共有できる場合などにはさらに削減できるが、この証明には不要である。最小整合回路へこの構成を適用すれば系が従う。∎

### 正確な帰結

\[
\boxed{\text{next bit が forced}\quad\Longrightarrow\quad
\tau_{n,A}(u)>s-\operatorname{popcount}(i)-1.}
\]

さらに方向別には、forced 0 の場合は \(\tau(u)>s-h(i)\)、forced 1 の場合は \(\tau(u)>s-h(i)-1\) が必要である。前者は label 1 を作る小さい方の patch で反証されるからである。

- i が 2 のべきなら h(i) = 1。slack 2 があればどちらの次ラベルも可能。
- 一般に h(i) <= floor(log2 i) + 1 なので、早い cut では n より log i が有効な量となる。
- NOT 無料の AND/OR size 規約では、両ラベルとも追加 h(i) で足りる。
- i = 0 は別扱い。定数が無料でない total-gate basis でも n >= 1 なら x_1 AND NOT x_1 と x_1 OR NOT x_1 が各 2 gates で最初のラベルを実現する。通常の s >= n では n >= 2 を満たせば両方が live。

この構成が最小の patch であるとは主張しない。また C を毎回 patch すると回路サイズが累積して s を超え得るので、これだけから efficient fixed-budget WC は得られない。必要な情報は local forced-label gadget を棄却する条件の強化である。

### 量化と新規性

命題は全 n、全非零 cut i、全 Boolean 回路 C と両 label に対する構成的上界である。無条件の一様計算時間下界でも、P ≠ NP の証明でもない。今回独立に導出した初等的補題として記録し、既知性を未確認のまま新規定理とは呼ばない。

### 有限全数検証

`verify_nextbit_patch.py` は n = 1,2,3,4 の全 Boolean 関数、全 1 <= i < 2^n、両 label を検査した。元 C の出力を任意の truth-table bitset として扱い、a_i を実際に AND で構成する。

| n | 全関数数 | 非零 proper cut 数 | 両ラベルの検査件数 |
|---:|---:|---:|---:|
| 1 | 4 | 1 | 8 |
| 2 | 16 | 3 | 96 |
| 3 | 256 | 7 | 3,584 |
| 4 | 65,536 | 15 | 1,966,080 |
| 合計 | — | — | 1,969,768 |

すべて PASS。各 cut で既読全点上の a_i = 0、次点上の a_i = 1、prefix 保全、要求 label、追加 gate 会計を確認した。空 prefix の定数構成は別に検査した。ログは `nextbit_patch_verification.json`。これは論証の補助検証であり、回路最小化の全数探索ではない。

## 8. 次に検査する具体的な命題

任意の proposed forced-next-bit gadget に対して、まず指定 cut i と \(\tau(u)\) の上界を具体的に出し、\(\tau(u)+h(i)+1\le s\) なら直ちに棄却する。上界を与える C は selector が選ぶ予定の canonical circuit に限定しない。

この検査を通った場合だけ、(a) 全 size-s 整合回路に対する rigidity、(b) 元問題からの prefix を十分短い時間で作れること、(c) 任意 decoded circuit からの witness 抽出、(d) size と oracle query の exact accounting を別々に証明する。現在 (a)〜(d) を同時に満たす一般回路の construction は、この監査では得られていない。

## 9. 追加の方向監査：NP witness-binding の完成だけでは分離しない

主担当からの終盤構想への監査依頼に対する結論である。§§28–30 の NP witness 抽出構想について、次の仮定を明示する。

1. SAT instance φ から explicit prefix uφ と対象族のパラメータ n,s を作れる。
2. prefix 長、s、生成時間がすべて poly(|φ|)。
3. φ が SAT なら uφ は live。
4. uφ に整合する任意の size-s 回路から、φ の SAT witness を poly(|φ|) 時間で抽出できる。

efficient WC があれば、uφ を流し、回路を decode し、抽出結果を φ で検証すればよい。promise 外の停止は §4 の clock で確保する。従ってこの bridge から得られるのは

\[
\text{efficient WC exists}\quad\Longrightarrow\quad P=NP.
\]

MMW の逆向き

\[
P=NP\quad\Longrightarrow\quad\text{efficient WC exists}
\]

と合わせても、両方向の同値化になるだけであり、矛盾は生じない。無条件な WC 不在が別途必要である。

同様に、C30 の arbitrary-small-circuit → short Resolution compiler と既知 PAP extractor を完成すれば、適切な forward reduction の下で上の witness-binding が得られる。しかしそれだけで P ≠ NP は証明されない。逆に、この P = NP への含意のみを理由に compiler を反証済みと呼ぶのも誤りである。計算量上の同値化や NP-hardness の証明として価値を持ち得るが、分離への最終ステップとは区別する。

この監査は prefix / size が多項式に収まる ordinary deterministic reduction の範囲である。oracle、randomness、subexponential parameter を使う場合には、実際の総時間と到達する複雑度クラスを改めて書き下す必要がある。
