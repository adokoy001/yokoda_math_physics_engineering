# P vs NP：有限検査の再現用ファイル

資料基準日：2026 09 05
公開解説HTMLのC35・C36・C37と、小回路の正確な列挙を検査するコードです。
標準Pythonのみを使います。外部通信は行いません。

## 実行

このZIPを一つのフォルダへ展開し、そのフォルダで実行してください。

python verify_nextbit_patch.py --max-n 4 --output nextbit_patch_verification.json
python verify_ordered_patch.py --output ordered_patch_experiment.json
python tiny_wc_synthesis.py --n 2 --size 4 --out tiny_wc_synthesis_n2.json
python tiny_wc_synthesis.py --n 3 --size 5 --out tiny_wc_synthesis_n3.json
python tiny_wc_synthesis.py --n 4 --size 4 --out tiny_wc_synthesis_n4.json
python verify_tiny_wc_synthesis.py

検査結果は同名のJSONに上書きされます。元の実行結果を残すなら別フォルダへ展開してください。
tiny_wc_synthesis.pyの既定時間予算は50秒です。必要なら --budget 300 などを指定できます。
complete_through_sizeを確認し、時間切れの未完了層を完全列挙と数えないでください。
verify_tiny_wc_synthesis.pyは同じフォルダのn2,n3,n4のJSONを読みます。

## 回路モデルと順序

AND/ORは入力2本、NOTは入力1本。各演算は1ゲート。
列挙では入力・定数0/1・fanoutは無料、既存の任意のwireを出力にできます。
真理値表を整数で符号化する際は、ビットjがf(j)です。
本文の真理値文字列は左からf(0),f(1),...の順であり、整数の通常の二進表示の読み順とは異なります。

## 証明との関係

有限検査は一般的な記号的証明の補助です。
P≠NP、超多項式の一般回路下界、全入力長での最適性、新規性を証明するものではありません。
n2はサイズ4までで全16関数、n3はサイズ5までで203関数、n4はサイズ4までで886関数。
n3,n4の全Boolean関数を覆ったという意味ではありません。
検査時刻・所要時間は再実行によって変わります。
