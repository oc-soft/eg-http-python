

## 使用するapi

1. `SimpleHTTPRequestHandler.translate_path`
2. `open`
3. `SimpleHTTPRequestHandler.copyfile`
4. `str.format`
5. `io.StringIO`
6. `io.StringIO.getvalue`


### 1. `SimpleHTTPRequestHandler.translate_path`

docrootからの相対パスをファイルシステムのパスに変換する。

### 2. `open`

ファイルをプログラムで読み書きできるようにする。
openで返却された値を便宜上、ファイルオブジェクトと呼びます。

### 3. `SimpleHTTPRequestHandler.copyfile`

ファイルオブジェクトが保持しているデータを別のファイルオブジェクトにコピーします。

### 4. `str.format`

文字列内の{value}の形式を、valueが指し示す値で置き換えます。


### 5. `io.StringIO`

メモリ上に文字列を保存する、ファイルオブジェクト互換のオブジェクトを生成します。


### 6. `io.StringIO.getvalue`

5のオブジェクトから、文字列を取り出します。

