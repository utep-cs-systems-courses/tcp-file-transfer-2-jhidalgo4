# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# """
# Created on Thur Oct 02 12:01:25 2020
# @author: joaquin
# """

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
    userInput = input('Enter here-->:')
    #exit
    if userInput == 'exit':
        print('exit, goodbye...')
        fsock.send( bytes('exit', encoding='utf-8'), debug)
        sys.exit(0)
    #Transfer
    print(userInput)
    fsock.send( bytes(userInput, encoding='utf-8'), debug)
    
    #Status recieved
    status = fsock.receive(debug).decode()
    print("Status from Server: ", status )












###############################3
# import socket, sys, re, os
# sys.path.append("../lib")
# import params
# sys.path.append("../framed-echo")
# import framedSock

# switchesVarDefaults = (
#     (('-s', '--server'), 'server', "127.0.0.1:50001"),
#     (('-d', '--debug'), "debug", False), # boolean (set if present)
#     (('-?', '--usage'), "usage", False), # boolean (set if present)
#     )

# progname = "framedClient"
# paramMap = params.parseParams(switchesVarDefaults)

# server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

# if usage:
#     params.usage()

# try:
#     serverHost, serverPort = re.split(":", server)
#     serverPort = int(serverPort)
#     proxySetting = input('run with proxy? ( y / n ) :')
#     if proxySetting == 'y':
#         serverPort = int(50000)
# except:
#     print("Can't parse server:port from '%s'" % server)
#     sys.exit(1)

# addrFamily = socket.AF_INET
# socktype = socket.SOCK_STREAM
# addrPort = (serverHost, serverPort)

# print('client\n')
# while True:
    
#     s = socket.socket(addrFamily, socktype)
#     if s is None:
#         print('could not open socket')
#         sys.exit(1)
#     s.connect(addrPort)
    
#     #input
#     cmmdLine = input('Enter (exit) or file name: ')
    
#     #Handle exit
#     if cmmdLine == 'exit':
#         print('exit, goodbye')
#         framedSock.framedSend(s, bytes('exit', encoding='utf-8'), debug) # send file name or 1st command
#         sys.exit(0)
    
#     #Send file name
#     print('sending to server: ', cmmdLine)
#     framedSock.framedSend(s, bytes(cmmdLine, encoding='utf-8'), debug) # send file name or 1st command 


#     #status
#     status = framedSock.framedReceive(s, debug).decode()
#     if status == 'exit':
#         sys.exit(0)
#     else:
#         print('\nStatus from server: ', status)
#         print('\n')
#         s.close()