import socket
s = socket.socket()
host = socket.gethostname()
port = 1247
s.bind((host,port))
s.listen(5)
while True:
    c, addr = s.accept()
    print("Connection accepted from\n" + repr(addr[1]))

    #c.send("Server accepted connection\n")
    #print(repr(addr[1]) + ": " + c.recv(1026))
    c.close()
