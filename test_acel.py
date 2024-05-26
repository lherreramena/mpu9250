# We imports the GPIO module
import RPi.GPIO as GPIO
# We import the command sleep from time

from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250

from time import sleep

import logging
import argparse
from datetime import datetime


class ServoCtrl:
    def __init__(self) -> None:
        logging.info("Starting Servo ...")
        # Stops all warnings from appearing
        GPIO.setwarnings(False)

        # We name all the pins on BOARD mode
        GPIO.setmode(GPIO.BOARD)
        # Set an output for the PWM Signal
        GPIO.setup(16, GPIO.OUT)

        # Set up the PWM on pin #16 at 50Hz
        self.__pwm = GPIO.PWM(16, 50)
        self.__pwm.start(0) # Start the servo with 0 duty cycle ( at 0 deg position )
        self.__current_ang = 0

    def stop_servo(self):
        self.__pwm.stop(0) # Stop the servo with 0 duty cycle ( at 0 deg position )
        print("Stopped")
        GPIO.cleanup() # Clean up all the ports we've used.

    def move_to(self, ang):
        if ang < -90  or ang > 90:
            return False
        self.__current_ang = ang
        self.__current_pww = 5 + (ang + 90) * 5 / 180 
        self.__pwm.ChangeDutyCycle(self.__current_pww)
        return True
    
    def current_ang(self):
        return self.__current_ang

    def current_pwd(self):
        return self.__current_pww


class Accelerometer:
    def __init__(self) -> None:
        logging.info("Starting Accelerometer ...")
        # Create an MPU9250 instance
        self.__mpu = MPU9250(
            address_ak=AK8963_ADDRESS,
            address_mpu_master=MPU9050_ADDRESS_68,  # In case the MPU9250 is connected to another I2C device
            address_mpu_slave=None,
            bus=1,
            gfs=GFS_1000,
            afs=AFS_8G,
            mfs=AK8963_BIT_16,
            mode=AK8963_MODE_C100HZ)
        # Configure the MPU9250
        self.__mpu.configure()

    def measure_to_str(self, label):
        dt = datetime.now()
        accel_data = self.__mpu.readAccelerometerMaster()
        gyro_data = self.__mpu.readGyroscopeMaster()
        mag_data = self.__mpu.readMagnetometerMaster()
        #time_stamp = datetime.timestamp(dt)
        str =f"{dt}" + "," + label
        for a in accel_data:
            str = str + "," + f"{a}"
        for a in gyro_data:
            str = str + "," + f"{a}"
        for a in mag_data:
            str = str + "," + f"{a}"
        return str
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--ang_ini', type=int, required=False, default=0)
    parser.add_argument('-s', '--ang_step', type=int, required=False, default=10)
    parser.add_argument('-e', '--ang_end', type=int, required=False, default=90)
    parser.add_argument('-n', '--samples', type=int, required=False, default=10)
    parser.add_argument('-t', "--sleep_time", type=float, required=False, default=2.5)

    args = parser.parse_args()

    ang_ini = args.ang_ini
    ang_step = args.ang_step
    ang_stop = args.ang_end
    samples = args.samples
    blank_time = args.sleep_time

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    logging.info("Starting Test Accelerometer ...")

    servo = ServoCtrl()
    sleep(0.2)
    accel = Accelerometer()
    sleep(0.2)
    
    for ang in range(ang_ini, ang_stop + 1, ang_step):
        servo.move_to(ang)
        pwd_val = servo.current_pwd()
        label = f"{ang},{pwd_val}"
        for i in range(samples):
            print(accel.measure_to_str(label))
        sleep(blank_time)
        


