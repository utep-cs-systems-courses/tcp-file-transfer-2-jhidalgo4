#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Sep 24 19:00:04 2020

@author: joaquin
"""
import socket

ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ls.bind(('',50001)) #bind the specific port to the OS

ls.listen(1) #listen mode - to 1 port

convoS, addr = ls.accept() #this accepts connection

with open ('recievedFile.txt', 'w') as writeFile:
    transWord = convoS.recv(1024).decode()
    for l in transWord:
        writeFile.write(l)
        
print('end of fileServer.py')
convoS.close()
    


