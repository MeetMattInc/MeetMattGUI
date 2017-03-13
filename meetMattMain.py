#!/usr/bin/python3

import pickle, time, os, queue
from MeetMattGui import *
from simulateMatrixData import simulateMatrixData
from GuiMatrixClient import *

obj_type = ''
value = ''
runThread = True
guiUpdatedFlag = False
dataQueue = queue.Queue()

class SignalThread(QThread):
    ''' Defines a new thread that's used to update the velostat matrix values.
    The thread calls the pySignal object (Communicate) which tirggers the
    setMatrix function.'''

    def __init__(self, event):
        super().__init__()
        self.event = event

    def run(self):
        global runThread
        global guiUpdatedFlag
        global dataQueue

        while runThread:
            while True:
                if dataQueue.empty():
                    # print("Queue is empty")
                    continue
                print("Emitting signal")
                self.event.writeData.emit()
                while not guiUpdatedFlag:
                    continue
                guiUpdatedFlag = False


class DataThread(QThread):
    ''''.'''

    def __init__(self, client):
        super().__init__()
        self.client = client

    def run(self):
        global runThread
        global dataQueue

        while runThread:
            value = self.client.getDataAndType()
            print("Value:", value)
            if value == '':
                print("Nothing")
                continue
            elif value == None:
                print("None")
                continue
            dataQueue.put((obj_type, value))


class MattGui(Ui_MainWindow):
    def __init__(self, MainWindow):
        super().setupUi(MainWindow)

        self.event = Communicate()
        self.event.writeData.connect(self.setMatrix)
        self.event.clearData.connect(self.clearMatrix)
        self.client = GuiMatrixClient()
        self.thread = SignalThread(self.event)
        self.dataThread = DataThread(self.client)

    def close_application(self):
        global runThread
        runThread = False

        print("Sending clear signal")
        self.event.clearData.emit()
        self.client.closeConnection()
        self.thread.quit()
        self.thread.wait()
        self.thread = None
        sys.exit()

    def setMatrix(self):
        global guiUpdatedFlag

        obj_type, value = dataQueue.get()
        if "velostat" in value:
            print('Weight and velostat')
            self.lineEdit_2.setText(str(value["velostat"]))
            for row in range(29):
                for col in range(43):
                    if value["velostat"][row][col]:
                        self.matrix[row][col].setStyleSheet("QFrame { background-color: green }")
                    else:
                        self.matrix[row][col].setStyleSheet("QFrame { background-color: rgb(236,236,236)}")
        if "user" in  value:
            self.lineEdit.setText(value["user"])
        if "wieght" in value:
            self.lineEdit_2.setText(str(value["weight"]))

        value = ''
        obj_type = ''
        guiUpdatedFlag = True


    def clearMatrix(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')

        for row in range(29):
            for col in range(43):
                self.matrix[row][col].setStyleSheet("QFrame { background-color: rgb(236,236,236)}")

    # Starts the thread that updates the GUI values
    def loopThread(self):
        self.thread.start()
        self.dataThread.start()



def main():

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MattGui(MainWindow)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


if __name__ =='__main__':
    main()

    def kill_proc_tree(pid, including_parent=True):
        parent = psutil.Process(pid)
        if including_parent:
            parent.kill()

    me = os.getpid()
    kill_proc_tree(me)


