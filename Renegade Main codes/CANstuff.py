import time
import can
import random
from threading import Thread


class Node:
    def __init__(self, msg):
        self.next = None
        self.data = msg


class CanSend:
    def __init__(self, numSensors):
        self.numSensors = numSensors
        self.startTime = time.time()

    def run(self):
        bustype1 = 'socketcan_ctypes'
        channel0 = 'can0'
        channel1 = 'can1'
        samples = 0
        """:param id: Spam the bus with messages including the data id."""
        bus = can.interface.Bus(channel=channel1, bustype=bustype1, bitrate = 1000000)
        var = str(7)
        sensorID = '0x' + var
        while True:
#             for i in range(self.numSensors):
#             var = str(i+1)
#             sensorID = '0x' + var
#                 msg = can.Message(arbitration_id=int(sensorID,16), data=[random.randint(1,50),random.randint(1,50),random.randint(1,50),random.randint(1,50)], is_extended_id=False)
#                 try:
#                     bus.send(msg)
#                 except can.CanError:
#                     print("Error caught")
#                     bus.flush_tx_buffer()
#                     bus = can.interface.Bus(channel=channel1, bustype=bustype1)

            msg = can.Message(arbitration_id=int(sensorID,16), data=[random.randint(1,50),random.randint(1,50),random.randint(1,50),random.randint(1,50),random.randint(1,50),random.randint(1,50),random.randint(1,50),random.randint(1,50)], is_extended_id=False)
            try:
                bus.send(msg)
#                 samples += 1
#                 if samples %1000 == 0:
#                     print(samples/(time.time()-self.startTime))
            except can.CanError:
                print("Error caught")
                bus.flush_tx_buffer
                bus = can.interface.Bus(channel=channel1, bustype=bustype1)
#                     
                
    
class CanRecieve:
    SensorDict = {}
    DataList = []
    var = 0
    datastorage = Node('start')
    head = datastorage
    tail = datastorage
    size = 1
    
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
        print('p')
        while True:
            msgIn = busReceive.recv()
            msgIn1 = busReceive.recv()
            msgIn2 = busReceive.recv()
#             data = str(msgIn)
            #msgIn2 = busReceive.recv()
            #msgIn3 = busReceive.recv()

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
#             CanRecieve.DataList[CanRecieve.SensorDict[SensorID]].append(17)
#             time1 = time.time()
#             print(time1-self.startTime)
            CanRecieve.DataList.append(msgIn)
#             time2 = time.time()
#             print(time2-time1)
            CanRecieve.DataList.append(msgIn1)
            CanRecieve.DataList.append(msgIn2)

#             time3 = time.time()
#             print(time2-time3)
#             time.sleep(2)
#             Datapoint = Node(msgIn)
#             CanRecieve.tail.next = Datapoint
#             CanRecieve.tail = Datapoint
#             Datapoint = Node(msgIn1)
#             CanRecieve.tail.next = Datapoint
#             CanRecieve.tail = Datapoint
#             CanRecieve.size +=2
#             

            samples += 3
            if samples %1000 == 0:
                print(samples/(time.time()-self.startTime))



# Can1 = CanSend(5)
# Can1.run()


