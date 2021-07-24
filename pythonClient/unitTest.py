# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 20:25:23 2021

@author: owner
"""

import socket
import threading
import time

host = '127.0.0.1'
port = 1278

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

def job(socket):
    #tell server it is db connector
    firstInit = dict()
    firstInit.setdefault('component', 'player')
    print(firstInit)
    firstInit = str(firstInit) + "\n"
    
    socket.send(bytes(firstInit, encoding = "utf8"))
    
    time.sleep(1)
    """
    fakeAPI = dict()
    name = 'TEST_GAME_SQL4'
    fakeAPI.setdefault('sendTo', 'databaseConnector')
    fakeAPI.setdefault('purpose', 'getPlayerId')
    fakeAPI.setdefault('parameter', name)
    fakeAPI = str(fakeAPI).replace("\'", "\"") + "\n"
    
    socket.send(bytes(fakeAPI, encoding = "utf8"))
    """
    fakeAPI = dict()
    fakeAPI.setdefault('sendTo', 'centerArduino')
    fakeAPI.setdefault('fanSpeed', 456789);
    fakeAPI = str(fakeAPI).replace("\'", "\"") + "\n"
    socket.send(bytes(fakeAPI, encoding = "utf8"))
    

sendThread = threading.Thread(target = job , args = (s,))
sendThread.start()
while(True):
    indata = str(s.recv(1024), encoding = 'utf-8')
    if len(indata) == 0: # connection closed
        s.close()
        print('server closed connection.')
        break
    print('recv: ' + indata)