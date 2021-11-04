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
from numpy.linalg import inv
import math


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
        
@jit(nopython=True)
def calculateLength(x, y, z):
    return ((x * x) + (y * y) + (z * z)) ** (1 / 2)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
dataQueue = Queue()

def getLeftLocation(playerToFanVector):
    OriginPoint = np.array([-30, 28, 30])

    NomalVextor = np.array([1, 0, -1])
    
    Constant = (NomalVextor[0] * OriginPoint[0] + NomalVextor[1] * OriginPoint[1] + NomalVextor[2] * OriginPoint[2]) * -1
    
    multiple = -1 * Constant / (NomalVextor[0] * playerToFanVector[0] + NomalVextor[1] * playerToFanVector[1] + NomalVextor[2] * playerToFanVector[2])
    
    playerToFanVectorWithMult = playerToFanVector * multiple
    
    playerToFanRealLocationIn3D = playerToFanVectorWithMult - OriginPoint
    
    leftBasis = np.array([[1, 0, 1], [0, 1, 0]])

    moveFan = leftBasis.dot(playerToFanRealLocationIn3D.T)
    
    return moveFan

def getRightLocation(playerToFanVector):
    
    OriginPoint = np.array([30, 28, 30])

    NomalVextor = np.array([1, 0, 1])
    
    Constant = (NomalVextor[0] * OriginPoint[0] + NomalVextor[1] * OriginPoint[1] + NomalVextor[2] * OriginPoint[2]) * -1
    
    multiple = -1 * Constant / (NomalVextor[0] * playerToFanVector[0] + NomalVextor[1] * playerToFanVector[1] + NomalVextor[2] * playerToFanVector[2])
    
    playerToFanVectorWithMult = playerToFanVector * multiple
    
    playerToFanRealLocationIn3D = playerToFanVectorWithMult - OriginPoint
    
    leftBasis = np.array([[1, 0, -1], [0, 1, 0]])

    moveFan = leftBasis.dot(playerToFanRealLocationIn3D.T)
    
    return moveFan

def getTopLocation(playerToFanVector):
    
    OriginPoint = np.array([0, 28, 30])

    NomalVextor = np.array([0, 1, 1])
    
    Constant = (NomalVextor[0] * OriginPoint[0] + NomalVextor[1] * OriginPoint[1] + NomalVextor[2] * OriginPoint[2]) * -1
    
    multiple = -1 * Constant / (NomalVextor[0] * playerToFanVector[0] + NomalVextor[1] * playerToFanVector[1] + NomalVextor[2] * playerToFanVector[2])
    
    playerToFanVectorWithMult = playerToFanVector * multiple
    
    playerToFanRealLocationIn3D = playerToFanVectorWithMult - OriginPoint
    
    leftBasis = np.array([[1, 0, 0], [0, 1, -1]])

    moveFan = leftBasis.dot(playerToFanRealLocationIn3D.T)
    
    return moveFan

def getDownLocation(playerToFanVector):
    
    leftOriginPoint = np.array([0, -47, 30])

    leftNomalVextor = np.array([0, 1, -1])
    
    leftConstant = (leftNomalVextor[0] * leftOriginPoint[0] + leftNomalVextor[1] * leftOriginPoint[1] + leftNomalVextor[2] * leftOriginPoint[2]) * -1
    
    multiple = -1 * leftConstant / (leftNomalVextor[0] * playerToFanVector[0] + leftNomalVextor[1] * playerToFanVector[1] + leftNomalVextor[2] * playerToFanVector[2])
    
    playerToFanVectorWithMult = playerToFanVector * multiple
    
    playerToFanRealLocationIn3D = playerToFanVectorWithMult - leftOriginPoint
    
    leftBasis = np.array([[1, 0, 0], [0, 1, 1]])

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
                
                fanSpeed = (calculateLength(currentData['fanLocation']['x'] - currentData['currentLocation']['x'], currentData['fanLocation']['y'] - currentData['currentLocation']['y'], currentData['fanLocation']['z'] - currentData['currentLocation']['z']) // 200) * 100
                
                
                r = R.from_quat([currentData['Quaternions']['x'], currentData['Quaternions']['y'], currentData['Quaternions']['z'], currentData['Quaternions']['w']])
                rotationMatrix = r.as_matrix()
                currentFanLocation = np.array([currentData['fanLocation']['x'], currentData['fanLocation']['y'], currentData['fanLocation']['z']]).T
                newFanLocation = rotationMatrix.dot(currentFanLocation.T)
                
                currentPlayerLocation = np.array([currentData['playerLocation']['x'], currentData['playerLocation']['y'], currentData['playerLocation']['z']])
                newPlayerLocation = rotationMatrix.dot(currentPlayerLocation.T)
                
                playerToFanVector = newFanLocation - newPlayerLocation
                
                case = 0
                
                if(playerToFanVector[0] >= 0 and playerToFanVector[1] >= 0) :
                    case = 1
                elif(playerToFanVector[0] < 0 and playerToFanVector[1] > 0) :
                    case = 2
                elif(playerToFanVector[0] < 0 and playerToFanVector[1] < 0) :
                    case = 3
                elif(playerToFanVector[0] > 0 and playerToFanVector[1] < 0) :
                    case = 4
                
                if(case == 1):
                    topMovement = getTopLocation(playerToFanVector)
                    rightMovement = getRightLocation(playerToFanVector)
                    
                    if(topMovement[0] <= 20 and topMovement[0] >= -20 and topMovement[1] <= 20 and topMovement[1] >= 20):
                        result = dict()
                        result.setdefault('sendTo', 'topArduino')
                        
                        result.setdefault('fanSpeed', fanSpeed)
                        result.setdefault('verticalMove', topMovement[1])
                        result.setdefault('parallelMove', topMovement[0])
                        result = str(result).replace("\'", "\"") + "\n"
                        socket.send(bytes(result, encoding = "utf8"))
                    
                    if(rightMovement[0] <= 20 and rightMovement[0] >= -20 and rightMovement[1] <= 20 and rightMovement[1] >= 20):
                        result = dict()
                        result.setdefault('sendTo', 'rightArduino')
                        
                        result.setdefault('fanSpeed', fanSpeed)
                        result.setdefault('verticalMove', rightMovement[1])
                        result.setdefault('parallelMove', rightMovement[0])
                        result = str(result).replace("\'", "\"") + "\n"
                        socket.send(bytes(result, encoding = "utf8"))
                        
                elif(case == 2):
                    topMovement = getTopLocation(playerToFanVector)
                    leftMovement = getLeftLocation(playerToFanVector)
                    
                    if(topMovement[0] <= 20 and topMovement[0] >= -20 and topMovement[1] <= 20 and topMovement[1] >= 20):
                        result = dict()
                        result.setdefault('sendTo', 'topArduino')
                        
                        result.setdefault('fanSpeed', fanSpeed)
                        result.setdefault('verticalMove', topMovement[1])
                        result.setdefault('parallelMove', topMovement[0])
                        result = str(result).replace("\'", "\"") + "\n"
                        socket.send(bytes(result, encoding = "utf8"))
                    
                    if(leftMovement[0] <= 20 and leftMovement[0] >= -20 and leftMovement[1] <= 20 and leftMovement[1] >= 20):
                        result = dict()
                        result.setdefault('sendTo', 'leftArduino')
                        
                        result.setdefault('fanSpeed', fanSpeed)
                        result.setdefault('verticalMove', leftMovement[1])
                        result.setdefault('parallelMove', leftMovement[0])
                        result = str(result).replace("\'", "\"") + "\n"
                        socket.send(bytes(result, encoding = "utf8"))
                
                elif(case == 3):
                    downMovement = getDownLocation(playerToFanVector)
                    leftMovement = getLeftLocation(playerToFanVector)
                    
                    if(downMovement[0] <= 20 and downMovement[0] >= -20 and downMovement[1] <= 20 and downMovement[1] >= 20):
                        result = dict()
                        result.setdefault('sendTo', 'downArduino')
                        
                        result.setdefault('fanSpeed', fanSpeed)
                        result.setdefault('verticalMove', downMovement[1])
                        result.setdefault('parallelMove', downMovement[0])
                        result = str(result).replace("\'", "\"") + "\n"
                        socket.send(bytes(result, encoding = "utf8"))
                    
                    if(leftMovement[0] <= 20 and leftMovement[0] >= -20 and leftMovement[1] <= 20 and leftMovement[1] >= 20):
                        result = dict()
                        result.setdefault('sendTo', 'leftArduino')
                        
                        result.setdefault('fanSpeed', fanSpeed)
                        result.setdefault('verticalMove', leftMovement[1])
                        result.setdefault('parallelMove', leftMovement[0])
                        result = str(result).replace("\'", "\"") + "\n"
                        socket.send(bytes(result, encoding = "utf8"))
                        
                elif(case == 4):
                    downMovement = getDownLocation(playerToFanVector)
                    rightMovement = getRightLocation(playerToFanVector)
                    
                    if(downMovement[0] <= 20 and downMovement[0] >= -20 and downMovement[1] <= 20 and downMovement[1] >= 20):
                        result = dict()
                        result.setdefault('sendTo', 'downArduino')
                        
                        result.setdefault('fanSpeed', fanSpeed)
                        result.setdefault('verticalMove', downMovement[1])
                        result.setdefault('parallelMove', downMovement[0])
                        result = str(result).replace("\'", "\"") + "\n"
                        socket.send(bytes(result, encoding = "utf8"))
                    
                    if(rightMovement[0] <= 20 and rightMovement[0] >= -20 and rightMovement[1] <= 20 and rightMovement[1] >= 20):
                        result = dict()
                        result.setdefault('sendTo', 'rightArduino')
                        
                        result.setdefault('fanSpeed', fanSpeed)
                        result.setdefault('verticalMove', rightMovement[1])
                        result.setdefault('parallelMove', rightMovement[0])
                        result = str(result).replace("\'", "\"") + "\n"
                        socket.send(bytes(result, encoding = "utf8"))
                
                
                
                
                
                
sendThread = threading.Thread(target = job , args = (s,))
sendThread.start()

while(True):
    
    indata = str(s.recv(1024), encoding = 'utf-8')
    if len(indata) == 0: # connection closed
        s.close()
        print('server close')
        
    array = json.loads(indata)
    dataQueue.Push(array)

    
