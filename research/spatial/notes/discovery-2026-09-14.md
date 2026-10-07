# 空間の観測と接続 — 厳密式・最良係数・再現検証

研究日：2026 09 14 ／ 研究記録 v1.0

横田さんとAIによる「探索的な数学的発見」プロジェクトの新しい探索記録。既存の成果台帳は変更せず、本稿内の命題を S1・S2 として識別する。

**数学的な到達点：二つの主題について一般証明を記録した。S2の予想は、より強い形を含めて最良係数まで証明できた。S1は距離観測の正確な誤差曲線と、基準点配置の有限探索への還元まで得た。**

**新規性の到達点：下記の正確な式・係数と一致する結果は、今回読んだ一次資料では特定できなかった。学術的新規性は未確定。** 複数の独立したAI作業で導出・監査したが、人間の専門家による査読およびLean等による形式検証は未実施である。有限検査は一般証明とは別の補強として扱う。

## 0. 結果の地図

| ID | 命題 | 数学的状態 | 新規性の扱い |
|---|---|---|---|
| S1.1 | 木上の距離観測の射影恒等式と単射条件 | 証明を記録 | 既知の木の識別構造と近い。新規の中心主張にしない |
| S1.2 | 任意の固定された識別可能な基準点集合の最良逆Lipschitz係数 | 証明を記録 | 正確な枝長／付け根間隔の式は一致未確認 |
| S1.3 | 有限誤差に対する曖昧さ直径の厳密式。非単射の場合も含む | 証明を記録 | 正確な式の一致未確認。追加照合を要する |
| S1.4 | 決定論的な最良推定誤差は曖昧さ直径の半分 | 証明を記録 | 半径・情報半径の既知原理を用いる系として扱う |
| S1.5 | 2個以上の基準点を、個数を増やさず葉へ移して全ての点対の観測差を改善できる | 証明を記録 | 最小識別集合の葉配置は既知。点対ごとの優越の正確な主張は追加照合対象 |
| S2.1 | 独立な直線上の不確実位置に対する固定／可変接続の比は高々 ceil(n/2) | 2通りの一般証明と等号例を記録 | 正確な最良係数は一致未確認 |
| S2.2 | 短い不確実区間の個数 m による最良係数 ceil((m+1)/2) | 構成的証明と全 m の等号例を記録 | 正確な強化は一致未確認 |
| S2.3 | 全配置連結性の短区間による必要十分条件 | 証明を記録 | 一致未確認 |
| S2.4 | 適応半径の O(n log n) 計算法、コンパクト集合への拡張 | 証明と独立照合を記録 | 初等的な計算法・系。新規性は主定理と別に確認 |
| S2.5 | 独立性を外すと n−1 倍が必要になる | 明示的な反例を記録 | 仮定の必要性を示す境界例として扱う |

## 1. S1：枝分かれ空間の距離観測

### 1.1 対象と誤差モデル

有限本の正の長さの辺からなる、閉路のない連結空間 T を考える。辺の途中も点として含める「有限実木」であり、距離 d は道に沿った長さである。平面に描いたときの直線距離ではない。まず diam(T)>0 とする。

有限非空の基準点集合 S を固定し、観測写像と観測差を

\[
F_S(x)=(d(x,s))_{s\in S},\qquad
\rho_S(x,y)=\|F_S(x)-F_S(y)\|_\infty
\]

と定義する。三角不等式より常に ρ_S(x,y)≤d(x,y)。基準点が辺の途中にある場合も、その点で辺を分割すれば以下の議論は変わらない。

K=hull(S) を、全基準点を結ぶ最小部分木とする。π(x) は x から K への最近点で、一意である。K の外の部分木は、ただ一つの付け根を通って K とつながる。

### 1.2 S1.1：観測が残す情報の恒等式

p=π(x), q=π(y), h=d(x,p), k=d(y,q) とおく。このとき、単射性を仮定せず

\[
\boxed{\rho_S(x,y)=d(p,q)+|h-k|.}
\tag{T1}
\]

**証明。** 全ての s∈S について、木の道の一意性から d(x,s)=h+d(p,s)。p=q なら直ちに成立する。p≠q のとき D=d(p,q) とおく。K が S の凸包であるため、p,q 自身を含めて道 [p,q] の両側に基準点が存在する。従って d(p,s)−d(q,s) の最大値と最小値は D と −D である。他の値はこの間にあるので、

\[
\rho_S(x,y)=\max\{|h-k+D|,|h-k-D|\}=D+|h-k|.
\]

ここで「両側にある」は、端に一致する場合を含む。p 側に基準点が一つもなければ、p は基準点を結ぶ最小部分木に属せない。∎

**単射の必要十分条件。** 各付け根から K の外へ出る部分が、根を端点とする一本の区間であること。すなわち、同じ付け根から二本以上の枝が出ず、その先にも枝分かれがないことである。

実際、外向きの二方向が分かれると、分岐から等距離にある別々の点は同じ根と高さを持ち、(T1) で識別不能になる。逆に各根の外側が一本の区間なら、ρ=0 は根と高さの一致を意味し、その点自身が一意に決まる。K 上の点は高さ0として含まれる。

### 1.3 S1.2：最悪増幅率の厳密式

単射の場合に、正の長さを持つ外枝の付け根を b、その長さを L_b とする。異なる付け根間の距離を D_bc=d(b,c)>0 とおく。

\[
c(T,S):=\inf_{x\ne y}\frac{\rho_S(x,y)}{d(x,y)}
=\boxed{\min\left(\{1\}\cup
\left\{\frac{D_{bc}}{D_{bc}+2\min(L_b,L_c)}:b<c\right\}\right)}.
\tag{T2}
\]

b<c は、付け根対を重複なく数えるための任意の順序である。外枝が二本未満なら c=1。単射でなければ c=0。

**証明。** 同じ外枝内の二点、または少なくとも一方が K にある二点では ρ=d。異なる付け根からの高さ h,k の二点では

\[
\rho=D+|h-k|,\qquad d=D+h+k.
\]

h≥k と仮定すると、比は 1−2k/(D+h+k) なので h を k まで減らすと増えない。次に h=k の共通値を増やすと D/(D+2k) は減少する。従って h=k=min(L_b,L_c) で最小になる。有限個の付け根対で最小を取れば (T2) を得る。∎

最良の逆Lipschitz係数、すなわち位置差／観測差の最大倍率は 1/c である。この量は、基準点が何個あるかだけでは決まらない。近接した分岐から長い無観測枝が伸びると、任意に大きくなる。

### 1.4 S1.3：有限の誤差でどこまで曖昧になるか

δ≥0 に対して

\[
A_S(\delta):=\max\{d(x,y):\rho_S(x,y)\le\delta\}
\]

を定義する。最大値はコンパクト性で達成される。単射の場合の完全な式は

\[
\boxed{A_S(\delta)=\max\left(
\{\min(\delta,\operatorname{diam}T)\}
\cup\left\{
\min\bigl(D_{bc}+L_b+L_c,\ \delta+2\min(L_b,L_c)\bigr)
: b<c,\ D_{bc}\le\delta
\right\}\right).}
\tag{T3}
\]

**証明。** 異なる外枝の対では、制約は D+|h−k|≤δ。δ<D ならこの対は実行不可能である。δ≥D とし、L_b≤L_c としてよい。h+k の最大値は、短い枝を h=L_b とし、もう一方を k=min(L_c,L_b+δ−D) に取ることで達成される。従って最大距離は min(D+L_b+L_c,δ+2L_b)。

残る対の距離は δ 以下である。一方、直径を与える道上には min(δ,diam T) 離れた二点があり、ρ≤d だからその対は必ず実行可能。これで上界と達成が一致する。∎

**閾値の条件 D_bc≤δ は不可欠。A は連続とは限らない。** 二本以上の外枝があるとき

\[
\Delta=\min_{b<c}D_{bc}
\]

とすれば、0≤δ<Δ では A_S(δ)=δ。最初の閾値では

\[
A_S(\Delta)=\Delta+
2\max_{b<c:\,D_{bc}=\Delta}\min(L_b,L_c)>\Delta.
\tag{T4}
\]

つまり、誤差がある幅に達した瞬間に、離れた枝の候補が一斉に現れる。局所等長性の存在そのものは既存のtravel-time理論で扱われており、ここでは木に対して閾値と跳躍量を明示した。

### 1.5 非単射の場合を含む一般式

各付け根 b に付く外部部分木の最大高さを H_b>0 とする。これらを K から外向きに根付ける。付け根自身も含め、二方向以上に外向きに分かれる頂点 z について、分岐点 z から測った各外向き方向の最大距離のうち大きい二つを α_z≥β_z>0 とする。

このとき一般の有限非空 S について

\[
\boxed{\begin{aligned}
A_S(\delta)=\max\Big(&\{\min(\delta,\operatorname{diam}T)\}\\
&\cup\{\min(D_{bc}+H_b+H_c,\delta+2\min(H_b,H_c)):
b<c,\ D_{bc}\le\delta\}\\
&\cup\{\min(\alpha_z+\beta_z,\delta+2\beta_z):z\text{ は外向き分岐}\}\Big).
\end{aligned}}
\tag{T5}
\]

同じ根へ射影される二点が別方向へ分かれる場合、その最終共通点 z からの距離を u,v とすれば、ρ=|u−v|、d=u+v。長方形の中での最大化は (T3) と同じ計算になる。方向別の高さを増やすほど候補値は増えるので、各分岐では大きい二つだけを使えばよい。同じ方向の祖先・子孫の対では ρ=d。他の根の対は (T1) と H_b を用いる。この分類で全対を覆い、各項に達成点がある。

特に無誤差でも残る曖昧さは

\[
A_S(0)=2\max_z\beta_z
\]

であり、分岐がなければ0とする。これは単射条件と一致する。

### 1.6 S1.4：最良の決定論的推定誤差

受信値を y=F_S(x)+e とし、各成分の誤差を独立に −ε≤e_s≤ε の任意値とする。推定器 g は受信値から **T の任意の点**を返してよい。このモデルで

\[
E_S(\varepsilon):=
\inf_g\sup_{x\in T,\ \|e\|_\infty\le\varepsilon}
d\bigl(g(F_S(x)+e),x\bigr)
=\boxed{\frac{A_S(2\varepsilon)}2}.
\tag{T6}
\]

**上界。** y に整合する集合 C_y={x:||F_S(x)−y||∞≤ε} は非空ならコンパクトで、その直径は A_S(2ε) 以下。実木上の非空コンパクト集合は、直径対の中点を中心として直径の半分の半径で覆える。その点を返す推定器を選ぶ。実現不能な y での出力は任意でよい。

この半径の事実は、直径対 u,v とその中点 m、任意の z の [u,v] への射影 p を使えば、d(z,u),d(z,v)≤D から d(z,m)≤D/2 と分かる。中心を C_y 内に制約する必要はない。

**下界。** A_S(2ε) を達成する x,x' の観測ベクトルの座標ごとの中点を y とする。これは両者と整合する。どの出力 g(y) も三角不等式から、少なくとも一方の真値まで A_S(2ε)/2 以上離れる。∎

この半直径の結論は、情報半径・最適回復の既知の考え方と実木の外接半径の性質を使った帰結として扱う。**推定器が必ず観測と整合する点だけを返す、という追加制約の下では一般に成立しない。**

### 1.7 21倍の例での正確な閾値

幹線 S₁—b—c—S₂ の各辺長を1、bとcから外へ伸びる行き止まりを各10とする。二つの先端 X,Y の距離は21だが、基準点への観測はそれぞれ (11,12)、(12,11)。この木の直径は21、Δ=1、c=1/21 である。

\[
A_S(\delta)=\begin{cases}\delta&0\le\delta<1,\\21&\delta\ge1,\end{cases}
\qquad
E_S(\varepsilon)=\begin{cases}\varepsilon&0\le\varepsilon<1/2,\\21/2&\varepsilon\ge1/2.\end{cases}
\]

| 各観測の最大誤差 ε | 同じ受信値に整合し得る2点の最大隔たり | 最良の推定器の最悪位置誤差 |
|---:|---:|---:|
| 0.10 | 0.20 | 0.10 |
| 0.49 | 0.98 | 0.49 |
| 0.50 | 21.00 | 10.50 |
| 1.00 | 21.00 | 10.50 |

これは「観測誤差に応じて位置誤差が常に滑らかに増える」という期待の反例になる。最悪の場合についての主張であり、平均誤差や確率的な発生頻度を述べてはいない。

### 1.8 S1.5：基準点配置を葉の有限集合へ還元する

**定理。** |S|≥2 なら、T の葉だけからなる集合 S' で、|S'|≤|S| かつ

\[
\rho_{S'}(x,y)\ge\rho_S(x,y)\qquad(\forall x,y\in T)
\tag{T7}
\]

を満たすものが存在する。

**証明。** K の各葉を、K に戻らない方向に T の葉まで延長する。既に T の葉であれば動かさない。各延長は異なる葉に到達し、その集合 S' の凸包 K' は K を含む。K の各葉は S に属するので、個数は増えない。

固定した x,y に対し f(s)=d(x,s)−d(y,s) は、s の道 [x,y] への射影位置のアフィン関数である。任意の道上では一定または単調に変化するため、|f| の基準点凸包上での最大値は基準点上の最大値に等しい。K⊂K' から、

\[
\max_{s\in S}|f(s)|=\max_{s\in K}|f(s)|
\le\max_{s\in K'}|f(s)|=\max_{s\in S'}|f(s)|.
\]

これが (T7) である。∎

従って、全ての δ で同時に A_{S'}(δ)≤A_S(δ)。c も悪化しない。基準点の設置位置を自由に選べ、各点の費用が同じで、個数予算が m≥2 のとき、c の最大化や任意の誤差幅での最悪誤差最小化は、葉の部分集合を調べれば最適解を得られる。

予算が2個以上で元の集合が1点の場合は、先に任意の別の基準点を一つ加えてから定理を適用できる。これは連続配置から有限配置への厳密な還元である。葉数を ℓ とすれば、素朴には高々 min(m,ℓ) 個を選ぶ部分集合を列挙できる。**葉の個数に関する多項式時間アルゴリズムは本稿では証明していない。** また設置禁止場所・位置依存の費用・基準点1個だけの一般問題は対象に含めない。

### 1.9 境界と適用外

- T が一点なら位置誤差と曖昧さは常に0。c は空集合上の下限となるため、本稿では別規約を与えず定理の対象を diam(T)>0 に限定した。
- 閉路のある空間には、付け根への一意な射影や道の一意性をそのまま移せない。
- 基準点への距離を異なる速度・未知の開始時刻を含む到達時間で観測するモデル、距離ごとに誤差幅が異なるモデルは未検証。
- 木の構造そのものは既知とする。空間全体の復元と、既知の空間内での位置推定は異なる問題である。



## 2. S2：直線上の不確実な位置の接続

### 2.1. 定義と主定理

`n >= 2` とし、各点の独立した位置不確実性を閉区間

\[
I_i=[a_i,b_i]\subset\mathbb R,\qquad a_i\le b_i
\]

で表す。点区間、同一区間の重複、点の一致を許す。全域木は点のラベル `1,...,n` 上の木である。配置 `x=(x_1,...,x_n)` に対して

\[
B(x)=\min_T\max_{ij\in E(T)}|x_i-x_j|,
\quad R_A=\max_{x\in\prod_i I_i}B(x),
\]

\[
R_F=\min_T\max_{x\in\prod_i I_i}\max_{ij\in E(T)}|x_i-x_j|.
\]

有限個の木とコンパクト配置空間を扱うので、最大・最小はいずれも存在する。`R_A` は、配置に応じて接続木を選び直せる場合の、全配置を保証する最小通信距離。`R_F` は、先に固定した同じ木の全辺を全配置で使用可能にする最小通信距離。

**主定理（一般証明を記録）。**

\[
\boxed{R_A\le R_F\le\left\lceil\frac n2\right\rceil R_A.}
\]

右側の係数は各 `n >= 2` で最良である。

### 2.2. 距離 r での補題

以下、`r>0` とし、全ての許容配置について、距離 `r` 以下の点対を辺とするグラフが連結であると仮定する。

#### 補題1：長い区間の削除

区間 `I_i` の長さが `r` 以上なら、その点を削除しても、残りの各配置の距離 `r` グラフは連結である（残りが1点なら自明）。

**証明。** 残りの点のある配置が不連結だとする。実直線上では、ソート順に隣接した点 `u<v` の間に `g=v-u>r` の隙間がある。その隙間の左と右を追加の1点 `x` で接続するには

\[
x\in[v-r,u+r]
\]

が必要である。この区間が空でなければ、その長さは `2r-g<r` である。長さが `r` 以上ある `I_i` の全点をここに含めることはできない。従って許容される `x` のどれかでは元の全体グラフも不連結になり、仮定に反する。∎

この補題は繰り返して適用できる。以降は境界処理を簡潔にするため、削除対象を長さが **厳密に** `r` より大きい区間に限る。

#### 補題2：短い区間は少なくとも1本存在する

\[
S=\{i:b_i-a_i\le r\},\qquad m=|S|
\]

とおくと、`m>=1` である。

**証明。** 全区間の長さが `r` より大きいと仮定する。補題1を使って2本を残すまで削除する。残った2区間の長さを `w_1,w_2>r` とすれば、両区間間の最大距離は少なくとも

\[
\frac{w_1+w_2}{2}>r
\]

である。実際 `b_1-a_2` と `b_2-a_1` の和が `w_1+w_2` なので、その少なくとも一方はこの半分以上である。許容される2点配置に距離が `r` を超えるものが存在し、連結性に反する。∎

#### 補題3：短い区間だけなら固定木が距離 r で存在する

全区間の幅が `r` 以下で、全配置で距離 `r` 連結なら、同じ距離 `r` で全配置に使える固定全域木が存在する。

**証明。** 各区間について非空閉区間

\[
J_i=[b_i-r,a_i]
\]

を定義する。ラベル `i,j` を、全許容位置で距離 `r` 以下になる場合に結ぶ。その条件は

\[
b_i-a_j\le r,\quad b_j-a_i\le r,
\]

従ってちょうど `J_i` と `J_j` が交差することに等しい。

この交差グラフが不連結なら、有限個の閉区間の成分の間に正の隙間がある。隣接成分の間で、全ラベルを非空な左群 `L` と右群 `R` に分けると

\[
\max_{i\in L}a_i < \min_{j\in R}(b_j-r).
\]

左群では `x_i=a_i`、右群では `x_j=b_j` を選ぶ。その配置には幅 `r` より大きな隙間が生じ、連結性の仮定に反する。よって交差グラフは連結であり、その任意の全域木を固定木にできる。∎

補題1で長い区間を全て削除すると短い区間集合 `S` の全配置連結性が残り、補題3が適用できる。その固定距離 `r` グラフを `H` とする。

#### 補題4：長い区間の両端には、それぞれ確実に接続できる短い区間がある

長い区間 `I_i=[A,B]` を1本選ぶ。少なくとも1個の `u in S` が存在して

\[
\max_{y\in I_u}|A-y|\le r
\]

となる。同様に、少なくとも1個の `v in S` について `max_{y in I_v}|B-y|<=r` となる。

**証明。** `I_i` 以外の長い区間を全て削除すると、短い区間集合と `I_i` の全配置連結性が残る。`x_i=A` に固定する。仮に全ての短い区間 `I_j` について `|A-y_j|>r` となる位置 `y_j in I_j` を選べるなら、それらを独立に同時選択することで `A` が孤立する。従って、全ての位置で `A` と距離 `r` 以内にある短い区間が少なくとも1本ある。`B` も同様。∎

### 2.3. 主定理の構成的証明

`r=R_A>0` とする。上記の短い区間集合 `S`、そのサイズ `m>=1`、固定距離 `r` グラフ `H` を使う。

長い区間がなければ補題3より `R_F<=r` であり、証明が完了する。

長い区間 `I_i=[A,B]` を1本選び、補題4の短い区間 `u,v` を選ぶ。`H` 内の `u` から `v` への単純路を取る。仮想的な固定端点 `A,B` を加えると

\[
A\longrightarrow I_u\longrightarrow\cdots\longrightarrow I_v\longrightarrow B
\]

という、全ての辺が全配置で距離 `r` 以下である道が得られる。内部頂点は短い区間のラベルで、全辺数 `L` は高々 `m+1`。`u=v` の場合は2辺の道とする。

この道の中央の内部頂点 `j` を選ぶ。両端から `j` までの辺数はともに `ceil(L/2)` 以下である。各辺の距離保証と三角不等式により、`I_j` の任意の位置 `y` について

\[
|A-y|\le\left\lceil\frac L2\right\rceil r,
\qquad
|B-y|\le\left\lceil\frac L2\right\rceil r.
\]

実直線上では `|x-y|` の `x in [A,B]` に関する最大値は端点で達成される。従って

\[
\max_{x\in I_i,y\in I_j}|x-y|
\le\left\lceil\frac{m+1}{2}\right\rceil r.
\]

各長い区間に対し、このような短い区間を1本選んで固定辺を加える。短い区間の固定木と合わせると、全ての長い区間が葉となる固定全域木が得られる。長い区間が1本以上ある場合、`m<=n-1` なので

\[
R_F\le\left\lceil\frac{m+1}{2}\right\rceil r
\le\left\lceil\frac n2\right\rceil r.
\]

`R_A=0` の場合、どの配置でも距離0で全点が繋がる必要があるので、独立性から全区間が同一の点区間となり、`R_F=0`。最後に `R_A<=R_F` は、配置を見て木を選ぶ自由を許すと必要距離が増えないことから直ちに従う。∎

### 2.4. より強い定理と等号例

**短い区間数による強化（証明済み）。** `r=R_A>0`、`m=#{i:b_i-a_i<=r}` とする。

- 長い区間がなければ `R_F=R_A`。
- 長い区間があれば `R_F<=ceil((m+1)/2) R_A`。

後者は、任意の `m>=1` と任意の長い区間数 `k>=1` に対して最良である。

**等号構成。** `m` 本の固定点区間

\[
\{1\},\{2\},\ldots,\{m\}
\]

と、`k` 本の同一区間 `[0,m+1]` を使う。全ての可動点は固定点のどれかと距離1以内にあり、固定点の鎖も距離1で連結するので `R_A<=1`。可動点を全て0に配置すれば幅1の隙間が残るので `R_A>=1`。従って `R_A=1`。

長い区間同士の最悪距離は `m+1`。長い区間と固定点 `j` の最悪距離は `max(j,m+1-j)` で、その最小値は `ceil((m+1)/2)`。従ってこの値未満では長い区間はどの頂点とも固定辺を持てず、固定木は存在しない。一方、全長区間を中央の固定点に接続すればこの値で固定木ができる。

`k=1`、`m=n-1` とすれば元の `ceil(n/2)` の各点数に対する鋭さが得られる。

### 2.5. 路の短さによる実例ごとの改善

長い区間 `I_i=[A_i,B_i]` の両端に確実に距離 `r` で接続する短い区間の集合を、それぞれ `U_i,V_i` とする。短い区間の固定距離 `r` グラフを `H` とし、集合間最短路の辺数を

\[
d_i=\operatorname{dist}_H(U_i,V_i)
\]

とすれば、上の構成で

\[
R_F\le r\max\left\{1,\max_{i\notin S}\left\lceil\frac{d_i+2}{2}\right\rceil\right\}
\]

という実例ごとの証明書が得られる。長い区間がないときは右辺を `r` とする。これは最適な `R_F` の公式ではなく、構成的な上界である。

### 2.6. 計算検査の再現性

`spatial_research_verify.py intervals` は標準Pythonのみを使い、整数演算で以下を再現する。

1. 端点 `0,...,6` の全28種類の閉区間から、重複可・順序無視で `n=3,4,5` 本選ぶ。
2. 全 `2^n` の端点配置を列挙し、ソート後の最大隣接間隔の最大を `R_A` とする。
3. 完全グラフの辺重み `max(|a_i-b_j|,|b_i-a_j|)` にKruskal法を適用し、最大木辺を `R_F` とする。
4. 上の証明に対応した構成で固定木を実際に作り、短い区間の連結性、両端の確実な接続先、道の中央頂点による上界、全域木の辺数、強化上界を検査する。

端点配置だけで `R_A` が厳密に求まる理由: 任意配置の最大隙間で点を左右群に分け、左群の各点をその左端、右群をその右端へ動かす。隙間は減らず、端点配置が得られる。逆方向は端点配置が許容配置の一部なので自明。

前回検査と同じ母集団:

| n | 区間族数 | R_A=0 の例 | 最大比 R_F/R_A |
|---|---:|---:|---:|
| 3 | 4,060 | 7 | 2 |
| 4 | 31,465 | 7 | 2 |
| 5 | 201,376 | 7 | 3 |
| 合計 | 236,901 | 21 | — |

これらの有限検査は証明の代わりではない。主定理の一般的な根拠は上記の数学的証明である。

### 2.7. 任意のコンパクト集合への拡張と独立性の境界

**凸包不変性（証明済み）。** 各ラベルの不確実集合を任意の非空コンパクト集合 `U_i subset R` としても、これを閉区間 `I_i=[min U_i,max U_i]` に置き換えて `R_A` と `R_F` は変わらない。

`R_F` については、各点対の最大距離は互いの端点の組で達成されるためである。`R_A` については、区間族の任意配置の最大隙間で左右群を分け、左群を各集合の最小値、右群を各集合の最大値へ移すと隙間が減らない。移動先の全点は元のコンパクト集合に属する。従って区間族の `R_A` は元の集合族の `R_A` 以下で、逆不等式は配置空間の包含から従う。

従って主定理は、独立した任意非空コンパクト集合 `U_i subset R` にそのまま成り立つ。強化定理の短さは `diam(U_i)<=R_A` で判定すればよい。

**独立性を外すと主定理は偽。** 許容配置を、固定位置集合 `{0,1,...,n-1}` の全順列だけに限定する相関モデルを考える。各配置では隣接位置を結べるので `R_A=1`。一方、どのラベル対も許容配置のどれかで両端 `0,n-1` を占めるため、各固定辺の最大距離は `n-1` である。従って `R_F=n-1` となり、`n>=4` で `ceil(n/2)` 上界を破る。この相関モデルでは、各点の周辺的な不確実集合だけを用いると独立性の情報を失うため、凸包不変性を適用できない。

#### 2.7.1 全配置連結性の必要十分条件

任意の `r>0` に対し、幅が `r` 以下の区間を短い区間集合 `S` とし、その全配置で使える距離 `r` グラフを `H` とする。`n>=2` では、全配置が距離 `r` で連結であることは、次の3条件と同値である。

1. `S` が非空。
2. `H` が連結。
3. 各長い区間の両端について、その端点との距離が全位置で `r` 以下になる短い区間が存在する（両端で別の短い区間でよい）。

必要性は補題2〜4で証明済み。十分性を示すため、短い区間の任意配置を固定する。`H` の固定木があるので短い点の距離 `r` グラフは連結し、それらの閉 `r` 近傍の和集合は実直線上の1つの閉区間になる。条件3により各長い区間の両端がこの和集合に属するので、長い区間全体も含まれる。従って各長い点のどの位置も、短い点のどれかと距離 `r` 以下で結ばれる。

条件2が成り立つとき、条件3は各長い区間 `[A,B]` について

\[
A\ge\min_{j\in S} b_j-r,
\qquad
B\le\max_{j\in S} a_j+r
\]

と同値になる。確実に少なくとも1個の短い区間へ接続できる位置集合は

\[
\bigcup_{j\in S}[b_j-r,a_j+r]
=\left[\min_{j\in S} b_j-r,\max_{j\in S} a_j+r\right]
\]

だからである。等号は、`H` が区間 `[b_j-r,a_j]` の連結な交差グラフであることから従う。



## 3. 計算方法・独立監査・再現

### 3.1 適応半径の簡潔な高速公式

n≥2 とし、区間を左端の順 a₁≤⋯≤aₙ に並べる。同じ左端を持つ区間の順序は任意でよい。

\[
\boxed{R_A=\max\left\{0,
\max_{1\le k<n}\left(\min_{j>k}b_j-a_k\right),
\max_j b_j-a_n\right\}.}
\tag{I-fast}
\]

並べ替え後の右端のsuffix最小値を使えば O(n log n) 時間、O(n) 作業領域で計算できる。実数の比較・四則演算を一定費用とするモデルであり、有理数ビット長の費用は別に数える。

**証明。** 全配置の最大隣接gapの最大は、非空真部分集合 U を左側にする全てのcutについて

\[
R_A=\max_{\varnothing\ne U\subsetneq[n]}
\left(\min_{j\notin U}b_j-\max_{i\in U}a_i\right)
\]

で与えられる。任意配置の最大gapはそのcutの右辺以下で、正の右辺は左群の点を各左端、右群を各右端に置けば達成する。最大値が0の場合も R_A≥0 と合わせればよい。

任意のcutの t=max_{i∈U}a_i について、a_j>t の点が残っていれば、U を {i:a_i≤t} へ拡大してもgapは減らず、prefixの項に帰着する。残っていなければ t=a_n なのでgapは max_j b_j−a_n 以下。逆に各prefixは実際のcutであり、jを最大右端のラベルとして補集合を {j} にすれば、そのgapは b_j−max_{i≠j}a_i≥max_jb_j−a_n となる。∎

n=1 では R_A=R_F=0 と別に定義する。この場合に (I-fast) を適用すると、幅のある一区間で誤答になるので適用しない。

固定半径 R_F は、既知のrobust bottleneck原理によって、各辺の最悪距離を重みにした最小ボトルネック全域木で求まる。完全グラフの全辺を列挙する素朴なKruskal実装で O(n² log n) 時間である。第2節の構成は最良係数を保証する固定木を返すが、その木が各入力における R_F を必ず達成するという主張ではない。

### 3.2 検証の範囲

| 対象 | 方法 | 今回の結果 |
|---|---|---|
| S2の一般上界 | 短い区間の交差グラフを使う構成的証明 | 主本文に全証明を収録 |
| S2の独立証明 | 長区間の削除・幅の上界・左右の点数による帰納法 | 付録Aに収録。主証明とは別に導出 |
| 区間の全域木構成 | n=3,4,5、整数端点0〜6の全区間多重集合。全端点配置oracle・高速式・Kruskal・構成木の保証を整数演算で照合 | 236,901族、全件一致 |
| (I-fast)そのものの独立検査 | n=2,3,4、整数端点0〜6の全区間多重集合で、全cutと照合 | 35,931族、全件一致。上の母集団と重複するため合算しない |
| 木の係数 c | 80本の重み付き木。辺対の直線配置を有理数で厳密列挙 | 80件一致。単射60・非単射20 |
| 木の A_S(δ) | 各辺対で二変数半平面制約の頂点を有理数で厳密列挙。閾値の直前・一致・直後を含む | 586設定、全件一致 |
| 葉への優越 | 新旧観測差の全直線配置を共通細分し、その頂点で検査 | 4,707頂点、全件一致 |

木の検証は点を格子状に抜き出す方法ではなく、列挙した各木の**辺内部を含む連続領域**を最適化する。観測差を表す符号付きアフィン関数の最大値を直接扱い、幾何学的な射影公式を最適化oracleに使用しない。分岐構造から求める予測式と比較する。

比率の検査では、観測差のアフィン関数が切り替わる直線配置の各セル内で線形分数関数になる。分母が正のセルでは値は頂点値の範囲にあり、対角上で分母・分子が共に0の場合も、その点からの線分で比は一定なので欠落しない。葉優越の差は共通細分した各セルでアフィンになる。

80本は、明示した5例と seed=20260914 で生成した75例。辺長は正整数、頂点数3〜8を中心とする。基準点は頂点に置くが、次数2の点も含むため、辺を分割した内部基準点を含めて扱える。これは全ての木の列挙でも一般定理の形式証明でもない。

### 3.3 再現コード

同時に提供する `spatial_research_verify.py` は標準Pythonのみを使用する。数学的な比較に浮動小数は使用せず、整数または `fractions.Fraction` で処理する。

```bash
python spatial_research_verify.py all
python spatial_research_verify.py intervals --sizes 3 4 5 --max-endpoint 6
python spatial_research_verify.py trees
```

最初のコマンドで全検査を再現できる。木の全入力、各係数、閾値数、葉への移動結果は、実行したスクリプトと同じディレクトリの `tree_verification_results.json` に出力される。区間は全入力を規則から再生成する。簡易実行には `intervals --sizes 3 --max-endpoint 4` を使える。

高速の区間実装は (I-fast) と同値な「補集合が一点であるcut」の最大を用いる形で実装し、独立な全端点配置oracleと比較している。式に似たコードを二つ書いて一致を確認するだけの検査を避けた。

## 4. 新規性の照合と既知研究への帰属

照合日：2026 09 14。検索語の一致だけで判断せず、量化順序、目的関数、連続点かグラフ頂点か、測定誤差か基準点の故障かを比較した。以下の「一致未確認」は、世界の文献に存在しないという断定ではない。

### 4.1 S1に近い一次研究

| 一次資料 | 閲覧範囲と既知の内容 | 今回の位置づけ |
|---|---|---|
| [Khuller・Raghavachari・Rosenfeld, Localization in Graphs](https://drum.lib.umd.edu/bitstreams/fc568aaf-1954-4721-9884-854431b48e67/download) | 技術報告本文 §2.1、補題2.1–2.3、定理2.4。木の脚と基準点の識別構造、葉による最小基準点構成 | 単射条件や最小識別集合を葉に置く発想を新規扱いしない |
| [Beardon・Rodríguez-Velázquez, On the k-metric Dimension of Metric Spaces](https://arxiv.org/html/1603.04049v1) | 本文の距離写像・二等分集合・冗長識別の定義 | 距離座標という枠組みは既知 |
| [Ilmavirtaほか, Lipschitz Stability of Travel Time Data](https://arxiv.org/html/2410.16224v1) | 定義1–4、注意11、命題13・17・23など。supノルムの同一距離写像、全葉観測の実木の等長性、局所逆写像の性質 | 最も近い理論。一般的な安定性の存在を発見とはしない。枝長による正確な係数と誤差曲線を照合対象にする |
| [Aksoy・Oikhberg, Some results on Metric Trees](https://arxiv.org/html/1007.2207v1) | 定義6.1、定理6.2、注意6.4。実木内の有界集合の中心と半直径の性質 | 最良推定誤差が A(2ε)/2 になる議論で使う既知の幾何学的原理 |
| [Leほか, Landmark-Based Node Representations for Shortest Path Distance Approximations in Random Graphs](https://arxiv.org/html/2504.08216v2) | Algorithm 1、定理4.1など。ランドマーク距離座標と定量的な距離歪み | 「一意性から定量的歪みへ」だけでは新規性にならない。今回の有限実木・固定集合・厳密係数に絞る |
| [Mürmannほか, Reducing Sensor Requirements by Relaxing the Network Metric Dimension](https://arxiv.org/html/2505.11193v2) | 定義2.2、定理3.1–3.2等。等しい観測なら近い頂点であるという緩和識別 | 数値観測に誤差を許す本稿とは異なる。微小な非零差を完全識別とするモデルとの差を明示 |
| [Gotsman・Hormann, On Landmark Distances in Polygons](https://doi.org/10.1111/cgf.14373) | 出版社要約など。全文PDFは今回取得できず | 関連する未読全文として残す。本文に同一の補題がないとは判断していない |

強距離次元の等長な場合も既知であり、木で全葉のうち一つを除いて観測すればよいという基本事実は今回の新規主張に含めない。[関連する一次研究の §5](https://arxiv.org/html/1504.04820v1)

新規性候補として残す正確な範囲は、(T2) の任意固定集合の最良係数、(T3)/(T5) の有限誤差曲線、および (T7) の同じ予算による全点対同時の優越である。(T6) は既知の中心原理を使う系として位置づける。

### 4.2 S2に近い一次研究

| 一次資料 | 閲覧範囲と既知の内容 | 今回との差 |
|---|---|---|
| [Chambersほか, Connectivity Graphs of Uncertainty Regions](https://arxiv.org/html/1009.3469v4) | 定義、結果、§5、結論。Worst-Case Connectivity with Uncertaintyは R_A と同じ目的。単位円盤で中心の固定木による近似を扱う | 任意幅の直線上の不確実集合に対する ceil(n/2) と短い集合数の最良係数は見つからなかった。円盤半径と辺の通信距離の2倍換算に注意 |
| [Kasperski・Zieliński, Bottleneck combinatorial optimization problems with uncertain costs and the OWA criterion](https://arxiv.org/pdf/1307.4521) | 定義と §3 冒頭。robust bottleneck は各要素の最大シナリオ費用で置換して解ける | R_F の最大距離重み付き全域木への帰着は、この既知原理の特殊化 |
| [Connectivity with Uncertainty Regions Given as Line Segments](https://doi.org/10.1007/s00453-023-01200-5) | 要約、導入、関連研究、結果。線分上から有利な点配置を選ぶ問題のFPTアルゴリズム | min_x min_T のbest-caseであり、本稿の max_x min_T とは異なる |
| [Bougeret・Omer・Poss, Optimization problems in graphs with locational uncertainty](https://arxiv.org/html/2109.00389v4) | 定義、複雑さ、近似、結論。先にグラフを固定した後の最悪配置を扱う | 目的は辺長の合計。本稿の最大辺長の比を直接与えない |
| [Bougeret・Omer・Poss, Approximating optimization problems in graphs with locational uncertainty](https://arxiv.org/html/2206.08187v3) | 目的、一般還元、近似定理 | 固定グラフで「和の最大」と「最大の和」を比較する。木を配置の前後どちらで選ぶかという本稿の比とは異なる |

このほか、MST with neighborhoods、adversarial TSP、interval dispersion、color-spanning connectivity の一次資料も、全文の関連節または要約の閲覧範囲を区別して確認した。目的が全辺長の合計、最小点間距離、best-case選択である結果は、本稿の最良係数の根拠にも反証にも用いていない。

### 4.3 調査の限界と公開時の言い方

検索には resolving set、metric generator、strong metric dimension、landmark distortion、inverse-Lipschitz、travel-time representation、optimal recovery、locational uncertainty、worst-case connectivity、adaptivity gap、every transversal、interval graph などの用語を使った。定理が固まった後に、short-core と全点対の葉優越にも照合を追加した。

ただし、MathSciNet/Zentralblatt、全ての学位論文、全ての被引用文献、未取得の原著全文を網羅した調査ではない。数学的な証明の正しさと、先行発表の有無は別々に評価する。

公開時に適切な表現は次である。

> 有限実木の距離観測について厳密な安定性係数・誤差曲線を導出し、独立な直線上の位置不確実性について固定／可変接続の最良係数を証明した。距離座標、安定性の一般論、WCU、robust bottleneck の最大費用還元は既存研究である。今回照合した一次資料では、ここで述べた正確な係数・構造定理と同一の結果を特定できていない。新規性は独立確認を待つ。

## 5. 訂正・失敗しやすい推論・次の問い

| 論点 | 本稿で採用する正確な扱い |
|---|---|
| 前回は ceil(n/2) が予想だった | 今回、一般証明と全 n の達成例を記録。予想の状態を更新 |
| 短い区間だけの固定接続に2r必要という粗い見積り | 交差区間 J_i=[b_i−r,a_i] によって r で十分と分かった |
| 各頂点に近い隣接先があるだけで全体連結とする | それだけでは不足。独立証明では削除後の帰納法を必ず組み合わせる |
| 小さい観測誤差なら、誤差を増やしても滑らかに劣化する | (T3) は閾値で跳躍する。D≤δ の条件を落とさない |
| 推定器の最適中心は必ず観測に整合する | 一般には違う。(T6) の出力制約を明記 |
| 葉に最小識別集合を置けること自体を新規とする | 既知。今回の検討対象は全点対の数値的優越 |
| 独立な不確実集合と相関のある全配置集合を同一視する | 全順列の相関反例では n−1 倍になる |
| 有限検査・複数AIの一致を形式証明や人間査読と呼ぶ | いずれも未実施。証明本文と検査の実際の範囲を提示 |

次の研究として具体的に残るのは、(i) S1の葉部分集合最適化を効率よく解くアルゴリズム、(ii) 閉路が一本ある空間や異なる誤差幅への拡張、(iii) S2で最良係数を達成する全ての区間族の分類、(iv) 正確な命題ごとの文献追跡と外部レビュー、(v) 幾何学の定式化を含む証明支援系への移植である。

現段階で「空間一般を解いた」「新定理が学術的に確定した」とは主張しない。一方で、今回の二つの研究には、仮定・結論・達成例・完全な証明・再現コードを備えた検証可能な単位ができている。



## 付録A：S2の独立した帰納的証明

以下は主本文の交差区間による証明と別に導出した英語の証明記録。両方とも通常の数学的論証であり、証明支援系による形式証明ではない。

### A. Setting and claim

Let n >= 2 and let I_i = [a_i,b_i] be nonempty bounded closed intervals on the real line. A realization independently selects x_i in I_i. Let T range over spanning trees on the labelled vertex set {1,...,n}. Define

R_A = max_x min_T max_{ij in T} |x_i-x_j|,

R_F = min_T max_x max_{ij in T} |x_i-x_j|.

Then

**R_F <= ceil(n/2) R_A.**

The factor is sharp for every n >= 2, including both parities.

For a realization, its optimal bottleneck spanning-tree value is the largest consecutive gap after sorting its n coordinates (ties allowed). Thus R_A <= r means that every realization has all consecutive gaps <= r. Call such a family universally r-connected.

For distinct labels define the robust edge weight

d_ij = max(b_i-a_j, b_j-a_i).

This is exactly max_{x_i in I_i,x_j in I_j}|x_i-x_j|. Consequently R_F is the minimum bottleneck of a spanning tree in the complete graph with weights d_ij. It suffices to prove that the graph containing edges d_ij <= ceil(n/2)r is connected whenever the family is universally r-connected.

### A. Lemma 1: deleting a long interval

Assume r > 0. If a universally r-connected family contains an interval I_i of length at least r, deleting that interval leaves a universally r-connected family.

Proof. Otherwise some fixed realization of the remaining labels has a consecutive gap (y,z) of length g = z-y > r. For an added point x_i to remove every gap larger than r across this particular gap, it must lie in

[z-r, y+r].

This interval has length 2r-g < r; if its endpoints are reversed, it is empty. Since all choices x_i in I_i must work, I_i would have to be contained in this interval, contrary to its length being at least r. A remaining singleton is universally r-connected by convention. QED.

### A. Lemma 2: width bound for a deletable interval

Assume n >= 2, the full family is universally r-connected, and deleting I_i leaves a universally r-connected family. Then

b_i-a_i <= n r.

Proof. Put L = min_{j != i} b_j and R = max_{j != i} a_j. If a_i < L-r, select x_i=a_i and x_j=b_j for all j != i; x_i is isolated from the others by a gap > r. Hence a_i >= L-r. The symmetric realization x_i=b_i, x_j=a_j gives b_i <= R+r.

It remains to show R-L <= (n-2)r. If R <= L this is immediate. If R > L, the labels attaining R as a left endpoint and L as a right endpoint must be distinct. Choose those two endpoints in a realization of the remaining n-1 labels. The span of that realization is at least R-L and, by universal r-connectivity, is at most (n-2)r. Therefore

b_i-a_i <= R-L+2r <= nr.

QED.

### A. Lemma 3: robust neighbor by a two-sided counting argument

Assume r > 0, the n-interval family is universally r-connected, k is a positive integer with 2k >= n, and a distinguished interval I_i has width <= 2kr. Then some j != i satisfies d_ij <= kr.

Proof. Suppose every d_ij > kr. Define

ell = b_i-kr,    u = a_i+kr.

The width assumption implies ell <= u. For each j != i, the inequality d_ij > kr says that at least one of the following holds:

a_j < ell,    b_j > u.

Independently select a bad endpoint for every other label: choose a_j < ell whenever possible; otherwise choose b_j > u. The selected points partition into a left group of size p, with all coordinates < ell, and a right group of size q, with all coordinates > u. We have p+q=n-1.

Both groups are nonempty. If the right group were empty, choosing x_i=b_i would leave a gap > kr >= r between x_i and all remaining points. If the left group were empty, x_i=a_i gives the symmetric contradiction.

Now keep all selected endpoints fixed and choose x_i=a_i. Let z be the first right-group point. Then z-a_i > kr. All selected points strictly between a_i and z belong to the left group, so there are at most p of them. Universal r-connectivity therefore gives z-a_i <= (p+1)r. It follows that p+1 > k, and since p and k are integers, p >= k.

Next choose x_i=b_i. Let y be the last left-group point. Then b_i-y > kr, and at most q right-group points lie strictly between y and b_i. The same argument gives q >= k.

Thus n-1 = p+q >= 2k >= n, a contradiction. QED.

The strict inequalities here matter: d_ij > kr gives distances strictly greater than kr, forcing at least k intermediary points, rather than merely k-1.

### A. Main theorem by induction

It suffices to prove the graph statement for every r > 0 and n >= 2.

Base n=2: universal r-connectivity says precisely d_12 <= r, and ceil(2/2)=1.

Inductive step n>=3: put k=ceil(n/2), so k>=2 and 2k>=n.

Case 1: some interval has width >= r. Delete it using Lemma 1. By induction, the robust graph on the remaining n-1 labels is connected at threshold ceil((n-1)/2)r <= kr. Lemma 2 bounds the deleted interval's width by nr <= 2kr. Lemma 3 supplies a robust edge of weight <= kr from it to a remaining label. Adding that edge proves connectivity on all n labels.

Case 2: every interval has width < r. Choose its midpoint c_i=(a_i+b_i)/2 and half-width h_i=(b_i-a_i)/2 < r/2. Sort the midpoints. Since their realization is r-connected, consecutive midpoint gaps are <= r. For each consecutive pair i,j,

d_ij = |c_i-c_j| + h_i+h_j < 2r <= kr.

Their consecutive-pair path is therefore a spanning tree in the robust graph. This completes the induction.

Take r=R_A if R_A>0. If R_A=0, every realization consists of equal coordinates. Independence then forces every interval to be the same singleton, so R_F=0 as well.

### A. Sharpness

Take n-1 singleton intervals at 1,2,...,n-1 and one moving interval [0,n]. Every realization has consecutive gaps at most 1, and the realization with moving point 0 has a gap 1; hence R_A=1.

Every spanning tree must attach the moving label to at least one singleton t in {1,...,n-1}. That edge has robust weight

max(t,n-t) >= ceil(n/2).

Conversely, connect the singleton labels consecutively and attach the moving label to an integer t nearest n/2. The robust bottleneck is ceil(n/2). Therefore R_F=ceil(n/2), proving sharpness.

