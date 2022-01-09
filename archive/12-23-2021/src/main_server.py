from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import socket
import pages
import importlib

hostName = socket.gethostbyname(socket.gethostname())
serverPort = 80

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        importlib.reload(pages)
        if self.path == '/': #Handler for home page or index page
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(pages.home())
        elif self.path.endswith('.ico'): #Handles the ico file.
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            self.wfile.write(open("../web"+self.path, 'rb').read())
        elif self.path.endswith('style.css'): #Handles the CSS files.
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            self.wfile.write(open("../web/style.css", 'rb').read())
        elif self.path.endswith('script.js'): #Handles the JS files.
            self.send_response(200)
            self.send_header('Content-type', 'text/js')
            self.end_headers()
            self.wfile.write(open("../web/script.js", 'rb').read())
        elif "ufonts.com_bank-gothic-light.woff" in self.path:
            self.send_response(200)
            self.send_header("Content-type", 'font/woff')
            self.end_headers()
            self.wfile.write(open("../web/ufonts.com_bank-gothic-light.woff", 'rb').read())
        elif "/newitem" in self.path: #Handler for new item page.
            #Handleing any data that may be submitted to "New Item" page.
            if "?" in self.path:
                data = self.path.split('?')[1]
            else:
                data = None
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(pages.new_item(data))
        elif "/item/" in self.path:
            part_num = self.path.lstrip("/item/")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(pages.item(part_num))
        elif "/checkout-in/" in self.path:
            part_num = self.path.lstrip("/checkout-in/")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(pages.checkout(part_num))
        else:
            self.send_error(404)

if __name__ == '__main__':
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Starting server on:", hostName +":"+ str(serverPort))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")