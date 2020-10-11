#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Sep 24 19:00:04 2020

@author: joaquin
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thur Sep 24 19:00:04 2020

@author: joaquin
"""

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

while True:
    sock,addr = lsock.accept()
    print('connection recieved from: ', addr)
    
    rc = os.fork()
    
    #error fork - failure
    if rc<0:
        print('error fork')
        sys.exit(1)
        
    #child fork - sucess    
    elif rc == 0:
        
        #obtain fileName to write
        userFileName = framedSock.framedReceive(sock, debug)
        userFileName = userFileName.decode()
        
        if userFileName == 'exit':
            print('exit by client.... goodbye')
            sock.close()
            sys.exit(0)
        
        elif os.path.exists(userFileName ):
            print('\npath exists...')
            print('From Client obtaining: ', userFileName )
            payload = framedSock.framedReceive(sock, debug).decode() #obtain payload

            if debug:
                print('rec\'d: ', payload)
    
            
            with open(DIR + userFileName, 'w') as wFile:
                wFile.write(payload)
            
            print('done transfering file...')
            print('Sucess, payload recieved from: ', userFileName, '\n')
            framedSock.framedSend(sock, userFileName.encode(), debug)
            print('sending to client done message')
            
        else:
            print('From client: ',userFileName, ' -> path doesnt exist, client needs to try again')
            sys.exit(0)
          
        print('closing system')
        sock.close()
        sys.exit(0)
    
    #parent fork - sucess
    else:
        #print('parent fork')
        #os.wait() #needed???
        pass
    
    
    
    

