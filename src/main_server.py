#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import socket
import os
import posts
import pages
import importlib
import db_manager
import json
import pathlib
from urllib.parse import unquote
from tools import *



#"localhost"#
#socket.gethostbyname(socket.gethostname())
hostName = "localhost"#socket.gethostbyname(socket.gethostname())
if os.name == "nt":
    serverPort = 80
else:
    serverPort = 8080




class MyServer(BaseHTTPRequestHandler):
    def _send_headers(self,typ):
        self.send_response(200)
        self.send_header("Content-type", typ)
        self.end_headers()
    def do_GET(self):
        importlib.reload(pages)
        get_dict = {
            "/": ("text/html", pages.home.home()),
            "/script.js":("application/javascript", read_file('../web/script.js')),
            "/styles.css":("text/css", read_file('../web/styles.css')),
            "/newitem/": ("text/html", pages.home.new_item()),
            "/newitem/script.js":("application/javascript", read_file('../web/newitem/script.js')),
            "/newitem/styles.css":("text/css", read_file('../web/newitem/styles.css')),
            "/checkout/": ("text/html",pages.home.checkout()),
            "/checkout/script.js":("application/javascript", read_file('../web/checkout/script.js')),
            "/checkout/styles.css":("text/css", read_file('../web/checkout/styles.css')),
            "/checkin/": ("text/html",pages.home.checkin()),
            "/checkin/script.js":("application/javascript", read_file('../web/checkin/script.js')),
            "/checkin/styles.css":("text/css", read_file('../web/checkin/styles.css')),
            "/verify/":("text/html", pages.home.verify()),
            "/verify/script.js":("application/javascript", read_file('../web/verify/script.js')),
            "/verify/styles.css":("text/css", read_file('../web/verify/styles.css')),
            "/admin/":("text/html", pages.admin.admin()),
            "/admin/script.js":("application/javascript", read_file('../web/admin/script.js')),
            "/admin/styles.css":("text/css", read_file('../web/admin/styles.css')),
            "/item/":("text/html", pages.item.item_home),
            "/item/script.js":("application/javascript", read_file("../web/item/script.js")),
            "/item/styles.css":("text/css", read_file("../web/item/styles.css")),
            "/admin/import/":("text/html",pages.admin.admin_import()),
            "/admin/import/script.js":("application/javascript", read_file("../web/admin/import/script.js")),
            "/admin/import/styles.css":("text/css",read_file("../web/admin/import/styles.css")),
            "/admin/users/":("text/html",pages.admin.users()),
            "/admin/users/script.js":("application/javascript", read_file("../web/admin/users/script.js")),
            "/admin/users/styles.css":("text/css",read_file("../web/admin/users/styles.css"))
            }
        if "?" in self.path:
            main_path = self.path.split("?")[0]
            if main_path in get_dict.keys():
                args = self.path.split('?')[1]
                self._send_headers(get_dict[main_path][0])
                self.wfile.write(get_dict[main_path][1](args))
        elif self.path in get_dict.keys():
            self._send_headers(get_dict[self.path][0])
            self.wfile.write(get_dict[self.path][1])
        elif self.path.endswith(".woff"):
            self._send_headers("font/woff")
            self.wfile.write(read_file('../web/ufonts.com_bank-gothic-light.woff'))
        else:
            self.send_error(404)

    def do_POST(self):
        post_dict = {
            "/pst/checkout_submit": posts.checkout_post,
            "/pst/checkin_submit":posts.checkin,
            "/pst/newitem":posts.new_item,
            "/pst/verify_submit":posts.verify,
            "/pst/printBarcode":posts.print_barcode,
            "/pst/backup":posts.backup,
            "/pst/editpart":posts.editpart,
            "/pst/newuser":posts.newuser,
            "/pst/itemstatus":posts.itemstatus
        }
        if self.headers["Content-type"] != "application/json":
            self.send_response(400)
        else:
            str_data = self.rfile.read(int(self.headers["Content-length"])).decode("utf-8")
            data = json.loads(str_data)
            logger(2, "main_server:do_POSTS: Recieved the following data:" + str(data))
            self.send_response(200)
            resp = post_dict[self.path](data)
            print("Sending Response")
            self.wfile.write(resp.encode())

if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Starting server on:", hostName +":"+ str(serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")
