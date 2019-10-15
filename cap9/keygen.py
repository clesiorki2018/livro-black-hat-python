#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 10:13:15 2019

@author: max
"""

from Crypto.PublicKey import RSA
new_key = RSA.generate(2048, e=65537)
public_key = new_key.publickey('PEM')
private_key = new_key.exportKey('PEM')

print(public_key)
print(private_key)