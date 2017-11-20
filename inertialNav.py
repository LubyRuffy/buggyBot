#!/usr/bin/python3.4

## The following is code that will convert data read, as a string from an
## Arduino, into a python dictionary.
##

from serial import Serial
from time import sleep

class InertialNav(Serial):
    # A device that communicates over serial or USB i.e: Arduino

    # No __init__ required, takes automatically from SerialBase

    def read_imu(self, device):
        # Read serial data
        datalist = str(device.readline(), 'utf-8').rstrip('\r\n').split('\t\t')
        sleep(2)
        # Convert read string to python dict
        datalist = [datalist[i].split(':') for i in range(len(datalist))]
        datadict = {datadict[i][0]: {'X': datadict[i][1], 'Y': datadict[i][2], 
            'Z': datadict[i][3]} for i in range(2)} # Take only Orient and Accel, for now
        return datadict    
