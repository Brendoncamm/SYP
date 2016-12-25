import socket               

s = socket.socket()        
host = '192.168.0.191' #ip of Server (PI)?
port = 12345               
s.connect((host, port))
print(s.recv(1024))
s.close()
