#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Sep 24 19:00:04 2020

@author: joaquin
"""
#SIMPLE VERSION
# import socket

# ls = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# ls.bind(('',50001)) #bind the specific port to the OS

# ls.listen(1) #listen mode - to 1 port

# convoS, addr = ls.accept() #this accepts connection

# with open ('recievedFile.txt', 'w') as writeFile:
#     transWord = convoS.recv(1024).decode()
#     for l in transWord:
#         writeFile.write(l)
        
# print('end of fileServer.py')
# convoS.close()


import sys, socket, os
sys.path.append("../lib")
import params
sys.path.append("../framed-echo")
import framedSock

host = "127.0.0.1"
DIR = './recieve/'

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', 'debug'), "debug", False),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

paramMap = params.parseParams(switchesVarDefaults)
listenPort, usage, debug = paramMap["listenPort"],paramMap["usage"],paramMap["debug"]

if usage:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = (host,listenPort)
lsock.bind(bindAddr)
lsock.listen()
print('listening on (host/port): ', bindAddr)

sock,addr = lsock.accept()
print('connection recieved from: ', addr)

while True:
    # if not os.fork():
        #obtain fileName to write
        #userFileName = framedSock.framedReceive(sock, debug)
        #userFileName = userFileName.decode()
        
    userInput = sock.recv(1024).decode()
    if os.path.exists(userInput):
        print('Obtaining: ', userInput)
        fileSize = int( os.stat(userInput).st_size )
        print('File Size: ', fileSize)
        
        payload = ''
        thisBuffSize = 0
        
        while True:
        #obtain file payload
        #payload = framedSock.framedReceive(sock, debug)
            temp = sock.recv(1024)
            thisBuffSize += len(temp)
            temp = temp.decode()
            payload += temp
            if debug:
                print('rec\'d: ', payload)
            if not temp:
                 break
            if fileSize == thisBuffSize:
                break
    
        with open(DIR + userInput, 'w') as wFile:
            wFile.write(payload)
                
        print('Sucess, payload recieved from: ', userInput, '\n')
        sock.sendall('done'.encode() )
        # sys.exit(1)
    elif userInput == 'exit':
        print('exit by client.... goodbye')
        sys.exit(0)
    else:
        print('From client: ',userInput, ' -> path doesnt exist, client needs to try again')
        # sys.exit(1)
        # continue
    


