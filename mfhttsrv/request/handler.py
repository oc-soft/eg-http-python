from http import server, HTTPStatus
# httpパッケージからserverをインポート
from urllib.parse import parse_qs
# urllib.parseパッケージからparse_qsをインポート
from subprocess import Popen, PIPE
# pythonから任意のプログラムを実行することができるPopenをインポート
import datetime
# 日付、時刻関連のパケージをインポート


class Handler(server.SimpleHTTPRequestHandler):
    """ httpリクエストを処理する """

    def __init__(self, *args, **kwargs):
        """ Handlerの初期化 """
        super().__init__(*args, directory = 'docroot', **kwargs)
        pass

    def do_GET(self):
        """ http リクエストのGETメソッドに応答する """
       
        # 独自の応答処理 
        res = self.handle_get()

        if not res:
            # 独自の応答処理ができない場合
            # server.SimpleHTTPRequestHandler.do_GETに処理を委譲する。
            super().do_GET()  
        pass

    pass

    def handle_get(self):
        """独自の応答処理を行う。リクエストが処理できない場合はFalseを返却 """
        result = False
        if '/custom-msg' == self.path:
            result = self.handle_get_custom_message()     
        return result
    def handle_get_custom_message(self):
        """ custom-msgのGETメソッド処理"""
        # カスタムメッセージ処理に委譲
        result = self.handle_custom_message()
        return result
 
    def handle_custom_message(self):
        """ カスタムメッセージ処理 """
        date_time = datetime.datetime.now().strftime('%Y-%m-%d %X') 
        content_str = f"""
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>カスタムメッセージ</title>
    </head>
    <body>
        <p>今は{date_time}です。</p>
    </body>
</html>
        """
        result = True

        # strデータからbyteデータへ変換
        content = content_str.encode('UTF-8') 
        # 正常に処理が完了したことの応答をブラウザに返却
        self.send_response(200)
        # ブラウザに返却するhtmlファイルの情報を設定
        # データはUTF-8
        self.send_header("Content-type", "text/html; charset=UTF-8")
        # データの長さ contentsの長さ
        self.send_header("Content-Length", str(len(content)))
        # ブラウザに返却するhtmlファイルの情報の設定完了
        self.end_headers()

        # htmlデータ本文
        # byteデータとして書き込み
        self.wfile.write(content)
        return result 

# vi: se ts=4 sw=4 et:
