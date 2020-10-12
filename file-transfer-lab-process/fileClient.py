#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 17:54:59 2020

@author: joaquin
"""
import socket, sys, re, os
sys.path.append("../lib")
import params
sys.path.append("../framed-echo")

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
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


#Create Socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if s is None:
    print('Could not open socket... exit')
    sys.exit(1)
s.connect(serverPortAddr)

while True:
    #Obtain user input
    fileToSend = input('Enter the name of file you would like to send (or exit) ')
    fileToSend = fileToSend.strip()
    
    if fileToSend == 'exit':
        print('exiting... goodbye')
        s.sendall("exit".encode() )
        sys.exit(0)
    
    #Check if file exists
    if os.path.exists(fileToSend):
        print('\nPath exists: ', fileToSend)
        #send file name
        s.sendall(fileToSend.encode() )
            #Open file, begin to send bytes
        with open(fileToSend, 'r') as contentPayload:
            print('opening: ', fileToSend)
            msg=contentPayload.read()
            if len(msg) == 0:
                print('empty File')
            else:
                print('Beginning to send: ', fileToSend)
                #framedSock.framedSend(s, msg, debug)
                s.sendall(msg.encode() )
        print('From server: Status of writting message: ', s.recv(1024).decode(), '\n' )
        
    else:
        print(fileToSend,' --> filePath does not exist')
        s.sendall(fileToSend.encode() )
        sys.exit(1)
    

