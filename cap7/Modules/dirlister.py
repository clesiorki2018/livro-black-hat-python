#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 19:46:57 2019

@author: max
"""

import os

def run(**args):
     
    print('[*] In dirlister module')
    buffer = return os.listdir('.')
    return str(buffer)