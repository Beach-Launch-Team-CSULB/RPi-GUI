import tkinter as tk
from threading import Thread
import time
import smbus
import random
from CANstuff import CanSend, CanRecieve


#runTime for collection
runTime = 5

'start txt file'
num = "123"#input('text file number: ')
file = open("test" + num + ".txt", "w")
file.truncate(0)

'I2C setup'
bus = smbus.SMBus(1)

DEVICE = 0x22
IODIRA = 0x00
IODIRB = 0x01
OLATB = 0x15
OLATA= 0x14
GPIOA = 0x12

bus.write_byte_data(DEVICE, IODIRB, 0x00)
bus.write_byte_data(DEVICE, IODIRA, 0x00)
bus.write_byte_data(DEVICE, OLATB, 0)
bus.write_byte_data(DEVICE, OLATA, 0)



#Sensor and Valve List are Formatted as Name, Xcor, Ycor
#Coordinates are for GUI Placement
SensorList = [
    ['LOx Tank Pressure',2,1,1],
    ['LOx Dome Pressure',3,1,2],
    ['Fuel Tank Pressure',2,4,3],
    ['Fuel Dome Pressure',3,4,4],
    ['COPV Pressure',2,7,5],
    ['Load Cell Total',12,1,6],
    ['Load Cell 1',13,1,7],
    ['Load Cell 2',14,1,8],
    ['Load Cell 3',15,1,9],
    ['TC Ignitor 1',12,4,10],
    ['TC Ignitor 2',13,4,11],
    ['TC Tank Top',12,7,12],
    ['TC Tank Mid',13,7,13],
    ['TC Tank Bottom',14,7,14],
    ['Chamber Pressure 1',9,7,15],
    ['Chamber Pressure 2',10,7,16]
              ]

SensorIDList1 = []
for i in range(round(len(SensorList)/2)):
    SensorIDList1.append(SensorList[i][3])

SensorIDList2 = []
for i in range(round(len(SensorList)/2),len(SensorList)):
    SensorIDList2.append(SensorList[i][3])
    
SensorIDList3 = []
for i in SensorList:
    SensorIDList3.append(i[3])
    
    
pinset1 = OLATB
pinset2 = GPIOA

ValveList = [
    ['LOx Vent',5,1, pinset1,0],
    ['LOx Dome',6,1, pinset1,1],
    ['LOx Dome Vent',7,1, pinset1,2],
    ['Fuel Vent',5,4, pinset1,3],
    ['Fuel Dome',6,4, pinset1,4],
    ['Fuel Dome Vent',7,4, pinset1,5],
    ['High Press',5,7, pinset1,6],
    ['High Vent',6,7, pinset1,7],
    ['MV Fuel',9,4, pinset2,0],
    ['MV LOx',10,4, pinset2,1],
    ['Auto Sequence',1,10, pinset2,2],
    ['Abort',4,10, pinset2,3],
    ]



class Main(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self, bg = "black")
        container.pack(side = "top", fill = "both", expand = True)

        rows = 16
        columns = 10

        for row in range(rows):
            container.grid_rowconfigure(row, weight=1)
        for column in range(columns):
            container.grid_rowconfigure(column, weight=1)

        frame = GUI(container, self)
        frame.config(bg="black")
        frame.grid(row=0, column=int(columns/2), sticky="nsew")
        frame.tkraise()
        
        
class GUI(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self,parent)
        TitleLabel = tk.Label(self, text="Project Renegade",font=("Verdana", 15), fg='white', bg='black').grid(row=0,column=5,padx=10,pady=30)

        self.sensorList = []
        for sensor in SensorList:
            self.sensorList.append(Sensor(self,sensor))

        self.valveList = []
        for valve in ValveList:
            self.valveList.append(Valve(self,valve))
            
        self.RefreshLabel()

    def RefreshLabel(self):
        for sensor in self.sensorList:
            sensor.RefreshLabel()
        self.sensorList[1].ReadingLabel.after(500, self.RefreshLabel)


class Sensor():
    def __init__(self, parent, args):
        self.label = tk.Label(parent, text=args[0],font=("Verdana", 13), fg='white', bg='black').grid(row=args[1],column=args[2],padx=10,pady=10)
        self.ReadingLabel = tk.Label(parent,text = "N/A",font=("Verdana", 13), fg='orange', bg='black')
        self.ReadingLabel.grid(row=args[1], column=(args[2]+1))
        self.SensorID = args[3]
        
    def RefreshLabel(self):
        value = 1#CanRecieve.getVar(self.SensorID)
        self.ReadingLabel.config(text = value)

class Valve():
    
    pinNumSum1 = 0
    pinNumSum2 = 0

    def __init__(self, parent, args):
        self.pinNum = args[4]
        self.i2cPinSet = args[3]
        self.Button = tk.Button(parent, text=args[0],command=lambda: self.ValveActuaction(), font=("Verdana", 13),fg='black', bg='white')
        self.Button.grid(row=args[1], column=args[2])
        self.Status = False
        self.StatusLabel = tk.Label(parent,text = "OFF",font=("Verdana", 13), fg='red', bg='black')
        self.StatusLabel.grid(row=args[1], column=(args[2]+1))
        
    def ValveActuaction(self):
        if not self.Status:
            self.StatusLabel.config(text="ON", fg='green')
            self.Status = True
            if self.i2cPinSet == OLATB:
                Valve.pinNumSum1 += 2**self.pinNum
                pinNumSum = Valve.pinNumSum1
            elif self.i2cPinSet == GPIOA:
                Valve.pinNumSum2 += 2**self.pinNum
                pinNumSum = Valve.pinNumSum2

        else:
            self.StatusLabel.config(text="OFF", fg='red')
            self.Status = False
            if self.i2cPinSet == OLATB:
                Valve.pinNumSum1 -= 2**self.pinNum
                pinNumSum = Valve.pinNumSum1
            elif self.i2cPinSet == GPIOA:
                Valve.pinNumSum2 -= 2**self.pinNum
                pinNumSum = Valve.pinNumSum2
        bus.write_byte_data(DEVICE, self.i2cPinSet, pinNumSum)
        print(pinNumSum)
        
def main():    
    Can1 = CanSend(len(SensorList))
    Can2 = CanRecieve(SensorIDList3)
    #Can3 = CanRecieve(SensorIDList2)
    Can1Thread = Thread(target = Can1.run)
    Can2Thread = Thread(target = Can2.run)
    #Can3Thread = Thread(target = Can3.run)
    Can1Thread.setDaemon(True)
    #Can2Thread.setDaemon(True)

    Can1Thread.start()
    Can2Thread.start()
    #Can3Thread.start()
    ProjectRenegade = Main()
    ProjectRenegade.geometry("1280x720")
    ProjectRenegade.mainloop()
    
       
if __name__ == '__main__':
    main()


        
        
        
        
        
