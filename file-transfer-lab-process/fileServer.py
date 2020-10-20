#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
# Created on Thur Oct 02 12:20:25 2020
@author: joaquin
"""
import sys
sys.path.append("../lib")       # for params
import re, socket, params, os, threading

from threading import Thread
from encapFramedSock import EncapFramedSock

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
print("listening on:", bindAddr)

lock = threading.Lock()

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
    def run(self):
        print("new thread handling connection from", self.addr)
        while True:
            #Recieve
            payload = self.fsock.receive(debug)
            if debug: print(f"thread connected to ((addr var goes here!))done")
            if not payload:     # done
                self.fsock.close()
                return          # exit
            
            #Decode and echo
            status = payload
            payload = payload.decode()
            
            #exit
            if 'exit' in payload:
                sys.exit(0)
            
            #write payload
            if os.path.exists(payload):
                lock.acquire()
                print('\nlocking to write this file: ', payload )
                print('writing to file..')
                
                with open(payload, 'rb') as fContext:
                    readData = fContext.read()
                
                with open(DIR+payload, 'wb') as wFile:
                    wFile.write(readData)
                
                #Send
                self.fsock.send(b'DONE', debug)
                print('about to unlock..')
                lock.release()
                print('Done writing to: ', payload , '\n')
            else:
                self.fsock.send(b'File does not exist, try again', debug)
            
        

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()



