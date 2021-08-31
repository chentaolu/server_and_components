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
port = 5678
user = 'root'
password = 'root'
db = 'fly_in_nature'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

class Broom:
    id = int()
    name = str()
    speed = int()
    price = int()
    def setId(self, id):
        self.id = id
        
    def setName(self, name):
        self.name = name
        
    def setSpeed(self, speed):
        self.speed = speed
        
    def setPrice(self, price):
        self.price = price
        
    def getId(self):
        return self.id
    
    def getName(self):
        return self.name
    
    def getSpeed(self):
        return self.speed
    
    def getPrice(self):
        return self.price
    

class GetSqlData:
    
    def checkNameExists(self, userName):
        global host
        global user
        global password
        global db
        conn = pymysql.connect(
            host = host, user = user, passwd = password, db = db
            )
        cur  =  conn.cursor()
        Sql = "SELECT case WHEN EXISTS ( \
                   SELECT 1 FROM fly_in_nature.game_data WHERE `name` = '%s' LIMIT 1 \
                ) THEN True ELSE False END" %(userName)
        cur.execute(Sql)
        isUserExists = bool(cur.fetchall()[0][0])
        cur.close()
        conn.close()
        return isUserExists
        
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
    
    def getBroomList(self):
        global host
        global user
        global password
        global db
        conn = pymysql.connect(
            host = host, user = user, passwd = password, db = db
            )
        cur = conn.cursor()
        Sql = "SELECT * FROM fly_in_nature.broom"
        cur.execute(Sql)
        broomDataList = cur.fetchall()
        
        broomList = list()
        for broomData in broomDataList:
            broom = Broom()
            broom.setId(broomData[0])
            broom.setName(broomData[1])
            broom.setSpeed(broomData[2])
            broom.setPrice(broomData[3])
            broomList.append(broom)
        
        cur.close()
        conn.close()
        return broomList
    
    def getPurchaseRecord(self, playerId):
        global host
        global user
        global password
        global db
        conn = pymysql.connect(
            host = host, user = user, passwd = password, db = db
            )
        cur = conn.cursor()
        Sql = "SELECT * FROM fly_in_nature.purchase_record WHERE `playerId` = %d" %(playerId)
        cur.execute(Sql)
        broomDataList = cur.fetchall()
        
        broomList = list()
        for broomData in broomDataList:
            broom = Broom()
            broom.setId(broomData[0])
            broom.setName(broomData[1])
            broom.setSpeed(broomData[2])
            broom.setPrice(broomData[3])
            broomList.append(broom)
        
        cur.close()
        conn.close()
        return broomList
    
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
        conn.commit()
        cur.close()
        conn.close()
        
    def createNewPurchaseRecord(self, playerId, broomList):
        global host
        global user
        global password
        global db
        conn = pymysql.connect(
            host = host, user = user, passwd = password, db = db
            )
        cur = conn.cursor()
        for broom in broomList:
            
            if(broom.getId() == 1) :
                Sql = "INSERT INTO fly_in_nature.purchase_record (`playerId`, `broomId`, `purchase`) VALUES (%d, %d, %d)" %(playerId, broom.getId(), 1)
                
            else :
                Sql = "INSERT INTO fly_in_nature.purchase_record (`playerId`, `broomId`, `purchase`) VALUES (%d, %d, %d)" %(playerId, broom.getId(), 0)
                
            cur.execute(Sql)
            conn.commit()
        
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
        inputString = str(input('input send message'))
        if inputString == 'q':
            print("quit")
            socket.close()

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
    
    elif(array['purpose'] == 'registUser'):
        if(getData.checkNameExists(array['userName'])) :
            resultSend.setdefault('sendTo', 'player')
            resultSend.setdefault('result', 'failure')
        else :
            insertData.storeNewUser(array['userName'])
            playerId = getData.getIdByName(array['userName'])
            print(playerId)
            broomList = getData.getBroomList()
            insertData.createNewPurchaseRecord(playerId, broomList)
            resultSend.setdefault('sendTo', 'player')
            resultSend.setdefault('result', 'success')
    
    elif(array['purpose'] == 'login'):
        if(getData.checkNameExists(array['userName'])) :
            resultSend.setdefault('sendTo', 'player')
            resultSend.setdefault('login', 'success')
        else:
            resultSend.setdefault('sendTo', 'player')
            resultSend.setdefault('login', 'failure')    
    
    print(resultSend)
    resultSend = str(resultSend).replace("\'", "\"")  + "\n"
    
    s.send(bytes(resultSend, encoding = "utf8"))
        

