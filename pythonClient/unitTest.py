# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 20:25:23 2021

@author: owner
"""

import socket
import threading
import time

host = '127.0.0.1'
port = 5678

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

def job(socket):
    #tell server it is db connector
    firstInit = dict()
    firstInit.setdefault('component', 'player')
    print(firstInit)
    firstInit = str(firstInit) + "\n"
    
    socket.send(bytes(firstInit, encoding = "utf8"))
    
    while (True) :
        apiNumber = int(input('input api number :'))
        # test get player id
        if (apiNumber == 0) :
            fakeAPI = dict()
            name = 'TEST_GAME_SQL4'
            fakeAPI.setdefault('sendTo', 'databaseConnector')
            fakeAPI.setdefault('purpose', 'getPlayerId')
            fakeAPI.setdefault('parameter', name)
            fakeAPI = str(fakeAPI).replace("\'", "\"") + "\n"
            
            socket.send(bytes(fakeAPI, encoding = "utf8"))
        
        # test android fan test
        elif (apiNumber == 1) :
            fanSpeed = int(input('input fanSpeed :'))
            parallelMove = int(input('input parallelMove :'))
            verticalMove = int(input('input verticalMove :'))
            waterSpary = int(input('input waterSpary :'))
            fakeAPI = dict()
            fakeAPI.setdefault('sendTo', 'centerArduino')
            fakeAPI.setdefault('fanSpeed', fanSpeed);
            fakeAPI.setdefault('parallelMove', parallelMove);
            fakeAPI.setdefault('verticalMove', verticalMove);
            fakeAPI.setdefault('waterSpary', waterSpary);
            fakeAPI = str(fakeAPI).replace("\'", "\"") + "\n"
            socket.send(bytes(fakeAPI, encoding = "utf8"))
            
        elif (apiNumber == 2):
            userName = str(input('input user name :'))
            fakeAPI = dict()
            fakeAPI.setdefault('sendTo', 'databaseConnector')
            fakeAPI.setdefault('purpose', 'registUser')
            fakeAPI.setdefault('userName', userName)
            fakeAPI = str(fakeAPI).replace("\'", "\"") + "\n"
            socket.send(bytes(fakeAPI, encoding = "utf8"))
            
        elif (apiNumber == 3):
            userName = str(input('input user name :'))
            fakeAPI = dict()
            fakeAPI.setdefault('sendTo', 'databaseConnector')
            fakeAPI.setdefault('purpose', 'login')
            fakeAPI.setdefault('userName', userName)
            fakeAPI = str(fakeAPI).replace("\'", "\"") + "\n"
            socket.send(bytes(fakeAPI, encoding = "utf8"))
            
        elif (apiNumber == 99) :
            socket.close()

sendThread = threading.Thread(target = job , args = (s,))
sendThread.start()
while(True):
    indata = str(s.recv(1024), encoding = 'utf-8')
    if len(indata) == 0: # connection closed
        s.close()
        sendThread.terminate()
        print('server closed connection.')
        break
    print('recv: ' + indata)