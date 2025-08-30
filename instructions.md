
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


## Rの設定

以下のような文字列を追加する。<XXX>は、インストールしているRのバージョン。

C:\Program Files\R\R-<XXX>\bin

[R-location](./img/R-location.png)


# ターミナルのcmd.exeを実行 

[スタートメニュー]をクリックして、上部の検索バーに"ターミナル"を入力。
ターミナルを起動。
タブ横の展開ボタンをクリックして"コマンドプロンプト"を選択。
以下のように、入力プロンプトが表示される。XXXはログイン名

[terminal-1](./img/terminal-1.png)

```
C:\Users\XXXX>

```

# cmd.exeでpythonとRが実行できるか確認

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

## Rが実行できるかの確認

```
C:\Users\XXX> R --version

```

以下のような文字列が出力される。

```
R version 4.5.1 (2025-06-13 ucrt) -- "Great Square Root"
Copyright (C) 2025 The R Foundation for Statistical Computing
Platform: x86_64-w64-mingw32/x64

R is free software and comes with ABSOLUTELY NO WARRANTY.
You are welcome to redistribute it under the terms of the
GNU General Public License versions 2 or 3.
For more information about these matters see
https://www.gnu.org/licenses/.

```

# pythonによるhttpサーバの実行

プログラムを作成して運用まで実施することをProjectと呼ぶことが多い。
作業用のフォルダ(Projects)を作成してそのフォルダ内で、eg-http-python-Rフォルダを作成して、そこにプログラムファイル、参考資料をおいて、プログラムを完成させる。

以下のようなフォルダ構成にして、作業を進める。

C:\Users\XXX\Projects\eg-http-python-R


cmd.exeを実行して
eg-http-python-Rを作業ディレクトリにする。

```
C:\Users\XXX> cd Projects

C:\Users\XXX\Projects> cd eg-http-python-R

C:\Users\XXX\Projects\eg-http-python-R>

```


# httpサーバの起動
cmd.exeで以下のコマンドを実行

```
C:\Users\XXX\Projects\eg-http-python-R> svr.bat
Serving HTTP on port 8000 

```
上記のような出力がでて、"C:\Users\XXX\Projects\eg-http-python-R>"が最後に出力されない状態になる。
これは、入力プロンプトが表示されていない状態。
つまり、コマンド入力を受け付けない状態。

httpサーバが起動している状態になっているため。


# httpサーバの終了
入力コマンドを受け付ける状態にするには、httpサーバを終了する必要がある。
httpサーバを終了するには、カーソルが点滅している状態で、[Ctrl]キーと[C]キーを同時に押す。
```
C:\Users\XXX\Projects\eg-http-python-R> svr.bat 
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


# commentの表示


ブラウザのアドレスバーに以下を入力
http://localhost:8000/comment


コメントを書き込むページが表示される。
新しいコメント欄に文字を入力して、送信すると、コメントが記録される。
再度コメントのページを開くと、以前のコメントが表示される。

この処理は以下の個所で実施される。

最初にページを開いた時

mfhttsrv/request/handler.pyの193行目

送信ボタンを押下した時
mfhttsrv/request/handler.pyの211行目


# sumの表示

ブラウザのアドレスバーに以下を入力
http://localhost:8000/sum


数値の総和を計算するページが表示される。
数値データに数字を入力して、送信すると、総和が計算される。
総和計算はR言語によって実行される。

この処理は以下の個所で実施される。

最初にページを開いた時

mfhttsrv/request/handler.pyの202行目

送信ボタンを押下した時
mfhttsrv/request/handler.pyの244行目

PythonからR言語処理呼び出し
mfhttsrv/request/handler.pyの310行目

R言語の総和計算
sum.R


# R言語単体の総和計算

cmd.exeで以下のコマンドを実行

```
C:\Users\XXX\Projects\eg-http-python-R> Rscript sum.R

```
上記の状態で入力待ちになる

図示のように 1 3 4を入力しする
```
C:\Users\XXX\Projects\eg-http-python-R> Rscript sum.R
1 3 4

```
入力後、[Ctrl] + [Z]を押下のち[Enter]キーを押下で1 3 4の総和が出力される。

```
C:\Users\XXX\Projects\eg-http-python-R> Rscript sum.R
1 3 4
^Z
Read 3 items
Read 1 item
Read 1 item
Read 1 item
8
```


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

