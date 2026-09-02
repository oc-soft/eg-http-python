# 要件


1. 任意のTODO項目を追加できる
2. チェックボックスにチェックし更新をすると、当該TODOは消える
3. スマートフォン対応とする。
4. ダークモード対応とする。


# 仕様

## 入力

入力は、TODO項目が1つもない状態とそれ以外の状態がある。

## 未入力時

<div>
  <iframe src="todo-1.html"></iframe>
</div>

## 入力時
<div>
  <iframe src="todo-2.html"></iframe>
</div>

### 送信

送信を押下した場合の動作を記載する。

#### 新規アイテム

空白ではない場合、入力がTODO項目として登録される。


#### TODO項目

チェックがついている場合、TODO項目から削除される。


# 設計

サイトへのアクセスは、以下のとおり。

1. TODOリストを表示する。
2. TODOリストを更新する。


表示、更新の応答htmlのstyleで、スマートフォン表示、ダークモードの対応を行う。


## TODOリストを表示

TODOリストを表示では、HTTPリクエストは、GETリクエストとする。

ブラウザのアドレスバーにURLを入力して、サイトにアクセスする場合の挙動である。

<div id="get-todo">
</div>


## TODOリストを更新

TODOリストを更新では、HTTPリクエストは、POSTリクエストする。

ブラウザで入力フォームを送信するデフォルトの挙動である。

<div id="post-todo">
</div>


## 詳細設計

### TODOリスト表示

TODO項目は、チェックで完了となるまで、TODOリストに残っている必要がある。
TODO項目をサーバ側のファイルに保存して、ファイルからTODO項目を読み取ることによって、要件を満たす。
TODO項目が記録されるファイルを`todo.txt`とする。

TODOリストの表示のサーバの処理は次のようなフローになる。

<div id="get-todo-flow">
</div>


### TODOリスト更新

新規アイテムがある場合は、`todo.txt`ファイルに新規アイテムを追加する。
完了TODO項目がある場合は、`todo.txt`ファイルから削除する。
処理完了後、TODOリスト表示と同様にhtml形式のTODOリストを作成する。

<div id="post-todo-flow">
</div>


### TODOリスト表示、更新の統合

TODOリスト表示は、リクエストに新規アイテムがなく、完了TODO項目がない場合にあたる。TODOリスト表示においては、TODOリスト更新の処理で代用する。ただし、リクエストメソッドはPOSTとGETで異なるため、リクエストの受付処理はそれぞれ設ける。


### todo.txtの位置

サーバがリソースを検索するdocroot配下のuser-dataに`todo.txt`を格納する。

<div id="todo-txt-loc">
</div>

### todoリストのhtmlテンプレート

クライアントに送信するhtml文字列のhtmlは、以下の方針とする。

- docroot配下のassetsにテンプレート形式のファイルで保存する。
- 内容の一部は、処理中の変数で置き換える。
- ファイル名は`todo-tmpl.html`とする。

サーバ側の格納場所は以下とする。

<div id="todo-html-loc">
</div>




## styleの追加

htmlの表示に関わるstyleは、todo.cssというファイルに記述し、htmlからlink参照する。
サーバ側の格納場所は以下とする。

<div id="todo-css-loc">
</div>

<!-- vi: se ts=2 sw=2 et: -->
