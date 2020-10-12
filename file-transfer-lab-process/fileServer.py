#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 18:26:20 2020

@author: joaquin
"""
import sys, socket, os
sys.path.append("../lib")
import params
sys.path.append("../framed-echo")
import threading

host = "127.0.0.1"
DIR = './recieve/'

switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', 'debug'), "debug", False),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

def sendMessage(sock, addr):
    print(f"connection {addr} connected")
    while True:
        userInput = sock.recv(1024).decode()
        if os.path.exists(userInput):
            print('Obtaining: ', userInput)
            fileSize = int( os.stat(userInput).st_size )
            print('File Size: ', fileSize)
            
            payload = ''
            thisBuffSize = 0
            
            while True:
                #obtain file payload
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
            break
            #sys.exit(0)
        elif userInput == 'exit':
            print('exit by client.... goodbye')
            sock.close()
            sys.exit(0)
        else:
            print('From client: ',userInput, ' -> path doesnt exist, client needs to try again')
            sock.close()
            sys.exit(1)
    print('closing...')
    sock.close()


def start(s):
    s.listen()
    print('listening on (host/port): ', bindAddr)
    while True:
        sock, addr = s.accept()
        print('connection recieved from: ', addr)
        
        thread = threading.Thread(target = sendMessage, args = (sock, addr) )
        thread.start()  #start thread
        #print(f"{threading.activeCount()-1 }" ) #prints how many active cliients

paramMap = params.parseParams(switchesVarDefaults)
listenPort, usage, debug = paramMap["listenPort"],paramMap["usage"],paramMap["debug"]

if usage:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = (host,listenPort)
lsock.bind(bindAddr)

start(lsock)


lsock.close()
sys.exit(0)




