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

def insertGameData(insertName):
    conn = pymysql.connect(
        host = host, user = user, passwd = password, db = db
        )
    cur  =  conn.cursor()
    Sql = ("INSERT INTO sys.game_data (`score`, `name`) VALUES (0, '%d')", insertName)
    cur.execute(Sql)
    cur.close()
    
def getScoreById(gdid):
    conn = pymysql.connect(
        host = host, user = user, passwd = password, db = db
        )
    cur  =  conn.cursor()
    Sql = "SELECT `score` FROM sys.game_data WHERE `id` = %d" %(gdid)
    cur.execute(Sql)
    userScore = cur.fetchall()[0][0]
    cur.close()
    
    return userScore
    
def getIdByName(userName):
    conn = pymysql.connect(
        host = host, user = user, passwd = password, db = db
        )
    cur  =  conn.cursor()
    Sql = "SELECT `id` FROM sys.game_data WHERE `name` = '%s'" %(userName)
    cur.execute(Sql)
    gdId = cur.fetchall()[0][0]
    cur.close()

    return gdId

def job(socket):
    #tell server it is db connector
    firstInit = dict()
    firstInit.setdefault("component", "databaseConnector")
    print(firstInit)
    firstInit = str(firstInit) + "\n"
    
    socket.send(bytes(firstInit, encoding = "utf8"))
    
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
    
    
    

