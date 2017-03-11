# GuiMatrixClient.py - Server client used to interface with the PI.

import socket, sys, pickle, time

class GuiMatrixClient():
    def __init__(self):
        self.HOST = 'localhost'
        # self.HOST = '192.168.2.201'
        self.PORT = 1000
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((self.HOST, self.PORT))

    def getPickleObject(self, infile):
        buf = b''
        while True:
            line = infile.readline()
            if not line:
                continue
            buf += line
            if line.endswith(str.encode('.\n')):
                return pickle.loads(buf)

    def getDataValues(self):
        try:
            filehandle = self.clientsocket.makefile(mode='rb')
            return self.getPickleObject(filehandle)

        except KeyboardInterrupt:
            print("closing...")
            self.clientsocket.close()

    def closeConnection(self):
        print("closing...")
        self.clientsocket.close()


    def getDataAndType(self):
        obj = self.getDataValues()
        if type(obj) == list:
            print('We got a list!')
            return list, obj
        elif obj.isalpha():
            print('We got a username.', obj)
            return str, obj
        else:
            print('We got a float', obj)
            return float, float(obj)

if __name__ == "__main__":
    client = GuiMatrixClient()

    while True:
        obj_type, value = client.getDataAndType()
        if value == '':
            continue
        elif value == 'quit':
            break
        time.sleep(1)

print("Connection closed.")
client.closeConnection()

