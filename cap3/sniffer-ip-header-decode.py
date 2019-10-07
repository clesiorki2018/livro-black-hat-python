#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 16:49:44 2019

@author: max
"""

import socket

import os
import struct
from ctypes import Structure, c_ubyte, c_ushort, c_ulong

# Host que ouvirá
host = '127.0.0.1'

# Nosso cabeçalho IP
class IP(Structure):
    _filds_ = [
            ("ihl",         c_ubyte, 4),
            ("version",     c_ubyte, 4),
            ("tos",         c_ubyte),
            ("len",         c_ushort),
            ("id",          c_ushort),
            ("offset",      c_ushort),
            ("ttl",         c_ubyte),
            ("protocol_num", c_ubyte),
            ("sum",         c_ushort),
            ("src",         c_ulong),
            ("dst",         c_ulong)
        ]
    
    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer=None):
        
        # Mapeia constantes do protocolo ao seus nomes
        self.protocol_map = {1:'ICMP', 6:'TCP', 17:'UDP'}
        
        # Endereços legíveis aos seres humanos
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack('<L', self.dst))
        
        # Protocolo legível aos seres humanos
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = self.protocol_num
        
        
# Este código deve parecer familiar pois foi visto no exemlo anterior

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
    
try:
    while True:
        
        # Le um pacote
        raw_buffer = sniffer.recvfrom(65565)[0]
        
        #Cria um cabeçalho a partir dos 20 primeiros bytes do buffer
        ip_header = IP(raw_buffer[0:20])
        
        #Exibe 
        print('Protocol: %s %s -> %s'%(ip_header.protocol, ip_header.src_address, ip_header.dst_address))
        
# Trata o CTRL+C
except KeyboardInterrupt:
    
    # Se estiver usando o windows desabilita o modo promíscuo
    if os.name == 'nt':
        sniffer.ioctl(socket.SIO_RECVALL, socket.RECVALL_ON)
    