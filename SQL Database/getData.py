# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 15:55:24 2021

@author: owner
"""
import socket
import threading
import struct
import json
import  pymysql 

host = '127.0.0.1'
port = 1278
user = 'root'
password = 'root'
db = 'sys'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
"""
def connectToData():
    json
"""
def job(socket):
    #tell server it is db connector
    firstInit = dict()
    firstInit.setdefault("component", "databaseConnector")
    print(firstInit)
    firstInit = str(firstInit) + "\n"
    
    socket.send(bytes(firstInit, encoding = "utf8"))
    
    #init conn
    conn = pymysql.connect(
        host = '127.0.0.1', user = 'root', passwd = 'root', db = 'sys'
        )
    cur  =  conn.cursor()
    
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
