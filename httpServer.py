from http.server import HTTPServer, BaseHTTPRequestHandler

from http.server import HTTPServer, CGIHTTPRequestHandler
import webbrowser
import threading
import os

class MyHttpServer():

    def __init__(self,):

        pass
        #self.path = path
        #self.address = (ip, port)

    def start(self):

        httpd = HTTPServer(self.address, BaseHTTPRequestHandler)
        httpd.serve_forever()



    def start_server(self, path, port=8999):

        '''Start a simple webserver serving path on port'''

        os.chdir(path)
        httpd = HTTPServer(('', port), CGIHTTPRequestHandler)
        httpd.serve_forever()

# Start the server in a new thread



# Open the web browser
