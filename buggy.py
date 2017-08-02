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
import smbus
from io import BytesIO, StringIO
import matplotlib.image as mpimg
## Set-up a class that forms the basis for our buggyBot this will allow us to update
## the bot as we go.
class buggBot(object):
    """A buggy that's going to roam over the house. A lot of these will be None."""

    def __init__(self):
        self.time = None # Start the navigation time
        self.total_time = None # Total time passed
        self.img = None # No image to begin with
        self.yaw = None # Not yet initialised
        self.pitch = None # Not yet initialised
        self.roll = None # Not yet initialised
        self.vel = None # Not yet initialised
        self.motor1 = eh.motor.one
        self.motor2 = eh.motor.two
        self.max_vel = 100
        self.buggy_vision = np.zeros((160,230,3), dtype = np.float)
        self.world_map = np.zeros((200, 200, 3), dtype = np.float)
