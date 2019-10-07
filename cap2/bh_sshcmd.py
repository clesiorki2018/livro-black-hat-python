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
    ssh_sesssion = client.get_transport().open_session()
    if ssh_sesssion.active:
        ssh_sesssion.exec_command(command)
        print(ssh_sesssion.recv(1024).decode('UTF-8'))
    return

ssh_command('192.168.0.9', 'max', 'lua123', 'ls')