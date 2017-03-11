# GuiMatrixServer.py - Server class that runs on the pi and is used to transfer
# the matrix data and the user information to the GuiMatrixClient.py file. 

import socket, sys, pickle, time, random
from random import randint
from simulateMatrixData import simulateMatrixData

class MeetMattGUIServer():
    def __init__(self, host='', port=1000):
        self.host = host
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((self.host, self.port))
        self.connection = None

    def waitForIncomingConnection(self):
        self.serversocket.listen(1)
        self.connection, self.client_address = self.serversocket.accept()

    def sendPythonObject(self, obj):
        pickledObject = pickle.dumps(obj)
        self.connection.sendall(pickledObject)
        self.connection.sendall(str.encode('.\n'))

    def cleanup(self):
        if self.connection != None:
            self.connection.close()
        self.serversocket.close()


if __name__ == "__main__":

    server = MeetMattGUIServer()

    try:
        server.waitForIncomingConnection()

        while True:
            inn = input("Send Data")
            if inn  == 'Q':
                break
            if inn == '':
                a, b, testData = simulateMatrixData()

                # Send random information to the client
                testData = [a, b,testData][randint(0,2)]
                server.sendPythonObject(testData)
            else:
                server.sendPythonObject(inn)


    except KeyboardInterrupt:
        print("closing...")
        server.cleanup()

server.sendPythonObject('quit')
print("closing...")
server.cleanup()

