# -*- coding: utf-8 -*-
"""
Created on Fri May 14 17:43:45 2021

@author: owner
"""

import socket
import threading
import json
import numpy as np
from scipy.spatial.transform import Rotation as R
from numba import jit

import time


host = '127.0.0.1'
port = 5678

class Queue:
    datas = list()
    
    def Push(self, data):
        self.datas.append(data)
        
    def Pop(self):
        return self.datas.pop(0)

    def IsEmpty(self):
        if(len(self.datas) != 0):
            return False
        else:
            return True
        
class FanDetail:
    hasData = False
    inputTime = time.time()
    fanSpeed = int()
    whichFan = str()
    verticalMove = int()
    parallelMove = int()
    
    def __init__(self, whichFan):
        self.whichFan = whichFan
    
    def needToChange(self, newSpeed, newVerticalMove, newParallelMove, currentTime):
        if(newVerticalMove == self.verticalMove and newParallelMove == self.parallelMove and newSpeed == self.fanSpeed) :
            self.inputTime = currentTime
            return False
        
        if(newVerticalMove != self.verticalMove or newParallelMove != self.parallelMove) :
            self.inputTime = currentTime
            self.fanSpeed = newSpeed
            self.verticalMove = newVerticalMove
            self.parallelMove = newParallelMove
            
            return True
        else :
            if(newSpeed <= self.fanSpeed) :
                self.inputTime = currentTime
                self.fanSpeed = newSpeed
                self.verticalMove = newVerticalMove
                self.parallelMove = newParallelMove
                
                return True
            else :
                return False
    def makeRecoverDict(self) :
        result = dict()
        result.setdefault('sendTo', self.whichFan)
        result.setdefault('fanSpeed', 0)
        result.setdefault('verticalMove', 0)
        result.setdefault('parallelMove', 0)
        result.setdefault('waterSpary', -1)
        return result
        
@jit(nopython=True)
def calculateLength(x, y, z):
    return ((x * x) + (y * y) + (z * z)) ** (1 / 2)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

dataQueue = Queue()
leftFan = FanDetail('leftArduino')
rightFan = FanDetail('rightArduino')
topFan = FanDetail('topArduino')
downFan = FanDetail('downArduino')

def getLeftLocation(playerToFanVector):
    
    OriginPoint = np.array([-30, 28, 30])

    NomalVextor = np.array([1, 0, -1])
    
    Constant = (NomalVextor[0] * OriginPoint[0] + NomalVextor[1] * OriginPoint[1] + NomalVextor[2] * OriginPoint[2]) * -1
    
    multiple = -1 * Constant / (NomalVextor[0] * playerToFanVector[0] + NomalVextor[1] * playerToFanVector[1] + NomalVextor[2] * playerToFanVector[2])
    
    playerToFanVectorWithMult = playerToFanVector * multiple
    
    playerToFanRealLocationIn3D = playerToFanVectorWithMult
    
    leftBasis = np.array([[1 / 1.414, 0, 1 / 1.414], [0, 1, 0]])

    moveFan = leftBasis.dot(playerToFanRealLocationIn3D.T)
    
    return moveFan

def getRightLocation(playerToFanVector):
    
    OriginPoint = np.array([30, 28, 30])

    NomalVextor = np.array([1, 0, 1])
    
    Constant = (NomalVextor[0] * OriginPoint[0] + NomalVextor[1] * OriginPoint[1] + NomalVextor[2] * OriginPoint[2]) * -1
    
    multiple = -1 * Constant / (NomalVextor[0] * playerToFanVector[0] + NomalVextor[1] * playerToFanVector[1] + NomalVextor[2] * playerToFanVector[2])
    
    playerToFanVectorWithMult = playerToFanVector * multiple
    
    playerToFanRealLocationIn3D = playerToFanVectorWithMult
    
    leftBasis = np.array([[1 / 1.414, 0, -1 / 1.414], [0, 1, 0]])

    moveFan = leftBasis.dot(playerToFanRealLocationIn3D.T)
    
    return moveFan

def getTopLocation(playerToFanVector):
    
    OriginPoint = np.array([0, 28, 30])

    NomalVextor = np.array([0, 1, 1])
    
    Constant = (NomalVextor[0] * OriginPoint[0] + NomalVextor[1] * OriginPoint[1] + NomalVextor[2] * OriginPoint[2]) * -1
    
    multiple = -1 * Constant / (NomalVextor[0] * playerToFanVector[0] + NomalVextor[1] * playerToFanVector[1] + NomalVextor[2] * playerToFanVector[2])
    
    playerToFanVectorWithMult = playerToFanVector * multiple
    
    playerToFanRealLocationIn3D = playerToFanVectorWithMult
    
    leftBasis = np.array([[1, 0, 0], [0, 1 / 1.414, -1 / 1.414]])

    moveFan = leftBasis.dot(playerToFanRealLocationIn3D.T)
    
    return moveFan

def getDownLocation(playerToFanVector):
    
    leftOriginPoint = np.array([0, -47, 30])

    leftNomalVextor = np.array([0, 1, -1])
    
    leftConstant = (leftNomalVextor[0] * leftOriginPoint[0] + leftNomalVextor[1] * leftOriginPoint[1] + leftNomalVextor[2] * leftOriginPoint[2]) * -1
    
    multiple = -1 * leftConstant / (leftNomalVextor[0] * playerToFanVector[0] + leftNomalVextor[1] * playerToFanVector[1] + leftNomalVextor[2] * playerToFanVector[2])
    
    playerToFanVectorWithMult = playerToFanVector * multiple
    
    playerToFanRealLocationIn3D = playerToFanVectorWithMult
    
    leftBasis = np.array([[1, 0, 0], [0, 1 / 1.414, 1 / 1.414]])

    moveFan = leftBasis.dot(playerToFanRealLocationIn3D.T)
    
    return moveFan


def job(socket):
    firstInit = dict()
    firstInit.setdefault('component', 'calculator')
    print(firstInit)
    firstInit = str(firstInit).replace("\'", "\"") + "\n"
    socket.send(bytes(firstInit, encoding = "utf8"))
    originSpeed = -1
    while(True):
        if(not dataQueue.IsEmpty()):
            result = dict()
            currentData = dataQueue.Pop()
            print(currentData)
            if(currentData['speedChange'] == 'centerArduino') :
            
                if (originSpeed == -1) :
                    fanSpeed = int(currentData['CurrentSpeed']) // 10
                    
                    result.setdefault('sendTo', currentData['speedChange'])
                    result.setdefault('fanSpeed', fanSpeed)
                    
                    result = str(result).replace("\'", "\"") + "\n"
                    socket.send(bytes(result, encoding = "utf8"))
                    originSpeed = fanSpeed
                    
                else :
                    fanSpeed = int(currentData['CurrentSpeed']) // 10
                    if (originSpeed != fanSpeed) :
                        result.setdefault('sendTo', currentData['speedChange'])
                        result.setdefault('fanSpeed', fanSpeed)
                        
                        result = str(result).replace("\'", "\"") + "\n"
                        socket.send(bytes(result, encoding = "utf8"))
                        originSpeed = fanSpeed
                        
            elif(currentData['speedChange'] == 'otherArduino') :
                print(calculateLength(currentData['fanLocation']['x'] - currentData['playerLocation']['x'], currentData['fanLocation']['y'] - currentData['playerLocation']['y'], currentData['fanLocation']['z'] - currentData['playerLocation']['z']) / 150)
                fanSpeed = int((1 - (calculateLength(currentData['fanLocation']['x'] - currentData['playerLocation']['x'], currentData['fanLocation']['y'] - currentData['playerLocation']['y'], currentData['fanLocation']['z'] - currentData['playerLocation']['z']) / 150)) * 100)
                
                try :
                    r = R.from_quat([currentData['Quaternions']['x'], currentData['Quaternions']['y'], currentData['Quaternions']['z'], currentData['Quaternions']['w']])
                except Exception as e:
                    print(e)
                    r = R.from_quat([1, 0, 0, 1])
                
                rotationMatrix = r.as_matrix().T
                print(rotationMatrix)
                currentFanLocation = np.array([currentData['fanLocation']['x'], currentData['fanLocation']['y'], currentData['fanLocation']['z']]).T
                newFanLocation = rotationMatrix.dot(currentFanLocation.T)
                
                currentPlayerLocation = np.array([currentData['playerLocation']['x'], currentData['playerLocation']['y'], currentData['playerLocation']['z']])
                newPlayerLocation = rotationMatrix.dot(currentPlayerLocation.T)
                
                print(newFanLocation)
                print(newPlayerLocation)
                
                playerToFanVector = newFanLocation - newPlayerLocation
                print(playerToFanVector)
                
                case = 0
                if(playerToFanVector[2] > 0) :
                
                    if(playerToFanVector[0] >= 0 and playerToFanVector[1] >= 0) :
                        case = 1
                    elif(playerToFanVector[0] <= 0 and playerToFanVector[1] >= 0) :
                        case = 2
                    elif(playerToFanVector[0] <= 0 and playerToFanVector[1] <= 0) :
                        case = 3
                    elif(playerToFanVector[0] >= 0 and playerToFanVector[1] <= 0) :
                        case = 4
                    
                print(case)
                try :
                    if(case == 1):
                        topMovement = getTopLocation(playerToFanVector)
                        rightMovement = getRightLocation(playerToFanVector)
                        print(topMovement)
                        print(rightMovement)
                        if(int(topMovement[0]) <= 20 and int(topMovement[0]) >= -20 and int(topMovement[1]) <= 20 and int(topMovement[1]) >= -20):
                            if(not topFan.hasData) :
                                result = dict()
                                topFan.hasData = True
                                topFan.inputTime = time.time()
                                topFan.fanSpeed = int(fanSpeed)
                                topFan.verticalMove = int(topMovement[1])
                                topFan.parallelMove = int(topMovement[0])
                                
                                result.setdefault('sendTo', 'topArduino')
                                
                                result.setdefault('fanSpeed', int(fanSpeed))
                                result.setdefault('verticalMove', int(topMovement[1]))
                                result.setdefault('parallelMove', int(topMovement[0]))
                                result.setdefault('waterSpary', -1)
                                result = str(result).replace("\'", "\"") + "\n"
                                socket.send(bytes(result, encoding = "utf8"))
                            else :
                                if(topFan.needToChange(fanSpeed, int(topMovement[1]), int(topMovement[0]), time.time())) :
                                                                        
                                    result = dict()
                                    
                                    result.setdefault('sendTo', 'topArduino')
                                    
                                    result.setdefault('fanSpeed', int(fanSpeed))
                                    result.setdefault('verticalMove', int(topMovement[1]))
                                    result.setdefault('parallelMove', int(topMovement[0]))
                                    result.setdefault('waterSpary', -1)
                                    result = str(result).replace("\'", "\"") + "\n"
                                    socket.send(bytes(result, encoding = "utf8"))
                                
                        
                        if(int(rightMovement[0]) <= 20 and int(rightMovement[0]) >= -20 and int(rightMovement[1]) <= 20 and int(rightMovement[1]) >= -20):
                            if(not rightFan.hasData) :
                                result = dict()
                                rightFan.hasData = True
                                rightFan.fanSpeed = int(fanSpeed)
                                rightFan.inputTime = time.time()
                                rightFan.verticalMove = int(rightMovement[1])
                                rightFan.parallelMove = int(rightMovement[0])
                                result.setdefault('sendTo', 'rightArduino')
                                
                                
                                result.setdefault('fanSpeed', int(fanSpeed))
                                result.setdefault('verticalMove', int(rightMovement[1]))
                                result.setdefault('parallelMove', int(rightMovement[0]))
                                result.setdefault('waterSpary', -1)
                                result = str(result).replace("\'", "\"") + "\n"
                                socket.send(bytes(result, encoding = "utf8"))
                            else :
                                if(rightFan.needToChange(fanSpeed, int(rightMovement[1]), int(rightMovement[0]), time.time())) :
                                    result = dict()
                                    result.setdefault('sendTo', 'rightArduino')
                                    
                                    result.setdefault('fanSpeed', int(fanSpeed))
                                    result.setdefault('verticalMove', int(rightMovement[1]))
                                    result.setdefault('parallelMove', int(rightMovement[0]))
                                    result.setdefault('waterSpary', -1)
                                    result = str(result).replace("\'", "\"") + "\n"
                                    socket.send(bytes(result, encoding = "utf8"))
                            
                    elif(case == 2):
                        topMovement = getTopLocation(playerToFanVector)
                        leftMovement = getLeftLocation(playerToFanVector)
                        print(topMovement)
                        print(leftMovement)
                        if(int(topMovement[0]) <= 20 and int(topMovement[0]) >= -20 and int(topMovement[1]) <= 20 and int(topMovement[1] >= -20)):
                            if(not topFan.hasData) :
                                result = dict()
                                topFan.hasData = True
                                topFan.verticalMove = int(topMovement[1])
                                topFan.parallelMove = int(topMovement[0])
                                topFan.fanSpeed = int(fanSpeed)
                                topFan.inputTime = time.time()
                                
                                result.setdefault('sendTo', 'topArduino')
                                
                                result.setdefault('fanSpeed', int(fanSpeed))
                                result.setdefault('verticalMove', int(topMovement[1]))
                                result.setdefault('parallelMove', int(topMovement[0]))
                                result.setdefault('waterSpary', -1)
                                result = str(result).replace("\'", "\"") + "\n"
                                socket.send(bytes(result, encoding = "utf8"))
                            else :
                                if(topFan.needToChange(fanSpeed, int(rightMovement[1]), int(rightMovement[0]), time.time())) :
                                    
                                    result = dict()
                                    result.setdefault('sendTo', 'topArduino')
                                    
                                    result.setdefault('fanSpeed', int(fanSpeed))
                                    result.setdefault('verticalMove', int(topMovement[1]))
                                    result.setdefault('parallelMove', int(topMovement[0]))
                                    result.setdefault('waterSpary', -1)
                                    result = str(result).replace("\'", "\"") + "\n"
                                    socket.send(bytes(result, encoding = "utf8"))
                        
                        if(int(leftMovement[0]) <= 20 and int(leftMovement[0]) >= -20 and int(leftMovement[1]) <= 20 and int(leftMovement[1]) >= -20):
                            if(not leftFan.hasData) :
                                result = dict()
                                leftFan.hasData = True
                                leftFan.fanSpeed = int(fanSpeed)
                                leftFan.inputTime = time.time()
                                leftFan.verticalMove = int(leftMovement[1])
                                leftFan.parallelMove = int(leftMovement[0])
                                
                                result.setdefault('sendTo', 'leftArduino')
                                
                                result.setdefault('fanSpeed', int(fanSpeed))
                                result.setdefault('verticalMove', int(leftMovement[1]))
                                result.setdefault('parallelMove', int(leftMovement[0]))
                                result.setdefault('waterSpary', -1)
                                result = str(result).replace("\'", "\"") + "\n"
                                socket.send(bytes(result, encoding = "utf8"))
                            else :
                                if(leftFan.needToChange(fanSpeed, int(leftMovement[1]), int(leftMovement[0]), time.time())) :
                                    
                                    result = dict()
                                    result.setdefault('sendTo', 'leftArduino')
                                    
                                    result.setdefault('fanSpeed', int(fanSpeed))
                                    result.setdefault('verticalMove', int(leftMovement[1]))
                                    result.setdefault('parallelMove', int(leftMovement[0]))
                                    result.setdefault('waterSpary', -1)
                                    result = str(result).replace("\'", "\"") + "\n"
                                    socket.send(bytes(result, encoding = "utf8"))
                    
                    elif(case == 3):
                        downMovement = getDownLocation(playerToFanVector)
                        leftMovement = getLeftLocation(playerToFanVector)
                        print(downMovement)
                        print(leftMovement)
                        if(int(downMovement[0]) <= 20 and int(downMovement[0]) >= -20 and int(downMovement[1]) <= 20 and int(downMovement[1]) >= -20):
                            if(not downFan.hasData) :
                                result = dict()
                                downFan.hasData = True
                                downFan.fanSpeed = int(fanSpeed)
                                downFan.inputTime = time.time()
                                downFan.verticalMove = int(downMovement[1])
                                downFan.parallelMove = int(downMovement[0])
                                result.setdefault('sendTo', 'downArduino')
                                
                                result.setdefault('fanSpeed', int(fanSpeed))
                                result.setdefault('verticalMove', int(downMovement[1]))
                                result.setdefault('parallelMove', int(downMovement[0]))
                                result.setdefault('waterSpary', -1)
                                result = str(result).replace("\'", "\"") + "\n"
                                socket.send(bytes(result, encoding = "utf8"))
                            else :
                                if(downFan.needToChange(fanSpeed, int(downMovement[1]), int(downMovement[0]), time.time())) :
                                        
                                    result = dict()
                                    result.setdefault('sendTo', 'downArduino')
                                    
                                    result.setdefault('fanSpeed', int(fanSpeed))
                                    result.setdefault('verticalMove', int(downMovement[1]))
                                    result.setdefault('parallelMove', int(downMovement[0]))
                                    result.setdefault('waterSpary', -1)
                                    result = str(result).replace("\'", "\"") + "\n"
                                    socket.send(bytes(result, encoding = "utf8"))
                        
                        if(int(leftMovement[0]) <= 20 and int(leftMovement[0]) >= -20 and int(leftMovement[1]) <= 20 and int(leftMovement[1]) >= -20):
                            if(not leftFan.hasData) :
                                result = dict()
                                leftFan.hasData = True
                                leftFan.fanSpeed = int(fanSpeed)
                                leftFan.inputTime = time.time()
                                leftFan.verticalMove = int(leftMovement[1])
                                leftFan.parallelMove = int(leftMovement[0])
                                
                                result.setdefault('sendTo', 'leftArduino')
                                
                                result.setdefault('fanSpeed', int(fanSpeed))
                                result.setdefault('verticalMove', int(leftMovement[1]))
                                result.setdefault('parallelMove', int(leftMovement[0]))
                                result.setdefault('waterSpary', -1)
                                result = str(result).replace("\'", "\"") + "\n"
                                socket.send(bytes(result, encoding = "utf8"))
                            else :
                                if(leftFan.needToChange(fanSpeed, int(leftMovement[1]), int(leftMovement[0]), time.time())) :
                                    result = dict()
                                    result.setdefault('sendTo', 'leftArduino')
                                    
                                    result.setdefault('fanSpeed', int(fanSpeed))
                                    result.setdefault('verticalMove', int(leftMovement[1]))
                                    result.setdefault('parallelMove', int(leftMovement[0]))
                                    result.setdefault('waterSpary', -1)
                                    result = str(result).replace("\'", "\"") + "\n"
                                    socket.send(bytes(result, encoding = "utf8"))
                            
                    elif(case == 4):
                        downMovement = getDownLocation(playerToFanVector)
                        rightMovement = getRightLocation(playerToFanVector)
                        print(downMovement)
                        print(rightMovement)
                        if(int(downMovement[0]) <= 20 and int(downMovement[0]) >= -20 and int(downMovement[1]) <= 20 and int(downMovement[1]) >= -20):
                            if(not downFan.hasData) :
                                result = dict()
                                downFan.hasData = True
                                downFan.fanSpeed = int(fanSpeed)
                                downFan.inputTime = time.time()
                                downFan.verticalMove = int(downMovement[1])
                                downFan.parallelMove = int(downMovement[0])
                                
                                result.setdefault('sendTo', 'downArduino')
                                
                                result.setdefault('fanSpeed', int(fanSpeed))
                                result.setdefault('verticalMove', int(downMovement[1]))
                                result.setdefault('parallelMove', int(downMovement[0]))
                                result.setdefault('waterSpary', -1)
                                result = str(result).replace("\'", "\"") + "\n"
                                socket.send(bytes(result, encoding = "utf8"))
                            else :
                                if(downFan.needToChange(fanSpeed, int(downMovement[1]), int(downMovement[0]), time.time())) :
                                    result = dict()
                                    result.setdefault('sendTo', 'downArduino')
                                    
                                    result.setdefault('fanSpeed', int(fanSpeed))
                                    result.setdefault('verticalMove', int(downMovement[1]))
                                    result.setdefault('parallelMove', int(downMovement[0]))
                                    result.setdefault('waterSpary', -1)
                                    result = str(result).replace("\'", "\"") + "\n"
                                    socket.send(bytes(result, encoding = "utf8"))
                        
                        if(int(rightMovement[0]) <= 20 and int(rightMovement[0]) >= -20 and int(rightMovement[1]) <= 20 and int(rightMovement[1]) >= -20):
                            if(not rightFan.hasData) :
                                result = dict()
                                rightFan.hasData = True
                                rightFan.fanSpeed = int(fanSpeed)
                                rightFan.inputTime = time.time()
                                rightFan.verticalMove = int(rightMovement[1])
                                rightFan.parallelMove = int(rightMovement[0])
                                result.setdefault('sendTo', 'rightArduino')
                                
                                result.setdefault('fanSpeed', int(fanSpeed))
                                result.setdefault('verticalMove', int(rightMovement[1]))
                                result.setdefault('parallelMove', int(rightMovement[0]))
                                result.setdefault('waterSpary', -1)
                                result = str(result).replace("\'", "\"") + "\n"
                                socket.send(bytes(result, encoding = "utf8"))
                            else :
                                if(rightFan.needToChange(fanSpeed, int(rightMovement[1]), int(rightMovement[0]), time.time())) :
                                    result = dict()
                                    result.setdefault('sendTo', 'rightArduino')
                                    
                                    result.setdefault('fanSpeed', int(fanSpeed))
                                    result.setdefault('verticalMove', int(rightMovement[1]))
                                    result.setdefault('parallelMove', int(rightMovement[0]))
                                    result.setdefault('waterSpary', -1)
                                    result = str(result).replace("\'", "\"") + "\n"
                                    socket.send(bytes(result, encoding = "utf8"))
                except Exception as e:
                    print(e)
                        
def countFanClock(socket):
    while(True) :
        result = dict()
        currentTime = time.time()
        
        if(leftFan.hasData) :
            if(currentTime - leftFan.inputTime > 5) :
                result = leftFan.makeRecoverDict()
                result = str(result).replace("\'", "\"") + "\n"
                socket.send(bytes(result, encoding = "utf8"))
                leftFan.hasData = False
                
        if(rightFan.hasData) :
            if(currentTime - rightFan.inputTime > 5) :
                result = rightFan.makeRecoverDict()
                result = str(result).replace("\'", "\"") + "\n"
                socket.send(bytes(result, encoding = "utf8"))
                rightFan.hasData = False
                print("rightClose")
        
        if(topFan.hasData) :
             if(currentTime - topFan.inputTime > 5) :
                result = topFan.makeRecoverDict()
                result = str(result).replace("\'", "\"") + "\n"
                socket.send(bytes(result, encoding = "utf8"))
                topFan.hasData = False
        
        if(downFan.hasData) :
            if(currentTime - downFan.inputTime > 5) :
                result = downFan.makeRecoverDict()
                result = str(result).replace("\'", "\"") + "\n"
                socket.send(bytes(result, encoding = "utf8"))
                downFan.hasData = False
                
        time.sleep(1)

                
sendThread = threading.Thread(target = job , args = (s,))
sendThread.start()


clockThread = threading.Thread(target = countFanClock, args = (s,))
clockThread.start()


while(True):
    
    indata = str(s.recv(1024), encoding = 'utf-8')
    if len(indata) == 0: # connection closed
        s.close()
        print('server close')
        
    array = json.loads(indata)
    dataQueue.Push(array)
    
    
