# -*- coding: utf-8 -*-
"""
Created on Fri May 14 17:43:45 2021

@author: owner
"""

import socket
import threading
import struct

host = '127.0.0.1'
port = 1254

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

def job(socket):
    selfObject = "calculator" + '\n'
    socket.send(struct.pack("!H", len(selfObject)))
    socket.send(selfObject.encode())
    
    while(True):
        inputString = str(input('input send message')) + '\n'
        inputSize = len(inputString)
        if inputString is not None:
            print(inputString)
            socket.send(struct.pack("!H", inputSize))
            socket.send(inputString.encode())

sendThread = threading.Thread(target = job , args = (s,))
sendThread.start()
while(True):
    indata = s.recv(1024)
    if len(indata) == 0: # connection closed
        s.close()
        print('server closed connection.')
        break
    print('recv: ' + indata.decode())