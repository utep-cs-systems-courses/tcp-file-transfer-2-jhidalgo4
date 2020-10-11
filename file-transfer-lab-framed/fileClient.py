#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Sep 24 19:02:15 2020

@author: joaquin
"""

import socket, sys, re, os
sys.path.append("../lib")
import params
sys.path.append("../framed-echo")
import framedSock

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50000"),
    (('-d', 'debug'), "debug", False),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

paramMap = params.parseParams(switchesVarDefaults)
server, usage, debug = paramMap["server"],paramMap["usage"],paramMap["debug"]

if usage:
    params.usage()
    
#split/parse switchesVarDefaults
try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print('unable to parse "server" arg... exit')
    sys.exit(1)
serverPortAddr = (serverHost, serverPort)

#Obtain user input
fileToSend = input('Enter the name of file you would like to send (or exit) ')
fileToSend = fileToSend.strip()

#Create Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if s is None:
    print('Could not open socket... exit')
    sys.exit(1)
    
s.connect(serverPortAddr)

while True:
    if fileToSend == 'exit':
        print('exiting... goodbye')
        framedSock.framedSend(s, "exit".encode(), debug)
        sys.exit(0)
    
    #Check if file exists
    if os.path.exists(fileToSend):
        print('\nPath exists: ', fileToSend)
        #send file name
        framedSock.framedSend(s, bytes(fileToSend, encoding='utf-8'), debug) 
        
        #Open file, begin to send bytes
        with open(fileToSend, 'r') as contentPayload:
            print('opening: ', fileToSend)
            msg=contentPayload.read()
            if len(msg) == 0:
                print('empty File')
                sys.exit(1)
            
            print('Beginning to send: ', fileToSend)
            framedSock.framedSend(s, msg.encode(), debug)
            
        print('\nFrom Server: done writing to, ', framedSock.framedReceive(s, debug).decode(), '\n' )  
        print('closing system')
        s.close()
        sys.exit(0)

    else:
        print(fileToSend,' --> filePath does not exist')
        framedSock.framedSend(s, 'exit'.encode(), debug)
        print('closing system')
        s.close()
        sys.exit(1)
        


