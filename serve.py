import http.server, socketserver

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='/Users/eugeniasam/Desktop/code/빕인-개인 세금계산기', **kwargs)
    def log_message(self, format, *args):
        pass

with socketserver.TCPServer(('', 3000), Handler) as httpd:
    httpd.serve_forever()
