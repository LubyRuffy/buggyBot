#!/usr/bin/python3.4

## The following is code that will convert data read, as a string from an
## Arduino, into a python dictionary.
##

import serial
from time import sleep

ser = serial.Serial('/dev/tty.usbserial', 9600)

def read_arduino(flag='1'):
    # Write to serial, as a request for data
    ser.write(flag)
    # Read serial data
    datastring = ser.readline()
    sleep(2)
    # Convert read string to python dict
    datadict = {gx: datalist[:3],  gy: datalist[3:7], gz: datalist[7:]}
    return datadict    
