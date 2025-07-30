from http import server # httpパッケージからserverをインポート

class Handler(server.SimpleHTTPRequestHandler):
    """ httpリクエストを処理する """

    def do_GET(self):
        """ http リクエストのGETメソッドに応答する """

        # server.SimpleHTTPRequestHandler.do_GETに処理を委譲する。
        super().do_GET()  
        pass

    pass
# vi: se ts=4 sw=4 et:
