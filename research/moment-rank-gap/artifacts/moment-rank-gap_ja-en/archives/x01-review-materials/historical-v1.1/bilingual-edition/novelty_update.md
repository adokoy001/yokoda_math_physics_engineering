# HTML版用：追加の限定的新規性照合

照合日：2026 09 08。検索6件に絞った追加確認。過去の照合記録と今回読めた一次本文を対応させたもので、網羅的な文献調査でも優先権の認定でもない。

## 日本語：HTMLに載せる短い結論

追加調査でも、普遍順位不等式と誤差帯の三段の鋭い公式について、同一の記述がある一次文献は同定できなかった。ただし、これは新規性を示す証拠ではない。整数総和の順位保証は既知不等式の系、成分数の分類は既知の凸幾何の一般定理の具体化として扱う。今回の独立導出・証明・形式検証と、学術的新規性の判定は区別する。

| 対象 | 文献との関係 | 現在の扱い |
|---|---|---|
| 普遍順位式 \(2D+e^2+g^2\ge1\)、等号配置、余裕の分解 | 箱制約なしの決定論的順位境界は既存分野。読んだ一次文献ではこの式との一致を未同定 | 独立導出した命題。新規性未確定 |
| 総和誤差帯の三段の鋭い最小順位差 | 普遍順位式と、既知の箱内二乗和最大から導出。同じ三段式の一次文献を未同定 | 明示的な系・最適化結果。新規性未確定 |
| 整数総和の丸め上限と順位差 | Rastegin (2023), Theorem 1, (30)–(31) の高純度枝と集約による系 | 独立した新規不等式とは主張しない |
| 二線分の欠損非増加経路 | Gorban (2013), Lemma 4 の頂点への線分接続と関連。今回の貪欲な頂点選択・二値代表への明示経路は本文で直接証明 | 具体的な構成。新しい一般原理とは主張しない |
| 非整数総和の二段階合流、誤差帯の成分数 | Gorban (2013), Proposition 7、Lemma 14 による辺グラフへの還元の具体化 | 既知一般理論の明示的な系 |
| 切頂四面体の穴の遷移 | 本文の面複体による計算。今回の6検索では高次位相の文献を別途網羅していない | 証明・検算と新規性を分離。照合未完 |

## English: concise text for the HTML page

The additional limited search did not identify a primary source stating the universal rank-gap inequality or the exact three-branch formula for a sum-error band. Failure to find a match does not establish novelty. The integer-sum bound is treated as a corollary of a known inequality, and the component counts as explicit applications of known convex-geometric results. Independent derivation, mathematical proof, formal verification, and scholarly novelty are separate claims.

| Result | Relation to prior work | Current status |
|---|---|---|
| Universal inequality \(2D+e^2+g^2\ge1\), equality pattern, and slack decomposition | Deterministic order-statistic bounds are established literature. No identical formula was identified in the primary sources inspected | Independently derived; novelty unconfirmed |
| Exact three-branch minimum gap under a sum-error band | Follows from the universal inequality and the known box-constrained maximum of the sum of squares. No identical three-branch statement was identified | Explicit corollary and optimization result; novelty unconfirmed |
| Integer-sum rounding and gap bounds | Corollaries of the high-purity branch in Rastegin (2023), Theorem 1, equations (30)–(31), with an aggregation argument | No claim of an independently new inequality |
| A defect-nonincreasing path with at most two segments | Related to the vertex-access lemma in Gorban (2013), Lemma 4. The greedy vertex and binary endpoint are constructed directly here | Explicit construction; no claim of a new general principle |
| Two-stage merging for noninteger sums; component counts for the error band | Applications of Gorban (2013), Proposition 7 and Lemma 14 | Explicit corollaries of known general theory |
| Changes in holes for the truncated-tetrahedron example | Derived through a face complex. Higher-topology literature was not separately surveyed in this six-query update | Proof and computation recorded; novelty audit incomplete |

## 一次資料・今回読んだ箇所

1. **Alexey E. Rastegin, _Uncertainty relations in terms of generalized entropies derived from information diagrams_ (2023).**
   URL: https://arxiv.org/html/2305.18005v1
   今回再確認：Theorem 1、式 (30)–(31)。\(I>1/2\) の枝は \(\max p_i\ge(1+\sqrt{2I-1})/2\)。これが一般の非整数総和の順位式を原論文中で証明している、とは述べない。
   Read: Theorem 1 and equations (30)–(31). The high-purity maximum-probability bound supports the integer-sum corollary, not a claim that the general noninteger formula appears in that paper.

2. **Alexander N. Gorban, _Thermodynamic Tree: The Space of Admissible Paths_ (2013).**
   URL: https://arxiv.org/html/1201.6315v3
   今回再確認：Lemma 4 とその証明、Proposition 7、Lemma 14 とその放射射影の証明、§3.3 の辺・頂点の水準による合流手順。Lemma 4 は凸多面体の外部凸集合を避けてある頂点に線分で到達できることをいう。Lemma 14 は最小値より高い水準に適用するため、最小値に達する一様配置は別に処理する。
   Read: Lemma 4 and proof; Proposition 7; Lemma 14 and its projection proof; the vertex/edge filtration in §3.3. The minimum level is handled separately because Lemma 14 assumes a level strictly above the minimum.

3. **Agnieszka Goroncy and Tomasz Rychlik, _How deviant can you be? The complete solution_ (2006), Mathematical Inequalities & Applications 9, 633–647.**
   URL: https://files.ele-math.com/articles/mia-09-57.pdf
   今回再確認：導入、pp.636–637 の順位差の下界に関する記述、§2 の設定と Theorem 1。外部の共通箱 [0,1] を課さない、実数標本の中心化された線形順位統計量を扱う。その前提差を保ったまま近接文献として引用する。
   Read: Introduction, the spacing discussion on pp.636–637, the setup of §2 and Theorem 1. It treats real samples without our externally prescribed common box [0,1].

4. **Emanuel H. Rubensson and Anders M. N. Niklasson, _Accelerated density matrix expansions for Born–Oppenheimer molecular dynamics_ (2013 preprint).**
   URL: https://arxiv.org/html/1302.7292v1
   今回再確認：§5.1、式 (7)–(14)。Frobeniusノルムと trace による近射影性から固有値の除外区間を推定する。式 (14) は \(\|X-X^2\|_F<1/4\) の下での中央の除外区間であり、今回の \((D,e,s)\) による順位を指定した鋭式との同一性は確認していない。
   Read: §5.1, equations (7)–(14). These use Frobenius norms and traces of the idempotency defect; they do not provide an identified match to the present rank-specific formula.

5. **_Parameterless stopping criteria for recursive density matrix expansions_ (arXiv:1507.02087v3).**
   URL: https://arxiv.org/html/1507.02087v3
   今回の追加近接資料：導入、Theorem 1、§6 のHOMO/LUMO境界への言及を確認。主題は再帰的射影展開の停止判定と近射影誤差の収束比であり、今回の順位式の同一定理としては扱わない。全定理の逐語的な照合はしていない。
   Newly inspected: introduction, Theorem 1, and the discussion of HOMO/LUMO bounds in §6. This concerns stopping criteria and idempotency-error convergence; a complete theorem-by-theorem audit was not performed.

## 未完部分と検索範囲

今回の6検索系列：`eigenvalue gap trace idempotency inequality`、`order statistics bounded sum of squares gap inequality`、`hypersimplex connected components sphere`、`rank gap sum squares inequality`、`deterministic lower bounds spacings bounded sample mean variance order statistics`、`idempotency error trace HOMO LUMO eigenvalue bounds Rubensson Niklasson`。

検索結果の書誌・断片だけを同一定理の根拠にはしなかった。Fahmy–Proschan (1981)、SPREAD制約の2014年後続論文など、前回全文未読とした資料を今回読了したことにはしない。式の別表記、書籍、非英語文献、索引化されていない文献を含む網羅性はない。最終HTMLでは「新定理を発見した」とせず、「箱制約下の鋭い順位保証を独立導出し、核となる有限列不等式を形式検証した。新規性は未確定」とする。
