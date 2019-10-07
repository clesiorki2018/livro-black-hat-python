#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 11:05:48 2019

@author: max
"""

import sys
import socket
import threading

# Esta é uma boa função de dumping de valores hexa diretamente obtida dos comentários em:
# http://code.activestate.com/recipes/142812-hex-dumper
def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    
    for i in range(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(['%0*X'%(digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append(b'%04X %-*s %s'%(i, length*(digits+1), hexa, text))
        
    print(b'\n'.join(result))
    
def receive_from(connection):
    buffer = ''
    
    # Definimos um timeeout de 2 segundos; de acordo com
    # seu alvo, pode ser que  esse valor precise ser ajustado
    connection.timeout(2)
    try:
        
        # continua lendo em buffer até 
        # que não haja maiss dados
        # ou  a temporização exxpire
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass
    
    return buffer

# Modifica qualquer solicitaação destinada ao host remoto
def request_handler(buffer):
    
    # Faz modificações no pacote
    return buffer

# Modifica qualquerr resposta ao host local
def response_handler(buffer):
    
    #faz modificações no pacote
    return buffer


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except:
        print('[!!] Failed to listen on %s:%d'%(local_host, local_port))
        print('[!!] Check for other listening sockets or correct permissions.')
        sys.exit(0)
    
    print('[*] Listening on %s:%d'%(local_host, local_port))
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        
        # Exibe informações sobre a conexão local
        print('[==>] Received incomming connection from %s:%d'%(addr[0], addr[1]))
        
        # Inicia uma thread para conversar com host remoto
        proxy_thread  = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()
     
def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    
    # Conecta-se ao host remoto
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    
    # Receebe dados do lado remoto se for necessário
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        
        # Envia os dados ao nosso handler de resposta
        remote_buffer = response_handler(remote_buffer)
        
        # Se houver dados para serem enviados ao nosso cliente local, envia-os
        if len(remote_buffer):
            print('[<==] Sending %d bytes to localhost.'%len(remote_buffer))
            client_socket.send(remote_buffer)
            
    # Agora vamos entrar no laço e ler do buffer local,
    # Enviar  para o host remoto, enviar para o host loca,
    # Enchaguar, lavar e repetir
    while True:
        
        # Lê do host local
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print('[==>] received %d bytesfrom localhost.'%len(local_buffer))
            hexdump(local_buffer)
            
            # Envia os dados para o nosso handler de solicitações
            local_buffer = request_handler(local_buffer)
            
            # Envia os dados ao host remoto
            remote_socket.send(local_buffer)
            print('[==>] Send to remote')
            
        # Recebe a resposta
        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print('[<==] Received %d bytes from remote.'%len(remote_buffer))
            hexdump(remote_buffer)
            
            # Envia os dados ao nosso handler de resposta
            remote_buffer = response_handler(remote_buffer)
            
            # Envia a resposta para o socket local
            client_socket.send(remote_buffer)
            print('[<==] Send to localhost.')
            
        # Se não houver mais dados em nenhum dos lados, encerra as conexões
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print('[*] No more data. Closing connections.')
            break
        
def main():
    
    # Sem arsing sofisticado da linha de comando como neste caso
    if(len(sys.argv[1:]) != 5):
        print('Usage: ./%s [localhost] [localport] [remotehost] [remoteport] [receive_first]'%sys.argv[0])
        print('Example: ./%s 127.0.0.1 9000 10.12.132.1 9000 true'%sys.argv[0])
        sys.exit(0)
        
    # Define parametros para ouvir localmente
    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    
    # Define o alvo remoto
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    
    # O código a seguir diz ao nosso proxy para enviar e receber dados
    # antes de enviar ao host remoto
    receive_first = sys.argv[5]
    if 'true' in receive_first:
        receive_first = True
    else:
        receive_first = False
        
    # Agora coloca em ação o nosso proxy que ficará ouvindo
    server_loop(local_host, local_port, remote_host, remote_port, receive_first)
    
main()