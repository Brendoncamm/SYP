import socket

s = socket.socket()
host = '192.168.0.192'# IP of Server (PI?)
port = 12345
s.bind((host, port))

s.listen(5)
while True:
  c, addr = s.accept()
  print ('Got connection from',addr)
  c.send('Thank you for connecting')
  c.close()
