#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 08:03:01 2019

@author: max
"""

import os

def run(**args):
    
    print('[*] In environment module')
    return str(os.environ)