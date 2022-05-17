# CoeFont_to_FVTT_LOCAL_API
CoeFont[^1] APIとFVTT modの[Bouyomichan Connector]()を接続するためのローカルAPIサーバーです
<br>
<br>
<br>
# インストールの仕方と使い方
1. 右側リリース内の最新のリリースから、`hontai.zip`ファイルをダウンロードして解凍してください
 <br>
 <br>

2. `CoeFont_to_FVTT.exe`というアプリケーションを実行してください
<br>
<br>

3. 実行すると下のようなコマンドラインとアプリケーションウィンドウが表示されます

![コマンドラインとアプリケーションウィンドウ](https://user-images.githubusercontent.com/52102146/168811129-c19fcfd9-ba7a-45d9-b79b-c23a6567ac14.png)

<br>
<br>

4. CoeFont APIのアクセスキーを➊に入力します
<br>
<br>

5. CoeFont APIのクライアントシークレットを➋に入力します
<br>
<br>

6. 取得したwavファイルをPC上に自動保存する場合には「wavファイルをダウンロードする」にチェックをつけて、フォルダを指定してください

![wavファイルをダウンロードする](https://user-images.githubusercontent.com/52102146/168811226-ae73ae41-5660-48bd-96d8-6c2c1ddeceef.png)

<br>
<br>

7. 「サーバーを立ち上げる」ボタンを押すとアプリケーションウィンドウが閉じてコマンドラインが下のようになります
<br>
<br>

8. ここの赤線のURLをコピー（あるいは覚えて）ください（最後の「：2000」も含めて）

![赤線のURLをコピー](https://user-images.githubusercontent.com/52102146/168811280-86ebf1c1-be20-436b-b069-7ec1895b9f5d.png)

<br>
<br>

9. このURLをBouyomichan ConnectorのMODを有効化したワールドの「コンフィグ設定」⇒「Bouyomichan Connector」⇒「CoeFont APIと接続する独自APIのURL」に張り付けてください

![CoeFont APIと接続する独自APIのURL](https://user-images.githubusercontent.com/52102146/168811830-303664ce-5fb3-4125-af7f-e26c03790385.png)

<br>
<br>

10. 「変更内容を保存」してください（「CoeFont APIと接続する独自APIのURL」が表示されていない場合は、「CoeFontとの連携機能を使用する」にチェックを入れて一度「変更内容を保存」してから再度「コンフィグ設定」を開いてみてください）
<br>
<br>
<br>

# EXE化
実行形式ファイルが心配な人は、Python 3.10.4(32bit)にてPyInstaller(5.0.1)で`pyinstaller CoeFont_to_FVTT.spec`を実行してください（CoeFont_to_FVTT.pyファイル内でimportしているパッケージをインストールください）

