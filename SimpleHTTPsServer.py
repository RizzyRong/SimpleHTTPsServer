# SimpleHTTPsServer, A SimpleHTTPServer that listens on 443, and captures GET/POST requests
# I recommend using certbot to create a valide certificate.

import http.server
import socketserver
import logging
import cgi
import ssl


PORT = 443
# Don't forget to set the path to your key and cert
ssl_key_file = "key.pem"
ssl_certificate_file = "cert.pem"


class ServerHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.error(self.headers)
        http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.error(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        for item in form.list:
            logging.error(item)
        http.server.SimpleHTTPRequestHandler.do_GET(self)


Handler = ServerHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.socket = ssl.wrap_socket(httpd.socket, server_side=True,
                               keyfile=ssl_key_file,
                               certfile=ssl_certificate_file)

print(f"serving at port: {PORT}")
httpd.serve_forever()
