import socket
import os

s = socket.socket()
host = '192.168.0.10'# IP of Server (PI?)
port = 12345
s.bind((host, port))

s.listen(5)
while True:
  c, addr = s.accept()
  data=c.recv(1024)
  print(data)
  os.system('clear')
  c.close()

