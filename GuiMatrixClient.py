# GuiMatrixClient.py - Server client used to interface with the PI.

import socket, sys, pickle, time, json

class GuiMatrixClient():
    def __init__(self):
        self.HOST = 'localhost'
        self.HOST = '192.168.2.201'
        self.PORT = 1000
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((self.HOST, self.PORT))
        self.filehandle = self.clientsocket.makefile(mode='r')


    def getDataValues(self):
        try:
            while True:
                line = self.filehandle.readline()
                if line:
                    break
                time.sleep(0.0001)

            #print("decoding: %s"%(line))
            #print("Packet of length %d bytes recvd"%(len(line)))
            return json.loads(line)

        except KeyboardInterrupt:
            print("closing...")
            self.clientsocket.close()

    def closeConnection(self):
        print("closing...")
        self.clientsocket.close()


    def getDataAndType(self):
        return self.getDataValues()


if __name__ == "__main__":
    client = GuiMatrixClient()

    while True:
        obj_type, value = client.getDataAndType()
        if value == '':
            continue
        elif value == 'quit':
            break
        time.sleep(0.0001)

    print("Connection closed.")
    client.closeConnection()

