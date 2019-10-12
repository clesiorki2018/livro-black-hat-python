#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 14:29:18 2019

@author: max
"""

import ctypes
import random
import time
import sys

user32          = ctypes.windll.user32
kernel32        = ctypes.windll.kernel32
keystrokes      = 0
mouse_clicks    = 0
double_clicks   = 0


class LASTINPUTINFO(ctypes.Structure):
    __fields_ = [
            ('cbSize', ctypes.c_uint),
            ('dwTime', ctypes.c_uint32)
            ]


def get_last_input():
    struct_lastinputinfo = LASTINPUTINFO()
    struct_lastinputinfo.cbSize = ctypes.sizeof(LASTINPUTINFO)
    struct_lastinputinfo.dwTime = 0
    
    # Obtém a última entrada registrada
    user32.GetLastInputInfo(ctypes.byref(struct_lastinputinfo))
    
    # Agora determina há quanto tempo o computador está executando
    run_time = kernel32.GetTickCount()
    
    elapsed = run_time - struct_lastinputinfo.dwTime
    
    print('[*] Its been %d millisecounds since the last input event.'%elapsed)
    
    return elapsed


'''
while 1:
    get_last_input()
    time.sleep(1)
    
'''

def get_key_press():
    
    global keystrokes
    global mouse_clicks
    for i in range(0, 0xff):
        if user32.GetAsyncKeyState(i) == -32767:
            
        
            # 0x1 é o código para um clique do botão esquerdo do mouse
            if i == 0x1:
                mouse_clicks += 1
                return time.time()
            elif i > 32 and i < 127:
                keystrokes += 1
    return None


def detect_sandbox():
    
    global mouse_clicks
    global keystrokes
    
    max_keystrokes = random.randint(10, 25)
    max_mouse_clicks = random.randint(5, 25)
    
    double_clicks = 0
    max_double_clicks = 10
    double_click_threshold = 0.250 # em segundos
    first_double_click = None
    
    average_mousetime = 0
    max_input_threshold = 30000 # em milisegundos
    previous_timestamp = None
    detection_complete = False
    
    last_input = get_last_input()
    
    # Se nosso limite for atingido, salvamos
    if last_input == max_input_threshold:
        sys.exit(0)
    
    while not detection_complete:
        
        keypress_time = get_key_press()
        
        if keypress_time is not None and previous_timestamp is not None:
            
            # Calcula o periodo de tempo entre cliques
            elapsed = keypress_time - previous_timestamp
            
            # O usuario deu um clique duplo
            if elapsed <= double_click_threshold:
                double_clicks += 1
                
                if first_double_click is None:
                    
                    
                    # Obtém o timestamp do primeiro clique duplo
                    first_double_click = time.time()
                
                else:
                    if double_clicks == max_double_clicks:
                        if keypress_time - first_double_click <= (max_double_clicks * double_click_threshold):
                            sys.exit(0)
                        
            # Estamos satifeitos com o fato de haver entradas suficientes do usuário
            if keystrokes >= max_keystrokes and double_clicks >= max_double_clicks and mouse_clicks >= max_mouse_clicks:
                return
            
            previous_timestamp = keypress_time
            
        elif keypress_time is not None:
            previous_timestamp = keypress_time
            
detect_sandbox()
print('We are ok!')