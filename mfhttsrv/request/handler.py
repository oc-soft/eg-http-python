from http.server import SimpleHTTPReqesHandler

class Handler(SimpleHTTPRequestHandler):


    def do_GET(self):
        super().do_GET()  
    pass
# vi: se ts=4 sw=4 et:
