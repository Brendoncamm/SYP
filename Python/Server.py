import socket
import os
import binascii
import RPi.GPIO as gp
from arduino import Arduino_Controller
from subprocess import check_output
import sys

if sys.version_info[0] < 3:
    raise Exception('Lucas','not compatible with Python version 2')

controller = Arduino_Controller(0x08)

#request_pin = 7
Transmit_Begin=""

gp.setmode(gp.BOARD)
gp.setup(request_pin, gp.IN)
last_state = gp.LOW
s = socket.socket()
#host = '192.168.0.10'# IP of Server (PI?)
host = check_output(['hostname', '-I']).strip() #Strip to remove newline char
port = 12345
s.bind((host, port))

s.listen(5)
c, addr = s.accept()
while True:
  #print('waiting for receive')
  #c, addr = s.accept()
  data=bytes(c.recv(16))
  #if gp.input(request_pin) == last_state:
    #last_state = not(last_state)
    
  Transmit_Begin=ser.readline()  
  if Transmit_Begin="xmit"
    controller.write_axes(data)
    print('Writing {0} bytes.'.format(len(data)))
    Transmit_Begin=""
    
  #os.system('clear')
  #c.close()
