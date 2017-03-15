import socketserver
import sys
import arduino
import threading
import queue
from subprocess import check_output

#TODO:
#   Control Side
#       Write Server w/ logging
#       Test
#   Backchannel
#       Write Handler
#       Test
#   Read
#       TCP Binding

class SerialRequestHandler(threading.Thread):
    def __init__(self, stateq):
        super(self.__class__, self).__init__()
        self.stateq = stateq

    def run(self):
        #TODO: Add poison pill to exit thread
        sbus = arduino.Arduino_Controller(9600)
        while True:
            ready = sbus.ready()
            if ready:
                sbus.serial_bus.read(ready)
                sbus.write(self.stateq.get())


class QuadControlHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server, stateq):
        self.stateq = stateq
        super(self.__class__, self).__init__(request, client_address, server)
        return

    def handle(self):
        if self.stateq.full():
            self.stateq.get() #Queue has size of 1, if full clear for new state
        recv = self.request.recv(16)
        self.stateq.put(recv)
        print('Received: ' + str(recv))
        return


class QuadControlServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        super(self.__class__, self).__init__(server_address, RequestHandlerClass)
        self.controller = arduino.Arduino_Controller(9600)
        self.stateq = queue.Queue(1)
        return

    def serve_forever(self, poll_interval=0.5):
        thread = SerialRequestHandler(self.stateq)
        thread.start()
        super(self.__class__, self).serve_forever(poll_interval)
        return

    def finish_request(self, request, client_address):
        self.RequestHandlerClass(request, client_address, self, self.stateq)



if __name__ == '__main__':
    if sys.version_info[0] < 3:
        raise Exception('Version Error', 'Not compatible with Python version 2')

    HOST = check_output(['hostname', '-I']).strip()
    CONTROL_PORT = 2222
    COMMS_PORT = 4444

    test_serv = QuadControlServer((HOST, CONTROL_PORT), QuadControlHandler)
    test_serv.serve_forever()
