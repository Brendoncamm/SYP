import socket
import os
import binascii
from subprocess import check_output

s = socket.socket()
#host = '192.168.0.10'# IP of Server (PI?)
host = check_output(['hostname', '-I']).strip() #Strip to remove newline char
port = 12345
s.bind((host, port))

s.listen(5)
while True:
  print('waiting for receive')
  c, addr = s.accept()
  data=bytes(c.recv(1024))
  print(len(data))
  #os.system('clear')
  #c.close()
