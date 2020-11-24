#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Oct 02 12:01:25 2020
@author: joaquin
"""

import socket, sys, re

sys.path.append("../lib")       # for params
import params

from encapFramedSock import EncapFramedSock

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

sock = socket.socket(addrFamily, socktype)

if sock is None:
    print('could not open socket')
    sys.exit(1)

sock.connect(addrPort)

fsock = EncapFramedSock((sock, addrPort))

while True:
    #User Input
    userInput = input('Enter here$ ')
    #exit
    if userInput == 'exit':
        print('exit, goodbye...')
        fsock.send( bytes('exit', encoding='utf-8'), debug)
        sys.exit(0)
    #Transfer
    print('Sending to client: ',userInput)
    fsock.send( bytes(userInput, encoding='utf-8'), debug)
    
    #Status recieved
    status = fsock.receive(debug).decode()
    print("Status from Server: ", status , '\n')

