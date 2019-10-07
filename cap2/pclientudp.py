#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 11:46:23 2019

@author: max
"""

import socket

target_host = "127.0.0.1"
target_port = 80

# Cria um objeto socket
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Envia alguns dados
msg = "GET / HTTP /1.1\r\nHost:clesiomaxuel.org\r\n\r\n"
msg = bytes(msg, encoding='UTF-8')
client.sendto(msg,(target_host, target_port))

# Recebe alguns dados
data, addr = client.recvfrom(4096)

print('oi')