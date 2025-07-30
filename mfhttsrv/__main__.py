from http import server
# httpパッケージからserverモジュールをインポート
import socket
# socketモジュールをインポート
from .request.handler import Handler
# 自作Httpリクエスト応答モジュールをインポート


# httpサーバが待ち受けするポートを指定
port_number = 8000

# 稼働システムの全てのアドレスで待ち受け(スマホからテストするため)
bind_address = '0.0.0.0'

# 稼働システムのport_numberに対するアドレス一覧を得る
address_info_list = socket.getaddrinfo(bind_address, port_number)

# http リクエストの対応バージョンを1.0とする。
Handler.protol_version = 'HTTP/1.0'


# address_info_listの一番最初が、streamになっている。
# streamがhttpサーバが対応するデータタイプ

# 取得したアドレス最初のデータを各種設定に使用する
address_info = address_info_list[0]

# 通信のアドレスファミリをipに設定
server.ThreadingHTTPServer.address_familiy = address_info[0]

# http サーバインスタンスを作成
# address_info[1]は、サーバアドレス
# Handlerは、httpリクエストを処理するクラス
with server.ThreadingHTTPServer(address_info[4], Handler) as httpd:
    # httpサーバインスタンスが実際に待ち受けしているホスト名とポート番号を取得
    host, port = httpd.socket.getsockname()[:2] 
    print(f'Serving HTTP on port {port}')
    try:
        # サービス開始
        httpd.serve_forever()
        # これ以降の処理は実施されない  
        print('finished server')
        # この処理は実行されない
    except KeyboardInterrupt:
        # コンソールでCtrl+Cを押下するとこの処理が実行される。
        print('Kyeboad interrupt received, exiting.') 
# ここに処理がくるのは、コンソールでCtrl+Cを押下した場合
print('service is closed')

# vi: se ts=4 sw=4 et:
