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
db = 'fly_in_nature'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
"""
def connectToData():
    json
"""
class GetSqlData:
    
    def insertGameData(self, insertName):
        global host
        global user
        global password
        global db
        conn = pymysql.connect(
            host = host, user = user, passwd = password, db = db
            )
        cur  =  conn.cursor()
        Sql = ("INSERT INTO fly_in_nature.game_data (`money`, `name`) VALUES (0, '%d')", insertName)
        cur.execute(Sql)
        cur.close()
        conn.close()
        
    def getScoreById(self, gdid):
        global host
        global user
        global password
        global db
        conn = pymysql.connect(
            host = host, user = user, passwd = password, db = db
            )
        cur  =  conn.cursor()
        Sql = "SELECT `money` FROM fly_in_nature.game_data WHERE `id` = %d" %(gdid)
        cur.execute(Sql)
        userScore = cur.fetchall()[0][0]
        cur.close()
        conn.close()
        return userScore
        
    def getIdByName(self, userName):
        global host
        global user
        global password
        global db
        conn = pymysql.connect(
            host = host, user = user, passwd = password, db = db
            )
        cur = conn.cursor()
        Sql = "SELECT `id` FROM fly_in_nature.game_data WHERE `name` = '%s'" %(userName)
        cur.execute(Sql)
        try :
            gdId = cur.fetchall()[0][0]
        except IndexError:
            gdId = -1
        finally:
            cur.close()
            conn.close()
        return gdId
    
    def getMinTimeRecordByPlayerIdAndMap(self, playerId, mapId):
        global host
        global user
        global password
        global db
        conn = pymysql.connect(
            host = host, user = user, passwd = password, db = db
            )
        cur = conn.cursor()
        Sql = "SELECT min(`time`) FROM fly_in_nature.race_record WHERE `playerId` = %d AND `map` = %d" %(playerId, mapId)
        cur.execute(Sql)
        timeRecord = cur.fetchall()[0][0]
        cur.close()
        conn.close()
        return timeRecord
    
class StoreNewData:
    
    def storeNewUser(self, playerName):
        global host
        global user
        global password
        global db
        conn = pymysql.connect(
            host = host, user = user, passwd = password, db = db
            )
        cur = conn.cursor()
        Sql = "INSERT INTO fly_in_nature.game_data (`money`, `name`) VALUES (0, '%s')" %(playerName)
        cur.execute(Sql)
        cur.close()
        conn.close()


def job(socket):
    #tell server it is db connector
    firstInit = dict()
    firstInit.setdefault('component', 'databaseConnector')
    print(firstInit)
    firstInit = str(firstInit).replace("\'", "\"") + "\n"
    
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
getData = GetSqlData()
insertData = StoreNewData()
while(True):
    indata = str(s.recv(1024), encoding = 'utf-8')
    if len(indata) == 0: # connection closed
        s.close()
        print('server closed connection.')
        break
    print('recv: ' + indata)
    array = json.loads(indata)
    resultSend = dict()
    if(array['purpose'] == 'getPlayerId'):
        result = getData.getIdByName(array['parameter'])
        resultSend.setdefault('sendTo', 'player')
        resultSend.setdefault('result', result)
    
    elif(array['purpose'] == 'newUser'):
        insertData.storeNewUser(array['newUserName'])
        resultSend.setdefault('sendTo', 'player')
        resultSend.setdefault('result', 'success')
    
    print(resultSend)
    resultSend = str(resultSend).replace("\'", "\"")  + "\n"
    
    s.send(bytes(resultSend, encoding = "utf8"))
        

