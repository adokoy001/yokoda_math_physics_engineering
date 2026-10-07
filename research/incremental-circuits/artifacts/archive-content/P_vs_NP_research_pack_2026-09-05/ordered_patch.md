# 連続区間の回路パッチ：C23 の初等的な改善候補

作成日：2026 09 05

**数学的状態：以下の構成と上界は証明済み。新規性は未確認であり、既知の trie 共有による初等的な改良として扱う。回路の漸近下界や P≠NP の証明は主張しない。**

元資料 `sources/P_vs_NP_candidate_original_results.md` の C23 は、任意の相異なる k 点への変更を O(kn) gates で行う。ここでは変更点が辞書順の連続区間の場合に限定し、共有した prefix trie により O(n+k) gates に改善する。元ノートは変更していない。

## 1. 会計と定義

- 入力は n≥1 個の Boolean 変数 x₁,…,xₙ。x₁ を最上位 bit として整数 0,…,2ⁿ−1 と同一視する。
- 基底は fan-in 2 の AND / OR、および unary NOT。NOT も 1 gate と数える。
- fan-out と配線は無料。元回路 C の入力と出力は再利用できる。
- 定数入力は仮定しない。以下のパッチ構成では定数を使用しない。
- 区間 I=[a,a+k) は 1≤k≤2ⁿ、0≤a≤2ⁿ−k を満たす。k=0 は C をそのまま返せばよい。
- 区間上の任意のラベル列 α=(α₀,…,αₖ₋₁) を指定する。

## 2. 主命題：普遍的な連続区間パッチ

任意の基回路 C と上記の I,α に対し、I 外では C と厳密に一致し、a+j 上では αⱼ を出力する回路 Cα が存在する。追加 gate 数は

\[
B(n,a,k)=n+T(n,a,k)+k+1
\]

以下でよい。ただし

\[
T(n,a,k)=\sum_{d=2}^{n}
\left(
\left\lfloor\frac{a+k-1}{2^{n-d}}\right\rfloor
-\left\lfloor\frac{a}{2^{n-d}}\right\rfloor+1
\right).
\]

n=1 のとき和は空で 0 とする。特に

\[
\boxed{|C_\alpha|\le |C|+3k+3n-3.}
\]

k=1 では精密な式が従来の **2n+1 gates** を返す。一様上界 3k+3n−3 は簡潔さを優先した非最適な定数である。

### 構成

I の各 n-bit 列を葉とする、根付きの prefix trie を作る。

1. 全 n 入力の否定を n NOT gates で一度だけ作る。
2. 根の子に対応する深さ 1 の prefix indicator は x₁ または ¬x₁ を直接使う。
3. 深さ d≥2 の各 trie node では、親 indicator と、対応する x_d または ¬x_d を 1 AND gate で接続する。
4. 各葉 z の indicator δ_z を、α(z)=0 と α(z)=1 の二群に分ける。

両群が非空なら、それぞれの OR を D₀,D₁ として

\[
C_\alpha=(C\land\neg D_0)\lor D_1.
\]

α がすべて 1 なら Cα=C∨D₁、すべて 0 なら Cα=C∧¬D₀ とする。空の OR を作らないため、定数 gate は不要である。

I 外ではすべての δ_z が 0 となるので元の C が保存される。I 内の点 z ではその点の δ_z だけが 1 となるので、指定した α(z) が出力される。これは C の内部構造に依存しない。

### 正確な gate 数

深さ d に存在する trie node 数は

\[
N_d=
\left\lfloor\frac{a+k-1}{2^{n-d}}\right\rfloor
-\left\lfloor\frac{a}{2^{n-d}}\right\rfloor+1.
\]

したがって、共有 indicator 部分は n NOT + T AND gates。

| ラベル配置 | ラベル群の OR gates | 最終接続 gates | 合計追加 gates |
|---|---:|---:|---:|
| 0 と 1 が両方ある | k−2 | 3 | n+T+k+1 |
| すべて 0 | k−1 | 2 | n+T+k+1 |
| すべて 1 | k−1 | 1 | n+T+k |

### T=O(n+k) の証明

trie の二子 node 数を b、一子 node 数を u、根の子の数を r とする。葉は k 個なので b=k−1。辺の総数 e は

\[
e=2b+u=2k-2+u.
\]

各深さにおいて、一子 node は高々 2 個しかない。理由は、occupied dyadic blocks のうち左右の端以外は I の内部に完全に含まれるので、両方の子を必ず含むためである。深さ 0 には根しかないため

\[
u\le 1+2(n-1)=2n-1.
\]

深さ 1 の r 本の辺には AND gate が不要なので

\[
T=e-r\le 2k+2n-4,
\]

ここで r≥1 を使った。これを代入すると B≤3k+3n−3 が従う。∎

## 3. 未読区間への適用

prefix u と整合する C があり、I が未読の連続区間なら、上の構成は既読部分を厳密に保存する。したがって

\[
|C|\le s-B(n,a,k)
\]

なら、その区間上の全 2ᵏ ラベルがサイズ s 以下の整合回路で実現できる。簡単な十分条件は

\[
|C|\le s-(3k+3n-3).
\]

これは version space の shattering に関する上界であり、与えられていない基回路 C を効率よく見つけられるとは述べていない。selector / WC の容易性はこれだけでは従わない。普通の gates だけを追加するため、この基底を含む oracle circuits にも同じ構成が適用できる。

## 4. 派生：explicit prefix の suffix-0 completion

長さ k≥1 の明示的な真理値表 prefix u を与える。I=[0,k) の同じ trie を作り、uⱼ=1 となる葉 indicator だけを OR すれば、

\[
D_u(x)=
\begin{cases}
u_x&0\le x<k,\\
0&k\le x<2^n
\end{cases}
\]

を計算できる。

1 の個数を t とすると、t≥1 の場合の gate 数は

\[
n+T(n,0,k)+t-1\le 3k+3n-5.
\]

t=0 では、x₁∧¬x₁ という **2 gates** の回路を直接返す。したがって全場合で安全な共通上界は

\[
\boxed{|D_u|\le 3k+3n-3.}
\]

k=0 の場合も同じ 2-gate zero circuit を使える。

### 構築時間についての会計

全 k 点を独立に n 段歩いて trie に挿入する必要はない。区間と交差する子だけを深さ優先で辿れば、訪問 node と出力 gate は O(n+k) 個である。ラベルの振り分けも O(k) 操作。

従って、n-bit の区間端点や gate index の演算を単位操作とする word-RAM では **O(n+k) 操作**で構築できる。通常の bit complexity では、gate index の符号化・n-bit 整数演算の費用を加える必要があり、O(n+k) bit time とは主張しない。どちらのモデルでも n+k に関する多項式時間で構築できる。添付検査プログラムのビット並列真理値評価は全入力を扱う検査機能なので、構築時間の上界を測定する実装ではない。

## 5. 追加 kill-test：全 completion からの witness 抽出

次は新しい困難性結果ではなく、提案する reduction を棄却するための条件付き監査補題である。

SAT instance F から、n, explicit prefix u, gate budget s を多項式時間で出力する手続き R を考える。n と |u| も |F| の多項式以下とする。以下を同時に要求すると仮定する。

1. R の出力は、上の明示的 zero-suffix completion D_u を許すだけの budget を持つ。例えば k=|u|≥1 なら s≥3k+3n−3。
2. 全域で多項式時間の decoder E があり、F が充足可能なら、u に整合する **すべての** サイズ s 以下の回路 D に対し E(F,D) が F の充足割当を返す。

この場合、R(F) を計算し、既知の構成で D_u を作り、E(F,D_u) の出力を F に代入して検査すれば SAT を多項式時間で決定できる。充足可能なら仮定 2 によって必ず成功し、充足不能なら正当な充足割当は存在しないので検査で拒否する。従って、**これらの条件だけで P=NP が従い、WC / selector の oracle は不要**となる。

また「F が充足不能な場合には prefix が dead になる」という別の reduction 要件があれば、仮定 1 はすべての出力を live にするので、直ちに衝突する。

これは SAT→WC の reduction 一般を排除しない。上界以下の厳しい s、explicit prefix より強い制約、ある特別な completion だけを対象にした decoder、あるいは非効率な decoder は上記の仮定から外れる。狙いは、任意の completion に witness を強制したつもりでも、素朴な zero-suffix completion が残っていないかを先に確認することにある。

## 6. 再現検査

- `verify_ordered_patch.py`：構成した AND / OR / NOT DAG をビット並列で評価する。
- `ordered_patch_experiment.json`：実行した検査範囲と結果。
- n=1,…,4 について、全非空連続区間、全ラベル配置 α、全入力 x、および基回路出力 c∈{0,1} を全数検査する。x ごとに両 c を検査するため、任意の基回路 C を点ごとに包含する。
- n=5,6,8,10 では、境界区間と固定 seed のサンプルを追加する。
- 真理値、正確な gate 数、普遍上界、k=1 の 2n+1 上界、prefix completion の suffix-0 性と元回路非依存性を検査する。

今回の実行結果は **PASS**。n≤4 の全数検査は 263,172 個の patch circuits、8,403,968 行の (x,c) 評価を含む。さらに 1,754 個の大きめのサンプル回路を検査した。n≤4 の prefix completion は 131,616 個を検査した。実行時間は約 3.71 秒だった。

有限検査は証明の補助であり、漸近下界・新規性・P versus NP に関する結論の根拠とはしない。

実行例：

```bash
python verify_ordered_patch.py --output ordered_patch_experiment.json
```
