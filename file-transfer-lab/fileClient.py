#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Sep 24 19:02:15 2020

@author: joaquin
"""
import socket

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(("127.0.0.1", 50001)) # connect to my computer (client)

#Read file
with open ('fileSend.txt', 'r') as inputFile:
    fileTrans = inputFile.read()
    cs.send(fileTrans.encode() )
    

print('end of fileClient.py')
cs.close()
    
