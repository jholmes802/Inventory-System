from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import socket
import posts
import pages
import importlib
import db_manager
import re
import json
import dataio

hostName = 'localhost'#socket.gethostbyname(socket.gethostname())
serverPort = 80

post_dict = {
    "/pst/checkout_submit": posts.checkout_post,
    "/pst/new_item":posts.new_item
}


class MyServer(BaseHTTPRequestHandler):
    def _send_headers(self,typ):
        self.send_response(200)
        self.send_header("Content-type", typ)
        self.end_headers()

    def do_GET(self):
        importlib.reload(pages)
        importlib.reload(dataio)
        if self.path == "/":
            self._send_headers("text/html")
            self.wfile.write(pages.home())
        elif self.path == "/style.css":
            self._send_headers("text/css")
            self.wfile.write(open('../web/style.css', 'rb').read())
        elif self.path == '/script.js':
            self._send_headers("application/javascript")
            self.wfile.write(open("../web/script.js", 'rb').read())
        elif self.path.endswith("ufonts.com_bank-gothic-light.woff"):
            self._send_headers("font/woff")
            self.wfile.write(open("../web/ufonts.com_bank-gothic-light.woff", 'rb').read())
        elif self.path.startswith("/item"):
            part_num = self.path.split("/")[2]
            if re.search("^/item/.*/", self.path):
                if self.path.endswith(".css"):
                    self._send_headers("text/css")
                    self.wfile.write(open("../web/item/style.css", 'rb').read())
                elif self.path.endswith(".js"):
                    self._send_headers("application/javascript")
                    self.wfile.write(open("../web/item/script.js", 'rb').read())
                self._send_headers('text/html')
                self.wfile.write(pages.item(part_num))
            elif re.search("^/item/.*/verify", self.path):
                self._send_headers("text/html")
                self.wfile.write(pages.verify())
        elif self.path.startswith("/newitem/"):
            pass
        elif self.path.startswith("/checkout/"):
            self._send_headers("text/html")
            if self.path == "/checkout/":
                self.wfile.write(pages.checkout())
            else:
                self.wfile.write(open("../web" + self.path, "rb").read())
        elif self.path.startswith("/admin/"):
            self._send_headers("text/html")
            if self.path.startswith("/admin/locations/"):
                if self.path.endswith(".css"):
                    pass
                elif self.path.endswith(".js"): pass
                else:
                    self.wfile.write(pages.admin_locations())
            else:
                self.wfile.write(pages.admin())
        else:
            self.send_error(404)
    
    def do_POST(self):
        data = json.load(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
        self.send_response(200)
        resp = post_dict[self.path](data)  
        self.wfile.write(resp)          



if __name__ == '__main__':
    db_manager.sql_setup()
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Starting server on:", hostName +":"+ str(serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")