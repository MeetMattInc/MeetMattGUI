import pickle, time, os
from MeetMattGui import *
from simulateMatrixData import simulateMatrixData
from GuiMatrixClient import *

obj_type = ''
value = ''
runThread = True

class AThread(QThread):
    ''' Defines a new thread that's used to update the velostat matrix values.
    The thread calls the pySignal object (Communicate) which tirggers the
    setMatrix function.'''

    def __init__(self, event, client):
        super().__init__()
        self.event = event
        self.client = client

    def run(self):
        global obj_type
        global value
        global runThread

        while runThread:
            obj_type, value = self.client.getDataAndType()
            if value == '':
                continue
            # elif value == 'quit':
                # break
            self.event.writeData.emit()
            time.sleep(2)




class MattGui(Ui_MainWindow):
    def __init__(self, MainWindow):
        super().setupUi(MainWindow)

        self.event = Communicate()
        self.event.writeData.connect(self.setMatrix)
        self.event.clearData.connect(self.clearMatrix)
        self.client = GuiMatrixClient()
        self.thread = AThread(self.event, self.client)


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
        global obj_type
        global value
        global runThread

        if obj_type == list:
            print('We got a list!')
            for row in range(29):
                for col in range(43):
                    if value[row][col]:
                        self.matrix[row][col].setStyleSheet("QFrame { background-color: green }")
                    else:
                        self.matrix[row][col].setStyleSheet("QFrame { background-color: rgb(236,236,236)}")
        elif obj_type == str:
            print('We got a string')
            self.lineEdit.setText(value)
        elif obj_type == float:
            print('We got a float')
            self.lineEdit_2.setText(value)
        else:
            print('Its a mystery')
        value = ''
        obj_type = ''

    def clearMatrix(self):

        self.lineEdit.setText('')
        self.lineEdit_2.setText('')

        for row in range(29):
            for col in range(43):
                self.matrix[row][col].setStyleSheet("QFrame { background-color: rgb(236,236,236)}")


    def loopThread(self):
        self.thread.start()
        self.threadDone = False



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


