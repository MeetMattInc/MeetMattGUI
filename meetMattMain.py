#!/usr/bin/python3

import pickle, time, os, queue
from MainGui import *
from simulateMatrixData import simulateMatrixData
from GuiMatrixClient import *
import datetime
import VelostatFeatureExtraction as vfe
import scipy.ndimage
import numpy as np

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
        #self.setPriority()

    def run(self):
        global runThread
        global guiUpdatedFlag
        global dataQueue

#self.setPriority(QThread.HighestPriority)

        while runThread:
            while True:
                if dataQueue.empty():
                    #print("Queue is empty")
                    continue
            #print("Emitting signal ",str(datetime.datetime.now()))
                # print("Emitting signal")
                self.event.writeData.emit()
                while not guiUpdatedFlag:
                    continue
                        #print("GUI Updated ",str(datetime.datetime.now()))
                guiUpdatedFlag = False


class DataThread(QThread):
    ''''.'''

    def __init__(self):
        super().__init__()

    def run(self):
        global runThread
        global dataQueue

        self.client = GuiMatrixClient()

#self.setPriority(QThread.LowestPriority)

        while runThread:
            value = self.client.getDataAndType()
           # print("Value:", value)
            if value == '':
                print("Nothing")
                continue
            elif value == None:
                print("None")
                continue
            dataQueue.put((obj_type, value))
            print("Queue backlog %d"%dataQueue.qsize())

        self.client.closeConnection()


class MattGui(Ui_MainWindow):
    def __init__(self, MainWindow):
        super().setupUi(MainWindow)

        self.event = Communicate()
        self.event.writeData.connect(self.setMatrix)
        self.event.clearData.connect(self.clearMatrix)
        self.thread = SignalThread(self.event)
        self.dataThread = DataThread()

    def close_application(self):
        global runThread
        runThread = False

        print("Sending clear signal")
        self.event.clearData.emit()
        self.thread.quit()
        self.thread.wait()
        self.thread = None
        sys.exit()

    def setUser(self, userId):

        if userId == 'u':
            userString = 'Unknown User'
        elif userId == 'a':
            userString = 'Anthony'
        elif userId == 'l':
            userString = 'Lucas'
        elif userId == 't':
            userString = 'Tian'
        elif userId == 'm':
            userString = 'Marc'
        elif userId == 'd':
            userString = 'Detecting ...'
        elif userId == 'n':
            userString = 'No User on Matt'
        else:
            userString = userId
    

        self.userValueLabel.setText(userString)

    def setMatrix(self):
        global guiUpdatedFlag

#print("start ",str(datetime.datetime.now()))
        obj_type, value = dataQueue.get()
        if "velostat" in value:
            print('updating velostat')
            #self.lineEdit_2.setText(str(value["velostat"]))
            pMap = value["velostat"]

            pMapm = np.array(pMap)
            pMap = scipy.ndimage.morphology.binary_erosion(pMap)
            
            (diag, area) = vfe.getDiagonalAndArea(pMap, binaryErosion = False)
            self.diagonalValueLabel.setText("%.2f" % round(diag,2))
            self.areaValueLabel.setText(str(area))
            
            for row in range(29):
                for col in range(43):
                    if pMap[row][col]:
                        self.matrix[row][col].setStyleSheet("QFrame { background-color: green }")
                    else:
                        self.matrix[row][col].setStyleSheet("QFrame { background-color: white }")
        if "user" in  value:
            print('updating user')
            self.setUser(value["user"])
        
        
        if "weight" in value:
            print('updating weight')
            self.weightValueLabel.setText(str(round(value["weight"])))

        value = ''
        obj_type = ''
        guiUpdatedFlag = True
#print("stop ",str(datetime.datetime.now()))

    def clearMatrix(self):
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')

        for row in range(29):
            for col in range(43):
                self.matrix[row][col].setStyleSheet("QFrame { background-color: white }")

    # Starts the thread that updates the GUI values
    def loopThread(self):
        self.thread.start()
        self.dataThread.start()
        self.userValueLabel.setText('No User on Matt')



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


