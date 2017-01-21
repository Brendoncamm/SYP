import socket
import os
import binascii
import arduino
from subprocess import check_output

controller = Arduino_Controller(0x08)

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
  controller.write(data)
  print(len(data))
  #os.system('clear')
  #c.close()
