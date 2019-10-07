#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 14:19:04 2019

@author: max
"""

import socket
import os

# Host que ouvirá
host = '192.168.0.134'

# Cria um socket puro e o asssocia-o à interface pública
if os.name == 'nt':
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol =  socket.IPPROTO_ICMP
    
sniffer  = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host,0))

# Queremos cabeçalhos IP incluídos na captura
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# Se estiver no windows, deveremos enviar um IOCTL
# para configurarr o modo promiscuo
if os.name == 'nt':
    sniffer.ioctl(socket.SIO_RECVALL, socket.RECVALL_ON)

# lê um únicco pacote
print(sniffer.recvfrom(65565).decode('UTF-8'))

# Se estiver no windows, desabilitará o modo promiscuo
if os.name == 'nt':
    sniffer.ioctl(socket.SIO_RECVALL, socket.RECVALL_OFF)
