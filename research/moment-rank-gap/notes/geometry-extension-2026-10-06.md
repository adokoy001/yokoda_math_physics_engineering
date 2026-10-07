# 空間・順位・ゲームの再評価（scratch 調査メモ）

調査日 2026 10 06。元資料3本の本文を読み、既に証明済みの部分と今回の導出を分けた。以下の命題は通常の数学的証明であり、形式検証・独立査読・学術的新規性の確認は未了。

## 優先候補

|候補|現行到達点|有用な抽象化・需要|次に残す具体問題|評価|
|---|---|---|---|---|
|X01 ほぼ射影の行列を監査する|二つのtrace量からrank gapの鋭い下限、ベクトル側の成分・位相|電子構造計算の密度行列purification、occupied subspaceの誤差証明|誤差付きtrace推定から丸めるsubspaceの保証、計算誤差と統計誤差の分離|実需要の確認が最も明確。既知のspectral roundingとの差分を詰める必要|
|S1 故障・外れ値に強い木上の位置推定|木上距離観測の全誤差曲線、半直径minimax、葉配置|正確な識別と距離誤差を同じ決定論的証明書へ。センサーの欠測と悪意ある値の違いを定量化|有限誤差＋q個改ざんの全曲線を木の枝構造で閉形式化し、最小費用配置へ|k-resolving/error-correcting codeは既知。数値誤差・連続実木・厳密曲線が差分候補|
|S2 固定/可変ネットワーク|独立な直線区間でRF/RAの鋭い最悪比ceil(n/2)、短区間core、O(nlogn)|再設定不能な配線と実現後適応通信の費用比較|木距離上の独立な部分木領域、少数の木を事前選択するk-adaptability、有限回の再接続|既存成果の中では定理単位が最も明確。一般化はまだ未証明|
|一例外Arc Kayles→局所証明書|T1、三角例外、抽象Mの必要十分条件、等重量R|全ゲーム木を展開せず局所応手を検証する証明書、ソルバーの削減規則|共有接点を通すcontextual equivalenceの有限要約、証明書の発見計算量|すでに抽象化がかなり進んでいる。さらに一般記述だけ増やすより検証器実装が有用|

## 今回導出 M1：exact-trace行列空間の位相

実対称または複素Hermitian行列について、1≤s<n、0≤δ<1/2とし、

Mδ={X: 0≤X≤I, tr X=s, D(X)=tr(X−X²)≤δ}。

**命題：Mδはrank-s直交射影全体へ強変形収縮する。従って実/複素Grassmannianと同じホモトピー型を持つ。**

P(X)を上位s固有値のスペクトル射影とし、H_t(X)=(1−t)X+tP(X)と置けばよい。

証明：既存X01の順位不等式からg=λ_s−λ_{s+1}≥sqrt(1−2δ)>0。したがってP(X)は一意かつXに連続。σ=Σ_{i≤s}(1−λ_i)、ρ=Σ_{i>s}λ_iとするとtr X=sによりσ=ρ。u=λ_s、v=λ_{s+1}と置くと

D'(H_t)|_{t=0}=2[Σ_{i>s}λ_i²−Σ_{i≤s}λ_i(1−λ_i)]≤2(vρ−uσ)=−2gσ≤0。

さらにD(H_t)=D(X)+tD'(0)−t²||P−X||_F²≤D(X)。凸結合なのでbox制約とtraceは保たれ、P自身ではH_t(P)=P。これが強変形収縮の全条件。□

既存本文にあった「ベクトルのbinomial個の島を行列全空間に移せない」を、行列側の正しい代替結論で補う。方法は標準的なスペクトル丸めなので、独立した大定理と呼ぶべきではない。同じ具体的なtrace-defect sublevelの記述は今回の簡易照合では未特定。

δ=1/2ではλ=(1^{s−1},1/2,1/2,0^{n−s−1})が境界gapを閉じる。これで上記のP選択が全体に連続には延長できない。n=2,s=1ではδ<1/2の集合は球殻で、δ=1/2で凸なball全体になる。一般のn,sに対する全位相遷移までは主張しない。

**trace誤差帯への同じ直線証明の拡張は失敗する。** λ=(.45,.05), s=1, η=.5ではD=.295<δ_c=.375だが、P=(1,0)に向かう直線のD'(0)=.01>0。任意δ≥.295でこの反例が直接収縮不可能を示すわけではなく、δ=.295で上記直線が許容集合を一時的に出ることを示す。別の収縮の存在は未判断。

## 今回導出 M2：trace証明書からsubspaceの安定性へ

X,YはHermitian。両者のs番目gap g_X,g_Y>0、上位s射影をP,Qとする。既知の変分原理から

||P−Q||_F ≤ 2||X−Y||_F/(g_X+g_Y)。

短い証明：r=tr(P(I−Q))=||P−Q||_F²/2。Xの固有基底で対角成分を比較すればtr X(P−Q)≥g_X r。同様にtr Y(Q−P)≥g_Y r。加えてCauchy–Schwarzを適用する。□

ここにX01のg_X≥sqrt(1−2D_X−e_X²)、g_Y≥sqrt(1−2D_Y−e_Y²)を代入できる（両radicand>0、0≤X,Y≤I）。これは新しいDavis–Kahan原理ではなく、既存のtrace証明書を実際のsubspace誤差に変換する系。traceが正確ならe=0。

需要との接続：purificationには既にtrace defectやnorm defectによる停止基準と、occupied subspaceの摂動制御がある。したがって「二つのtraceだけでgapの証明を供給できる条件」に価値を限定する。物理HamiltonianのHOMO–LUMO gapそのものを、任意のXのgapと同一視しない。正しい物理subspaceへ向いている保証にはHamiltonianとの関係・残差等が別に要る。

## 今回導出 S1q：任意値q個＋有界雑音の統一誤差半径

Tを既知の有限実木、Sを有限センサー集合とする。観測y_sは少なくとも|S|−q個のセンサーで|y_s−d(x,s)|≤εを満たし、残りq個は任意の実数を返せる。攻撃箇所は観測者に未知。

A_{S,q}(δ)=max{d(x,x'): #{s∈S: |d(x,s)−d(x',s)|>δ}≤2q}。

**命題：木内の任意点を出力してよい最良推定器の最悪誤差はE_{S,q}(ε)=A_{S,q}(2ε)/2。**

証明：二点x,x'の許容観測集合が交差するための必要十分条件が、上記のcount≤2qである。必要性は両仮説の故障集合の和集合が高々2q。十分性は差>2εの座標集合を各サイズ≤qの二つに分割し、それぞれ片方の仮説にとって故障とし、残りの座標では両距離の中点を観測にする。同じ観測の整合集合C_yは有限個の閉集合の和なのでcompact。木の中心原理から半直径で覆える。任意の曖昧な二点は同じyを持つため半距離の下界も成立。□

誤差rを保証する設置条件は、d(x,x')>2rの全対に対し、距離差>2εとなるセンサーが少なくとも2q+1個あること。有限候補の点対モデルならmulticover制約として整数計画化できる。ただし連続実木で有限個の点対制約だけを調べれば十分という還元はまだ証明していない。

q=0は既存S1の式。ε=0の2q+1条件は誤り訂正符号・k-resolvingの既知原理と直接一致する。q個の「欠測」（欠測位置が分かる）なら2qではなくqであり、両者を混同しない。葉配置優越は最大成分についての旧証明なので、q>0へ自動移植してはいけない。ここで新規候補なのはこの一般原理自体より、有限誤差曲線の明示計算・設置最適化への落とし込み。

## 文献更新・一次資料（rootが引用するときは自らopenして確認）

1. Kruchinina, Rudberg, Rubensson, Parameterless stopping criteria for recursive density matrix expansions, JCTC 12(12), 5788–5802 (2016). https://arxiv.org/html/1507.02087v3 。導入全文確認。密度行列はoccupied eigenvectorsへの射影、gap依存のcondition number、trace(X−X²)を用いた既存停止基準、CP2K/Ergo等の実装を述べる。web refs turn15view0 / turn14view1。候補の需要を裏付ける。停止基準自体の新規性は主張不可。
2. Artemov, Rubensson, Sparse approximate matrix-matrix multiplication for density matrix purification with error control. https://arxiv.org/abs/2005.10680 / https://doi.org/10.1016/j.jcp.2021.110354 。要旨確認。厳密誤差制御を含む大規模電子構造計算。web refs turn16view2 / turn14search0。
3. Bailey, Yero, Error-correcting codes from k-resolving sets, Discussiones Mathematicae Graph Theory 39 (2019), 341–355. https://arxiv.org/abs/1605.03141 、大学リポジトリPDF https://rodin.uca.es/bitstream/handle/10498/21882/2019_333.pdf?isAllowed=y&sequence=1 。要旨と導入検索結果確認、web refs turn25academia26 / turn25search25。距離署名の誤り訂正は既知。
4. Fawzi, Tabuada, Diggavi, Secure estimation and control for cyber-physical systems under adversarial attacks. https://arxiv.org/abs/1205.5073 。要旨確認、web ref turn25academia24。任意センサー誤りへの回復は既存の大きな研究分野。
5. Bonnet, Arc Kayles is PSPACE-complete, arXiv:2609.23777, 2026 09 20. arxivのopenは取得失敗したが、arxiv検索索引要旨と著者本人ページ https://perso.ens-lyon.fr/edouard.bonnet/papers.htm のmanuscript 11に同じ題を確認。web refs turn15academia13 / turn16view0。**一般Arc Kaylesの計算困難性を現在も未解決と書かない。** 最新プレプリントが解決を報告、と精度を保つ。証明本文未監査、査読状況未確認。

## 推奨

X01を応用監査の第一候補として、低コストなtrace/trace-square証明書とsubspace誤差の実装比較まで進める。数学だけならM1のGrassmannian帰結が短く閉じており、本文の位相上の穴を埋める。S2は別途木距離への一般化を実験する価値が高いが、本日証明した扱いにしない。一例外ゲームは一般化R/Mまで到達しているため、次は証明書のソルバー応用・共有接点の最小情報を狙う方が具体的。
