#!/usr/bin/python3

#####################################################################################
##                                  imu.py                                     ##
##                                                                                 ##
## This is a test script taken from:                                               ##
## http://blog.bitify.co.uk/2013/11/reading-data-from-mpu-6050-on-raspberry.html   ##
## and transposed into python3 (Adding brackets to `print` statements)             ##
## Pieces of this code will be used to form an update method for the buggy class   ##
## in buggy.py                                                                     ##
## I am using an MPU 6500 which, I know, can carry out Digital Motion Processing.  ##
##          ....I need to learn how to use that data fully...                      ##
#####################################################################################

import smbus
import math

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

## Get gyro data
def get_gyro_data():
    gyro_x = read_word_2c(0x43)
    gyro_y = read_word_2c(0x45)
    gyro_z = read_word_2c(0x47)
    return  gyro_x, gyro_y, gyro_z

##print("gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131))
##print("gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131))
##print("gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131))

def get_accel_data():
    accel_x = read_word_2c(0x3b)
    accel_y = read_word_2c(0x3d)
    accel_z = read_word_2c(0x3f)
    return accel_x, accel_y, accel_z

#accel_xout_scaled = accel_xout / 16384.0
#accel_yout_scaled = accel_yout / 16384.0
#accel_zout_scaled = accel_zout / 16384.0

# print("accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled)
# print("accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled)
# print("accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled)

# print("x rotation: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))
# print("y rotation: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled))