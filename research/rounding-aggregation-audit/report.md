# 数学探索の独立候補：丸め・集計・相対比較監査

作成日：2026 09 08。独立探索3枝の保存版。本文は証明・適用範囲・既知との関係をまとめ、付録には検証コードを全文収録した。

| 候補ID | 対象 | 今回の到達点 | 新規性の扱い |
|---|---|---|---|
| X02 | 区間和を保つ整数丸め | 不偏性に伴う最悪誤差と出力分布の一意性を証明 | 既知のglobal rounding構造からの短い系。未確定 |
| X03 | 区間集計からの時系列復元 | 全単調重みの各クエリで同時ミニマックスとなる復元列を証明 | 差分制約・確率順序の既知理論に近い。未確定 |
| X04 | 相対比較の三角監査 | 最少本数と不完全監査中の最良保証を同時達成する方式を証明 | 比較行列・循環空間の既知部品を使用。同一結果の照合未完 |

いずれも「学術的新規性が確定した成果」への登録ではない。一般命題の証明と有限計算の一致を区別し、未証明の強化は独立に記載する。形式証明支援系および外部専門家による査読は未実施。

## X02：区間丸めにおける不偏性の厳密な代価

固定入力 $x\in\mathbb R^n$ の各成分を $y_i\in\{\lfloor x_i\rfloor,\lceil x_i\rceil\}$ に丸める。全連続区間での最大絶対誤差を

$$
D_x(y)=\max_{0\le a<b\le n}\left|\sum_{a<i\le b}(y_i-x_i)\right|
$$

とする。累積和 $S_0=0,S_k=\sum_{i\le k}x_i$ の**異なる小数部分**を $0=r_0<\cdots<r_{m-1}<1$ と並べ、$r_m=1$、$g_j=r_j-r_{j-1}$ と置く。

### 命題と証明

決定論的最適値と、不偏ランダム丸めの最良の最悪値はそれぞれ

$$
\min_yD_x(y)=1-\max_jg_j,
\qquad
\inf_{\mathbb EY=x}\operatorname{ess\,sup}D_x(Y)=1-\min_jg_j.
$$

さらに、$\mathbb EY=x$ かつ $D_x(Y)<1$ をほぼ確実に満たす出力分布は一意である。その $m$ 個の出力を $y^{(j)}$ とすると

$$
\Pr(Y=y^{(j)})=g_j,\quad D_x(y^{(j)})=1-g_j,
\quad \mathbb ED_x(Y)=1-\sum_jg_j^2.
$$

**証明。** 整数累積和 $T_k=\sum_{i\le k}y_i$、累積誤差 $e_k=T_k-S_k$ を置くと、区間誤差は $e_b-e_a$ なので $D=\max e_k-\min e_k$。$D<1,e_0=0$ より、$\rho_k=\{S_k\}$ として $T_k=\lfloor S_k\rfloor+z_k$、$z_k\in\{0,1\}$。$\rho_k=0$ なら $z_k=0$。$\rho_a<\rho_b$ で $z_a=1,z_b=0$ なら $e_a-e_b=1+\rho_b-\rho_a>1$ となり矛盾する。同じ小数部分に異なる $z$ を付けることもできない。

従って $D<1$ の出力は、小数部分の一つのギャップに閾値 $\theta\in(r_{j-1},r_j)$ を置いた

$$
T_k=\lfloor S_k\rfloor+\mathbf1\{\rho_k>\theta\}
=\lfloor S_k+1-\theta\rfloor
$$

の $m$ 候補に限る。差 $y_i=T_i-T_{i-1}$ は必ず許容された丸めであり、累積誤差の幅は $1-g_j$。全候補が $D<1$ なので決定論最適値が従う。

不偏性から $\mathbb ET_k=S_k$、従って $\mathbb Ez_k=\rho_k$。$\rho_k=r_l$ の位置では候補 $j\le l$ だけが $z_k=1$ なので、候補確率 $p_j$ は $\sum_{j\le l}p_j=r_l$ を満たす。差を取ると $p_j=g_j$ が一意に決まる。逆も成立する。この分布の最悪値は $1-\min g_j<1$。これより良い不偏分布があればやはり $D<1$ となり、一意性に反する。期待値の式は $\sum_jg_j(1-g_j)$ から得る。入力が全て整数なら $m=1,g_1=1$ で全誤差が0になる。□

### 例・検証・未解決

$x=(0.1,0.8,0.1)$ ではギャップは $(0.1,0.8,0.1)$。$(1,0,0),(0,1,0),(0,0,1)$ の出力確率は順に $0.1,0.8,0.1$、最大区間誤差は $0.9,0.2,0.9$。決定論なら誤差0.2で済むが、不偏性を要求すると最悪0.9が不可避。上記分布の平均誤差は0.34。

分母4、長さ1〜6、各値 $\{0,1/4,1/2,3/4,1\}$ の19,530数列と299,592丸めを全列挙した。$D<1$ の61,740丸めについて、候補の完全性・決定論最適値・不偏性・平均誤差式を整数演算で確認し、反例0。

**未証明の強化：** $D<1$ の制限を外した全不偏分布中でも $\mathbb ED$ の最小値が $1-\sum g_j^2$ か。長さ2〜10の各500ランダム入力の線形計画では一致したが、一般証明はない。関連整数不等式も $m=2$〜14の各100,000件で反例がなかったものの未証明。これら追加実験は作業ログの記録で、再現コードは本書に含まれない。命題の根拠として使わない。

### 一次出典と帰属

- B. Doerr, *Global roundings of sequences* (2004)：全区間誤差 $<1$ の特徴づけと最適丸めは既知。[出版社・DOI](https://www.sciencedirect.com/science/article/pii/S0020019004002194)。今回は抄録を確認し、本文は取得できていない。
- K. Sadakane, N. Takki-Chebihi, T. Tokuyama, *Combinatorics and Algorithms on Low-Discrepancy Roundings of a Real Sequence* (ICALP 2001)：丸め候補数と列挙の先行研究。[出版社](https://link.springer.com/chapter/10.1007/3-540-48224-5_14)。抄録確認、本文未取得。
- B. Doerrほか, *Unbiased Matrix Rounding* (2006)：1次元の全区間誤差 $<1$ 丸めと、不偏controlled roundingの系譜。[本文](https://arxiv.org/pdf/cs/0604068)。本文を確認した。

比較公式と不偏分布の一意性が同じ形で先行文献に明記されるかは未確定。ただし既知特徴づけから短く導けるため、「新定理」と断言する根拠はない。

## X03：区間集計からの全単調クエリ同時ミニマックス復元

未知の実数列 $x=(x_1,\ldots,x_n)$ について、各成分の有限上下界、任意の重複区間総和の上下界、および正確な全体総和 $T$ が既知とする。これらを満たす集合 $F$ は非空と仮定する。

### 命題と証明

累積和 $S_0=0,S_i=\sum_{k\le i}x_k$ の極値を $L_i=\min_F S_i,U_i=\max_F S_i$ と置く。すると $L,U$ はそれぞれ一本の実現可能列の累積和となる。また

$$
C_i=\frac{L_i+U_i}{2},\qquad x_i^*=C_i-C_{i-1}
$$

は実現可能で、**任意の単調重み** $w$ の線形クエリ $Q_w(x)=\sum_iw_ix_i$ について

$$
\inf_{a\in\mathbb R}\sup_{x\in F}|a-Q_w(x)|
=\frac12\sum_{i=1}^{n-1}|w_{i+1}-w_i|(U_i-L_i)
$$

を $a=Q_w(x^*)$ が達成する。全単調重みの各クエリで同時最適となる復元列は $x^*$ のみ。

**証明。** 区間総和制約は累積和に対する差分制約 $S_j\le S_i+c$ の集まりになる。この制約を満たす2ベクトルの成分ごとのmin/maxも同じ制約を満たす。各成分の最小値を達成する有限個のベクトルのminを取れば $L$ 自体が実現可能であり、$U$ も同様。制約集合は凸なので中点 $C$ も実現可能。

離散部分積分から

$$
Q_w(x)=w_nT-\sum_{i=1}^{n-1}(w_{i+1}-w_i)S_i.
$$

重みが単調なら係数の符号が揃い、極値は $S=L,U$ で同時に達成される。その回答区間の中点は $Q_w(x^*)$、半径は上式である。区間 $[A,B]$ の真値を絶対誤差で推定する唯一のミニマックス回答は $(A+B)/2$ なので結論が従う。前半和を読む段差重みを全位置で使うと、同時最適な累積和は各 $C_i$ に一意に定まり、復元列も一意になる。□

計算は差分制約 $S_j-S_i\le c$ を辺 $i\to j$、重み $c$ にしたグラフで行う。最短路距離を $d$ とすると $U_i=d(0,i),L_i=-d(i,0)$。経路上の制約和が上下界を与え、最短路の三角不等式から両ベクトル自体も制約を満たす。元グラフと逆向きグラフでBellman–Fordを一回ずつ行えばよい。負閉路は情報の矛盾を表す。

### 例・検証・限界

$0\le x_i\le1$、総和 $T$ だけなら $L_i=\max(0,T-(n-i))$、$U_i=\min(i,T)$。古い側へ総量を詰めた列と新しい側へ詰めた列の平均が $x^*$ になる。

$n=4,T=1$ なら $x^*=(1/2,0,0,1/2)$。最近ほど倍に重くする $w=(1,2,4,8)/15$ の可能回答は $[1/15,8/15]$。$x^*$ の回答は $3/10$、最悪誤差は $7/30$。全要素を保存平均 $1/4$ で埋めると最悪誤差は $17/60$。この例で最悪誤差を約17.65%縮める。

長さ2〜7の600制約系で全格子列を調べ、実現可能な3899列と12000符号付き単調クエリを整数・Fractionで独立照合した。反例0。これは元ログのもっともらしさの推定ではなく、指定クエリ族に対する決定論的保証である。全忘却率の指数重みはこのクエリ族に入る。

**適用限界：** 非単調重みでは失敗する。$n=3,T=1$ の $x^*=(1/2,0,1/2)$ で中央だけ読むと回答0だが、真値範囲 $[0,1]$ の最適回答は $1/2$。総和固定も無条件には外せない。$x_1,x_2\ge0,x_1+x_2\le1$ では各成分と総和の個別最適回答は全部 $1/2$ となり、単一列で同時に答えられない。二次モーメント・滑らかさ条件を追加した場合にも、min/max閉性を再証明する必要がある。

### 一次出典と帰属

- R. Dechter, I. Meiri, J. Pearl, *Temporal Constraint Networks* (1991)：差分制約と最短路の既知基盤。[著者公開PDF](https://ics.uci.edu/~dechter/publications/r10.pdf)、[DOI](https://doi.org/10.1016/0004-3702(91)90006-6)。
- *An Efficient Incremental Simple Temporal Network Data Structure for Temporal Planning*：第2節に距離グラフ・負閉路・反転グラフの計算構造。[本文](https://arxiv.org/html/2212.07226v2)。
- M. Troffaes, S. Destercke, *Probability boxes on totally preordered spaces for multivariate modelling* (2011)：累積分布の上下包絡から期待値境界へ進む既知理論。[論文](https://arxiv.org/abs/1103.1805)。

最短路計算そのものは新手法ではない。「任意の重複区間集計から一本を復元し、全単調クエリの各ミニマックス回答を得る」という一体の記述との直接照合は未完。既知理論の明示的な応用上の帰結として保存する。

## X04：相対比較の三角監査を最少本数で行う

全ペアの実数比較 $a_{ij}=-a_{ji}$、$a_{ii}=0$ が既知とする。整合する比較はあるスコア $x_i$ による差 $x_i-x_j$ であり、最小最大修正量を

$$
d(a)=\min_x\max_{i<j}|a_{ij}-(x_i-x_j)|
$$

とする。三角循環和 $\tau_{ijk}=a_{ij}+a_{jk}+a_{ki}$ を調べる監査集合 $T$ に対し、$C(T)=\sup\{d(a):|\tau_t|\le1\ (t\in T)\}$ と定義する。

### 四命題と短い証明

$n\ge4$、$q=(n-1)(n-2)/2$ とする。

1. **全三角監査の係数は $(n-2)/n$。** $x_i=n^{-1}\sum_k a_{ik}$ なら各残差は $n^{-1}\sum_k\tau_{ijk}$。非零になり得る項は $n-2$ 個なので上界が従う。鋭さは $i<j$ で $a_{ij}=1$ とする例から得る。各三角和は1、長さ $n$ の循環和は $n-2$。スコア差の循環和は0なので $nd(a)\ge n-2$。
2. **固定頂点 $r$ を含む $q$ 三角形の監査は係数1。** $x_i=a_{ir}$ なら残差は $\tau_{ijr}$ で上界1。下界は次項から得る。
3. **三角形を一つでも省いた監査は係数が1以上。** 未監査三角形の向きに沿う三辺だけを1、その他を0とする。他の三角形はこれらを高々一辺しか共有せず、全監査を閾値1で通る。しかし未監査三角和は3なので $d(a)\ge1$。$x=0$ が上界1を達成する。
4. **有限係数には少なくとも $q$ 本が必要。** 反対称比較の空間は次元 $m=n(n-1)/2$、スコア差部分空間は次元 $n-1$。監査本数が $q=m-(n-1)$ 未満なら、全監査が0でもスコア差ではないベクトルが核に残る。それを任意倍率に拡大できるため係数は無限大。□

従って固定頂点方式は、**本数が最少で、かつ全ての不完全な監査方式中で最良の最悪保証**を達成する。閾値 $\varepsilon$ の場合は斉次性で修正量上界も $\varepsilon$ 倍となる。

### 例・厳密検査・未解決

$n=100$ では全三角形161,700個に対し固定頂点方式は4,851個、3%。同じ監査閾値を満たすデータ族の修正量上界は $0.98\varepsilon$ から $\varepsilon$ になる。全ペアの取得数を減らす主張ではなく、内部整合性の監査数を減らす主張である。正しい順位・外界の真実・測定器の健全性は保証しない。固定頂点も「信頼できる対象」という仮定を要さない。

$n=5$ の最少6三角形を選ぶ全210設計を、逆向きを同一視した全37単純循環と有理数演算で分類した。

| 保証係数 | 設計数 |
|---|---:|
| 1 | 5：固定頂点方式と完全一致 |
| $5/3$ | 120：その他の独立な監査基底 |
| $\infty$ | 85：階数不足 |

この検査では既知の式 $d(a)=\max_c|\sum_{e\in c}a_e|/|c|$ を使う。下界は循環相殺から得られ、上界は差分制約 $x_j\le x_i-a_{ij}+d$ に負閉路がなければ解を持つことから得られる。固定頂点0との辺値を0にした座標で監査基底を $B$、循環行を $c$ とすれば、係数は $\max_c\|cB^{-1}\|_1/|c|$ となり、厳密に計算できる。

例として頂点0〜4、監査 $012,013,014,023,024,134$、辺 $12,13,14,23,24,34$ の値を $(-1,-1,1,1,-1,3)$、辺 $0i$ を0とする。全監査三角和の絶対値は1だが、三角形234の循環和は5で修正量が少なくとも $5/3$。どの最少基底でも係数1というわけではない。別途SciPyの線形計画で $n=3$〜6の基本設計と $n=5$ の全設計を数値照合した。

**追加の証明済み必要条件：** 最少本数の基底が係数1なら、未監査三角形 $abc$ ごとに、外側の一意な頂点 $v$ があり、三角形 $abv,bcv,cav$ が全部監査されている。実際、$\tau_{abc}=\sum_t\lambda_t\tau_t$ の一意な基底展開に対し、係数1の保証は $\sum|\lambda_t|\le3$ を与える。命題3の三辺データでは $\tau_{abc}=3$ なので等号となる。等号条件から、非零係数の面は $abc$ の辺を共有し、向きを揃えた係数は非負。外側頂点 $v$ ごとの三面係数を $\alpha_v,\beta_v,\gamma_v$ とすれば、外向き辺の相殺で三者は等しく、$\sum_v\alpha_v=1$。よって一つ以上の三面組が存在する。二組あれば両者が同じ境界 $abc$ を持ち、基底の線形独立性に反する。

**未解決：** $n\ge6$ でも最少本数かつ係数1の設計が固定頂点方式に限られるか。この必要条件を十分条件としては用いていない。境界では $n=3$ の全監査係数は $1/3$、その唯一の三角形を省くと無限大。$n\le2$ は常に整合し $d=0$。

### 一次出典と帰属

- N. Krivulin, *Using tropical optimization techniques to evaluate alternatives via pairwise comparisons* (2015/2016)：log-Chebyshev近似の既知分野。[論文](https://arxiv.org/abs/1503.04003)。抄録確認。
- H. Goto, S. Wang, *Polyad inconsistency measure for pairwise comparisons matrices: max-plus algebraic approach* (2020/2022)：循環とmax-plus固有値。[出版社](https://link.springer.com/article/10.1007/s12351-020-00547-9)。抄録・参考文献確認、本文未読。
- R. Singh, O. Davidov, *The analysis of paired comparison data in the presence of cyclicality and intransitivity* (2024)：スコア差・三角循環・循環空間。[本文](https://arxiv.org/html/2406.11584v1)。関連箇所を確認。
- S. Bozóki, J. Fülöp, A. Poesz, *On pairwise comparison matrices that can be made consistent by the modification of a few elements* (2011)：少数要素修正という隣接問題。[機関公開原稿](https://real.mtak.hu/62931/1/BozokiFulopPoesz-CEJOR-2011-Manuscript.pdf)、[出版社](https://link.springer.com/article/10.1007/s10100-010-0136-9)。抄録・索引確認、全文照合は残る。

循環和・行平均・最大平均循環・次元下限は既知部品。四命題を合わせた設計保証と同じ結果は今回の予備照合で特定していないが、cofilling/filling norms、simplicial spanning trees、hypertree設計等の別用語で既出の可能性がある。



## 付録：再現コード全文と結果要約

以下のPythonブロックを見出しに指定されたファイル名で保存し、`python ファイル名.py` で実行できる。X02・X03・X04の有理数検査は標準ライブラリのみ。X04の独立した数値照合コードだけはNumPyとSciPyを必要とする。入力を変えれば一般的な研究用計算にも使えるが、掲載した検証範囲を越える正しさは本文の一般証明と適用条件に依存する。

コードは各探索枝の検証ファイルをそのまま収録した。結果JSONは大きな個別設計一覧を省いた要約であり、X04の全設計の内容はコード実行で再生成できる。

### X02：check_rounding.py

```python
"""Exact arithmetic checks for sequence rounding; no random tolerance needed."""
from itertools import product
from fractions import Fraction
import json
from pathlib import Path

summary={'denominator':4,'max_n':6,'sequences':0,'rounding_vectors':0,'global_rounding_vectors':0,'failures':0}
q=summary['denominator']
for n in range(1,summary['max_n']+1):
    for a in product(range(q+1),repeat=n):
        s=[0]
        for v in a:s.append(s[-1]+v)
        residues=sorted({v%q for v in s})
        gaps=[b-a for a,b in zip(residues,residues[1:]+[q])]
        produced={}
        for lo,hi in zip(residues,residues[1:]+[q]):
            # Threshold strictly inside the gap; doubled integer arithmetic.
            threshold2=lo+hi
            z=[v//q + int(2*(v%q)>=threshold2) for v in s]
            y=tuple(z[i+1]-z[i] for i in range(n))
            e=[q*z[k]-s[k] for k in range(n+1)]
            D=max(e)-min(e)
            assert D==q-(hi-lo)
            assert y not in produced
            produced[y]=(hi-lo,D)
        globally_feasible=set()
        optimum=q*n+1
        for y in product([0,1],repeat=n):
            # Integer coordinates are required to stay exact when already integer.
            if any(a[i]==0 and y[i] or a[i]==q and not y[i] for i in range(n)):
                continue
            summary['rounding_vectors']+=1
            e=[0]
            for i in range(n):e.append(e[-1]+q*y[i]-a[i])
            D=max(e)-min(e)
            optimum=min(optimum,D)
            if D<q:globally_feasible.add(y)
        assert globally_feasible==set(produced)
        assert optimum==q-max(gaps)
        assert all(sum(m*y[i] for y,(m,D) in produced.items())==a[i] for i in range(n))
        assert sum(m*D for m,D in produced.values())==q*q-sum(g*g for g in gaps)
        summary['sequences']+=1
        summary['global_rounding_vectors']+=len(produced)
print(json.dumps(summary,indent=2))
Path(__file__).with_name('verification.json').write_text(json.dumps(summary,indent=2)+'\n')
```

実行結果（要約）：

```json
{
  "denominator": 4,
  "max_n": 6,
  "sequences": 19530,
  "rounding_vectors": 299592,
  "global_rounding_vectors": 61740,
  "failures": 0
}
```

### X03：verify_monotone_reconstruction.py

```python
"""Exact standard-library verification of monotone-query reconstruction.

Run: python verify_monotone_reconstruction.py
No floating-point comparisons, no external dependencies.
"""
from fractions import Fraction as F
from itertools import product, accumulate
from random import Random
import json


def shortest_paths(nvertices, edges, source=0):
    """Bellman-Ford: edges (i,j,c) encode S[j]-S[i] <= c."""
    d = [None] * nvertices
    d[source] = 0
    for _ in range(nvertices):
        changed = False
        for i, j, c in edges:
            if d[i] is not None and (d[j] is None or d[j] > d[i] + c):
                d[j] = d[i] + c
                changed = True
        if not changed:
            return d
    raise ValueError("Inconsistent interval summaries: negative cycle")


def reconstruct(n, interval_bounds):
    """Bounds are (i,j,lo,hi), for sum(x[i:j]) in [lo,hi].

    Include finite bounds for every x_i and an exact total bound.
    Indexing is Python's zero-based, half-open convention.
    All numbers may be int or fractions.Fraction.
    """
    edges = []
    for i, j, lo, hi in interval_bounds:
        edges += [(i, j, hi), (j, i, -lo)]
    U = shortest_paths(n + 1, edges)
    reverse = [(j, i, c) for i, j, c in edges]
    reverse_d = shortest_paths(n + 1, reverse)
    if any(v is None for v in U + reverse_d):
        raise ValueError("Every prefix needs finite upper and lower bounds")
    L = [-v for v in reverse_d]
    midpoint = [F(lo + hi, 2) for lo, hi in zip(L, U)]
    xstar = [midpoint[i + 1] - midpoint[i] for i in range(n)]
    return L, U, xstar


def query_interval(w, L, U):
    """Exact answer interval for any real-valued monotone w.

    Assumes fixed total: L[-1] == U[-1].
    """
    if not all(w[i] <= w[i + 1] for i in range(len(w) - 1)) and not all(
        w[i] >= w[i + 1] for i in range(len(w) - 1)
    ):
        raise ValueError("The theorem requires monotone weights")
    assert L[-1] == U[-1]
    a = w[-1] * L[-1] - sum((w[i] - w[i - 1]) * L[i] for i in range(1, len(w)))
    b = w[-1] * U[-1] - sum((w[i] - w[i - 1]) * U[i] for i in range(1, len(w)))
    return min(a, b), max(a, b)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def feasible(x, bounds):
    return all(lo <= sum(x[i:j]) <= hi for i, j, lo, hi in bounds)


def main():
    rng = Random(20260908)
    tested_queries = 0
    feasible_grid_vectors = 0
    cases = 600
    for _ in range(cases):
        n = rng.randrange(2, 8)
        witness = tuple(rng.randrange(3) for _ in range(n))
        total = sum(witness)
        bounds = [(i, i + 1, 0, 2) for i in range(n)]
        bounds.append((0, n, total, total))
        for _ in range(2 * n):
            i = rng.randrange(n)
            j = rng.randrange(i + 1, n + 1)
            s = sum(witness[i:j])
            bounds.append((i, j, max(0, s - rng.randrange(4)), min(2 * (j - i), s + rng.randrange(4))))
        L, U, xstar = reconstruct(n, bounds)
        assert feasible(xstar, bounds)
        xmin = tuple(L[i + 1] - L[i] for i in range(n))
        xmax = tuple(U[i + 1] - U[i] for i in range(n))
        assert feasible(xmin, bounds) and feasible(xmax, bounds)
        possible = [x for x in product(range(3), repeat=n) if feasible(x, bounds)]
        assert xmin in possible and xmax in possible
        feasible_grid_vectors += len(possible)
        prefixes = [tuple(accumulate((0,) + x)) for x in possible]
        assert L == [min(s[i] for s in prefixes) for i in range(n + 1)]
        assert U == [max(s[i] for s in prefixes) for i in range(n + 1)]
        for _ in range(20):
            w = sorted((rng.randrange(-9, 10) for _ in range(n)), reverse=rng.choice([True, False]))
            lo, hi = query_interval(w, L, U)
            values = [dot(w, x) for x in possible]
            assert (lo, hi) == (min(values), max(values))
            assert dot(w, xstar) == F(lo + hi, 2)
            radius = F(sum(abs(w[i] - w[i - 1]) * (U[i] - L[i]) for i in range(1, n)), 2)
            assert radius == F(hi - lo, 2)
            tested_queries += 1

    # Four slots, range [0,1], total 1, half-life-one-slot weights.
    bounds = [(i, i + 1, 0, 1) for i in range(4)] + [(0, 4, 1, 1)]
    L, U, xstar = reconstruct(4, bounds)
    w = [F(z, 15) for z in (1, 2, 4, 8)]
    lo, hi = query_interval(w, L, U)
    answer = dot(w, xstar)
    uniform = F(1, 4)
    optimum_error = F(hi - lo, 2)
    uniform_error = max(uniform - lo, hi - uniform)
    assert xstar == [F(1, 2), 0, 0, F(1, 2)]
    assert answer == F(3, 10)
    assert optimum_error == F(7, 30)
    assert uniform_error == F(17, 60)

    # Nonmonotone weights: same center has twice the best possible error.
    bounds3 = [(i, i + 1, 0, 1) for i in range(3)] + [(0, 3, 1, 1)]
    _, _, center3 = reconstruct(3, bounds3)
    assert center3 == [F(1, 2), 0, F(1, 2)]
    assert dot([0, 1, 0], center3) == 0  # true query range [0,1], optimum midpoint 1/2.

    # Inconsistency detection.
    try:
        reconstruct(1, [(0, 1, 0, 1), (0, 1, 2, 2)])
    except ValueError:
        pass
    else:
        raise AssertionError("A negative cycle went undetected")

    result = {
        "seed": 20260908,
        "constraint_systems": cases,
        "monotone_weight_queries": tested_queries,
        "feasible_grid_vectors": feasible_grid_vectors,
        "arithmetic": "exact integers and Fraction",
        "all_assertions_passed": True,
        "example": {"xstar": list(map(str, xstar)), "query_interval": [str(lo), str(hi)],
                    "minimax_answer": str(answer), "uniform_fill_answer": str(uniform),
                    "minimax_error": str(optimum_error), "uniform_fill_error": str(uniform_error)},
        "scope": "Finite grid verification and counterexamples support but do not replace the written real-valued proof."
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

実行結果（要約）：

```json
{
  "seed": 20260908,
  "constraint_systems": 600,
  "monotone_weight_queries": 12000,
  "feasible_grid_vectors": 3899,
  "arithmetic": "exact integers and Fraction",
  "all_assertions_passed": true,
  "example": {
    "xstar": [
      "1/2",
      "0",
      "0",
      "1/2"
    ],
    "query_interval": [
      "1/15",
      "8/15"
    ],
    "minimax_answer": "3/10",
    "uniform_fill_answer": "1/4",
    "minimax_error": "7/30",
    "uniform_fill_error": "17/60"
  },
  "scope": "Finite grid verification and counterexamples support but do not replace the written real-valued proof."
}
```

### X04 厳密有理数検査：check_n5_exact.py

```python
"""Exact rational verification of all 6-triangle audit designs on K5.

For a full-rank audit basis B in root-zero gauge, the worst repair
constant is max_cycle ||c B^{-1}||_1 / length(c). This follows from
the known maximum-cycle-mean formula and box duality. There are no
floating-point rank, optimization, or equality decisions here.
"""
import itertools as it
import json
from fractions import Fraction as F

def invert(matrix):
    size=len(matrix)
    aug=[[F(x) for x in row]+[F(i==j) for j in range(size)] for i,row in enumerate(matrix)]
    for col in range(size):
        pivot=next((r for r in range(col,size) if aug[r][col]),None)
        if pivot is None:return None
        aug[col],aug[pivot]=aug[pivot],aug[col]
        p=aug[col][col]
        aug[col]=[v/p for v in aug[col]]
        for r in range(size):
            if r!=col and aug[r][col]:
                p=aug[r][col]
                aug[r]=[a-p*b for a,b in zip(aug[r],aug[col])]
    return [row[size:] for row in aug]

n=5
edges=list(it.combinations(range(1,n),2))
edge_idx={e:i for i,e in enumerate(edges)}
def vec(cycle):
    v=[0]*len(edges)
    for a,b in zip(cycle,cycle[1:]+cycle[:1]):
        if a==0 or b==0:continue
        v[edge_idx[tuple(sorted((a,b)))]]+=1 if a<b else -1
    return v

triangles=list(it.combinations(range(n),3))
T=[vec(t) for t in triangles]
cycles=[]
for k in range(3,n+1):
    for subset in it.combinations(range(n),k):
        for tail in it.permutations(subset[1:]):
            cycle=(subset[0],)+tail
            if cycle[1]<cycle[-1]:cycles.append(cycle)
C=[vec(c) for c in cycles]
hist={}
designs=[]
for sel in it.combinations(range(10),6):
    B=[T[i] for i in sel]
    inv=invert(B)
    if inv is None:
        hist['unbounded']=hist.get('unbounded',0)+1
        continue
    Q=[[sum(row[k]*inv[k][j] for k in range(6)) for j in range(6)] for row in C]
    values=[sum(abs(q) for q in Q[j])/len(cycle) for j,cycle in enumerate(cycles)]
    worst=max(values)
    key=str(worst)
    hist[key]=hist.get(key,0)+1
    common=set(range(n))
    for i in sel:common.intersection_update(triangles[i])
    assert (worst==1)==bool(common)
    designs.append({'triangles':[triangles[i] for i in sel], 'constant':key, 'common_anchor':list(common)})

out={'n':n,'total_designs':210,'cycles_up_to_reversal':len(cycles),'histogram':hist,'designs':designs}
print(json.dumps(out,indent=2))
```

実行結果（要約）：

```json
{
  "n": 5,
  "total_designs": 210,
  "cycles_up_to_reversal": 37,
  "histogram": {
    "1": 5,
    "unbounded": 85,
    "5/3": 120
  },
  "omitted_details": "125 full-rank designs; regenerated by the code above"
}
```

### X04 独立数値照合：check_audits.py

```python
import itertools as it
import json
import numpy as np
from scipy.optimize import linprog

def model(n):
    edges=list(it.combinations(range(1,n),2))
    edge_idx={e:i for i,e in enumerate(edges)}
    def vec(sequence):
        out=np.zeros(len(edges))
        for a,b in zip(sequence,sequence[1:]+sequence[:1]):
            if a==0 or b==0: continue
            out[edge_idx[tuple(sorted((a,b)))]]+=1 if a<b else -1
        return out
    triangles=list(it.combinations(range(n),3))
    T=np.array([vec(t) for t in triangles])
    cycles=[]
    C=[]
    for k in range(3,n+1):
        for subset in it.combinations(range(n),k):
            for tail in it.permutations(subset[1:]):
                cyc=(subset[0],)+tail
                if cyc[1]>cyc[-1]: continue
                cycles.append(cyc)
                C.append(vec(cyc)/k)
    return edges,triangles,T,cycles,np.array(C)

def constant(n,selection,mdl=None):
    if mdl is None:mdl=model(n)
    edges,triangles,T,cycles,C=mdl
    A=T[selection]
    if np.linalg.matrix_rank(A)<len(edges): return float('inf'),None
    best=(-1,None)
    for cyc,c in zip(cycles,C):
        res=linprog(-c,A_ub=np.r_[A,-A],b_ub=np.ones(2*len(A)),bounds=[(None,None)]*len(edges),method='highs')
        assert res.success
        if -res.fun>best[0]+1e-8:best=(-res.fun,{'cycle':cyc,'gauge_edges':edges,'values':res.x.tolist()})
    return best

def main():
    out={'basic':[]}
    for n in range(3,9):
        mdl=model(n)
        tris=mdl[1]
        # n=8 has 8000+ cycles, explicit full worst matrix provides a smaller check.
        if n<=6:
            full=constant(n,list(range(len(tris))),mdl)[0]
            star=constant(n,[i for i,t in enumerate(tris) if 0 in t],mdl)[0]
            single_missing=constant(n,list(range(len(tris)-1)),mdl)[0] if n>=4 else 'unbounded'
            out['basic'].append({'n':n,'full':full,'star':star,'single_missing':single_missing})
    mdl=model(5)
    hist={}
    worst=(0,None)
    count=0
    for sel in it.combinations(range(10),6):
        c,w=constant(5,list(sel),mdl)
        if not np.isfinite(c):continue
        count+=1
        key=str(round(c,8))
        hist[key]=hist.get(key,0)+1
        if c>worst[0]+1e-8:worst=(c,{'triangles':[mdl[1][i] for i in sel],'witness':w})
    out['n5_bases']={'count':count,'histogram':hist,'worst':worst}
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
```

実行結果（要約）：

```json
{
  "basic": [
    {
      "n": 3,
      "full": 0.3333333333333333,
      "star": 0.3333333333333333,
      "single_missing": "unbounded"
    },
    {
      "n": 4,
      "full": 0.5,
      "star": 1.0,
      "single_missing": 1.0
    },
    {
      "n": 5,
      "full": 0.6000000000000001,
      "star": 1.0,
      "single_missing": 1.0
    },
    {
      "n": 6,
      "full": 0.6666666666666666,
      "star": 1.0,
      "single_missing": 1.0
    }
  ],
  "n5_bases": {
    "count": 125,
    "histogram": {
      "1.0": 5,
      "1.66666667": 120
    },
    "worst": [
      1.6666666666666665,
      {
        "triangles": [
          [
            0,
            1,
            2
          ],
          [
            0,
            1,
            3
          ],
          [
            0,
            1,
            4
          ],
          [
            0,
            2,
            3
          ],
          [
            0,
            2,
            4
          ],
          [
            1,
            3,
            4
          ]
        ],
        "witness": {
          "cycle": [
            2,
            3,
            4
          ],
          "gauge_edges": [
            [
              1,
              2
            ],
            [
              1,
              3
            ],
            [
              1,
              4
            ],
            [
              2,
              3
            ],
            [
              2,
              4
            ],
            [
              3,
              4
            ]
          ],
          "values": [
            -1.0,
            -1.0,
            1.0,
            1.0,
            -1.0,
            3.0
          ]
        }
      }
    ]
  }
}
```
