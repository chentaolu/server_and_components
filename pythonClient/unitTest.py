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
            
        elif (apiNumber == 4):
            
            fakeAPI = dict()
            fakeAPI.setdefault('sendTo', 'databaseConnector')
            fakeAPI.setdefault('purpose', 'getGameRecords')
            fakeAPI.setdefault('playerId', 2)
            fakeAPI = str(fakeAPI).replace("\'", "\"") + "\n"
            socket.send(bytes(fakeAPI, encoding = "utf8"))
            
        elif (apiNumber == 5):
            
            fakeAPI = dict()
            fakeAPI.setdefault('sendTo', 'database4Connector')
            fakeAPI.setdefault('purpose', 'storeGameRecord')
            fakeAPI.setdefault('playerId', 2)
            fakeAPI.setdefault('mapId', 1)
            fakeAPI.setdefault('time', '00:00:40.71')
            fakeAPI = str(fakeAPI).replace("\'", "\"") + "\n"
            socket.send(bytes(fakeAPI, encoding = "utf8"))
            
        elif(apiNumber == 6):
            fakeAPI = dict()
            fakeAPI.setdefault('sendTo', 'calculator')
            fakeAPI.setdefault('speedChange', 'otherArduino')
            fanDetail = dict()
            fanDetail.setdefault('x', 2555.5)
            fanDetail.setdefault('y', 106.50)
            fanDetail.setdefault('z', 1455.4)
            fakeAPI.setdefault('fanLocation', fanDetail)
            playerDetail = dict()
            playerDetail.setdefault('x', 2568.04272)
            playerDetail.setdefault('y', 106.5)
            playerDetail.setdefault('z', 1468.662)
            fakeAPI.setdefault('playerLocation', playerDetail)
            quaternionsDetail = dict()
            quaternionsDetail.setdefault('x', 0.0)
            quaternionsDetail.setdefault('y', 0.845795035)
            quaternionsDetail.setdefault('z', 0.0)
            quaternionsDetail.setdefault('w', -0.533508062)
            fakeAPI.setdefault('Quaternions', quaternionsDetail)
            print(fakeAPI)
            fakeAPI = str(fakeAPI).replace("\'", "\"") + "\n"
            socket.send(bytes(fakeAPI, encoding = "utf8"))
            
        elif(apiNumber == 7):
            fakeAPI = dict()
            fakeAPI.setdefault('sendTo', 'leftArduino')
            fakeAPI.setdefault('fanSpeed', 70)
            fakeAPI.setdefault('verticalMove', 1)
            fakeAPI.setdefault('parallelMove', 1)
            fakeAPI.setdefault('waterSpary', -1)
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