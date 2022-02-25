#!/usr/bin/python3
from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import posts
import pages
import importlib
import json
from tools import *
import socket
#"localhost"#
#socket.gethostbyname(socket.gethostname())
hostName = socket.gethostbyname(socket.gethostname())
if os.name == "nt":
    serverPort = 80
else:
    serverPort = 8080

get_funcs = {
    "/": ("text/html", pages.home.home),
    "/newitem/": ("text/html", pages.home.new_item),
    "/checkout/": ("text/html",pages.home.checkout),
    "/checkin/": ("text/html",pages.home.checkin),
    "/verify/":("text/html", pages.home.verify),
    "/admin/":("text/html", pages.admin.admin),
    "/item/":("text/html", pages.item.item_home),
    "/admin/import/":("text/html",pages.admin.admin_import),
    "/admin/users/":("text/html",pages.admin.users)
}
get_files = {
    "/script.js":("application/javascript", read_file('../web/script.js')),
    "/styles.css":("text/css", read_file('../web/styles.css')),
    "/newitem/script.js":("application/javascript", read_file('../web/newitem/script.js')),
    "/newitem/styles.css":("text/css", read_file('../web/newitem/styles.css')),
    "/checkout/script.js":("application/javascript", read_file('../web/checkout/script.js')),
    "/checkout/styles.css":("text/css", read_file('../web/checkout/styles.css')),
    "/checkin/script.js":("application/javascript", read_file('../web/checkin/script.js')),
    "/checkin/styles.css":("text/css", read_file('../web/checkin/styles.css')),
    "/verify/script.js":("application/javascript", read_file('../web/verify/script.js')),
    "/verify/styles.css":("text/css", read_file('../web/verify/styles.css')),
    "/admin/script.js":("application/javascript", read_file('../web/admin/script.js')),
    "/admin/styles.css":("text/css", read_file('../web/admin/styles.css')),
    "/item/script.js":("application/javascript", read_file("../web/item/script.js")),
    "/item/styles.css":("text/css", read_file("../web/item/styles.css")),
    "/admin/import/script.js":("application/javascript", read_file("../web/admin/import/script.js")),
    "/admin/import/styles.css":("text/css",read_file("../web/admin/import/styles.css")),
    "/admin/users/script.js":("application/javascript", read_file("../web/admin/users/script.js")),
    "/admin/users/styles.css":("text/css",read_file("../web/admin/users/styles.css"))
}
    
class MyServer(BaseHTTPRequestHandler):
    def _send_headers(self,typ):
        self.send_response(200)
        self.send_header("Content-type", typ)
        self.end_headers()
    def do_GET(self):
        if "?" in self.path:
            main_path = self.path.split("?")[0]
            args=self.path.split("?")[1]
        else:
            main_path = self.path
            args = None

        if main_path in get_files.keys():
            typ, page = get_files[main_path]
            self._send_headers(typ)
            self.wfile.write(page)
        elif main_path in get_funcs.keys():
            typ, page = get_funcs[main_path]
            if args != None:
                page = page(args)
            else:
                page = page()
            self._send_headers(typ)
            self.wfile.write(page)
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
