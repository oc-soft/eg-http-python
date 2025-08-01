from http import server
# httpパッケージからserverをインポート
from urllib.parse import parse_qs
# urllib.parseパッケージからparse_qsをインポート
import datetime
# 日付、時刻関連のパケージをインポート

class Handler(server.SimpleHTTPRequestHandler):
    """ httpリクエストを処理する """

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

    def do_POST(self):
        """ http リクエストのPOSTメソッドに応答する"""
        res = self.handle_post()
        if not res:
            super().do_POST()
        pass

    def handle_get(self):
        """独自の応答処理を行う。リクエストが処理できない場合はFalseを返却 """
        result = False
        if '/custom-msg' == self.path:
            result = self.handle_get_custom_message()     
        elif '/comment' == self.path:
            result = self.handle_get_comment()
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

    def read_old_comment(self):
        """ 以前のコメントをファイルから読み取る"""

        result = ''
        try: 
            with open('comment.txt', encoding = 'UTF-8') as f:
                # commment.txtがあればfにデータが読み取り情報が格納されている 
                # commment.txtがない場合は、ここの処理はとおらない。
                result = f.read()
        except:
            pass
        
        return result

    def write_new_comment(self, new_comment):
        """ 新しいコメントをファイルに書き込む """
        result = False 
        with open('comment.txt', encoding = 'UTF-8', mode = 'w') as f:
            # comment.txtがない場合は、新しくcomment.txtが作成される
            # fにデータ書き込みのための各種情報が格納されている。
            f.write(new_comment)
            result = True
        return result


    def create_comment_page(self, new_comment = None):
        """ コメントページの作成 """
        # htmlページでは、formタグでサーバにデータを送信できる。
        old_comment = self.read_old_comment()

        if not new_comment:
            new_comment = ''

        result = f"""
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>コメント</title>
        <style>
            textarea[name="comment"] {{
                display: block;
            }}
        </style>
    </head>
    <body>
        <h1>コメント</h1>
        <div>
            <form action="comment" method="post">
                <label>新しいコメント</label>
                <textarea name="comment">{new_comment}</textarea>
                <label>以前のコメント</label>
                <p>{old_comment}</p>
                <!-- 送信ボタン -->
                <input type="submit">
            </form>
        </div>
    </body>
</html>
        """
        return result

    def handle_get_comment(self):
        """ GETメソッドのcomment処理"""
        # ページデータを作成
        page = self.create_comment_page()
        
        # ページをクライアント(ブラウザ)に返却
        result = self.response_comment_page(page)
        return result 

    def handle_post_comment(self):
        """ POSTメソッドのcomment処理 """
        result = True
    
        # リクエストにある内容のサイズを取得
        content_len = int(self.headers['Content-Length'])
        # 内容サイズ分だけ、データを取得(byte)
        body_byte = self.rfile.read(content_len)
        # UTF-8として文字列(str)に変換
        body_str = body_byte.decode('UTF-8')
        # body_strを解析(パース)して、dictionary形式のデータに変換
        # 処理を簡単にするため
        request_param = parse_qs(body_str)
        # request_paramのcommentにページで入力したコメントが格納されている
        new_comment = request_param['comment']
        if new_comment:
            # パースしたcommentは、listの形式になっている。
            # name=value&name=value1のような形式でデータ送られてくる
            # 可能性があるため
            # 一つ目の値をコメントとする。
            # フォームではcommentは1つしか送信されない
            new_comment = new_comment[0] 

        # ページデータを作成
        page = self.create_comment_page(new_comment)
        
        # 新しいコメントをファイルに保存
        self.write_new_comment(new_comment)        
        
        # ページをクライアント(ブラウザ)に返却
        result = self.response_comment_page(page)
        return result 
        
    def response_comment_page(self, comment_page):
        """ コメントページをクライアント(ブラウザ)に返却 """
        result = True
        # strデータからbyteデータへ変換
        content = comment_page.encode('UTF-8') 
        # 正常に処理が完了したことの応答をブラウザに返却
        self.send_response(200)
        # ブラウザに返却するhtmlファイルの情報を設定
        # データはUTF-8
        self.send_header("Content-type", "text/html; charset=UTF-8")
        # データの長さ contentの長さ
        self.send_header("Content-Length", str(len(content)))
        # ブラウザに返却するhtmlファイルの情報の設定完了
        self.end_headers()

        # htmlデータ本文
        # byteデータとして書き込み
        self.wfile.write(content)
        return result
        

    def handle_post(self):
        """ 独自のPOST処理 """ 
        result = False 
        if '/comment' == self.path:
            result = self.handle_post_comment()     
         
        return result
# vi: se ts=4 sw=4 et:
