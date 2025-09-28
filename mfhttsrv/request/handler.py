from http import server, HTTPStatus
# httpパッケージからserverをインポート
from urllib.parse import parse_qs, urlparse
# urllib.parseパッケージからparse_qs, urlparseをインポート
from subprocess import Popen, PIPE
# pythonから任意のプログラムを実行することができるPopenをインポート
import datetime
# 日付、時刻関連のパケージをインポート
import json
# pythonのデータをjson化するパッケージをインポート
import sys
# デフォルトの例外を扱うためにインポート

class Handler(server.SimpleHTTPRequestHandler):
    """ httpリクエストを処理する """

    @property
    def datetime_fmt(self):
        """ 仕様の日時フォーマット """
        return '%Y-%m-%d %H:%M:%S.%f %Z'

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

    def do_POST(self):
        """ http リクエストのPOSTメソッドに応答する"""
        res = self.handle_post()
        if not res:
            self.send_error(HTTPStatus.NOT_IMPLEMENTED, 
                "Can not handle your request.")
        pass

    def handle_get(self):
        """独自の応答処理を行う。リクエストが処理できない場合はFalseを返却 """
        result = False
        
        parse_res = urlparse(self.path)
        if '/custom-msg' == parse_res.path:
            result = self.handle_get_custom_message(parse_res.query)
        elif '/server-time' == parse_res.path:
            result = self.handle_get_server_time(parse_res.query)
        elif '/todo' == parse_res.path:
            result = self.handle_get_todo_list()
        return result
    def handle_get_custom_message(self, query):
        """ custom-msgのGETメソッド処理"""
        qparams = parse_qs(query)

        request_time = None
        if 'request-time' in qparams:
           request_times = qparams['request-time'] 
           if request_times:
               request_time = request_times[0]
        # カスタムメッセージ処理に委譲
        result = self.handle_custom_message(request_time)
        return result

    def handle_get_server_time(self, query):
        """ server-timeのGETメソッド処理"""
        qparams = parse_qs(query)

        request_time = None
        if 'request-time' in qparams:
           request_times = qparams['request-time'] 
           if request_times:
               request_time = request_times[0]
        result = self.handle_server_time(request_time) 
        return result
 
    def handle_custom_message(self, request_time):
        """ カスタムメッセージ処理 """
        # タイムゾーンが付与されたdatetimeオブジェクトを取得
        cur_datetime = datetime.datetime.now().astimezone()
        req_time = None
        if request_time:
            try:
                req_time = datetime.datetime.fromisoformat(request_time)
                req_time = req_time.astimezone()
            except: 
                req_time = cur_datetime
        else:
            req_time = cur_datetime
                
        date_time = cur_datetime.strftime(self.datetime_fmt) 
        req_time = req_time.strftime(self.datetime_fmt)
        content_str = f"""
<!doctype html>
<html>
    <head>
        <!-- スマートフォン対応 -->
        <meta name="viewport" content="width=device-width; initial-scale=1.0">
        <meta charset="utf-8">
        <title>カスタムメッセージ</title>
        <style>
            body {{
                /* bodyの高さを表示高さと一致させる*/ 
                height: calc(100vh - 2 * 8px);
                /* 日本語でいうゴシック的なフォントを使用 */
                font-family: sans-serif;
                /* 完全な黒ではなく非常に濃いグレーを表示に使用 */
                color: #0f0f0f;
                margin: 8px;
            }}
            main:first-of-type {{
                /* 縦方向の位置調整をしたい */
                position: absolute; 
                /* 日時を表示する位置を画面中央やや上にする */
                top: 20%;
                /* 幅は包含する要素幅と同じとする */
                left: 0;
                right: 0;
                /* 日時表示テーブル横方向を中央にしたい */
                display: flex;
                justify-content: center;
            }}
            main table {{
                /* 3秒で徐々に文字が表示されるように設定 */
                transition: opacity 3s; 
                @starting-style {{
                   opacity: 0; 
                }}
            }}
            /* ダークモード */
            @media (prefers-color-scheme: dark) {{
                html {{
                    /* 完全な黒ではなく非常に濃いグレーを表示に使用 */
                    background: #0f0f0f;
                }}
                body {{
                    /* 完全な白ではなく非常に薄いグレーを表示に使用 */
                    color: #cccccc;
                }}
            }}
            @media (width <= 450px) {{
                main table {{
                    display: block;
                }}
                main table tr {{
                    display: block;
                    margin-top: 10px;
                }}
                main table tr:first-element {{
                    margin-top: 0px;
                }}
                main table tr td {{
                    display: block;
                }}
            }}
            @media (width <= 380px) {{
                body {{
                    font-size: 0.8em;
                }}
            }}

        </style>
        <script>
            /**
             * サーバ日時を取得
             * @return json形式のサーバ日時、リクエスト日時
             */
            async function getServerTime() {{
                // リクエスト日時 
                const currentTime = new Date().toISOString() 
                let requestUrl = `/server-time?request-time=${{currentTime}}`
                // リクエストURLを生成(URLで有効な文字だけにエスケープ)
                requestUrl = encodeURI(requestUrl)
                let result = undefined
                try {{
                    // リクエストを送信し、結果を受信
                    const res = await window.fetch(requestUrl)
                    if (res.ok) {{
                        // 受信がOK
                            // 受信結果からjson形式のオブジェクトを取得
                            result = res.json() 
                    }}
                }} catch (error) {{
                    // 送受信のエラーが発生した場合の制御
                    // 特に何も処理を実施しない
                }}
                return result
            }}
            /**
             * HTML要素を更新
             *
             */
            function updateElement(elem, datetime) {{
               elem.textContent = datetime 
            }}
            /**
             * サーバ日時を表示しているHTML要素を取得
             * @return サーバ日時を表示しているHTML要素
             */
            function getServerTimeElement() {{
                return document.getElementsByClassName('server-time')[0]
            }}
            /**
             * リクエスト日時を表示しているHTML要素を取得
             * @return リクエスト日時を表示しているHTML要素
             */
            function getRequestTimeElement() {{
                return document.getElementsByClassName('request-time')[0]
            }}

            /**
             * サーバ日時、リクエスト日時を更新
             */
            async function updateServerTime() {{
                // サーバ日時を取得
                const resp = await getServerTime()
                if (resp) {{
                    // 取得に成功
                    if (resp['server-time'] && resp['request-time']) {{
                        // 受信したjsonオブジェクトにserver-time、request-time
                        // の要素がある場合にHTML要素を更新する
                        updateElement(getServerTimeElement(),
                            resp['server-time'])
                        updateElement(getRequestTimeElement(),
                            resp['request-time'])

                    }}
                }}
            }}
            /**
             * サーバ日時を更新し続ける
             */
            async function updateServerTimeForever() {{
                // サーバ日時を更新
                await updateServerTime() 
                // 更新が完了したら、10秒後にこの処理が呼ばれるように設定
                setTimeout(updateServerTimeForever, 1000 * 10)
            }}
            /**
             * HTMLページの読み込みが完了した時の処理
             */
            function handleLoad() {{
                // 10秒後からサーバ日時を更新し続ける
                setTimeout(updateServerTimeForever, 1000 * 10)
            }}
            // HTMLページ読み込みが完了した時に処理が呼ばれるように設定
            window.addEventListener('load', handleLoad)
        </script>
    </head>
    <body>
        <main>
            <table>
                <tr aria-describedby="server-response">
                    <td>サーバ日時</td>
                    <td class="server-time">{date_time}</td>
                </tr>
                <tr aria-describedby="client-request">
                    <td>リクエスト日時</td>
                    <td class="request-time">{req_time}</td>
                </tr>
            </table>
        </main>
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

    def handle_server_time(self, request_time):
        """ サーバ日時をjson形式としてレスポンスを作成"""
        cur_datetime = datetime.datetime.now().astimezone()
        req_time = None
        if request_time:
            try:
                req_time = datetime.datetime.fromisoformat(request_time)
                req_time = req_time.astimezone()
            except: 
                req_time = cur_datetime
        else:
            req_time = cur_datetime
        date_time = cur_datetime.strftime(self.datetime_fmt) 
        req_time = req_time.strftime(self.datetime_fmt)
        json_obj = {
            'server-time': date_time,
            'request-time': req_time
        }
        content_str = json.JSONEncoder().encode(json_obj)
        
        result = True
        # strデータからbyteデータへ変換
        content = content_str.encode('UTF-8') 
        # 正常に処理が完了したことの応答をブラウザに返却
        self.send_response(200)
        # ブラウザに返却するhtmlファイルの情報を設定
        # データはUTF-8
        self.send_header("Content-type", "application/json; charset=UTF-8")
        # データの長さ contentsの長さ
        self.send_header("Content-Length", str(len(content)))
        # ブラウザに返却するhtmlファイルの情報の設定完了
        self.end_headers()

        # htmlデータ本文
        # byteデータとして書き込み
        self.wfile.write(content)

        return result 
    def convert_to_html_todo_list(self, todo_list):
        """ TODO リストをhtml形式の文字列に変換する"""
        todo_list_html = []
        for item in todo_list:
            html_item = f"""
                <tr><td><input type="checkbox"></td>
                <td><label>{item}</label></td></tr>
            """ 
            todo_list_html.append(html_item)
        table_contents = "\n".join(todo_list_html)

        result = f"""
            <table>
                {table_contents}
            </table>
        """
        return result
    def create_todo_list_page(self, new_item = None):
        """ TODOリストページの作成 """
        # htmlページでは、formタグでサーバにデータを送信できる。
        if new_item:
            todo_list = []
            self.update_todo_list(new_item, todo_list)
        else:
            todo_list = self.read_todo_list()
        todo_list_html = self.convert_to_html_todo_list(todo_list)

        result = f"""
<!doctype html>
<html>
    <head>
        <meta charset="utf-8">
        <title>TODOリスト</title>
        <style>
        </style>
    </head>
    <body>
        <h1>TODOリスト</h1>
        <div>
            <form action="todo" method="post">
                <label>新規アイテム:<input name="new-item" type="text"></label>
                {todo_list_html}  
                <!-- 送信ボタン -->
                <input type="submit">
            </form>
        </div>
    </body>
</html>
        """
        return result

    def update_todo_list(self, new_item, todo_list = None):
        """
        todoリストにnew_itemを追加する。
        todo_listが指定されていれば、todo_listに保存した要素の一覧が
        格納される。    
        """
        lines = None
        # 両端の空白を削除  
        new_item = new_item.strip()
        # 末端に改行を追加
        new_item += "\n"
        try: 
            with open('todo.txt', mode = 'r', encoding = 'UTF-8') as f:
                # todo.txtがあればfにデータが読み書き情報が格納されている 
                # todo.txtがない場合は、ここの処理はとおらない。
                lines = f.readlines()
        except:
            pass
        try:    
            with open('todo.txt', mode = 'a', encoding = 'UTF-8') as f:
                f.writelines([new_item])
        except Exception as e:
            print(e) 
            pass
        if todo_list is not None:
            if lines is not None:
                lines.append(new_item)
                lines.reverse()
                todo_list.extend(lines)
            else:
                todo_list.append(new_item) 

    def read_todo_list(self):
        """
        保存しているtodoの一覧を所得する。
        """
        result = [] 
        try: 
            with open('todo.txt', mode = 'r', encoding = 'UTF-8') as f:
                # todo.txtがあればfにデータが読み書き情報が格納されている 
                # todo.txtがない場合は、ここの処理はとおらない。
                result = f.readlines()
                result.reverse()
        except:
            pass
        return result 

    def handle_get_todo_list(self):
        """ GETメソッド todo処理"""
        # ページデータを作成
        page = self.create_todo_list_page()
        
        # ページをクライアント(ブラウザ)に返却
        result = self.response_todo_list_page(page)
        return result 

    def handle_post_todo_list(self):
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
        # request_paramのnew-itemにページで入力したコメントが格納されている
        new_items = None
        if 'new-item' in request_param:
            new_items = request_param['new-item']
        new_item = None
        if new_items:
            # パースしたnew_itemは、listの形式になっている。
            # name=value&name=value1のような形式でデータ送られてくる
            # 可能性があるため
            # 一つ目の値をコメントとする。
            # フォームではcommentは1つしか送信されない
            new_item = new_items[0] 

        # ページデータを作成
        page = self.create_todo_list_page(new_item)
        
        # ページをクライアント(ブラウザ)に返却
        result = self.response_todo_list_page(page)
        return result 

        
    def response_todo_list_page(self, page):
        """ TODOリストページをクライアント(ブラウザ)に返却 """
        result = self.response_general_html_page(page)
        return result


    def response_general_html_page(self, page_data):
        """ 一般的なページをブラウザに返却""" 
        result = True
        # strデータからbyteデータへ変換
        content = page_data.encode('UTF-8') 
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
        if '/todo' == self.path:
            result = self.handle_post_todo_list()
         
        return result
# vi: se ts=4 sw=4 et:
