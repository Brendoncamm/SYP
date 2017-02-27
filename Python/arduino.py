# Test script for writing too serial bus.
# For test purposes, assuming target address is 0x08
# 2017-01-13 Auth: Dylan

import serial

class Arduino_Controller(object):
    #  Provides a wrapper for communicating with the Arduino over I2C/SMBUS.
    def __init__(self, baud):
        self.baudrate = baud
        self.serial_bus = serial.Serial('/dev/ttyACM0', self.baudrate)

    def write_axes(self, axes):
        self.serial_bus.write(axes)

    def write_button(self, button):
        pass
