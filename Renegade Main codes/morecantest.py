import time
import can
import random
from threading import Thread

class CanRecieve:
    SensorDict = {}
    DataList = []
    var = 0
    
    def __init__(self, SensorIDList):
        self.startTime = time.time()
        self.SensorList = SensorIDList
    
    def getVar(SensorID):
        if SensorID in CanRecieve.SensorDict.keys():
            DataPoint = CanRecieve.DataList[CanRecieve.SensorDict[SensorID]][-1]
        else:
            DataPoint = 0
        return DataPoint
    
    
    def run(self):
        bustype1 = 'socketcan_ctypes'
        channel0 = 'can0'
        channel1 = 'can1'
        samples = 0
        busReceive = can.interface.Bus(channel=channel0, bustype=bustype1)
        while True:
            print('p')
            msgIn = busReceive.recv(timeout = 0.0001)
#             data = str(msgIn)
#             datalist = data.split()
#             SensorID = int(datalist[3])
#             if SensorID not in self.SensorList:
#                 continue
#             if SensorID not in CanRecieve.SensorDict:
#                 CanRecieve.SensorDict[SensorID] = len(CanRecieve.SensorDict)
#                 CanRecieve.DataList.append([])
#             datalist = datalist[7:len(datalist)-2]
#             i = 0
#             for datapoint in datalist:
#                 try:
#                     i+= int(datapoint, 16)
#                 except ValueError:
#                     print(str(datapoint) + "BBBBBBBBBBBBBBBBBBB")
#             CanRecieve.var = i
            #CanRecieve.DataList[CanRecieve.SensorDict[SensorID]].append(17)
            CanRecieve.DataList.append(msgIn)
#             samples += 1
#             if samples %1000 == 0:
#                 print(samples/(time.time()-self.startTime))



Can1 = CanRecieve(5)
Can1.run()



