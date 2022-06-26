import socket
import sys


class ConnectionManager:
    def __init__(self):
        self.sock = None
        self.server_address = ('192.168.100.9', 10000)
        # self.server_address = ('172.20.10.2', 10000)

    def Connect(self):
        # Create a TCP/IP socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening
        print('connecting to %s port %s' % self.server_address)
        self.sock.connect(self.server_address)
        name = 'ghon'
        msg = self.sock.recv(1024)
        if len(msg) > 1:
            # print(msg)
            self.SendMsg(name)
            # self.SendMsg(msg.decode())
            self.SendMsg('a7a')



    def SendMsg(self, message):
        try:

            # Send data
            # message = txt_msg
            print(message)
            self.sock.sendall(message.encode())
            # Du's notes
            # Expect feedback from receiver to confirm that he received msg, otherwise tell sender sending failed


            # Look for the response
            # amount_received = 0
            # amount_expected = len(message)
            #
            # while amount_received < amount_expected:
            #     data = self.sock.recv(100)
            #     amount_received += len(data)
            #     print('received "%s"' % data.decode())

        except:
            print('failed')


    def ReceiveMsg(self):
        print('Waiting for a message from server')
        msg = self.sock.recv(1024).decode()
        if (len(msg) > 1):
            print('RECEIVED: ' + msg)
            return msg

    def Disconnect(self):
        print('closing socket')
        self.sock.close()
