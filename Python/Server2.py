import socketserver
import sys
import arduino
import threading
import queue
from pickle import dumps as serialize
from subprocess import check_output

class SerialRequestHandler(threading.Thread):
    """
    Thread object for handling the serial bus connection.  When the arduino controller writes to the serial bus to
    signal    that it is ready for control data, the thread clears the serial bus and then writes the current state from
    the queue it was initialized with.

    :param stateq: Queue object for holding control state.  The queue should be of size one.  It is being used for
    its multi-thread implementation over its properties as a queue.
    """
    def __init__(self, stateq):
        """
        Initialize thread object.
        """
        super(self.__class__, self).__init__()
        self.stateq = stateq

    def run(self):
        """
        Creates object for handling the serial bus to the arduino and then writes to it when signaled to.
        """
        sbus = arduino.Arduino_Controller(9600)
        while True:
            ready = sbus.ready()
            if ready:
                sbus.serial_bus.read(ready)
                sbus.serial_bus.write(self.stateq.get())


class QuadControlHandler(socketserver.BaseRequestHandler):
    """
    Request handler that puts 16 received bytes into the queue for the SerialRequestHandler.

    :param request: Inherited from BaseRequestHandler
    :param client_address: Inherited from BaseRequestHandler
    :param server: Inherited from BaseRequestHandler
    :param stateq: Threading queue object of size 1.
    """
    def __init__(self, request, client_address, server, stateq):
        """
        Initialize request handler.
        """
        self.stateq = stateq
        super(self.__class__, self).__init__(request, client_address, server)
        return

    def handle(self):
        """
        Handles connection.  If queue is full it empties it, then reads the received bytestring to the queue.
        """
        if self.stateq.full():
            self.stateq.get() #Queue has size of 1, if full clear for new state
        recv = self.request.recv(16)
        self.stateq.put(recv)
        print('Received: ' + str(recv))
        return

class QuadControlServer(socketserver.UDPServer):
    """
    Handles UDP datagrams containing 16 Bytes

    :param server_address: Inherited from UDPServer, a tuple of (Address, Port)
    :param RequestHandlerClass: Should be QuadControlHandler
    """
    def __init__(self, server_address, RequestHandlerClass):
        """
        Initialize controller.
        """
        super(self.__class__, self).__init__(server_address, RequestHandlerClass)
        self.stateq = queue.Queue(1)
        return

    def serve_forever(self, poll_interval=0.5):
        """
        Overridden from UDPServer, added creating of SerialRequestHandler and start of that thread.
        """
        thread = SerialRequestHandler(self.stateq)
        thread.start()
        super(self.__class__, self).serve_forever(poll_interval)
        return

    def finish_request(self, request, client_address):
        """
        Overriden from UDPServer.  Adds passing queue to the request handler.
        """
        self.RequestHandlerClass(request, client_address, self, self.stateq)

class FeedbackCommHandler(socketserver.BaseRequestHandler):
    """
    Handles data requests from the GUI.
    """
    def __init__(self, request, client_address, server, data):
        """
        Overridden to bring datadictionary to request handler.
        """
        self.DataDictionary = data
        super(self.__class__, self).__init__(request, client_address, server)

    def handle(self):
        """
        Pickles datadictionary and sends it as a response.
        """
        byte_string = serialize(self.DataDictionary)
        self.request.send_all(byte_string)

class CommunicationServer(socketserver.TCPServer):
    """
    Server inherited from TCPServer, handles request for data as well as acquiring data.  Periodically runs functions
    from a list of DataFunctions and appends their returned values/object to a list of data.

    :param server_address: Inherited from UDPServer, a tuple of (Address, Port)
    :param RequestHandlerClass: Should be FeedbackComHandler
    :param DataFuntions:  A list of functions that acquire data.
    """
    def __init__(self, server_address, RequestHandlerClass, DataFuntions):
        """
        Initializes server.
        """
        self.DataFunctions = DataFuntions
        self.DataDictionary = {}
        for x in self.DataFunctions:
            self.DataDictionary[x[0]] = {'name' : x[0],
                                         'function' : x[1],
                                         'data' : []
                                        }
        super(self.__class__, self).__init__(server_address, RequestHandlerClass)

    def service_actions(self):
        """
        Iterates through list of functions in self.DataFunctions and records them in the corresponding dictionary within
        self.DataDictionary.
        """
        for x in self.DataDictionary:
            x['data'].append(x['function']())

    def finish_request(self, request, client_address):
        """
        Overriden from TCPServer.  Adds passing data to the request handler.
        """
        self.RequestHandlerClass(request, client_address, self, self.DataDictionary)

if __name__ == '__main__':
    if sys.version_info[0] < 3:
        raise Exception('Version Error', 'Not compatible with Python version 2')

    HOST = check_output(['hostname', '-I']).strip()
    CONTROL_PORT = 2222
    COMMS_PORT = 4444

    test_serv = QuadControlServer((HOST, CONTROL_PORT), QuadControlHandler)
    test_serv.serve_forever()
