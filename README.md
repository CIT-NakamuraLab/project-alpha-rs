# Project-Alpha-RS（仮）
入退出鍵管理アプリ（リーダーサーバ）

#### controller.serial_read()について
- 関数が実行されると、Arduinoに対してデータ要求を行い返答データを処理します。
- 返答データの処理は1回0.1秒を最大5回繰り返します。

(応答データ処理の待機時間はそこそこブレます)

戻り値  
(読み取り成功(bool), [BIT0(int), BIT1, ... BIT7])  
BIT0→ 鍵状態（存在するときTrue  
BIT1,2,3→ ボタン1,2,3（押されると 1  