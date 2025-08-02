
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


## Rの設定

以下のような文字列を追加する。<XXX>は、インストールしているRのバージョン。

C:\Program Files\R\R-<XXX>\bin


# ターミナルのcmd.exeを実行 

[スタートメニュー]をクリックして、上部の検索バーに"ターミナル"を入力。
ターミナルを起動。
タブ横の展開ボタンをクリックして"コマンドプロンプト"を選択。
以下のように、入力プロンプトが表示される。XXXはログイン名

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

テスト用のプログラムを作る。プログラム名を任意の名前にする。
任意の名前としてmfhttsvrというプログラムとして説明を続ける。

プログラムを作成して運用まで実施することをProjectと呼ぶことが多い。
作業用のフォルダ(Projects)を作成してそのフォルダ内で、mfhttsrvフォルダを作成して、そこにプログラムファイル、参考資料をおいて、プログラムを完成させる。

以下のようなフォルダ構成にして、作業を進める。

C:\Users\XXX\Projects\mfhttsv

cmd.exeを実行して
mfhttsrvを作業ディレクトリにする。

```
C:\Users\XXX> cd Projects

C:\Users\XXX\Projects> cd mfhttsrv

C:\Users\XXX\Projects\mfhttsrv>

```

Visual Studio Codeを実行して、以下の内容を入力して、index.htmlとして保存する。

```
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>My first http page</title>
  </head>
  <body>
    <p>今日は世界!</p>
  </body>
</html>
```


# httpサーバの起動
cmd.exeで以下のコマンドを実行

```
C:\Users\XXX\Projects\mfhttsrv> svr.bat
Serving HTTP on port 8000 

```
上記のような出力がでて、"C:\Users\XXX\Projects\mfhttsrv>"が最後に出力されない状態になる。
これは、入力プロンプトが表示されていない状態。
つまり、コマンド入力を受け付けない状態。

これは、httpサーバが起動している状態になっているため。


# httpサーバの終了
入力コマンドを受け付ける状態にするには、httpサーバを終了する必要がある。
httpサーバを終了するには、カーソルが点滅している状態で、[Ctrl]キーと[C]キーを同時に押す。
```
C:\Users\XXX\Projects\mfhttsrv> svr.bat 
Serving HTTP on port 8000 
|
^
これが点滅している状態
```

httpサーバが終了すると、以下の文字列が表示される

```
Keyboard interrupt received, exiting.
```

# index.htmlの表示

cmd.exeでhttpサーバを起動する。

ブラウザを起動してアドレスバーに以下を入力

http://localhost:8000

index.htmlの内容が確認できる。


# httpサーバでpythonプログラムを実行

