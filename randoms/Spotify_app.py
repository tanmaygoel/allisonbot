import os
import sys
from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer

class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def translate_path(self,path):
        path = SimpleHTTPRequestHandler.translate_path(self,path)
        if os.path.isdir(path):
            for base in "index", "default":
                for ext in ".html", ".htm", ".txt":
                    index = path + "/" + base + ext
                    if os.path.exists(index):
                        return index
        return path

def test(HandlerClass = MyHTTPRequestHandler,
         ServerClass = BaseHTTPServer.HTTPServer):
    BaseHTTPServer.test(HandlerClass, ServerClass)


if __name__ == '__main__':
    test()