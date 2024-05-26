import time
from mpu9250_jmdev.registers import *
from mpu9250_jmdev.mpu_9250 import MPU9250
import logging
import math

#import numpy as np
#import matplotlib.pyplot as plt

# Create an MPU9250 instance
mpu = MPU9250(
    address_ak=AK8963_ADDRESS,
    address_mpu_master=MPU9050_ADDRESS_68,  # In case the MPU9250 is connected to another I2C device
    address_mpu_slave=None,
    bus=1,
    gfs=GFS_1000,
    afs=AFS_8G,
    mfs=AK8963_BIT_16,
    mode=AK8963_MODE_C100HZ)

# Configure the MPU9250
mpu.configure()

g_xyz = [0,0,0]
count = 0
g_acum = 0

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

while True:
    # Read the accelerometer, gyroscope, and magnetometer values
    accel_data = mpu.readAccelerometerMaster()
    gyro_data = mpu.readGyroscopeMaster()
    mag_data = mpu.readMagnetometerMaster()

    # Print the sensor values
    #print("Accelerometer:", accel_data)
    #print("Gyroscope:", gyro_data)
    #print("Magnetometer:", mag_data)

    g_acum = 0
    dat = []
    for a in accel_data:
        g_acum = g_acum + a*a
        dat.append("{:.4f}".format(a))

    dat.append("{:.4f}".format(g_acum))

    for a in gyro_data:
        dat.append("{:.4f}".format(a))

    for a in mag_data:
        dat.append("{:.4f}".format(a))

    g_abs = math.sqrt(g_acum)
    g_norm = []

    if g_acum == 0:
      continue

    for a in accel_data:
        g_norm.append(a/g_abs)
    #factor = math.sqrt(
    cos_theta = g_norm[2]
    sin_theta = math.sqrt(1-cos_theta*cos_theta)

    cos_phi = g_norm[0] / sin_theta
    sin_phi = g_norm[1] / sin_theta

    try:
      theta = 180*math.acos(cos_theta)/math.pi
      phi_cos = 180*math.acos(cos_phi)/math.pi
      phi_sin = 180*math.asin(sin_phi)/math.pi
    except OSError as err:
      logging.info("OS error:", err)
      logging.info(f"{cos_theta},{cos_phi},{sin_phi}")
    except ValueError:
      logging.info("Could not convert data to an integer.")
    except Exception as err:
      logging.info(f"Unexpected {err=}, {type(err)=}")

    ang = ["{:.4f}".format(theta), "{:.4f}".format(phi_cos), "{:.4f}".format(phi_sin)]
    dat.append(ang)

    #for i in range(3):
    #    g_xyz[i] = g_xyz[i] + accel_data[i]

    #logging.info(f"{accel_data}, {g_acum}, {gyro_data}, {mag_data}")
    logging.info(dat)

    #count = count + 1
    #if count >= 10:
    #    for i in range(3):
    #        g_xyz[i] = g_xyz[i] / count

        #print(accel_data, g_acum, gyro_data, mag_data)
    #    g_acum = g_acum / count
    #    logging.info(f"{g_xyz}, {g_acum}, {gyro_data}, {mag_data}")
    #    g_xyz = [0,0,0]
    #    g_acum = 0
    #    count = 0

    # Wait for 1 second before the next reading
    time.sleep(2)
