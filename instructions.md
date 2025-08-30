
# インストールするソフト
以下のソフトをインストールする。

- Visual Studio code
- python3 (最新版)

# Visual Studio code
プログラムを書くためのソフト。総称エディタ。文字だけのファイルを編集するためのツール。

[リンク](https://code.visualstudio.com/)から"Download for Windows"をクリックしてインストーラをダウンロード。VSCodeUserSetup-x64.exeをダブルクリックしてインストール

いろんな種類があって、プログラムができるようになってくると、好みで変えることが多い。
Visual Studio codeは、日本の中堅のエンジニアに利用者が多いと思う。


# python3のインストール

[python3のダウンロードページ](https://www.python.org/downloads/)から"Download Python 3.13.x"をクリックしてインストーラをダウンロード。
通常ユーザーでインストール
環境変数のPATHの追加はしない(後で自分で設定する)


# 環境変数の編集

[スタートメニュー]->[設定]を開く。上部の検索バーに"環境変数"と入れて検索。
ユーザー変数用の環境変数のペインで、Pathを選択して、編集する。



## pythonの設定

以下のような文字列をAppData\Local\Microsoft\WindowsAppsより前に追加する。<XXX>は、自分のサインインの名前になる。

C:\Users\<XXX>\AppData\Local\Programs\Python\Python313

[environment-settings-1](./img/environment-settings-1.png)


# ターミナルのcmd.exeを実行 

[スタートメニュー]をクリックして、上部の検索バーに"ターミナル"を入力。
ターミナルを起動。
タブ横の展開ボタンをクリックして"コマンドプロンプト"を選択。
以下のように、入力プロンプトが表示される。XXXはログイン名

[terminal-1](./img/terminal-1.png)

```
C:\Users\XXXX>

```

# cmd.exeでpythonが実行できるか確認

以下のコマンドを実行

## pythonが実行できるかの確認

```
C:\Users\XXX> python --version
              ^^^^^^^^^^^^^^^^
              ここだけ入力
```

以下のような文字列が出力される。
```
Python 3.13.5
```

# pythonによるhttpサーバの実行

プログラムを作成して運用まで実施することをProjectと呼ぶことが多い。
作業用のフォルダ(Projects)を作成してそのフォルダ内で、eg-http-pythonフォルダを作成して、そこにプログラムファイル、参考資料をおいて、プログラムを完成させる。

以下のようなフォルダ構成にして、作業を進める。

C:\Users\XXX\Projects\eg-http-python


cmd.exeを実行して
eg-http-pythonを作業ディレクトリにする。

```
C:\Users\XXX> cd Projects

C:\Users\XXX\Projects> cd eg-http-python

C:\Users\XXX\Projects\eg-http-python>

```


# httpサーバの起動
cmd.exeで以下のコマンドを実行

```
C:\Users\XXX\Projects\eg-http-python> svr.bat
Serving HTTP on port 8000 

```
上記のような出力がでて、"C:\Users\XXX\Projects\eg-http-python>"が最後に出力されない状態になる。
これは、入力プロンプトが表示されていない状態。
つまり、コマンド入力を受け付けない状態。

httpサーバが起動している状態になっているため。


# httpサーバの終了
入力コマンドを受け付ける状態にするには、httpサーバを終了する必要がある。
httpサーバを終了するには、カーソルが点滅している状態で、[Ctrl]キーと[C]キーを同時に押す。
```
C:\Users\XXX\Projects\eg-http-python> svr.bat 
Serving HTTP on port 8000 
|
^
これが点滅している状態
```

httpサーバが終了すると、以下の文字列が表示される

```
Keyboard interrupt received, exiting.
service is closed
バッチジョブを終了しますか (Y/N)?
```

Yを入力してリターンすると終了する

```
Keyboard interrupt received, exiting.
service is closed
バッチジョブを終了しますか (Y/N)? Y
```


# index.htmlの表示

cmd.exeでhttpサーバを起動する。

ブラウザを起動してアドレスバーに以下を入力

http://localhost:8000

docrootフォルダ内のindex.htmlの内容が確認できる。

この処理は、mfhttsrv/request/handler.pyの28行目で実施される。
pythonライブラリのSimpleHTTPRequestHandlerに詳細がある。

Handlerクラスは、SimpleHTTPRequestHandlerを継承している。



# custom-msgの表示

この処理は、mfhttsrv/request/handler.pyの55行目で実施される。
現在の日時を最初に取得して、その日時を含むhtmlの文字列作成する。
作成した文字列をwriteで書き出している。writeで書き出している。
__main__.pyで作成したhttpのサーバがwriteで書き出されたデータをブラウザに返却する。


# todoの表示


ブラウザのアドレスバーに以下を入力
http://localhost:8000/todo


todoを追加できるページが表示される。
新規アイテムに文字を入力して、送信すると、TODOリストが記録される。

この処理は以下の個所で実施される。

最初にページを開いた時

mfhttsrv/request/handler.pyの192行目

送信ボタンを押下した時
mfhttsrv/request/handler.pyの196行目

実際のページ生成処理
mfhttsrv/request/handler.pyの106行目

todoリストのデータは、todo.txtというファイルで管理されている。
読み込み処理
mfhttsrv/request/handler.pyの172行目
追加処理:
mfhttsrv/request/handler.pyの140行目


# httpサーバでpythonプログラムをデバッグ

Visual Studio CodeにPython拡張をインストール

[install-python-ext](./img/python-ext-for-vs-code.png)


## ブレイクポイントを挿入してステップ実行する

httpサーバの起動の個所のとおりhttpサーバを実行する

Visual Studio Codeで、httpサーバを実行しているフォルダを開く

処理を確認したいファイルを開き、ブレイクポイントを設定する

[break-handler-1](./img/break-handler-1.png)


デバッグボタンをクリックして、デバッグ対象のプロセスにアタッチする。

[select-python-debugger](./img/select-python-debugger.png)

[select-python-process-id](./img/select-python-process-id.png)

[select-python-process-id-2](./img/select-python-process-id-2.png)


ブラウザで http://localhost:8000/comment を開く

[open comment](./img/open-comment-page-1.png)

Visual Studio Codeの画面を表示すると、以下のように、処理が停まっていることが確認できる。

[break-1](./img/break-1.png)

ボタン上部のアイコン列が、処理制御を行うボタンになっている。

左から
停止を解除して実行(コンティニュー)
関数を実行して次の行に移って停止(ステップオーバー)
関数の中に入って停止(ステップイン)
関数を内の処理を全て実行して停止(ステップアウト)
プログラムを最初から実行(リスタート) アタッチの場合はできない
デバッグを解除して、通常実行に戻る(切断)

図示は、ブレイクの後にステップインした状態

[break-2](./img/break-2.png)

