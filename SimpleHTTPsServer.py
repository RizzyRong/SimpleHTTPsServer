# SimpleHTTPsServer, A SimpleHTTPServer that listens on 443, and captures GET/POST requests
# I recommend using certbot to create a valide certificate.

import SimpleHTTPServer
import SocketServer
import logging
import cgi
import ssl


PORT = 443
# Don't forget to set the path to your key and cert
ssl_key_file = "<PATH TO KEY FILE>"
ssl_certificate_file = "<PATH TO Cert>"

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        logging.error(self.headers)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        logging.error(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        for item in form.list:
            logging.error(item)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

Handler = ServerHandler

httpd = SocketServer.TCPServer(("", PORT), Handler)
httpd.socket = ssl.wrap_socket (httpd.socket, server_side=True,
                                keyfile=ssl_key_file,
                                certfile=ssl_certificate_file)

print "serving at port", PORT
httpd.serve_forever()
