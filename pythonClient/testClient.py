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
                r = R.from_quat([currentData['Quaternions']['x'], currentData['Quaternions']['y'], currentData['Quaternions']['z'], currentData['Quaternions']['w']])
                rotationMatrix = inv(r.as_matrix())
                newXAxis = rotationMatrix.dot(np.array([1, 0, 0]).T)
                newYAxis = rotationMatrix.dot(np.array([0, 1, 0]).T)
                newZAxis = rotationMatrix.dot(np.array([0, 0, 1]).T)
                BMatrix = np.column_stack([list(newXAxis), list(newYAxis), list(newZAxis)]).T
                currentFanLocation = np.array([currentData['fanLocation']['x'], currentData['fanLocation']['y'], currentData['fanLocation']['z']]).T
                newFanLocation = np.linalg.inv(BMatrix).dot(currentFanLocation)
                
                fanSpeed = (calculateLength(currentData['fanLocation']['x'] - currentData['currentLocation']['x'], currentData['fanLocation']['y'] - currentData['currentLocation']['y'], currentData['fanLocation']['z'] - currentData['currentLocation']['z']) // 200) * 100
                
                result.setdefault('fanSpeed', fanSpeed)
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

    
