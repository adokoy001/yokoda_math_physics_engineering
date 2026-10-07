# 数学探索：平均と分散に隠れた「島」

2026 09 08 ／ 探索候補 X01 ／ 第1版

## 今回の到達点

件数・平均・分散しか分からない有限データについて、「一部を取り出した合計はどんな値になり得るか」を調べた。単なる上限・下限では足りず、**その間に実現不可能な穴が開く**ことを、必要十分条件と構成証明で記述できた。

整数の総和を持つ場合には、穴の位置、島の個数、データ全体の集合の連結性が変わる閾値、0/1丸めの鋭い誤差限界まで明示できる。統計量の整合性検査、削除後の集計、制約付きデータ生成、連続探索の初期値設計に使える。

**数学的状態：一般証明を記録し、別担当のAIによる独立監査と有限計算を実施。新規性の状態：既知結果の組合せ・明示的な系を多く含み、学術的新規性は確定していない。** 文献照合で見つかった既知構造は第8節に帰属した。形式証明・人間の専門家による査読は未実施。

添付の既存成果台帳は参照資料とし、公開済みE01・E02は変更しない。本ノートは新しい探索候補であり、公開済み成果には数えない。

図：[moment_islands.png](sandbox:/workspace/scratch/969dff4f4f1c/deliverables/moment_islands.png)。上段は3個のデータ全体の集合、下段は4個のデータのうち2個の合計。緑が可能な集合を示す。

## 1. まず、4個の数字だけで現れる穴

各値が0以上1以下の4個の実数について、平均が0.5、分散が0.2と分かっているとする。分散は分母を4とする定義である。総和と二乗和は

\[
S=2,\qquad Q=4(0.2+0.5^2)=1.8.
\]

先頭2個の合計を \(t\) とすると、可能な値は正確に次の3区間となる。

| 島 | 可能な合計（小数表示は近似） |
|---|---|
| 1 | 0.1055728090 ～ 0.1127016654 |
| 2 | 0.8872983346 ～ 1.1127016654 |
| 3 | 1.8872983346 ～ 1.8944271910 |

例えば **t=0.5は不可能**。2個の値の和が0.5なら二乗和は最大0.25。残る2個の和が1.5なら二乗和は最大1.25なので、全体の二乗和は最大1.5にしかならない。指定の1.8には届かない。

一方、t=0.11は可能である。第2節の式から、その条件に合う元データを具体的に構成できる。つまり「最小値と最大値の間なら可能」という直感を、数値上の丸め誤差とは無関係に反証している。

ここでいう可能集合は、**同じ統計量を持つ全データを動かしたとき**の集合である。既に一つに固定された4個のデータから2個を選ぶ、有限個の部分和の集合とは区別する。

## 2. 部分和の完全な実現可能条件

整数 \(n\ge2\)、\(1\le k<n\) と実数 \(S,Q,t\) を与える。求めるのは

\[
x_i\in[0,1],\quad \sum_{i=1}^n x_i=S,\quad
\sum_{i=1}^n x_i^2=Q,\quad \sum_{i=1}^k x_i=t
\tag{1}
\]

を満たす実数ベクトルの存在である。任意の固定されたk個のラベルでも、添字を入れ替えれば同じ問題になる。

\[
\phi(u)=\lfloor u\rfloor+(u-\lfloor u\rfloor)^2
\]

と定めると、(1)の必要十分条件は次の三条件だけである。

\[
\boxed{\begin{aligned}
\max(0,S-(n-k))&\le t\le\min(k,S),\\
q_0(t):=\frac{t^2}{k}+\frac{(S-t)^2}{n-k}&\le Q,\\
Q&\le q_1(t):=\phi(t)+\phi(S-t).
\end{aligned}}
\tag{2}
\]

### 必要性

長さm、総和uの[0,1]内の列では、Cauchy–Schwarzより二乗和の最小値は \(u^2/m\)。全成分をu/mにすれば達成する。

最大値は \(\phi(u)\)。1を \(\lfloor u\rfloor\) 個置き、残りの小数部分を1個に置き、他を0にすれば達成する。証明は、端点でない2成分を選び、和を保存して小さい方から大きい方へ量を移す操作を繰り返せばよい。二乗和は増加し、最後には端点でない成分は高々1個になる。この最大化の部品は既知である。[Rosenberg–Jakobsson (2008), Appendix Lemma 3](https://web.stanford.edu/group/rosenberglab/papers/RosenbergJakobsson2008-Genetics.pdf)、[Ellis (2025), Theorem 1](https://arxiv.org/pdf/2508.17525)

これを先頭k個と残りn−k個に適用すると(2)が必要になる。

### 十分性：存在だけでなく元データを作れる

各ブロックを一様にしたベクトルをb、各ブロックで端点に詰めた最大配置をeとする。両ブロックの和は一致するため、\(\langle b,e-b\rangle=0\)。したがって

\[
\|b+\lambda(e-b)\|^2=q_0+\lambda^2(q_1-q_0).
\]

\(q_1>q_0\) なら

\[
\boxed{x=b+\sqrt{\frac{Q-q_0}{q_1-q_0}}(e-b)}
\tag{3}
\]

とする。(2)より係数は[0,1]内なので、箱制約と両ブロック和を保存する。二乗和もQになる。

**退化例：\(q_1=q_0\) ならx=bとする。** この場合に平方根式を使うと0/0になる。特にn=2,k=1では常にこの分岐が必要である。

判定は、実数演算モデルでは固定個数の四則・床関数評価でできる。証人の出力はn成分なのでO(n)。これは固定された既知配列の部分和問題を解くアルゴリズムではない。

### 複数ブロックへの直接拡張

互いに重ならないブロックの長さ \(m_j\) と総和 \(t_j\) が全て指定されている場合も、

\[
0\le t_j\le m_j,\qquad
\sum_j\frac{t_j^2}{m_j}\le Q\le\sum_j\phi(t_j)
\]

が必要十分。全ブロックの一様配置と最大配置を同じ係数で結ぶ(3)がそのまま証人になる。重複するブロックへの拡張はここでは主張しない。

## 3. 整数総和なら島の位置と数まで決まる

以下、\(S=s\in\{1,\ldots,n-1\}\) を整数とする。分散v、平均μ=s/nを使えば

\[
D=s-Q=\sum_i x_i(1-x_i)=n\{\mu(1-\mu)-v\}.
\tag{4}
\]

Dは、0/1だけからなる最大分散の配置からどれだけ離れたかを測る量である。**確率的な信頼度ではなく、データに関する厳密な代数的量**である。

\(0\le D<1/2\) で

\[
a(D)=\frac{1-\sqrt{1-2D}}2<\frac12
\tag{5}
\]

と置く。\(r=\{t\}\) をtの小数部分とすると

\[
q_1(t)=s-2r(1-r).
\]

よって(2)の上側条件は、tがいずれかの整数から距離a以下という条件になる。

\[
\mathcal T=
[L,U]\cap[c-h,c+h]\cap
\bigcup_{j=L}^{U}[j-a,j+a],
\tag{6}
\]

\[
L=\max(0,s-(n-k)),\quad U=\min(k,s),\quad
c=\frac{ks}{n},\quad
h=\sqrt{\frac{k(n-k)}n\left(Q-\frac{s^2}n\right)}.
\]

各整数帯は必ず非空になり、互いの間に隙間がある。したがって可能な部分和集合の連結成分数は正確に

\[
\boxed{\#\pi_0(\mathcal T)=\min(k,s,n-k,n-s)+1.}
\tag{7}
\]

非空性は第4節の丸め評価から分かる。どれか一つの実現データを丸めると、1がs個ある。k個の選択内にj個の1を含める選び方は、L≤j≤Uの全てで存在する。その部分和は[j−a,j+a]内に入る。座標を並べ替えれば先頭k個の実現例になる。

\(D\ge1/2\) なら \(2r(1-r)\le1/2\le D\) なので上側条件は自動的に成立し、可能な部分和は一つの閉区間 \([L,U]\cap[c-h,c+h]\) になる。D=0では低Dの各島が整数の一点に縮む。

## 4. どの部分集合にも同時に効く丸め保証

同じ整数総和と \(D<1/2\) の下で、各値を近い方の0/1に丸めたベクトルzは一意で、

\[
\sum_i z_i=s,\qquad
\boxed{\|x-z\|_1\le1-\sqrt{1-2D}=2a(D)}
\tag{8}
\]

が成り立つ。さらに任意の部分集合Aに対し

\[
\boxed{\left|\sum_{i\in A}(x_i-z_i)\right|\le a(D).}
\tag{9}
\]

**証明。** \(d_i=\min(x_i,1-x_i)\) とすると \(\sum d_i\le2D<1\)。任意の最近整数丸めzで \(|s-\sum z_i|<1\) となり、左辺は整数なので総和を保存する。もし値1/2があれば、その座標の丸め方を変えた二つの総和がどちらもsになるという矛盾が生じるため、丸めは一意。

0側の正の誤差和と1側の負の誤差の絶対値の和は等しい。その値をρとすると \(2\rho=\sum d_i<1\)。各側の平方和はρ²以下だから

\[
D=2\rho-\sum d_i^2\ge2\rho(1-\rho).
\]

ρ<1/2でこの右辺は増加するためρ≤a。全体の絶対誤差は2ρ、どの部分集合の符号付き誤差も[−ρ,ρ]に入るので(8)(9)を得る。

**鋭さ。** \((a,1-a,\underbrace{1,\ldots,1}_{s-1},\underbrace{0,\ldots,0}_{n-s-1})\) は指定のs,Dを持ち、(8)の等号を達成する。適切な部分集合で(9)も等号になる。

これは各入力の近傍にある丸め先を特定する保証である。s,Dだけから、どのラベルが1に丸まるかを決められるという意味ではない。

## 5. データ全体の集合にも、正確な連結性の閾値がある

ラベルを区別した実現データ全体を

\[
X_D=\left\{x\in[0,1]^n:\sum_i x_i=s,\ \sum_i x_i(1-x_i)=D\right\},
\quad 0\le D\le D_{\max}=\frac{s(n-s)}n
\]

とする。このとき

\[
\boxed{
\#\pi_0(X_D)=
\begin{cases}
\binom ns,&0\le D<1/2,\\
1,&1/2\le D\le D_{\max}.
\end{cases}}
\tag{10}
\]

後半は単に連結というだけでなく道連結。すなわち、平均・分散・値域を保った連続な変形で任意の実現データ同士を結べる。前半では、異なる0/1丸め先に属する島の間を、その制約を保って移れない。

**この連結性の結論は、Gorbanの既知の一般理論の明示的な系に位置づける。** 凸多面体上の凸関数の等位集合の成分を、頂点・辺から計算する枠組みが既にある。[Gorban (2013), Proposition 7・Lemma 14](https://arxiv.org/html/1201.6315v3) 以下には独立に得た初等的な証明を残す。

### 低D：各島の元データを生成する座標

総和sの0/1列zを一つ固定する。zが0の添字集合をI₀、1の集合をI₁とし、それぞれの上の確率ベクトルu,vを選ぶ。\(0<D<1/2\) で

\[
A=\|u\|^2+\|v\|^2,\quad
\rho=\frac{D}{1+\sqrt{1-AD}},\qquad
x_i=\begin{cases}\rho u_i&i\in I_0,\\1-\rho v_i&i\in I_1\end{cases}
\tag{11}
\]

とする。A≤2より平方根は正。\(0<\rho<1/2\) なので各座標は指定したzに丸まる。総和はs、Dは \(2\rho-A\rho^2=D\) で保存される。

逆に、zへ丸まる全てのxは、片側の誤差和ρを使って \(u_i=x_i/\rho\)、\(v_i=(1-x_i)/\rho\) と一意に戻せる。写像と逆写像は連続であり、各島は

\[
\Delta_{n-s-1}\times\Delta_{s-1}
\]

と同相。ここで \(\Delta_m\) はm次元の閉確率単体である。異なる丸め先の島は少なくとも一座標で \(1-2a(D)>0\) 離れている。各島は道連結かつ非空なので、島数は \(\binom ns\)。D=0は0/1頂点だけ。

同相型の単体積そのものも既知のhypersimplexの頂点図に対応する。[Schröter, Example 8](https://arxiv.org/pdf/1707.02814) (11)はこの構造を、モーメントを正確に保つ生成座標として具体化したものである。

### 高D：全ての島をつなぐ道を構成する

\(H=\{x\in[0,1]^n:\sum x_i=s\}\)、中心 \(c=(s/n)\mathbf1\)、\(R^2=D_{\max}\)、\(r^2=R^2-D\) と置くと、X_DはHと中心c・半径rの球面の交わりになる。r=0なら中心一点なので、以下r>0。

Hは総和sの0/1頂点の凸包。全頂点はcから同じ距離Rにある。1と0を1個ずつ交換する隣接頂点v,wの辺上では

\[
\|(1-t)v+tw-c\|^2=R^2-2t(1-t)\ge R^2-1/2\ge r^2.
\]

したがって辺全体を

\[
\pi(y)=c+\frac r{\|y-c\|}(y-c)
\]

で球面へ縮小できる。縮小はH内に留まる。隣接交換のグラフは連結なので、射影された全頂点をX_D内で結べる。

任意の \(x\in X_D\) を頂点の凸結合 \(x=\sum\lambda_vv\) と書くと、\(\sum\lambda_v\langle x-c,v-c\rangle=r^2\)。あるvでは内積がr²以上になる。そのvへ向かう線分は

\[
\|x+t(v-x)-c\|^2=r^2+2t\langle x-c,v-x\rangle+t^2\|v-x\|^2\ge r^2
\]

と球の外側に留まるため、同じ射影がxとπ(v)をつなぐ。以上で道連結性を得る。

閾値の1/2は、二つの座標を(0,1)から(1/2,1/2)にする際の \(\sum x_i(1-x_i)\) の増加量である。D=1/2で隣接する丸め領域が初めてその辺の中点で接する。

## 6. 何に使えるか、どこまで言えるか

| 用途 | この結果でできること | 条件・限界 |
|---|---|---|
| 削除後の集計 | k件を取り除く総和tの完全可能集合から、残りの平均(S−t)/(n−k)を評価 | 元データは未知。削除対象の値や順序の追加制約は含めない |
| 集計の整合性検査 | 全体の平均・分散と部分集計が両立するかを(2)で判定 | 入力統計量は正確な値というモデル |
| 制約付きデータ生成 | 目的の部分和に合うデータを(3)、低Dの各島を(11)で生成 | 一様サンプリングではない。生成器と検証器を混同しない |
| 連続探索の設計 | D<1/2では一つの島に留まる連続探索が全ラベル配置を巡れないことを判定 | 順列不変の目的ではラベルの重複を除ける。無条件の計算量下界ではない |
| 近二値データの圧縮 | (8)(9)で全部分集合に共通の丸め誤差を保証 | 総和が整数であることが必要 |

値域が[a,b]、a<bなら \(x_i=(y_i-a)/(b-a)\) で正規化して適用できる。ただし元データを正規化した後の総和が整数かどうかを確認する。分散の分母がn−1の標本分散なら、まずQ=(n−1)s_sample²+nμ²に換算する。

## 7. 反例・境界・検証記録

| チェックした対象 | 結果 |
|---|---|
| 「可能集合は常に区間」という予想 | 第1節のn=4例が反例 |
| 端点配置だけで十分か | 最小と最大の間のQを(3)で補う必要がある |
| q₁=q₀ | 平方根式の0/0を避ける分岐を追加 |
| n=2,s=1 | D<1/2で2点、D=1/2で一点。一般式と一致 |
| s=0またはn | 整合するデータは全0または全1のみ。主定理の範囲外の自明例 |
| 総和が整数でない場合 | (2)は成立。整数帯(6)、閾値(10)をそのまま移さない |
| 分散の上限だけが与えられた場合 | \(\sum x_i^2\le Q\) の実現集合は凸になる。等号制約が今回の分断の原因 |

主な有限検査は以下。一般証明とは独立に位置づける。

| 検査 | 件数・範囲 |
|---|---|
| 0,1/4,1/2,3/4,1の全ベクトル | n=2〜6、19,525ベクトル |
| 上記の全先頭部分和について必要条件を有理数照合 | 92,775件 |
| 箱と総和超平面の頂点最大値 | 119件 |
| 十分条件から構成した証人 | 694,125件 |
| 整数総和の島数・帯の非空性 | 42,775件 |
| 丸め安定性の等号例 | 4,704件 |
| 単体積座標からの生成 | 6,732件 |

全件PASS。証人の最大二乗和残差は約7.11×10⁻¹⁵。有限格子における必要条件の成立だけでは、連続領域の十分性・位相は証明できない。それらは第2〜5節の一般証明が支える。高Dの道連結性を有限点群の近傍グラフで判定したという報告ではない。

検証コードはPython標準ライブラリのみ。seed=8675309。以下の付録にコードと結果を全文収録する。

## 8. 先行研究との照合と、残った問い

2026 09 08に一次資料を確認した。全文を確認できた関連命題と今回の式の対応は次の通り。

| 部分 | 帰属・位置づけ |
|---|---|
| 固定総和・固定上限での二乗和最大 \(\phi(u)\) | Rosenberg–Jakobsson (2008) Appendix Lemma 3に同じ最大化構造。Ellis (2025) Theorem 1に有限データ分散として同じ式 |
| 部分集合平均の平方根型境界 | Mallows–Richter (1969)の既知不等式に一致。Sharma (2017) 式(1.8)でも確認 |
| 等位集合の成分を辺から読む構造、(10)の閾値・成分数 | Gorban (2013) Proposition 7、Lemma 14、§3.3の明示的な系 |
| 低D成分の単体積という形 | hypersimplexの頂点図として既知。Schröter Example 8で確認 |
| 部分和完全可能集合(2)(6)、構成式(3)、島数(7)、鋭い安定性(8)(9)のまとめ | この組合せと同じ先行記述は今回未特定。各部は初等的な帰結に近く、新規性の強い根拠とは扱わない |

参照した一次資料：

1. [N. A. Rosenberg and M. Jakobsson (2008), The Relationship Between Homozygosity and the Frequency of the Most Frequent Allele](https://web.stanford.edu/group/rosenberglab/papers/RosenbergJakobsson2008-Genetics.pdf).
2. [J. L. Ellis (2025), The maximum variance of a finite dataset, given its mean, minimum, and maximum](https://arxiv.org/pdf/2508.17525).
3. [C. L. Mallows and D. Richter (1969), Inequalities of Chebyshev Type Involving Conditional Expectations](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-40/issue-6/Inequalities-of-Chebyshev-Type-Involving-Conditional-Expectations/10.1214/aoms/1177697276.full). 原論文の書誌情報と、次のSharmaでの明示式を照合。原論文の全証明再読は未実施。
4. [R. Sharma (2017), Remark On Variance Bounds](https://arxiv.org/html/1704.06292v1), (1.8).
5. [A. N. Gorban (2013), Thermodynamic Tree: The Space of Admissible Paths](https://arxiv.org/html/1201.6315v3).
6. [B. Schröter, Multi-splits and tropical linear spaces from nested matroids](https://arxiv.org/pdf/1707.02814), Example 8.

調べた語には “finite sample maximum variance”, “subset mean variance bounds”, “fixed sum sum of squares”, “hypersimplex sphere connected components”, “thermodynamic tree”, “hypersimplex vertex figure” を含む。検索で見つからなかったことは、新規性の証明ではない。本文未読の関連領域としてSPREAD制約、有限モーメント問題、最適回復、近二値制約の安定性評価が残る。

**次に価値がありそうな問い**は、丸められた平均・分散に幅を許したときに穴がどれだけ残るか、総和が非整数のときの全実現集合の連結性、ラベルを同一視した集合で何が残るか、各島を指定分布でサンプルする方法である。本ノートではこれらを解決済みとしない。

同時に探索した「不偏丸めの最悪誤差」「区間集計からの復元」「三角監査の最少設計」は、別紙の探索候補台帳に証明・出典・再現コードとともに保存した。

今回の成果の置き方は、**身近な統計量から生じる離散的な構造を、検査・生成に使える式まで具体化し、既知理論への帰属も進めた探索記録**である。


## 付録A：検証コード全文

以下を `audit_moments.py` として保存し、`python3 audit_moments.py` で実行する。結果は同じフォルダの `results.json` に書き込まれる。

```python
"""Independent finite-grid and constructive audit; standard library only."""
from fractions import Fraction as F
from itertools import product
from math import sqrt, floor, comb
from random import Random
from pathlib import Path
import json

RNG = Random(8675309)
COUNTS = {"exact_grid_vectors": 0, "exact_grid_partition_checks": 0,
          "vertex_extrema_checks": 0, "witness_checks": 0,
          "integer_island_component_checks": 0, "sharp_stability_checks": 0,
          "topology_parameterization_checks": 0}
MAX_RESIDUAL = {"sum": 0.0, "square_sum": 0.0, "partial_sum": 0.0}

def phi(u):
    j = u.numerator // u.denominator if isinstance(u, F) else floor(u)
    return j + (u - j)**2

def bounds(n,k,S,t):
    return (t*t/k+(S-t)**2/(n-k), phi(t)+phi(S-t))

def endpoint(m,u):
    out=[]
    for _ in range(m):
        v=max(0.,min(1.,u));out.append(v);u-=v
    assert abs(u)<1e-10
    return out

def witness(n,k,S,Q,t):
    b=[t/k]*k+[(S-t)/(n-k)]*(n-k)
    e=endpoint(k,t)+endpoint(n-k,S-t)
    q0=sum(v*v for v in b);q1=sum(v*v for v in e)
    alpha=0 if q1-q0<1e-14 else sqrt(max(0.,min(1.,(Q-q0)/(q1-q0))))
    return [v+alpha*(w-v) for v,w in zip(b,e)]

def check_witness(n,k,S,Q,t):
    x=witness(n,k,S,Q,t)
    assert all(-1e-11<=v<=1+1e-11 for v in x),x
    residuals={"sum":abs(sum(x)-S),"square_sum":abs(sum(v*v for v in x)-Q),
               "partial_sum":abs(sum(x[:k])-t)}
    for name,value in residuals.items():
        MAX_RESIDUAL[name]=max(MAX_RESIDUAL[name],value)
        assert value<2e-10,(n,k,S,Q,t,x,residuals)
    COUNTS["witness_checks"]+=1
    return x

# An exhaustive lattice check is only a necessary-condition audit, not a
# proof of sufficiency: the latter is handled by the algebraic witness.
for n in range(2,7):
    for integers in product(range(5),repeat=n):
        x=[F(v,4) for v in integers]
        S=sum(x);Q=sum(v*v for v in x)
        COUNTS["exact_grid_vectors"]+=1
        for k in range(1,n):
            t=sum(x[:k]);lo,hi=bounds(n,k,S,t)
            assert max(0,S-(n-k))<=t<=min(k,S)
            assert lo<=Q<=hi,(n,k,x,lo,Q,hi)
            COUNTS["exact_grid_partition_checks"]+=1

# Enumerate every vertex of a box sliced by a fixed sum independently.
# At most one coordinate is fractional, so enumerate its position and the
# remaining binary coordinates.  Check the exact maximum squared norm.
for m in range(1,8):
    for j in range(4*m+1):
        u=F(j,4);extrema=[]
        for partial in product((F(0),F(1)),repeat=m-1):
            last=u-sum(partial)
            if 0<=last<=1:
                extrema.append(sum(v*v for v in partial)+last*last)
        assert extrema and max(extrema)==phi(u),(m,u,extrema)
        COUNTS["vertex_extrema_checks"]+=1

# Exact rational totals and independently drawn Q within the certified
# endpoint interval, including both endpoints and all degenerate blocks.
for n in range(2,13):
    for k in range(1,n):
        for _ in range(80):
            t=F(RNG.randrange(4*k+1),4)
            u=F(RNG.randrange(4*(n-k)+1),4)
            S=t+u;lo,hi=bounds(n,k,S,t)
            for lam in (F(0),F(1,7),F(1,2),F(6,7),F(1)):
                Q=lo+lam*(hi-lo)
                check_witness(n,k,float(S),float(Q),float(t))

def island_intervals(n,k,S,D):
    Q=S-D
    L=max(0,S-(n-k));U=min(k,S)
    center=k*S/n
    rad=sqrt(max(0.,k*(n-k)/n*(Q-S*S/n)))
    a=(1-sqrt(1-2*D))/2
    out=[]
    for j in range(L,U+1):
        left=max(float(L),center-rad,j-a)
        right=min(float(U),center+rad,j+a)
        if left<=right+1e-12:out.append((left,right))
    return out

for n in range(2,31):
    for S in range(1,n):
        for k in range(1,n):
            for D in (0.,.0001,.03,.2,.499999):
                intervals=island_intervals(n,k,S,D)
                assert len(intervals)==min(k,S,n-k,n-S)+1
                for left,right in intervals:
                    for t in (left,(left+right)/2,right):
                        check_witness(n,k,float(S),S-D,t)
                COUNTS["integer_island_component_checks"]+=1

# Sharpness of the stability bound: exact one-exchange witnesses.
for n in range(2,50):
    for S in range(1,n):
        for D in (0.,.0001,.1,.499999):
            a=(1-sqrt(1-2*D))/2
            x=[a,1-a]+[1.]*(S-1)+[0.]*(n-S-1)
            assert abs(sum(x)-S)<1e-11
            assert abs(sum(v*v for v in x)-(S-D))<1e-11
            z=[0. if v<.5 else 1. for v in x]
            assert sum(z)==S
            assert abs(sum(abs(v-w) for v,w in zip(x,z))-2*a)<1e-11
            COUNTS["sharp_stability_checks"]+=1

# Each low-defect component is parameterized by the product of two simplices:
# alpha_i,beta_j >=0, each sums to 1; e=P*alpha, f=P*beta.
for n in range(2,35):
    for S in range(1,n):
        for D in (.0001,.2,.499999):
            for _ in range(4):
                alpha=[RNG.random() for _ in range(S)]
                beta=[RNG.random() for _ in range(n-S)]
                alpha=[v/sum(alpha) for v in alpha]
                beta=[v/sum(beta) for v in beta]
                c=sum(v*v for v in alpha+beta)
                P=D/(1+sqrt(1-c*D)) # stable form of (1-sqrt(1-cD))/c
                x=[1-P*v for v in alpha]+[P*v for v in beta]
                assert all(v>.5 for v in x[:S])
                assert all(v<.5 for v in x[S:])
                assert abs(sum(x)-S)<1e-11
                assert abs(sum(v*v for v in x)-(S-D))<1e-11
                COUNTS["topology_parameterization_checks"]+=1

example=island_intervals(4,2,2,.2)
report={"status":"PASS", "counts":COUNTS, "max_witness_residual":MAX_RESIDUAL,
        "example_n4_k2_S2_Q1_8_intervals":example,
        "scope":"Numerical and exact finite audits support the proofs; finite enumeration does not prove the continuous theorem."}
Path(__file__).with_name("results.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps(report,indent=2))
```

## 付録B：実行結果

```json
{
  "status": "PASS",
  "counts": {
    "exact_grid_vectors": 19525,
    "exact_grid_partition_checks": 92775,
    "vertex_extrema_checks": 119,
    "witness_checks": 694125,
    "integer_island_component_checks": 42775,
    "sharp_stability_checks": 4704,
    "topology_parameterization_checks": 6732
  },
  "max_witness_residual": {
    "sum": 3.552713678800501e-15,
    "square_sum": 7.105427357601002e-15,
    "partial_sum": 3.552713678800501e-15
  },
  "example_n4_k2_S2_Q1_8_intervals": [
    [
      0.10557280900008414,
      0.1127016653792583
    ],
    [
      0.8872983346207417,
      1.1127016653792583
    ],
    [
      1.8872983346207417,
      1.8944271909999157
    ]
  ],
  "scope": "Numerical and exact finite audits support the proofs; finite enumeration does not prove the continuous theorem."
}
```

## 付録C：図の再現

図 `moment_islands.png` は、上段でn=3,s=1の実現ベクトル全体、下段でn=4,s=2,k=2の可能部分和を示す。緑が可能な集合。描画にはNumPyとMatplotlibを使用する。

```python
"""Render the exact examples in the accompanying research note."""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path(__file__).parent
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,
                     'axes.spines.top':False,'axes.spines.right':False})
fig = plt.figure(figsize=(10,8.7),facecolor='#fafaf7')
gs = fig.add_gridspec(2,3,height_ratios=[1,1.05],hspace=.40,
                      left=.14,right=.96,top=.78,bottom=.14)
fig.text(.07,.955,'The hidden islands in summary statistics',size=22,weight='bold',color='#142f3b')
fig.text(.07,.91,r'$0\leq x_i\leq1,\quad \sum x_i=s,\quad D=s-\sum x_i^2$   (integer $s$)',size=14)
fig.text(.07,.855,'A. All possible labeled data vectors: three values with total 1',size=12,weight='bold')
e1=np.array([1.,-1.,0.])/np.sqrt(2)
e2=np.array([1.,1.,-2.])/np.sqrt(6)
verts=np.eye(3)-1/3
poly=np.c_[verts@e1,verts@e2]
angles=np.linspace(0,2*np.pi,24001)
for col,D in enumerate([.2,.5,.6]):
    ax=fig.add_subplot(gs[0,col]);ax.set_facecolor('#fafaf7')
    closed=np.vstack([poly,poly[:1]])
    ax.fill(poly[:,0],poly[:,1],color='#e9efed')
    ax.plot(closed[:,0],closed[:,1],color='#8da5a6',lw=1.5)
    r=np.sqrt(2/3-D)
    x=1/3+r*(np.cos(angles)[:,None]*e1+np.sin(angles)[:,None]*e2)
    ok=np.all((x>=-1e-12)&(x<=1+1e-12),axis=1)
    ax.plot(np.where(ok,r*np.cos(angles),np.nan),np.where(ok,r*np.sin(angles),np.nan),color='#007c79',lw=4)
    ax.scatter([0],[0],s=14,color='#8da5a6',zorder=4)
    ax.set_title(f'D = {D:.2f}\n'+('3 separate arcs' if D<.5 else '1 connected circle'),pad=7)
    ax.set_aspect('equal');ax.set_xlim(-.85,.85);ax.set_ylim(-.95,.60);ax.axis('off')
    if col==1:ax.text(0,-1.02,'The threshold: D = 1/2',ha='center',size=11,color='#ab5700',weight='bold')
ax=fig.add_subplot(gs[1,:]);ax.set_facecolor('#fafaf7')
ax.set_title('B. Possible sum t of two values: four values with total 2',loc='left',weight='bold',pad=20)
Ds=[.2,.49,.5,.8]
for row,D in enumerate(Ds):
    low,high=1-np.sqrt(1-D),1+np.sqrt(1-D)
    ax.plot([low,high],[row,row],color='#d5dfdb',lw=3,zorder=1)
    if D<.5:
        a=(1-np.sqrt(1-2*D))/2
        intervals=[(max(low,j-a),min(high,j+a)) for j in range(3)]
    else:intervals=[(low,high)]
    for l,h in intervals:
        if l<=h:
            ax.plot([l,h],[row,row],color='#007c79',lw=11,solid_capstyle='butt')
    ax.text(2.07,row,'3 islands' if D<.5 else '1 interval',va='center',size=11)
ax.set_yticks(range(4),[f'D = {D:.2f}' for D in Ds]);ax.invert_yaxis()
ax.set_xticks([0,.5,1,1.5,2]);ax.set_xlim(-.02,2.36);ax.set_ylim(3.6,-.6)
ax.set_xlabel('Partial sum t');ax.spines[['left','right','top']].set_visible(False)
ax.tick_params(axis='y',length=0,pad=12);ax.grid(axis='x',alpha=.14)
fig.text(.07,.025,'Green = feasible. White gaps are impossible, even though they lie between feasible values.\nAnalytic sets; curves are numerically rendered. The research note gives proofs and prior-work attribution.',size=10,color='#526570')
fig.savefig(OUT/'moment_islands.png',dpi=180,facecolor=fig.get_facecolor())
plt.close(fig)
```
