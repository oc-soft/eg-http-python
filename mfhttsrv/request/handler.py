from http import server, HTTPStatus
# httpパッケージからserverをインポート
from urllib.parse import parse_qs, urlparse
# urllib.parseパッケージからparse_qs, urlparseをインポート
from subprocess import Popen, PIPE
# pythonから任意のプログラムを実行することができるPopenをインポート
import os
# 階層作成などが含まれるパッケージをインポート
import io
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

        # assets/content-mng.txtのdocoroot相対のファイルシステムパスにする。  
        custom_msg_path = self.translate_path('assets/custom-msg.txt') 
        # メモリ上に文字列データを書き込むファイルシステムオブジェクトを作成
        content_str_stream = io.StringIO()

        # custom-msg.txtファイルを開き、ファイルシステムオブジェクトを得る
        # ファイルはutf-8で保存しているので、utf-8の変換をして読み取る。
        with open(custom_msg_path, encoding='utf_8') as fp:
            # custom-msg.txtファイルの内容をcontent_str_streamにコピー
            self.copyfile(fp, content_str_stream)
        # io.StringIOオブジェクトが保持しているデータを文字列として取り出す 
        temp_str = content_str_stream.getvalue()
        # {date_time}、{req_time}を日時に置き換える
        content_str = temp_str.format(date_time=date_time, req_time=req_time)
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
                <li>
                    <label>
                        <input type="checkbox" />{item}
                    </label>
                </li>
            """ 
            todo_list_html.append(html_item)
        list_contents = "\n".join(todo_list_html)

        result = f"""
            <ul>
                {list_contents}
            </ul>
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
        # assets/todo-tmpl.htmlのdocoroot相対のファイルシステムパスにする。  
        todo_tmpl_path = self.translate_path('assets/todo-tmpl.html') 
        content_str_stream = io.StringIO()

        # todo-tmpl.htmlファイルを開き、ファイルシステムオブジェクトを得る
        # ファイルはutf-8で保存しているので、utf-8の変換をして読み取る。
        with open(todo_tmpl_path, encoding='utf_8') as fp:
            # todo-tmpl.htmlファイルの内容をcontent_str_streamにコピー
            self.copyfile(fp, content_str_stream)
        # io.StringIOオブジェクトが保持しているデータを文字列として取り出す 
        template_str = content_str_stream.getvalue()
        # {todo_list_html}を置き換える
        result = template_str.format(todo_list_html=todo_list_html)
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

        # user-data/todo.txtをdocoroot相対のファイルシステムパスにする。  
        todo_path = self.translate_path('user-data/todo.txt') 
        try: 
            with open(todo_path, mode = 'r', encoding = 'UTF-8') as f:
                # todo.txtがあればfにデータが読み書き情報が格納されている 
                # todo.txtがない場合は、ここの処理はとおらない。
                lines = f.readlines()
        except:
            pass
        try:    
            # user-dataをdocoroot相対のファイルシステムパスにする。  
            user_data_dir = self.translate_path('user-data')  
            # 階層(ディレクトリ)が存在しない場合があるので、階層を作成する。
            os.makedirs(user_data_dir, exist_ok=True)
            with open(todo_path, mode = 'a', encoding = 'UTF-8') as f:
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
            todo_path = self.translate_path('user-data/todo.txt') 
            with open(todo_path, mode = 'r', encoding = 'UTF-8') as f:
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
