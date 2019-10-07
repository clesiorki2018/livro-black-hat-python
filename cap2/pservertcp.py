#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 12:14:48 2019

@author: max
"""

import socket
import threading

bind_ip = "127.0.0.1"
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)

print("[*] Listing on %s:%d"%(bind_ip, bind_port))

# Esta é nossa thead para tratamento de clientes
def handle_client(client_socket):
    
    # Exibe o que o cliente enviar
    request = client_socket.recv(1024)
    print("[*] Received: %s"%request)
    
    # Envia um pacoote de volta
    client_socket.send(bytes('ACK!',encoding='UTF-8'))
    
    client_socket.close()
    

while True:
    client, addr = server.accept()
    print("[*] Accepted connection from %s:%d"%(addr[0],addr[1]))
    
    # Coloca nossa thread de cliente em ação para tratar dados deentrada
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()