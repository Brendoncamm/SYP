#Test script for writing too I2C bus.
#For test purposes, assuming target address is 0x08
# 2017-01-13 Auth: Dylan

import smbus

##bus = smbus.SMBus(1)
##
##DEVICE_ADDRESS = 0x08
##
##test_block = [0x11, 0x22]
##
##bus.write_i2c_block_data(DEVICE_ADDRESS, 0x01, test_block)

class Arduino_Controller(object):
    """
    Provides a wrapper for communicating with the Arduino over I2C/SMBUS.
    """
    def __init__(self, address):
        self.address = address
        self.bus = smbus.SMBus(1)

    def write_axes(self, axes):
	"""Breaks received 16 byte string into list of 4 byte floats.
	Then writes them to the bus.
	"""
    #I2C block data write requires a list, so we will build it from the byte array.
	axis_list = []
	for i in range(0,16,4):
		axis_list.append(axes[i:i+4])
        if type(axis_list) == type(list()):
            print('Created list: writing to bus.')
            self.bus.write_i2c_block_data(self.address, 0x01, axis_list)
        else
            raise TypeError('Failed to create a list, created a {0}'.format(type(axis_list)))

    def write_button(self, button):
        pass
