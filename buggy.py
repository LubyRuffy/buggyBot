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
class buggyBot(object):
    """A buggy that's going to roam over the house. A lot of these will be None."""

    def __init__(self):
        self.start_time
        self.time = None # Start the navigation time
        self.total_time = None # Total time passed
        self.img = None # No image to begin with
        self.img_array = None # Image will also be saved as np array, so no need to convert.
        self.yaw = None # Not yet initialised
        self.pitch = None # Not yet initialised
        self.roll = None # Not yet initialised
        self.vel = None # Not yet initialised
        self.steer = None # Not yet initialised
        self.motor1 = eh.motor.one
        self.motor2 = eh.motor.two
        self.max_vel = 100
        ## Add in address using sudo i2cdetect -y 1
        self.mpu_sensor = mpu6050(## address goes here)
        self.x_acc_ctr = None   ## These will need
        self.y_acc_ctr = None   ## Populating on flat, level
        self.z_acc_ctr = None   ## When stationary.
        self.camera = Picamera()
        self.buggy_vision = np.zeros((160,230,3), dtype = np.float)
        self.world_map = np.zeros((200, 200, 3), dtype = np.float)
        self._img_file = './images/'


    def update(self):
        """ Update buggyBot as time passes."""
        if self.start_time == None:
            self.start_time = time.time()
            self.total_time = 0

            if self.mpu_sensor.read_accel_range not 2:
                self.mpu_sensor.set_aacel_range(ACCEL_RANGE_2G)
            if self.mpu_sensor.read_gyro_range not 250:
                self.mpu_sensor.set_gyro_range(GYRO_RANGE_250DEG)
            self.camera.resolution = (320, 240)
            self.camera.framerate = 24
            self.camera.rotation = 180
        else:
            tot_time = time.time() - self.start_time
            if np.isinfinite(tot_time):
                self.total_time = tot_time
            ## If using an arduino, see `accelArdData.py` for helper code
            mpu_data = self.mpu_sensor.get_all_data()
            ## Output mpu_data to console, for debug
            print(mpu_data)
            mpu_temp = mpu_data[0]
            mpu_accel = mpu_data[1]
            mpu_gyro = mpu_data[2]
            self.pitch = self._calc_pitch(mpu_accel)
            self.roll = self._calc_roll(mpu_accel)
            self.img, self.img_array = self._take_picture()

    def _calc_pitch(self, accel_data):
        """ Calculate pitch angle of buggyBot."""
        x = accel_data["x"]
        y = accel_data["y"]
        z = accel_data["z"]
        denom = np.sqrt(y**2 + z**2)
        return arctan2(x, denom)

    def _calc_roll(self, accel_data):
        """ Calculate roll angle of buggyBot."""
        x = accel_data["x"]
        y = accel_data["y"]
        z = accel_data["z"]
        denom = np.sqrt(x**2 + z**2)
        return arctan2(y, denom)

    def _take_picture():
        """ Take picture as both standard image an np array."""
        timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
        array_out = np.empty((240, 320, 3), dtype=np.uint8)
        self.camera.capture(array_out, 'rgb')
        std_img = self.camera.capture(self._img_file + '{}.jpg'.format(timestamp))
        return std_img, array_out
