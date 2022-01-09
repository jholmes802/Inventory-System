from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import socket
import pages
import importlib
import db_manager
import re
import dataio

hostName = 'localhost'#socket.gethostbyname(socket.gethostname())
serverPort = 80



class MyServer(BaseHTTPRequestHandler):
    def _send_headers(self,typ):
        self.send_response(200)
        self.send_header("Content-type", typ)
        self.end_headers()

    def do_GET(self):
        importlib.reload(pages)
        importlib.reload(dataio)
        if self.path == '/': #Handler for home page or index page
            self._send_headers('text/html')
            self.wfile.write(pages.home())
        elif self.path.endswith('.ico'): #Handles the ico file.
            self._send_headers('image/png')
            self.wfile.write(open("../web"+self.path, 'rb').read())
        elif self.path.endswith('.css'): #Handles the CSS files.
            self._send_headers('text/css')
            self.wfile.write(open("../web" + self.path, 'rb').read())
        elif self.path.endswith('script.js'): #Handles the JS files.
            self._send_headers('text/javascript')
            self.wfile.write(open("../web" + self.path, 'rb').read())
        elif self.path.endswith("ufonts.com_bank-gothic-light.woff"):
            self._send_headers("font/woff")
            self.wfile.write(open("../web/ufonts.com_bank-gothic-light.woff", 'rb').read())
        elif "/newitem" in self.path: #Handler for new item page.
            #Handleing any data that may be submitted to "New Item" page.
            if "?" in self.path:
                data = self.path.split('?')[1]
            else:
                data = None
            self._send_headers("text/html")
            self.wfile.write(pages.new_item(data))
        elif re.search("^/item/.*/$", self.path) != None:
            part_num = self.path.lstrip("/item/").rstrip("/")
            self._send_headers("text/html")
            self.wfile.write(pages.item(part_num))
        elif self.path == '/checkout':
            self._send_headers("text/html")
            self.wfile.write(pages.checkout())
        elif re.search("^/item/.*/delete.*", self.path) != None:
            if "?" in self.path:
                data = [x.split("=")[1] for x in self.path.split("?")[1].split("&")]
            else: data = None
            part_num = self.path.split("/")[2]
            self._send_headers("text/html")
            self.wfile.write(pages.delete_part(part_num, data))
        elif re.search("^/item/.*/verify?", self.path) != None:
            data = self.path.split("/")[3].lstrip("verify?")
            print(data)
            self._send_headers("text/html")
            self.wfile.write(pages.verify(data, self.path))
        elif self.path == "/backup/":
            self._send_headers("text/html")
            self.wfile.write(pages.backup())
        elif self.path == "/barcodes/":
            self._send_headers("text/html")
            self.wfile.write(pages.barcodes_page())
        elif self.path.endswith(".png"):
            self._send_headers("img/png")
            self.wfile.write(open(".." + self.path, "rb").read())
        elif self.path == '/admin/':
            self._send_headers('text/html')
            self.wfile.write(pages.admin())
        else:
            self.send_error(404)
    
    def do_POST(self):
        self.send_response(200)
        if self.path.startswith("/checkout?"): #CHECKOUT Handler
            data = [x.split("=")[1] for x in self.path.lstrip("/checkout?").split("&")]
            dataio.transaction(data[0], data[1], 'OUT')
            transactions_list = dataio.get_transactions(types=["OUT", "IN"])
            sender =pages.transactions_table(transactions_list)
            self.wfile.write(sender)


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