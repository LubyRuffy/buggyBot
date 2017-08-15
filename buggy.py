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

class buggyBot():
    """A buggy that's going to roam over the house. A lot of these will be None."""

    def __init__(self):
        self.start_time = None # Start system time
        self.time = None # Start the navigation time
        self.total_time = None # Total time passed
        self.img = None # No image to begin with
        self.img_array = np.empty((240, 320, 3), dtype=np.uint8) # Image will also be saved as np array, so no need to convert.
        self.yaw = None # Not yet initialised
        self.pitch = None # Not yet initialised
        self.roll = None # Not yet initialised
        self.vel = None # Not yet initialised
        self.steer = None # Not yet initialised
        self.motor1 = eh.motor.one
        self.motor2 = eh.motor.two
        self.max_vel = 100
        ## Add in address using sudo i2cdetect -y 1
        self.mpu_sensor = mpu6050(0x68)
        self.x_acc_ctr = None   ## These will need
        self.y_acc_ctr = None   ## Populating on flat, level
        self.z_acc_ctr = None   ## When stationary.
        self.camera = PiCamera()
        self.buggy_vision = np.zeros((160,230,3), dtype = np.float)
        self.world_map = np.zeros((200, 200, 3), dtype = np.float)
        self._img_file = './images/'


    def update(self):
        """ Update buggyBot as time passes."""
        if self.start_time == None:
            self.start_time = time.time()
            self.total_time = 0

            if self.mpu_sensor.read_accel_range != 2:
                self.mpu_sensor.set_accel_range(2)
            if self.mpu_sensor.read_gyro_range != 250:
                self.mpu_sensor.set_gyro_range(250)
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

    def _take_picture(self):
        """ Take picture as both standard image an np array."""
        timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
        array_out = np.empty((240, 320, 3), dtype=np.uint8)
        self.camera.capture(array_out, 'rgb')
        std_img = self.camera.capture(self._img_file + '{}.jpg'.format(timestamp))
        return std_img, array_out

    def forwards(self, speed=100):
        """
        This method is taken straight from the gpiozero library.
        Simply calls the forward method for both motors via explorerhat

        Speed is defaulted to 100, to match explorerhat default.
        """

        self.motor1.forwards(speed)
        self.motor2.forwards(speed)

    def backwards(self, speed=100):
        """
        Again taken from gpiozero, calls explorerhat motor `backwards()`
        method for both motors.

        speed is again set to 100, as per the explorerhat default.
        """

        self.motor1.backwards(speed)
        self.motor2.backwards(speed)

    def stop(self):
        """
        Calls speed = 0 on both motors, via the explorerhat
        `motor.stop()` method.
        """
        self.motor1.stop()
        self.motor2.stop()
    
    ## These following methods will need to be augmented
    ## with either an internal or external function to
    ## match a required heading, once an integrated
    ## heading sensor has been installed.

    ## Can be used 'as is' for an RC solution.

    def turn_left(self, speed=100):
        """
        Call motor methods in opposite directions,
        in order to turn left.

        left backwards, right forwards. same speed.
        """
        self.motor1.backwards(speed)
        self.motor2.forwards(speed)

    def turn_right(self, speed=100):
        """
        As before, opposite direction.
        """
        self.motor1.forwards(speed)
        self.motor2.backwards(speed)
