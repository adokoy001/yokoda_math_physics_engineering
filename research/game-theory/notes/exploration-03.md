# 数学探索・第二弾の深掘り：共有誤差の校正と、監査パターン不足の厳密な損失

2026 09 10 ／ 第1版

前ノート『game-theory-exploration-02.md』の続編。今回は評価誤差に対する「改善を採用する最低幅」、および均一な個別監査率を仮定しない監査設計へ進めた。途中で、監査の結果が強正則グラフ上の確率制限付きゲームの特殊例になることも導いた。

**数学的状態：一般の証明と達成構成を収録し、独立したAI担当による監査と計算照合を実施した。形式証明・人間の専門家による査読は未実施。学術的新規性は未確定。**

## 1. 今回残す成果

| ID | 結果 | 証明の状態 | 新規性の暫定評価 |
|---|---|---|---|
| G04 | 共有されたベクトル誤差に対する、個人別の改善閾値の必要十分条件 | 明示的ポテンシャルと反例構成を証明 | 同一の一様な必要十分条件は今回未確認。主要候補 |
| G04-C | スカラー感度での最小費用校正、ベクトル版の線形計画 | 証明 | 重み付き中央値・LP双対は既知。G04の応用として扱う |
| G05 | 毎回２対象を外す監査で、１パターンの確率を減らしたときの正確な最適値 | 上界と達成戦略を証明 | 具体的な確率不足曲線は同一結果未確認。主要候補 |
| G05-C | 均一監査率を要求した場合との厳密な比較 | 証明 | G05と比較するための系 |
| G06 | 確率上限を持つ１頂点を含む、強正則グラフ上のゲームの厳密解 | 一般の証明・独立監査・13グラフで検証 | G05を含む一般化。分数全支配・制約付き行列ゲームとの追加照合が必要 |
| G07 | ４パターン以下の監査の完全分類、追加１パターンが無益な領域 | 証明と構成 | 正の値が可能になる境界は既知の被覆数に含まれる。重み付きの完全最適値は同一結果未確認 |

## 2. G04：誤差感度の差に合わせた、最小限の変更閾値

### 2.1 モデルと重要な量化

有限で空でない行動集合の直積を \(S=\prod_i S_i\) とする。全員に共通する真の目的を任意の実数値関数 \(\Phi:S\to\mathbb R\) とする。各人が使う固定の評価は

\[
U_i(s)=\Phi(s)+\langle a_i,h(s)\rangle.
\]

\(h:S\to\mathbb R^d\) は全員が共有する固定の誤差ベクトルで、任意の固定ノルムについて \(\|h(s)\|\le\varepsilon\) とする。\(a_i\in\mathbb R^d\) は誤差への感度、\(\|\cdot\|_*\) は双対ノルムである。

変更は一人ずつ行い、プレイヤー \(i\) は見かけの利益が \(\gamma_i\ge0\) を**厳密に超える**場合だけ変更する。つまり \(U_i(t)-U_i(s)>\gamma_i\)。

以下の必要十分性は、**すべての \(\Phi\)、すべての許された固定 \(h\) に対して保証する**命題である。既に決まっている特定の \(\Phi\) だけを考えるなら、もっと小さな閾値でも止まる場合がある。少なくとも２行動を持つ人を「有効なプレイヤー」とし、条件はその人たちの間だけに課す。

### 2.2 鋭い必要十分条件

**定理 G04。** 上のクラスのすべてのゲームで、受理される変更列が必ず有限になる必要十分条件は

\[
\boxed{\gamma_i+\gamma_j\ge
2\varepsilon\|a_i-a_j\|_*\quad\text{（全有効ペア）}.}
\]

条件が等号でも保証は成立する。これは変更条件が \(>\gamma_i\) であるためで、\(\ge\gamma_i\) に置き換えた命題ではない。

**十分性の証明。** 同じ状態での評価差は

\[
|U_i(s)-U_j(s)|\le\varepsilon\|a_i-a_j\|_*
\le\frac{\gamma_i+\gamma_j}{2}.
\]

次の明示的な関数を置く。

\[
\boxed{W(s)=\max_i\{U_i(s)-\gamma_i/2\}.}
\]

各人 \(i\) について、最大値の \(i\) 項から下界、ペア条件から上界を得るので、

\[
U_i(s)-\gamma_i/2\le W(s)\le U_i(s)+\gamma_i/2.
\]

従って、\(i\) の受理される変更では

\[
W(t)-W(s)\ge U_i(t)-U_i(s)-\gamma_i>0.
\]

\(W\) が厳密に増えるため同じ状態を再訪できず、実際に受理される変更は高々 \(|S|-1\) 回である。□

この十分性の証明は、共通誤差の線形モデルに限らず、上の点ごとの評価差条件を満たす任意の固定評価表に対して働く。

**必要性の構成的証明。** あるペアで条件が破れるとする。\(a_j-a_i\) の双対ノルムを達成するノルム１のベクトル \(v\) を選び、

\[
A=\langle a_i,v\rangle,\quad B=\langle a_j,v\rangle,
\quad B-A=\|a_j-a_i\|_*
\]

とする。有限次元なので達成ベクトルが存在する。

\[
L=\gamma_i+2\varepsilon A,
\quad R=2\varepsilon B-\gamma_j,
\quad q=(L+R)/2
\]

と置く。条件の違反から \(L<R\)。２人の２択部分ゲームで、

| 状態 | \(h\) | \(\Phi\) |
|---|---|---:|
| 00、11 | \(+\varepsilon v\) | 0 |
| 10、01 | \(-\varepsilon v\) | \(q\) |

と設定する。\(00\xrightarrow{i}10\xrightarrow{j}11\xrightarrow{i}01\xrightarrow{j}00\) の一周で、\(i\) の２変更の利益は \(q-2\varepsilon A>\gamma_i\)、\(j\) の２変更の利益は \(-q+2\varepsilon B>\gamma_j\)。全変更が受理される循環となる。他の状態では \(\Phi,h\) を任意に延長すればよい。□

### 2.3 共通閾値と、誤差の共通成分

全員に同じ閾値を使う場合、最小の一様保証値は

\[
\boxed{\gamma_{\rm universal}
=\varepsilon\max_{i,j}\|a_i-a_j\|_*.}
\]

スカラー感度では \(\varepsilon(\max_i a_i-\min_i a_i)\)。したがって、効くのは感度の絶対的大きさでなく、感度間の開きである。全感度に同じベクトルを加えた部分は共通目的へ吸収できる。

例えば誤差振幅上限が0.1、スカラー感度が1、1.2、1.5なら、共通閾値0.05を超える変更だけを受理すれば、このモデルのすべての固定目的・固定誤差について循環しない。これより小さい共通閾値では、ある目的と誤差を選んで循環を作れる。

### 2.4 なぜベクトル版が役に立つか

\(W\) は

\[
W(s)=\Phi(s)+\max_i\{\langle a_i,h(s)\rangle-\gamma_i/2\}
\]

と書ける。誤差に対して区分線形の関数であり、単一の係数 \(\alpha\) による \(\Phi+\langle\alpha,h\rangle\) に限定する必要がない。

例として、ユークリッド平面の感度ベクトルが一辺１の正三角形の頂点で、\(\varepsilon=1\) とする。G04は共通閾値１で保証する。一方、各人の誤差を同じ線形係数へ寄せ、\(2\|a_i-\alpha\|\) で評価する方式では、最小包含円の半径 \(1/\sqrt3\) により \(2/\sqrt3\approx1.1547\) が必要になる。

これはその線形な証明方式が保守的になる例である。特定の \(\Phi,h\) に対して、あらゆる線形ポテンシャルが使えないという一般主張ではない。

### 2.5 個人別の閾値を最小費用で決める

スカラー感度、\(\varepsilon>0\)、費用重み \(w_i>0\) とする。ペア条件は区間

\[
I_i=[a_i-\gamma_i/(2\varepsilon),\ a_i+\gamma_i/(2\varepsilon)]
\]

がすべて共通部分を持つことと同値である。区間では、ペアごとに交わることと全体で交わることが同値だからである。

従って、\(\sum_i w_i\gamma_i\) の最小化は

\[
\boxed{\min_\alpha 2\varepsilon\sum_iw_i|a_i-\alpha|}
\]

に帰着し、重み付き中央値 \(\alpha\) と \(\gamma_i=2\varepsilon|a_i-\alpha|\) で最適化できる。重み付き中央値自体は古典的な最適化結果であり、新規性を主張しない。

ベクトル感度では、正確な校正費用は線形計画

\[
\min_{\gamma\ge0}\sum_i w_i\gamma_i,
\qquad \gamma_i+\gamma_j\ge2\varepsilon\|a_i-a_j\|_*
\]

となる。双対は

\[
\max_{y_{ij}\ge0}2\varepsilon\sum_{i<j}\|a_i-a_j\|_*y_{ij},
\qquad\sum_{j\ne i}y_{ij}\le w_i.
\]

これは既知のLP双対で、近似的な幾何学的中央値への置き換えは不要である。\(\varepsilon=0\) なら全閾値０で足りる。

### 2.6 停止性の意味と限界

保証するのは「受理された一人変更の列が有限」という性質。外部の実行器が永遠に何もしない場合の時間的な終了や、真の目的の大域最適性は保証しない。極大な変更列の終点では、各人の見かけの改善余地が \(\gamma_i\) 以下となる。

状態を再訪したときに誤差表が変わる場合、同時変更、基準目的の変更は対象外である。また、この必要性は任意の実数値目的に対する一様保証。前ノートの固定目的 \(\Phi=xy\) の正の誤差境界とは量化が違い、矛盾しない。

## 3. G05：監査予定を一つ減らすコストを正確に求める

### 3.1 ゲームと既知の還元

\(n\ge5\) 対象のうち、毎回 \(k=n-2\) 対象を監査する。攻撃側は、実現した予定を知らずに１対象を選び、その対象の監査有無を正確に観察してから攻撃対象を選ぶ。観察した対象自身への攻撃も許す。監査対象への攻撃は確実に検出され、利得は対象によらず同じである。

監査予定の確率と、個別対象の監査率は自由。均等にする仮定はない。既知の１対象漏洩モデルから、監査側の値は

\[
V(w)=\min_{i\ne j}\Pr(i,j\text{がともに監査される})
\]

となる。この還元自体は[Xuらの研究](https://arxiv.org/html/1504.06058v2)に属する。

各予定を「監査から外す２対象」のペア \(e\) で表す。可能な予定は \(N=\binom n2\) 個。攻撃対象のペアと未監査ペアが交わらないときに検出されるので、ペア \(ij\) の同時監査率は、\(ij\) と交わらない未監査ペアの確率和である。

### 3.2 使用確率に上限を置いた場合の厳密解

指定した１予定 \(ab\) の確率を \(w_{ab}\le\rho\) に制限する。ただし \(0\le\rho\le1/N\)。他の予定に制約は置かない。

**定理 G05。** この制約下での最適検出率は

\[
\boxed{T_n(\rho)=
\frac{(n-3)(n-4+2\rho)}{n^2-3n-2}.}
\]

以下では \(r=n-2\)、\(D=r^2+r-4=n^2-3n-2\)、\(R=[n]\setminus\{a,b\}\) と置く。

**任意の監査戦略に対する上界証明。** \(x=w_{ab}\)、\(A\) を \(R\) 内部の未監査ペアに置く総確率とする。まず \(q_{ab}=A\)。一方、\(R\) 内部の攻撃ペアについて同時監査率を平均すると

\[
\overline q_R=
\frac{r-2}{r}
-\frac{2(r-2)}{r(r-1)}A
+\frac{2x}{r}.
\]

この式は、実現した未監査ペアが \(ab\)、\(R\) 内部、または交差ペアのいずれかにあるかで数えれば得られる。重みの対称性は仮定していない。

従って \(V(w)\le\min(A,\overline q_R)\)。一方は \(A\) に関して増加し、他方は減少するので、その交点が最も高い上界となる。交点は

\[
A=\frac{(r-1)(r-2+2x)}D=T_n(x)\le T_n(\rho).
\]

**達成戦略。** \(x=\rho\)、\(A=T_n(\rho)\) として次の確率を使う。

| 未監査ペアの種類 | 個数 | 各ペアの確率 |
|---|---:|---:|
| 指定ペア \(ab\) | 1 | \(\rho\) |
| \(\{a,b\}\) と \(R\) の間 | \(2r\) | \((1-\rho-A)/(2r)\) |
| \(R\) 内部 | \(\binom r2\) | \(2A/[r(r-1)]\) |

確率は非負で総和１。この戦略の \(q_{ab}\) と全 \(R\) 内部のペア率は \(A\) に等しい。交差する攻撃ペアの値と \(A\) の差は

\[
\frac{(r-1)(1-N\rho)}{rD}\ge0.
\]

よって最小値は \(A=T_n(\rho)\) であり、上界を達成する。□

達成戦略は、\(\rho=0\) の戦略と全予定の一様分布を、重み \(1-N\rho\) と \(N\rho\) で混ぜたものでもある。

### 3.3 攻撃側の短い証明書

上界には、次の固定されたランダム攻撃を使う別証明もある。確率 \(\theta=2(r-2)/D\) でペア \(ab\) を使い、残りで \(R\) 内部のペアを一様に選ぶ。ペアを使うとは、一方を観察し、未監査なら自身、監査されていればもう一方を攻撃することを意味する。

この方策の検出率は、未監査ペアが \(ab\) 以外なら常に \(T_n(0)\)、\(ab\) なら \(1-\theta\)。従って監査側がどんな分布を使っても検出率は

\[
T_n(0)+\frac{2(r-1)}D w_{ab}\le T_n(\rho)
\]

になる。これは、監査側の達成戦略と対になる上界証明書である。

### 3.4 欠落損失と、ほぼ最適な分布の必要条件

予定を制限しない最適値は

\[
\alpha=\frac{(n-2)(n-3)}{n(n-1)}=T_n(1/N).
\]

１予定でも欠ければ、値は高々 \(T_n(0)\) になる。従って最適値からの損失は少なくとも

\[
\boxed{\Delta_n=\frac{4(n-3)}{n(n-1)(n^2-3n-2)}.}
\]

これは \(N-1\) 個の予定で達成できる正確な損失である。

さらに、最適値からの損失が \(\delta\) 以下の分布では、**すべての予定**について

\[
\boxed{w_e\ge
\max\left(0,\frac1N-\frac{(n^2-3n-2)\delta}{2(n-3)}\right)}
\]

が必要である。各予定の重みが \(1/N\) 以下ならG05を適用し、それより大きければ不等式は自動的に成立する。

従って \(\delta<\Delta_n\) という精度を要求するなら、どの予定も削れない。これは厳密最適だけでなく、近似最適についての定量的な必要条件である。

### 3.5 G05-C：均一監査率を要求した場合との比較

各対象を監査から外す確率を \(2/n\) に揃える条件を追加すると、

\[
q_{ab}=1-\frac4n+w_{ab}
\]

なので、最適値は高々 \(1-4/n+\rho\)。この値も達成でき、

\[
\boxed{T_n^{\rm uniform}(\rho)=1-\frac4n+\rho.}
\]

\(\rho=0\) の達成分布は、交差未監査ペアに各 \(2/[n(n-2)]\)、内部ペアに各 \(2(n-4)/[n(n-2)(n-3)]\) を置く。どの対象も確率 \(2/n\) で外される。この分布を全予定一様分布と \(N\rho\) の割合で混ぜれば、一般の \(\rho\) を達成する。全未監査ペアの重みが \(\rho\) 以上なので、他のペア率も指定ペア率以上となる。

均一性を外すことによる改善幅は正確に

\[
\boxed{T_n(\rho)-T_n^{\rm uniform}(\rho)
=\frac{2(n-4)}{n(n^2-3n-2)}(1-N\rho).}
\]

例：５対象・３監査で１予定が欠けるとき、均一監査率では最適値20％、均一性を外すと25％である。これはこのモデル内の性能比較であり、現実の公平性の価値を否定する主張ではない。

## 4. G06：強正則グラフ上のゲームへの一般化

### 4.1 対称な自己同型を仮定しない一般形

単純無向グラフ \(G\) の頂点数を \(v\)、各頂点の次数を \(r\) とする。隣接する２頂点の共通隣接頂点数を \(\lambda\)、隣接しない２頂点の共通隣接頂点数を \(\mu\) とし、どのペアでもそれぞれ一定と仮定する。これがここで使う強正則性である。

\[
0<r<v-1,\qquad \mu>0,\qquad\mu\ge\lambda
\]

を仮定する。防御側は頂点上の確率分布 \(w\) を選び、攻撃側は頂点 \(x\) を選ぶ。検出率を \(x\) の開近傍の確率和 \(\sum_{y\sim x}w_y\) とする。指定頂点 \(o\) の確率だけを \(w_o\le\rho\le1/v\) に制限する。

**定理 G06。** 最適値は

\[
\boxed{T_G(\rho)=
\frac{\mu+(r-\mu)\rho}{r+\mu-\lambda}.}
\]

頂点推移性や、隣接・非隣接クラス内の自己同型の存在は仮定しない。

### 4.2 証明

\(x=w_o\)、\(A=\sum_{y\sim o}w_y\)、\(q=v-r-1\) と置く。指定頂点の検出率は \(A\)。\(o\) の隣接頂点を攻撃した場合の検出率の平均は、共通隣接点数を数えると

\[
B(A,x)=\frac{\mu+(r-\mu)x+(\lambda-\mu)A}{r}.
\]

従って値は \(\min(A,B(A,x))\) 以下。\(\mu>\lambda\) なら２直線の交点、\(\mu=\lambda\) なら一定の \(B\) が上界を与え、いずれも \(T_G(x)\le T_G(\rho)\) を得る。

達成戦略は、指定頂点に \(\rho\)、その各隣接頂点に \(T_G(\rho)/r\)、それ以外の各頂点に

\[
\frac{1-\rho-T_G(\rho)}{v-r-1}
\]

を置くもの。強正則性の恒等式

\[
r(r-\lambda-1)=(v-r-1)\mu
\]

より \(T_G(1/v)=r/v\)。また \(r\ge\mu\) なので \(T_G\) は非減少で、\(\rho\le1/v\) では \(T_G(\rho)\le r/v\)。ゆえに確率は非負である。

指定頂点とその全隣接頂点の検出率は \(T_G(\rho)\) になる。残りの頂点では共通の値 \(C\) となり、全行の値の和が次数 \(r\) であることから

\[
(r+1)T_G(\rho)+(v-r-1)C=r.
\]

従って \(C-T_G(\rho)=[r-vT_G(\rho)]/(v-r-1)\ge0\)。上界を達成する。□

\(\mu=r\) なら式は一定になる。この場合、指定頂点の重みを０にしても最適値を保てる場合があり、確率上限が常に性能を下げるとは主張しない。\(\mu<\lambda\) の場合は今回の定理に含めない。

### 4.3 監査との対応と新規性の照合先

\(n\) 対象の２要素部分集合を頂点とし、互いに交わらないペア同士を隣接させると \(KG(n,2)\) となる。そのグラフのパラメータは、\(n\ge5\) で

\[
v=\binom n2,\quad r=\binom{n-2}2,
\quad\lambda=\binom{n-4}2,
\quad\mu=\binom{n-3}2
\]

である。G06に代入すればG05を得る。

グラフゲームの値の逆数は、対応する分数全支配問題の最小総重みに対応する。\(\rho=0\) では「指定した頂点には重みを置けないが、その頂点の近傍制約も満たす」問題となる。これは、その頂点の行と列を両方削除する通常の頂点削除問題とは異なる。

Kneserグラフの支配に関する[Cornet–Torresの研究](https://arxiv.org/abs/2308.15603)、分数パラメータと分割の関係に関する[Bonomo-Braberman–Tilliの研究](https://arxiv.org/abs/2008.08499)を予備照合した。今回は両者の要旨を中心に確認し、上記の指定頂点の確率上限付き公式を確認するには至っていない。これらが公式を含まないという断定でもない。

## 5. G07：少数の監査パターンの完全分類

ここでは \(n\ge3,2\le k<n\)、\(d=n-k\) とし、使用できる監査パターン数を高々 \(m\) とする。確率と個別監査率は自由で、観察は前節と同じ完全な１対象観察とする。最適値を \(F_m(n,k)\) と書く。

### 5.1 未監査集合と重みの統合

実際に使う \(b\) 個のパターンの未監査集合を \(D_s\)、正の重みを \(w_s\) とする。各対象 \(i\) の「外されるパターン集合」を \(A_i=\{s:i\in D_s\}\) とすれば

\[
q_{ij}=1-\sum_{s\in A_i\cup A_j}w_s.
\]

最も重い２パターンからそれぞれ未監査対象を選べば、\(V\le1-w_1-w_2\le1-2/b\)。同じ対象を選んでしまう場合も、その対象と別の対象のペアにすれば和集合に必要な２パターンを含められる。

\(b\ge3\) で等号が成立するのは、全重みが \(1/b\) で、\(D_s\) が互いに交わらない場合に限る。重なりがあれば１対象が２パターンで外され、第三のパターンで外される対象と組み合わせることで少なくとも３パターンを避けるペアが生じる。

より一般に、ある対象が \(r\) 個のパターンで外されるとき、その \(r\) 個の重みを１つの仮想重みにまとめられる。残りと合わせた \(b-r+1\) 個の仮想重みの、どの２つにも対応する未監査ペアを作れるため、\(r<b\) なら

\[
V\le1-\frac2{b-r+1}.
\]

\(r=b\) なら値は０。したがって \(m\ge4\) で

\[
\boxed{(m-1)d\le n<md
\quad\Longrightarrow\quad
F_m(n,k)=F_{m-1}(n,k)=1-\frac2{m-1}.}
\]

上界は、\(m\) パターンなら未監査集合が重なること、\(m-1\) 以下なら元の支持数上界から得る。達成には \(m-1\) 個の互いに交わらない未監査集合を均等に選べばよい。この領域では、１パターン追加しても最良の保証は全く改善しない。

### 5.2 ３・４パターンの完全な値

３パターンでは

\[
F_3(n,k)=\begin{cases}1/3,&3d\le n,\\0,&3d>n.\end{cases}
\]

正の値には、どの対象も高々１パターンでしか外されないことが必要。２パターンで外される対象があると、残りのパターンで外される対象とのペアがすべての予定で検出を避けられる。従って３つの未監査集合が互いに素であることが必要十分となる。

４パターンでは次が完全な分類である。

| パラメータ条件 | 同値な監査率の条件 | \(F_4(n,k)\) |
|---|---|---:|
| \(2n<5d\) | \(k/n<3/5\) | 0 |
| \(5d\le2n<6d\) | \(3/5\le k/n<2/3\) | \(1/4\) |
| \(3d\le n<4d\) | \(2/3\le k/n<3/4\) | \(1/3\) |
| \(4d\le n\) | \(3/4\le k/n<1\) | \(1/2\) |

**証明。** 正の値を持つ４パターンでは、各対象の未監査署名 \(A_i\) は大きさ２以下。大きさ３なら残りのパターンで外れる対象と合わせて全パターンを覆い、値が０になる。

大きさ２の署名を４パターンのラベル上の辺と見なす。互いに交わらない辺があっても値０になるので、どの２辺も交わる。このような単純グラフは星または三角形に含まれる。実際、\(ab,ac\) があり、\(a\) を含まない辺があれば、それは \(bc\) しかなく、他の辺もこの三角形に限られる。

二重に外れる対象数を重複込みで \(t\) とする。未監査対象の延べ数は \(4d\) なので、必要な異なる対象数は \(4d-t\)。星の場合は中心の未監査容量から \(t\le d\)、従って \(n\ge3d\)。三角形の場合は３ラベルの容量から \(2t\le3d\)、従って \(n\ge\lceil5d/2\rceil\)。これで正値が不可能な領域が決まる。

\(\lceil5d/2\rceil\le n<3d\) では三角形の全３辺が必要。署名を12、13、23とする。第四のパターンで外れる対象は署名4に限られ、この対象と三角形署名とのペア、三角形署名同士のペアを使うと、各パターンの重みがそれぞれ検出率の上界となる。従って \(V\le\min_s w_s\le1/4\)。

達成構成は、\(d=2t\) なら署名12、13、23の対象をそれぞれ \(t\) 個、署名4を \(d\) 個置く。\(d=2t+1\) なら12を \(t+1\) 個、13と23を各 \(t\) 個、署名3を１個、署名4を \(d\) 個置く。必要対象数は \(\lceil5d/2\rceil\) で、残りの対象は常に監査する。４予定を均等に使えば値 \(1/4\) を達成する。

\(3d\le n<4d\) では前節の追加１パターンが無益な領域の定理から値 \(1/3\)。\(4d\le n\) では互いに素な４未監査集合から値 \(1/2\) を得る。□

### 5.3 ５対象・３監査の全パターン数曲線

G05とG07を組み合わせると、この小さなゲームは使用可能パターン数全域で解ける。

| 使用できる最大パターン数 | 最適検出率 |
|---|---:|
| 1〜3 | 0 |
| 4〜9 | \(1/4\) |
| 10以上 | \(3/10\) |

４パターンの具体的な監査対象は、\(123,145,245,345\) を各 \(1/4\) で選べばよい。どの対象ペアも少なくとも１パターンに含まれ、最悪検出率は \(1/4\)。９パターン以下なら必ず何か１予定が欠けるので、G05により \(1/4\) を超えられない。全10パターン一様で \(3/10\) を達成する。

探索中に「８〜９パターンで \(2/7\) まで上がるかもしれない」という仮説を試したが、LP探索とその後の一般証明により否定された。４から９までの長い停滞が正しい結果だった。

## 6. 新規性をどう評価するか

### 6.1 既知の結果として明確に帰属する部分

[Candogan–Ozdaglar–Parrilo, Dynamics in Near-Potential Games](https://arxiv.org/html/1107.4386v1) の§2〜4を確認した。近いポテンシャルとの逸脱利得差、閉路和、近似均衡集合への到達を扱う。G04の「十分大きい改善は近似ポテンシャルを増やす」という十分性の仕組みは、この既知の数学に近い。

前ノートの固定閉路に関する半径・最大改善幅の最適化は、別分野ではさらに直接の既知対応が見つかった。[Held–Korte–Rautenbach–Vygen, Combinatorial Optimization in VLSI Design](https://www.or.uni-bonn.de/research/montreal.pdf) の§4.1〜4.2に、頂点ポテンシャルの差と正の辺重みを使ったスラック最適化がある。\(\pi=h\)、\(c_e=-\Delta\Phi/a_i\)、\(w_e=1/a_i\) とすれば対応し、振幅制限は固定基準への辺で表せる。**固定閉路の最適化自体は新規性の主張から下げる。**

[Xuらの漏洩セキュリティゲーム](https://arxiv.org/html/1504.06058v2)は、１対象の観察とペア監査率への還元の出典である。

[Gordon–Kuperberg–Patashnik, New constructions for covering designs](https://arxiv.org/pdf/math/9502238)、[Horsley, Generalising Fisher's inequality to coverings and packings](https://arxiv.org/html/1409.0485v3)を照合した。\(V>0\) を実現できる最少パターン数は古典的な被覆数 \(C(n,k,2)\)。４パターンで正値が可能になる境界は、少数ブロック被覆の既知研究の範囲に入る。Horsleyが参照するMills（1979）等の原著全文は今回未取得であり、重み付き最適値の完全分類まで既出かは未確定である。

### 6.2 今回の候補として残す部分

- G04の、ベクトル共有誤差・個人別閾値・任意目的に対する**鋭い必要十分条件**と、対応する２人２択の反例。
- G05の、**１予定の確率不足に対する線形の厳密性能曲線**、一致する監査戦略と攻撃側の証明書、近似最適に必要な各予定の重み。
- G06の、強正則グラフの指定頂点に確率上限を置く**一般の閉形式**。頂点の確率を禁止しても、その頂点の行制約は残る点を含めて照合する。
- G07の、任意重みを許す少数パターンの最適値・停滞領域。ただし正値可能性だけは既知の被覆問題として帰属する。

今回の検索語には、shared/common payoff perturbation、finite improvement、heterogeneous thresholds、approximate potential、small-block covering、fractional covering、fractional total domination、Kneser、forbidden vertex、strongly regular matrix game 等を含めた。同一命題は確認できなかったが、検索の不発や要旨のみの確認は新規性の証拠として弱い。

**現時点の表記は「証明を収録した命題候補、同一結果未確認」である。「新しい定理を学術的に発見したと確定」ではない。** 基礎技法が初等的なため、専門家には既知理論の簡潔な系と見える可能性もある。それでも、境界・達成構成・失敗例が揃った検証可能な成果として残す。

## 7. 検証記録

seedは20260910。一般の証明と独立した方法で次を実施した。

| 対象 | 検証内容 | 結果 |
|---|---|---|
| G04十分性 | ２〜６人、各２択、３次元誤差。LPで個人別閾値を求め、全状態の \(W\) の挟み込みと受理辺を点検 | 150ゲーム、受理辺6,497本で違反なし |
| G04必要性 | 双対ノルムを１ノルムとする有理数の２人２択反例 | 200件で全変更が閾値を厳密に超える |
| スカラー校正 | LPと重み付き中央値による値を比較 | 100件一致 |
| G05構成 | \(n=5\)〜30、\(\rho\in\{0,1/(3N),2/(3N),1/N\}\)、確率とペア値を有理数計算 | 104構成一致。\(n\le12\) は全ペア、以降は３分類の代表を検査 |
| G05全LP | \(n=5\)〜10、同じ４上限値、すべての予定・すべての攻撃ペアを含むLP | 24件一致 |
| G06 | 構成から隣接行列を生成し強正則パラメータ自体も検査。Paley、Rook、Kneser、完全多部の13グラフ | 有理数構成と全LPの52条件で一致 |
| G07 | 独立担当による４パターンのMILP、９組の \((n,k)\) | 全件最適終了・分類と一致 |

独立した担当が、G04の量化と反例、G05の各ペア率と上界、G06の \(\mu=\lambda\)・\(\mu=r\) の境界、G07の星・三角形分類を再点検した。誤りは今回の主要証明では見つからなかった。

形式証明は行っていない。浮動小数点LPは許容差を持つ計算検証であり、有理数による構成点検とも区別する。有限検査が一般定理を証明したとは解釈しない。

## 8. 次に進むなら

G04は、共有誤差が再訪時に少し変わる場合の有限総変動・停止回数の評価へ進められる。固定誤差の証明をそのまま時間変動誤差に流用しない。

G05・G06は、指定パターン・頂点を２つ以上制限した場合に進められる。２制限の位置関係による分類が生じるため、一つの制限の式を単に足すことはできない。特にグラフの隣接・非隣接に応じた制限コストが次の具体的な問いとなる。

ただし次の拡張の前に、G04の必要十分条件とG06の確率制限付き公式を、近似共通利益ゲーム・制約付き行列ゲーム・分数全支配の専門文献へ照合する価値がある。

## 9. 再現コード

以下は今回実行したコード。Python・NumPy・SciPyを使用する。結果JSONは実行ディレクトリに保存する。これはLeanコードではない。
### verify_deep.py

```python
"""Reproducible checks for sharp shared-error margins and capped audit schedules."""
from itertools import combinations,product
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

rng=np.random.default_rng(20260910)

def margin_lp(a,weights,eps=1):
    n=len(a);rows=[];rhs=[]
    for i,j in combinations(range(n),2):
        r=np.zeros(n);r[i]=r[j]=-1;rows.append(r);rhs.append(-2*eps*np.sum(np.abs(a[i]-a[j])))
    res=linprog(weights,A_ub=rows,b_ub=rhs,bounds=[(0,None)]*n,method='highs')
    assert res.success
    return res.x,res.fun

margin_edges=0;games=0;scalar_medians=0;witnesses=0
for n in range(2,7):
    states=list(product([0,1],repeat=n));S=len(states);index={s:i for i,s in enumerate(states)}
    for case in range(30):
        a=rng.integers(-5,6,size=(n,3)).astype(float);eps=float(rng.uniform(.05,1))
        gamma,_=margin_lp(a,rng.uniform(.1,3,size=n),eps)
        h=rng.uniform(-eps,eps,size=(S,3));phi=rng.normal(size=S)*10
        U=phi[:,None]+h@a.T;W=np.max(U-gamma/2,axis=1)
        assert np.all(W[:,None]>=U-gamma/2-1e-8)
        assert np.all(W[:,None]<=U+gamma/2+1e-8)
        for s_idx,s in enumerate(states):
            for i in range(n):
                t=list(s);t[i]=1-t[i];t_idx=index[tuple(t)]
                if U[t_idx,i]-U[s_idx,i]>gamma[i]+1e-8:
                    assert W[t_idx]>W[s_idx]-1e-8; margin_edges+=1
        games+=1
for n in range(2,12):
    for case in range(10):
        a=rng.integers(-10,11,size=(n,1));weights=rng.integers(1,8,size=n)
        _,val=margin_lp(a,weights)
        candidates=[2*sum(int(w)*abs(int(x)-int(alpha)) for w,x in zip(weights,a[:,0])) for alpha in a[:,0]]
        assert abs(val-min(candidates))<1e-7;scalar_medians+=1
# Exact rational square witnesses, norm is infinity and dual norm is 1.
for _ in range(200):
    ai=[int(x) for x in rng.integers(-4,5,size=3)];aj=[int(x) for x in rng.integers(-4,5,size=3)]
    distance=sum(abs(y-x) for x,y in zip(ai,aj))
    if not distance:continue
    eps=F(1,3);gi=gj=eps*distance/F(2)
    v=[(y>x)-(y<x) for x,y in zip(ai,aj)]
    aa=sum(x*y for x,y in zip(ai,v));bb=sum(x*y for x,y in zip(aj,v))
    q=(gi+2*eps*aa+2*eps*bb-gj)/2
    gains=[q-2*eps*aa,-q+2*eps*bb,q-2*eps*aa,-q+2*eps*bb]
    assert gains[0]>gi and gains[1]>gj and gains[2]>gi and gains[3]>gj;witnesses+=1

audit_exact=0;audit_lp_cases=0
for n in range(5,31):
    edges=list(combinations(range(n),2));N=len(edges);r=n-2;D=n*n-3*n-2
    for fraction in [F(0),F(1,3),F(2,3),F(1)]:
        rho=fraction/N;target=F((n-3)*(n-4),D)+F(2*(n-3),D)*rho
        weights=[]
        for e in edges:
            if e==(0,1):w=rho
            elif 0 in e or 1 in e:w=(1-rho-target)/(2*r)
            else:w=2*target/(r*(r-1))
            weights.append(w)
        assert min(weights)>=0 and sum(weights)==1
        # Three symmetry classes checked exactly; for n<=12 enumerate all rows.
        q_values=[]
        testpairs=edges if n<=12 else [(0,1),(0,2),(2,3)]
        for e in testpairs:q_values.append(sum(w for f,w in zip(edges,weights) if set(e).isdisjoint(f)))
        assert min(q_values)==target;audit_exact+=1
        if n<=10:
            M=np.array([[int(set(e).isdisjoint(f)) for f in edges] for e in edges],float)
            obj=np.zeros(N+1);obj[-1]=-1
            bounds=[(0,float(rho))]+[(0,1)]*(N-1)+[(0,1)]
            res=linprog(obj,A_ub=np.column_stack([-M,np.ones(N)]),b_ub=np.zeros(N),A_eq=[list(np.ones(N))+[0]],b_eq=[1],bounds=bounds,method='highs')
            assert res.success and abs(-res.fun-float(target))<1e-9;audit_lp_cases+=1

def graph_case(name,M):
    v=len(M);degrees=M.sum(axis=1);assert np.all(degrees==degrees[0]);d=int(degrees[0])
    common=M@M;ls={int(common[i,j]) for i,j in combinations(range(v),2) if M[i,j]};mus={int(common[i,j]) for i,j in combinations(range(v),2) if not M[i,j]}
    assert len(ls)==len(mus)==1
    la=ls.pop();mu=mus.pop();assert mu>=la and mu>0
    for f in [F(0),F(1,3),F(2,3),F(1)]:
        rho=f/v;T=(F(mu)+(d-mu)*rho)/(d+mu-la)
        w=[rho]+[T/d if M[0,i] else (1-rho-T)/(v-d-1) for i in range(1,v)]
        assert min(w)>=0 and sum(w)==1
        q=[sum(w[j] for j in range(v) if M[i,j]) for i in range(v)]
        assert min(q)==T
        obj=np.zeros(v+1);obj[-1]=-1
        res=linprog(obj,A_ub=np.column_stack([-M,np.ones(v)]),b_ub=np.zeros(v),A_eq=[list(np.ones(v))+[0]],b_eq=[1],bounds=[(0,float(rho))]+[(0,1)]*v,method='highs')
        assert res.success and abs(-res.fun-float(T))<1e-9
    return {'name':name,'v':v,'d':d,'lambda':la,'mu':mu,'cases':4}

graphs=[]
for q in [5,13,17]:
    residues={(x*x)%q for x in range(1,q)}
    M=np.array([[int(i!=j and (j-i)%q in residues) for j in range(q)] for i in range(q)],int)
    graphs.append(graph_case('Paley'+str(q),M))
for q in [3,4]:
    pts=list(product(range(q),repeat=2));M=np.array([[int(x!=y and (x[0]==y[0] or x[1]==y[1])) for y in pts] for x in pts],int)
    graphs.append(graph_case('Rook'+str(q),M))
for n in range(5,10):
    E=list(combinations(range(n),2));M=np.array([[int(set(e).isdisjoint(f)) for f in E] for e in E],int)
    graphs.append(graph_case('KG('+str(n)+',2)',M))
for parts,size in [(2,3),(3,3),(4,2)]:
    pts=list(product(range(parts),range(size)));M=np.array([[int(x[0]!=y[0]) for y in pts] for x in pts],int)
    graphs.append(graph_case('Multipartite'+str((parts,size)),M))
out={'seed':20260910,'vector_games':games,'accepted_edges_checked':margin_edges,'scalar_weighted_medians':scalar_medians,'rational_cycle_witnesses':witnesses,'audit_exact_constructions':audit_exact,'audit_full_LP_cases':audit_lp_cases,'strongly_regular_graphs':graphs,'srg_LP_cases':sum(g['cases'] for g in graphs)}
Path('deep_verification_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out))

```

### 検証サマリーJSON

```json
{
  "seed": 20260910,
  "vector_games": 150,
  "accepted_edges_checked": 6497,
  "scalar_weighted_medians": 100,
  "rational_cycle_witnesses": 200,
  "audit_exact_constructions": 104,
  "audit_full_LP_cases": 24,
  "strongly_regular_graphs": [
    {
      "name": "Paley5",
      "v": 5,
      "d": 2,
      "lambda": 0,
      "mu": 1,
      "cases": 4
    },
    {
      "name": "Paley13",
      "v": 13,
      "d": 6,
      "lambda": 2,
      "mu": 3,
      "cases": 4
    },
    {
      "name": "Paley17",
      "v": 17,
      "d": 8,
      "lambda": 3,
      "mu": 4,
      "cases": 4
    },
    {
      "name": "Rook3",
      "v": 9,
      "d": 4,
      "lambda": 1,
      "mu": 2,
      "cases": 4
    },
    {
      "name": "Rook4",
      "v": 16,
      "d": 6,
      "lambda": 2,
      "mu": 2,
      "cases": 4
    },
    {
      "name": "KG(5,2)",
      "v": 10,
      "d": 3,
      "lambda": 0,
      "mu": 1,
      "cases": 4
    },
    {
      "name": "KG(6,2)",
      "v": 15,
      "d": 6,
      "lambda": 1,
      "mu": 3,
      "cases": 4
    },
    {
      "name": "KG(7,2)",
      "v": 21,
      "d": 10,
      "lambda": 3,
      "mu": 6,
      "cases": 4
    },
    {
      "name": "KG(8,2)",
      "v": 28,
      "d": 15,
      "lambda": 6,
      "mu": 10,
      "cases": 4
    },
    {
      "name": "KG(9,2)",
      "v": 36,
      "d": 21,
      "lambda": 10,
      "mu": 15,
      "cases": 4
    },
    {
      "name": "Multipartite(2, 3)",
      "v": 6,
      "d": 3,
      "lambda": 0,
      "mu": 3,
      "cases": 4
    },
    {
      "name": "Multipartite(3, 3)",
      "v": 9,
      "d": 6,
      "lambda": 3,
      "mu": 6,
      "cases": 4
    },
    {
      "name": "Multipartite(4, 2)",
      "v": 8,
      "d": 6,
      "lambda": 4,
      "mu": 6,
      "cases": 4
    }
  ],
  "srg_LP_cases": 52
}
```

### ４パターン問題の再現

前ノートに含めた `check_audit.py` の `solve(n,k,m)` を次の９組に対して呼び出した。各呼び出しで `m=4` とし、整数最適化により確率とパターン選択を同時に最適化する。

```python
from check_audit import solve
for n,k in [(4,2),(5,3),(6,4),(7,4),(7,5),(8,5),(8,6),(9,6),(10,7)]:
    print(solve(n,k,4))
```
