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
filesInUse = dict()
        
class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)
        
    def writeFile(self, fName):
        filesInUse.update( {fName:'True'} ) #mark as now in use, do not touch while in use
        lock.acquire()
        with open(fName, 'rb') as fContext:
            readData = fContext.read()
        with open(DIR+fName, 'wb') as wFile:
            wFile.write(readData)
        lock.release()
        filesInUse.update( {fName:'False'} ) #make open for use
        
        
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
                #Check to see if in use
                if filesInUse.get(payload) == None or filesInUse.get(payload) == 'False':
                    #pass in the file name
                    self.writeFile(payload)
                    
                    #Sent
                    self.fsock.send(b'DONE', debug)
                    print('Done writing to: ', payload , '\n')
                    
                else:
                    self.fsock.send(b'File In use, try again', debug)
            else:
                self.fsock.send(b'File does not exist, try again', debug)

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()


