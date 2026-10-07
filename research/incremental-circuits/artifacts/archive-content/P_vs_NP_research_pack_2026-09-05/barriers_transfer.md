# P vs NP 再始動監査：障壁・下方移送・量化

確認日：2026 09 05。対象：回収ノート v0.24 の主に §19、§25、§28–30。元ノートは変更していない。

## 1. 今回の実質的な修正

最も重要な修正候補は §19.5。そこでは「P=NP と NEXP⊄P/poly は既知包含からは矛盾しない」とされているが、より強く、既知定理から次が導かれる。

\[
\boxed{P=NP\ \Longrightarrow\ NEXP\not\subseteq P/poly.}
\]

**導出（既知結果の直接合成、新規性を主張しない）。** Impagliazzo–Kabanets–Wigderson の Theorem 23 は

\[
NEXP\subseteq P/poly\iff NEXP=MA
\]

を示す。P=NP なら PH=P であり、MA⊆PH から MA=P。もし同時に NEXP⊆P/poly なら NEXP=MA=P となり、時間階層定理に反する。従って上の含意を得る。[IKW 原論文 §4.1](https://www2.cs.sfu.ca/~kabanets/papers/exp_journal.pdf)、[Goldreich–Zuckerman：MA⊆PH](https://www.wisdom.weizmann.ac.il/~oded/R1/bpp-ph.pdf)

したがって NEXP⊄P/poly を証明しても、それを **P=NP の否定材料としてそのまま使うことはできない**。むしろ同じ回路下界は P=NP を仮定しても成立する。この論理整理は、P≠NP の真偽や形式的独立性を決めるものではない。

元ノート §19.5 の padding による EXP=NEXP 自体は正しい。削るべきなのは、単なる「両立可能性の未排除」に留めた説明である。§19.6–19.7 の「NPへ戻る既知移送なし」も、歴史的記述であることを明示し、§25 の MMW を現在の到達点とする。

## 2. 三つの『NP下界』を混ぜない

一般回路について次は異なる。

| 主張 | 量化 | P≠NP への位置づけ |
|---|---|---|
| 固定多項式サイズ下界が任意次数で成立 | ∀k ∃L_k∈NP：L_k∉SIZE(n^k) | この形だけでは十分でない |
| NP に超多項式回路下界を持つ一言語がある | ∃L∈NP ∀k：L∉SIZE(n^k) | NP⊄P/poly、従って P≠NP |
| SAT の一様多項式時間アルゴリズムがない | SAT∉P | P≠NP そのもの |

第一行から第二行への量化交換は禁止。P の各言語は多項式サイズ回路を持つが、**P 全体に共通する一つの次数**が必要なわけではない。同様に NP⊆P/poly は各言語ごとに異なる次数を許す。

Murray–Williams の原典 Theorem 1.1 は次の形である。典型的回路クラス C と ε∈(0,1) について、m 入力・2^{εm} サイズの GAP-C-UNSAT を nondeterministic O(2^{(1−ε)m}) 時間で解けるなら、ある c≥1 があり、全 k について

\[
NTIME[n^{ck^4/\epsilon}]\not\subseteq SIZE_C(n^k).
\]

これは上表第一行に相当する。『NPに下がった』ことを『NP⊄P/polyまで得た』と読まない。Theorem 1.2 はより弱い量的高速化から NQP の準多項式回路下界を与える。[Murray–Williams 原典 Theorems 1.1–1.2](https://people.csail.mit.edu/rrw/easy-witness-nqp.pdf)

## 3. Williams 系と MMW 系は異なる経路

Williams の代表的な無条件成果は NEXP⊄ACC。一般回路に対する NEXP⊄P/poly を証明したという意味ではなく、さらに NP⊄P/poly とも別である。[Non-Uniform ACC Circuit Lower Bounds](https://people.csail.mit.edu/rrw/acc-lbs-journal-final.pdf)

Vyas–Williams は、適切な閉包性を持つ C で、全 k について n^k サイズ回路の #SAT を 2^n/n^k 時間で解くと、疎な対称関数 f を上に置いた f∘C に対する NEXP 下界を得る。SAT と #SAT、回路サイズと変数数、必要な閉包性を固定して使う必要がある。[Vyas–Williams](https://arxiv.org/abs/2001.07788)

一方、MMW Theorem 1.3 は直接 P≠NP に到達する。固定した A∈PH と time-constructible s(n)≥n が存在し、search-MCSP^A[s(n)] に **poly(s) 空間と poly(s) update time を同時に満たす決定的一方向 streaming algorithm が存在しない**なら、P≠NP である。Theorem 1.2 は Σ₃SAT^A oracle を使う streaming 上界を与え、P=NP の下で oracle を除去する対偶が橋になる。[MMW Theorems 1.2–1.3](https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf)

この違いは現在のノートの判断を支持する。MMW を探し直す必要はなく、§25–30 が保存した search / witness / uniformity 条件を守って、未証明の構築・下界部分へ進むべきである。

### MMW 接続用の量化台帳（本監査による整理）

狙う不在命題は、概ね

\[
\exists A\in PH\ \exists s\ \forall d\ \forall M:\quad
M\text{ は全入力上正しく、space/update/report}\le O(s^d)
\text{ を同時には満たさない}.
\]

ここで M は全長を扱う固定された一様機械。入力は N=2^n ビットの明示真理値表。A は出力候補回路の oracle であり、oracle-free 更新器へ A を無料で与える意味ではない。s は変数数 n の関数である。

- 一つの次数 d の下界だけでは poly(s) 全体を排除しない。
- 一つの辞書順最小 selector だけでは全 search solver を排除しない。
- 最終出力は小回路、または存在しないことを示す sentinel。YES だけ正しい live-promise と total exact search を混同しない。
- 巨大な長さ別遷移表や前処理は一様性・初期化時間の外へ隠せない。
- **原典記述の修正。** Modanese §2 Definition 2 は update u と reporting r を別に定義し、直後に両者が poly(s) のモデルへ注力する。『原定義で reporting=O(u) が必須』とは書いていない。本ノートで u*=max(u,r) と統合して課金するのは正当な独自会計であり、poly(s) の結論は変わらない。MMW の構成自身も最終回路の出力を poly(s) 内で行う。[Modanese §2 Definition 2](https://arxiv.org/pdf/2007.12048)

## 4. 既存の反証を維持すべき箇所

以下は回収ノートを本監査が独立に手検算した結果であり、新規性主張ではない。

**疎性上界。** 固定長 N の言語 L の受理語数を M とすると、各切断の非空残余を持つ prefix は高々 M 個。従って残余同値類数 K≤M+1。MCSP の候補回路記述数は 2^{O(s log s)} 以下なので、log K=O(s log s)。§19.14 の MREC 反証は維持。

**Search でも幅は救済にならない。** 小回路出力を選ぶ任意の uniformizer に対し、異なる live prefix は、共通 suffix を付けた最終真理値表が異なる以上、同じ回路出力にはならない。よって関数残余数は『live prefix 数＋dead が存在すれば1』。それでも同じ 2^{O(s log s)} 上界内である。§25.4 の正確な式は正しい。

**Semantic oracle saturation。** §28.2 の補助 oracle が完全な PME 更新出力の各 bit を返すなら、小さい旧回路＋新 bit＋切断位置から次の小回路を得ることは当然可能。これは通常計算の上界ではなく、任意の意味 oracle に対しても成立すると称する下界法の反例である。通常の対称的 relativization と同一視しない、という注意は正しい。

従って現状で正当な標的は『状態が多すぎる』ではなく、**どの状態符号化・どの許される出力選択を使っても、通常の一様計算では所要資源で更新できない**こと。ただし、そう言い換えただけでは新しい下界証明にならない。

## 5. 障壁を適用する範囲

| 障壁 | 確定事項 | 本研究で禁止すべき読み |
|---|---|---|
| Relativization | P^A=NP^A の oracle と P^B≠NP^B の oracle がともに存在 | 対角線論法を全て禁止する、または非相対化なら成功する |
| Natural proofs | 適切に強い擬似乱数仮定の下で、constructivity・largeness・usefulness を持つ一般回路下界法を制限 | 無条件不可能性、あるいは単に one-way function があるだけの無指定仮定に省略する |
| Algebrization | algebraic extension oracle を許す議論でも P vs NP などは解決できない | 『代数を使う証明は全て無効』と読む |

[Baker–Gill–Solovay 原論文](https://epubs.siam.org/doi/10.1137/0204037)、[Razborov–Rudich 原論文](https://mit6875.github.io/PAPERS/natural_proofs.pdf)、[Aaronson–Wigderson 原論文](https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/SCOTT/alg.pdf)

Natural proofs の constructivity は通常、n 変数関数の **2^n ビット真理値表長に多項式**という尺度。『n に指数時間だから自然証明ではない』も誤りである。三障壁を回避したとの宣言だけでは、未証明 compiler や量化交換を補えない。

CHOPRS の locality barrier は、指定された oracle circuit の arity・個数・経路上の依存を追跡する定理。オンライン search transducer へ移すにはモデル変換と資源会計が要る。§28.3 の『Pich/CHOPRSを WC に直接適用しない』判断は維持する。[Beyond Natural Proofs: Hardness Magnification and Locality](https://arxiv.org/abs/1911.08297)

### 追加すべき文献更新

1. **Vyas–Williams、訂正版 2024。** *On Oracles and Algorithmic Methods for Proving Lower Bounds* は、ITCS 2023 会議版 Theorem 1.10 が誤りで、その否定が成立するとの erratum を公開している。『SAT 高速化から下界への経路は一律に非相対化』といった一般化は使わず、訂正版の定理単位で判定する。[著者訂正版・明示 erratum](https://eccc.weizmann.ac.il/report/2024/113/)
2. **Chen–Hu–Ren、ITCS 2026。** *New Algebrization Barriers to Circuit Lower Bounds via Communication Complexity of Missing-String* は、XOR-Missing-String の通信複雑性を通じ、複数の上位クラスの回路下界に新しい algebrization 障壁を示す。オンライン WC 全般を遮断する定理ではない。range-avoidance 系の案を採る際の追加照合先である。[2025 11 18 投稿、ITCS 2026](https://arxiv.org/abs/2511.14038)
3. **Ren–Williams、2026 07。** 回収ノートの参照 arXiv:2607.09963 の現在の題名は *Near-Maximum Circuit Lower Bounds for Exponential Time with Merlin-Arthur Queries*。E^{prMA}/1 に Ω(2^n/n) 下界を与える。promise oracle・1 bit advice・上位時間クラスを外して NP の下界として使えない。[一次資料](https://arxiv.org/abs/2607.09963)

## 6. PAP 接続の独立確認

Arteche–Atserias–de Rezende–Khaniki Theorem 1.1 は、n 変数・poly(n) 節の φ、r≥n³、および **明示 Resolution refutation π of Ref_r(φ)** から、φ が充足可能なら割当てを poly(n,r,|π|) 時間で抽出する。Corollary 5.6 は EF を p-simulate する任意の Q と任意の多項式 r に対して PAP_Q[r] の NP 完全性を示す。[The Proof Analysis Problem](https://arxiv.org/pdf/2506.16956)

Fleming–Grosser–Pitassi–Robere Theorem 1.1 の implicit Resolution ≃ [EF,Resolution] ≃ G₁ と、G₁ が EF を含むことも原典で確認した。[著者版 Theorem 1.1](https://www.cs.mcgill.ca/~robere/files/Implicit_Proofs.pdf)

そのため §30.2 の C31 は正しい条件付き停止判定である。ただし用語は『generic implicit-PAP extractor が **反証された**』より、**その全域多項式時間 extractor は P=NP を含意するため、容易な中間補題としては使えない**が正確。P≠NP 未証明の段階で、その extractor の無条件不存在を得たことにはならない。

PAP の poly(|π|) を、回路で圧縮された π の記述長に多項式と読み替えることは禁止。生き残る方向は、明示 poly-size Resolution proof への compiler、または認識可能な限定 compiler 像に限った解析。いずれも現在は未証明。TR26-128 の個別 width 指数監査は本担当では独立再証明していない。

## 7. 次に一つ進めるなら

MMW や PAP そのものの再命名ではなく、次の **compiler 仕様一枚**を先に固定する。

\[
(\varphi,C)\longmapsto\pi_C
\quad\text{with}\quad
\pi_C:\operatorname{Res}\vdash\neg\operatorname{Ref}_{r(\varphi)}(\varphi).
\]

明記する条件は、φ だけから作れる prefix generator、YES 時の小回路 completion 存在、**全ての**閾値内 completion C、poly(|φ|) の prefix 長・回路閾値・r・明示 proof 長、uniform compiler の時間である。まず限定された completion class で成立を証明し、その制約を外す追加定理を別の未証明項目にする。

**ただし compiler ができても直ちに P≠NP ではない。** この NP-witness binding が、効率的 WC の存在 W から SAT∈P、すなわち H=(P=NP) を導くなら、得られるのは W⇒H。MMW の H⇒W と合成しても W⇔H という特徴づけであり、矛盾ではない。無条件の ¬W または他の既知下界・階層定理に反する定量的アルゴリズムまで示す別の論証が必要。ここを省略すると、既知の条件付き下界を言い換えているだけになる。

この仕様が揃う前の『回路に情報があるから witness が読める』『強い下界なので NP に下りる』『implicit proof を局所的に読めばよい』は再利用しない。現時点で P vs NP の解決、新規性確認済みの下界定理、通常計算に対する WC 下界を得たとの主張はない。
