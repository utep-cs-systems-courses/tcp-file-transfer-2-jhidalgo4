#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Sep 24 19:00:04 2020
@author: joaquin
"""

import socket, sys, re, os
sys.path.append("../lib")
import params
sys.path.append("../framed-echo")
import framedSock

DIR = './recieve/'

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print('SERVER\n')
print("listening on:", bindAddr)

while True:
    sock, addr = lsock.accept()

    if not os.fork():
        print("handling connection from: ", addr)
        
        print('waiting for input...\n')
        cmdLine = framedSock.framedReceive(sock, debug) #
        fileName = cmdLine.decode()
        
        if 'exit' in fileName:
            print('exiting goodbye')
            # framedSock.framedSend(sock, bytes('exit', encoding='utf-8'), debug) # send file name or 1st command 
            print('\n')
            sys.exit(0)
        
        else:
            
            if debug: print("rec'd: ", cmdLine)
            if not cmdLine:
                if debug: print("child exiting")
                sys.exit(0)
                
            #write payload
            if os.path.exists(fileName):
                print('obtained, writing to:', fileName )
                payload = ''
                
                with open(fileName, 'rb') as fContext:
                    payload = fContext.read()
                
                with open(DIR+fileName, 'wb') as wFile:
                    wFile.write(payload)
                
                
                print('Done writing to: ', cmdLine.decode() )
                framedSock.framedSend(sock, bytes('DONE WRITING', encoding='utf-8'), debug) # send file name or 1st command 
                print('\n')
                
            else:
                print('ERROR: couldnt find file: ', fileName)
                framedSock.framedSend(sock, bytes('ERROR \nFile doesnt exist', encoding='utf-8'), debug) #



