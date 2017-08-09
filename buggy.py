#!/usr/bin/python3.4

#####################################################
##              This is the buggyBot               ##
##   the first robotics Project from dandrews7396  ##
#####################################################

from datetime import datetime
import time
import os
import numpy as np
import explorerhat as eh
import cv2
import scipy
from picamera import PiCamera
from io import BytesIO, StringIO
import matplotlib.image as mpimg
from mpu6050 import mpu6050
## Set-up a class that forms the basis for our buggyBot this will allow us to update
## the bot as we go.
class buggBot(object):
    """A buggy that's going to roam over the house. A lot of these will be None."""

    def __init__(self):
        self.start_time
        self.time = None # Start the navigation time
        self.total_time = None # Total time passed
        self.img = None # No image to begin with
        self.yaw = None # Not yet initialised
        self.pitch = None # Not yet initialised
        self.roll = None # Not yet initialised
        self.vel = None # Not yet initialised
        self.steer = None # Not yet initialised
        self.motor1 = eh.motor.one
        self.motor2 = eh.motor.two
        self.max_vel = 100
        self.mpu_sensor = mpu6050(## address goes here)
        self.x_acc_ctr = None   ## These will need
        self.y_acc_ctr = None   ## Populating on flat, level
        self.z_acc_ctr = None   ## When stationary.
        self.buggy_vision = np.zeros((160,230,3), dtype = np.float)
        self.world_map = np.zeros((200, 200, 3), dtype = np.float)



    def update(self):
        """ Update buggyBot as time passes."""
        if self.start_time == None:
            self.start_time = time.time()
            self.total_time = 0
            if self.mpu_sensor.read_accel_range not 2:
                self.mpu_sensor.set_aacel_range(ACCEL_RANGE_2G)
            if self.mpu_sensor.read_gyro_range not 250:
                self.mpu_sensor.set_gyro_range(GYRO_RANGE_250DEG)
        else:
            tot_time = time.time() - self.start_time
            if np.isinfinite(tot_time):
                self.total_time = tot_time
            mpu_data = self.mpu_sensor.get_all_data()
            ## Output mpu_data to console, for debug
            print(mpu_data)
            mpu_temp = mpu_data[0]
            mpu_accel = mpu_data[1]
            mpu_gyro = mpu_data[2]
