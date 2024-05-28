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
        self.__accel_x = []
        
    def getAccel_X(self):
        if len(self.__accel_x) == 0:
            key = list(self.__raw_data.keys())[0]
            print(f"key={key}, type={type(key)}")
            #self.__accel_x = self.__raw_data[key]['sensors'][0]['data'][0]
            print (self.__raw_data[key]['sensors'][0]['data'][0])
            print(self.__raw_data[key]['sensors'][1]['data'][0])
            self.__accel_x = [ sensors['data'][0] for sensors in self.__raw_data[key]['sensors'] ]
        return self.__accel_x
    
if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    filename = "accel_test_01.log"
    accel_log = read_log(filename)
    accel_data = accelData(process_accel_log(accel_log))
    
    #print (accel_data)
    data1 = accel_data.getAccel_X()
    print(data1[:3])
    fig, axs = plt.subplots(1, 2, figsize=(5, 2.7), layout='constrained')
    xdata = np.arange(len(data1))  # make an ordinal for this
    #data = 10**data1
    axs[0].plot(xdata, data1)
    