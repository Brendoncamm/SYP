#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Distributed under terms of the MIT license.

#TODO:
#   rewrite connection for new server
#   test

# import os
# import pprint
import pygame
import socket
import struct
import sys

if sys.version_info[0] < 3:
    raise Exception('Lucas', 'not compatible with Python version 2')


class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None

    def __init__(self, axis_order=[1, 2, 3, 4], hostname='raspberrypi', port=2222, limits = [10, 10, 1, 10]):
        """Initialize the joystick components"""

        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.hostname = hostname
        self.port = port
        self.limits = limits
        if isinstance(axis_order, list):
            self.axis_order = axis_order  # For changing how controller axes are bound
        else:
            raise Exception(TypeError, 'axis_order must be list.')

    def update_axes(self, axis_order):
        self.axis_order = axis_order

    def listen(self):
        """Listen for events to happen"""

        if not self.axis_data:
            self.axis_data = {0: float(0),
                              1: float(0),
                              2: float(0),
                              3: float(0),
                              4: float(-1),
                              5: float(-1)}  # Added explicity number of axes to avoid waiting for input

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)


        # host = '192.168.2.19' #ip of Server (PI)
        host = socket.gethostbyname(self.hostname)  # if fails install samba on pi and reboot

        while True:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    self.axis_data[event.axis] = round(event.value, 2)
                elif event.type == pygame.JOYBUTTONDOWN:
                    self.button_data[event.button] = True
                elif event.type == pygame.JOYBUTTONUP:
                    self.button_data[event.button] = False
                elif event.type == pygame.JOYHATMOTION:
                    self.hat_data[event.hat] = event.value

                # Insert your code on what you would like to happen for each event here!
                # In the current setup, I have the state simply printing out to the screen.

                # Defining Variables to send through the socket to the RPi, need to be strings

                # axis_data=str(self.axis_data)
                # button_data = str(self.button_data)
                # hat_data = str(self.hat_data)

                # Sending Data over a socket to the RPi
                # print(str(self.axis_data))
                # Isolate desired Axes

                axes_data = [self.axis_data[self.axis_order[0]] * self.limits[0],
                             self.axis_data[self.axis_order[1]] * self.limits[1],
                             self.axis_data[self.axis_order[2]] * self.limits[2],
                             self.axis_data[self.axis_order[3]] * self.limits[3]]
                byte_data = []  # To hold the axes data serialized to bytes
                for axis in axes_data:
                    byte_data.append(struct.pack("f", axis))  # F for float

                xmission_bytes = bytes().join(byte_data)
                connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                connection.connect((host, self.port))
                connection.send(xmission_bytes)  # sending the controller data over the port
                connection.close()
                # print(xmission_bytes)

                # os.system('cls')
                # break
                # s.send(button_data)
                # s.send(hat_data)
                # s.close()


if __name__ == "__main__":
    ps4 = PS4Controller()
    # ps4.init()
    ps4.listen()
