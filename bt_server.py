#! /usr/bin/python


from bluetooth import BluetoothSocket, RFCOMM, PORT_ANY, SERIAL_PORT_CLASS, SERIAL_PORT_PROFILE, advertise_service
from threading import Thread

config = {
    'backlog': 5,  # max unsuccesful connect attempts
    'uuid': 'a1a738e0-c3b3-11e3-9c1a-0800200c9a66'
}


class BtServer(object):

    def __init__(self, socket=None):
        super(BtServer, self).__init__()
        self.socket = socket

    def start(self):
        print('start called')
        if not self.socket:
            print('non socket, creating one')
            self.socket = BluetoothSocket(RFCOMM)
            # empty host address means this machine
            self.socket.bind(("", PORT_ANY))
            self.socket.listen(config['backlog'])

            advertise_service(
                self.socket,
                "Rewave Server",
                service_id=config['uuid'],
                service_classes=[config['uuid'], SERIAL_PORT_CLASS],
                profiles=[SERIAL_PORT_PROFILE]
            )

        self.port = self.socket.getsockname()[1] # need port for ref.
        self.accept()

    def stop(self):
        print("server stop called")
        self.socket.close()
        try:
            self.client_socket.close()
        except AttributeError as e:
            # in case if no client is connected
            pass

    def recv(self, buffer=2048):
        print('recv called')
        try:
            return self.client_socket.recv(buffer).decode(encoding='UTF-8')
        except UnicodeDecodeError as e:
            # return raw if unable to unicode decode
            return self.client_socket.recv(buffer)

    def send(self, data):
        self.client_socket.send(data)

    def close_connection(self):
        print("close_connection called")
        self.client_socket.close()

    def accept(self):
        # blocking call
        print("accept Called. Waiting for connection on RFCOMM channel", self.port)
        self.client_socket = self.socket.accept()[0] # returns socket, name
