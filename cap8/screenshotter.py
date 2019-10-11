#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 19:26:06 2019

@author: max
"""

import win32gui
import win32ui
import win32con
import win32api

# Obtém um handle para a janela principal do desktop
hdesktop = win32gui.GetDesktopWindow()

# Determina o tamanho de todos os monitores em pixels
width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

# Cria um contexto de dispositivo
desktop_dc = win32gui.GetWindowDC(hdesktop)
img_dc = win32ui.CreateDCFromHandle(desktop_dc)

# Cria um contexto de dispositivo na memória
mem_dc = img_dc.CreateCompatibleDC()

# Cria um objeto bitmap
screenshot = win32ui.CreateBitmap()
screenshot.CreateCompatibleBitmap(img_dc, width, height)
mem_dc.SelectObject(screenshot)

# Copia a tela para o nosso contexto de dispositivo em memória
mem_dc.BitBlt((0,0), (width, height), img_dc, (left, top), win32con.SRCCOPY)

# Salva o bitmap em um arquivo
screenshot.SaveBitmapFile(mem_dc, 'c:\\screenshot.bmp')

# Remove nossos objetos
mem_dc.DeleteDC()
win32gui.DeleteObject(screenshot.GetHandle())