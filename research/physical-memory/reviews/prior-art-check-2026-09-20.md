# 「見えない内部は、どこまで減らせる？」既知性の照合メモ

対象：数学探索・第六弾（2026-09-20）／works/physical-memory-reduction
照合日：2026-09-20
照合方法：Web検索（Wiley・IEEE Xplore・Semantic Scholar・ScienceDirect・arXiv・Springer の要旨・書誌）。本文が入手できたものはなく、**すべて要旨・書誌レベルの確認**。「見つからなかった」は「存在しない」を意味しない。

## 結論の要約

| 成果 | 判定 | 根拠 |
|---|---|---|
| 実現定理：最少内部熱容量数 = cp-rank(H) | **既知の可能性が高い** | 同じ問題（共通接地RC多端子網の実現・最少容量数）を1965–73年の論文が正面から扱っている。ただし cp-rank の言語で述べた文献は未発見 |
| 三集約値の鋭い不等式 m ≤ min{√[z(2d−z)], (d+z)/2} | **現時点で既知とは言えない** | 明示式に一致する文献なし。未照合の関連文献あり |
| 二窓測定プロトコルと誤差下限 1/6 | **新規性が残る可能性が最も高い** | 温度入力→熱流出力で cp-rank を有限時間データから認証する構成に対応する文献なし |

## 論点1：実現定理（cp-rank と最少容量数）

### 新たに見つかった要照合文献（文献表61件に未収録）

**[A] D. Basson & C. C. Halkias, "The Realization of RC N-Ports," IEEE Trans. Circuit Theory 12 (1965) 247–256.**
- 要旨の内容：有理関数を要素とする n×n 行列 Z(s) を開放インピーダンス行列として持つ**共通接地**RC回路網が存在するための、一般的な必要十分条件を与える。さらに Z(s) の要素の極が n+1 個以下という制限の下で実用的な判定・合成手順を示し、**等価な実現の完全なクラス**も提示する。
- 今回との関係：「共通接地」「必要十分条件」「等価実現のクラス」の三点が今回の設定と重なる。インピーダンス表現だがアドミタンスへの読み替えは容易。**最優先で本文入手**。残差行列が「非負ダイアドの和」で書ける旨の条件が本文にあれば、実現定理は実質的に既知となる。
- 入手先候補：IEEE Xplore document 1082411。

**[B] R. A. Stein & A. D. Moore, "On the synthesis of RC multiport networks by linear transformations," IEEE Trans. Circuit Theory CT-18 (1971) 294–297.**
- Stein (1973) の参考文献8。線形変換（合同変換）による多端子RC合成。松本(1981)・Ali(1976)と同じ系統で、Howitt変換と非負因子の対応（ページ§追究4-E）に直接関わる可能性。要旨未取得。

**[C] R. A. Stein, "Synthesis of grounded-capacitor multiport RC networks," Digest, IEEE Int. Symp. Electrical Network Theory, London (1971) 49–50.**
- Stein (1973) の参考文献9。1973年論文の原型。

### 既収録文献について今回確認できたこと

**Stein (1973) [46]** の要旨：全コンデンサが片端接地、任意ノード対間に抵抗を持つ多端子RC回路網の計算機支援合成法。短絡アドミタンス関数の実現に**反復最小化**を用い、総容量の最小値と**最少コンデンサ個数**の両方を達成する構造を与える。
- 読み：「反復最小化」から、閉形式の判定条件ではなく数値的合成法と推定。「最少」が手法の出力に対する主張か、構造クラス全体での最小性の証明かは本文で要確認。
- 定理的な最小性の証明が含まれていれば今回の必要性の証明と重なる。含まれていなければ「最小性の閉形式特徴づけ（cp-rank）」は今回の寄与として残る。

### cp-rank と回路合成の「橋」

- 「completely positive」「cp-rank」と RC/熱回路合成・Kron縮約・接地容量を組み合わせた検索では、該当文献が**一件も出なかった**。
- Berman & Shaked-Monderer (2003) [60] の目次にも回路応用の章はない。
- 正値実現理論（Benvenuti–Farina 2004 [35]、Grussler ら [36]）では「正値性で次数が上がる」一般論は既知だが、対称・単一極・相反という今回の制約で次数が cp-rank に一致するという明示的記述は見つからなかった。
- 解釈：回路合成側（1960–70年代）と完全正値行列側（1990年代以降）が同じ対象を別の言葉で扱い、橋がかかっていない可能性が高い。橋をかけること自体は寄与だが、[A][B] の本文次第で「言語の翻訳」に縮む。

## 論点2：三集約値の鋭い不等式

- 明示式 m ≤ min{√[z(2d−z)], (d+z)/2} に一致する文献は見つからなかった。
- H₀ の cp-rank が 4 である理由は、三角形なしグラフの古典結果（4-サイクルでは cp-rank が辺数 4 に一致）で説明でき、ページの「既知」判定と整合。

### 追加の照合候補

**[D] "Sufficient conditions for a doubly non-negative matrix to be completely positive," Computational and Applied Mathematics (Springer, 2026年9月掲載).**
- 要旨の内容：対称二重非負行列 M が完全正値であるための十分条件を、M に付随する**多面体錐の最大角度**で定式化。条件を満たす M に対し cp 分解を構成し、cp-rank が rank に一致することを観察。
- 今回との関係：方向は逆（cp-rank = rank を保証する側）だが、錐の角度による判定という発想が同系統。今回の不等式が「cp-rank > rank」側の角度条件として同値な形で含まれていないか要確認。
- 入手先：DOI 10.1007/s40314-026-03906-y。

**未照合のまま残るもの**：Berman & Shaked-Monderer (2003) の小行列（n ≤ 4）の章、Shaked-Monderer & Berman (2021) *Copositive and Completely Positive Matrices* の cp-rank の章。4×4 で cp-rank 3/4 を分ける明示的な不等式がここに載っている可能性は残る。

## 論点3：二窓測定プロトコルと誤差下限

- 温度入力→熱流出力の二窓積分で cp-rank を認証する構成に直接対応する文献は見つからなかった。
- 熱回路同定の文献（Fukunaga–Funaki 2020 [50] など）は熱入力→温度出力が主流で、この差はページも明記済み。
- 参考として、De Tommasi, Magnani, D'Alessandro, de Magistris, "Time domain identification of passive multiport RC networks with convex optimization," IEEE SPI Workshop (2014) の題名を確認。受動多端子RCの時間域同定を凸最適化で扱うもので、状態数の認証ではなく同定が主題と推定。要旨未取得のため関連度は未確定。

## 検索の限界

- 本文を読めた文献はゼロ。IEEE Xplore は要旨も JavaScript 描画で取得できず、Semantic Scholar の書誌経由で確認した。
- 1960–70年代の回路合成論文は要旨が短く、定理の内容（特に「最小性」の意味）が要旨から判別できない。
- 「見つからなかった」の信頼度は、cp-rank 側（arXiv・Springer で検索可能）が高く、回路合成側（紙媒体・要旨のみ）が低い。

## 次のアクション（優先順）

1. Basson & Halkias (1965) の本文入手。残差行列の条件が非負ダイアド分解に相当するかを確認。
2. Stein (1973) の本文入手。「最少コンデンサ個数」が証明付きの最小性かを確認。
3. Stein & Moore (1971) の要旨・本文入手。Howitt変換との対応を確認。
4. Berman & Shaked-Monderer (2003) 小行列の章、および CAM 2026 論文 [D] で、4×4 の cp-rank 3/4 判定式を照合。
5. 上記の結果にかかわらず、二窓測定プロトコルと誤差下限は独立に論文化可能な部分として切り出しておく。

## 文献表への追加提案

| 番号 | 年 | 文献 | 確認範囲 |
|---|---|---|---|
| [62] | 1965 | Basson & Halkias — The Realization of RC N-Ports, IEEE Trans. CT 12:247–256 | 要旨・書誌のみ |
| [63] | 1971 | Stein & Moore — On the synthesis of RC multiport networks by linear transformations, IEEE Trans. CT-18:294–297 | 書誌のみ（Stein 1973 の参考文献） |
| [64] | 2026 | Sufficient conditions for a doubly non-negative matrix to be completely positive, Comput. Appl. Math., DOI 10.1007/s40314-026-03906-y | 要旨のみ |
