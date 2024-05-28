import logging
import argparse
from datetime import datetime
from time import sleep

import matplotlib.pyplot as plt
import numpy as np


def read_log(filename):
    f = open(filename,"r")
    accel_log = []
    while True:
        if line := f.readline():
            accel_log.append(line)
        else:
             break
    return accel_log


def process_accel_log(accel_log):
    accel_data = {}
    for line in accel_log:
        data = line.rstrip('\r\n').split(',')
        timestamp = data[0]
        if not data[1].isnumeric():
            continue
        ang = data[1]
        
        sensor_data = [ float(x) for x in data[3:] ]
        if ang not in accel_data:
            pwm = data[2]
            accel_data[ang] = {'pwm' : pwm , 'sensors': [{ 'timestamp': timestamp, 'data':sensor_data}]}
        else:
            accel_data[ang]['sensors'].append({ 'timestamp': timestamp, 'data':sensor_data})
        #logging.info(f"{data}")
        #logging.info(f"{accel_data}")
        #sleep(5)
    return accel_data


class accelData:
    def __init__(self, accel_data) -> None:
        self.__raw_data = accel_data
        self.__accel = [[],[],[]]
        self.__accel_proc = [[],[],[]]
        
    def getAccel_Axis(self, axe):
        if len(self.__accel[axe]) == 0:
            key = list(self.__raw_data.keys())[0]
            #print(f"key={key}, type={type(key)}")
            #self.__accel_x = self.__raw_data[key]['sensors'][0]['data'][0]
            #print (self.__raw_data[key]['sensors'][0]['data'][0])
            #print(self.__raw_data[key]['sensors'][1]['data'][0])
            for key in self.__raw_data:
                rawData = [ sensors['data'][axe] for sensors in self.__raw_data[key]['sensors']]
                self.__accel[axe].extend(rawData)
                rawData.sort()
                rawDiff = [ y - x for x,y in zip(rawData[:-1], rawData[1:]) ]
                #rawDiff.sort()
                self.__accel_proc[axe].extend(rawDiff)
        #print("Axe=", axis[:3])
        self.__accel_proc[axe].sort()
        return self.__accel[axe]

    def getAccelProc_Axis(self, axe):
        return self.__accel_proc[axe]
    
            

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    filename = "accel_test_02.log"
    accel_log = read_log(filename)
    accel_data = accelData(process_accel_log(accel_log))
    
    #print (accel_data)
    dataX = accel_data.getAccel_Axis(0)
    dataY = accel_data.getAccel_Axis(1)
    dataZ = accel_data.getAccel_Axis(2)
    
    dataProcX = accel_data.getAccelProc_Axis(0)
    print("pp=", dataProcX)
    dataProcY = accel_data.getAccelProc_Axis(1)
    dataProcZ = accel_data.getAccelProc_Axis(2)
    #print("X=", data1[:3])
    
    fig, axs = plt.subplots(1, 3, figsize=(5, 2.7), layout='constrained')
    xdata = np.arange(len(dataX))  # make an ordinal for this
    xdataProc = np.arange(len(dataProcX))
    #data = 10**data1
    axs[0].plot(xdata, dataX)
    axs[1].plot(xdataProc, dataProcX)
    axs[2].plot(xdata, dataZ)

    plt.show()
    