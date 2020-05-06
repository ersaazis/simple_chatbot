from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
from SimpleChatbot.SimpleChatbot import SimpleChatbot
import sys
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        f = open("index.html", "r")
        self.wfile.write(bytes(f.read(), "utf8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        input=body.split(b'=')[1].decode("utf-8") 
        # print(input)
        chatbot = SimpleChatbot(input,'data.txt')
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(bytes(chatbot.getAnswere(), "utf8"))
        self.wfile.write(response.getvalue())


httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()