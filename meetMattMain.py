import pickle, time, os
from MeetMattGui import *
from simulateMatrixData import simulateMatrixData


class AThread(QThread):
    ''' Defines a new thread that's used to update the velostat matrix values.
    The thread calls the pySignal object (Communicate) which tirggers the
    setMatrix function.'''

    def __init__(self, c):
        super().__init__()
        self.event = c

    def run(self):
        count = 0
        while count < 5:
            self.event.writeData.emit()
            time.sleep(2)
            count += 1

        self.event.clearData.emit()



class MattGui(Ui_MainWindow):
    def __init__(self, MainWindow):
        super().setupUi(MainWindow)

        self.event = Communicate()
        self.event.writeData.connect(self.setMatrix)
        self.event.clearData.connect(self.clearMatrix)

        self.thread = AThread(self.event)


    def close_application(self):
        self.thread.quit()
        self.thread.wait()
        self.thread = None
        sys.exit()


    def setMatrix(self):

        # state=True
        # while state and not stop_event.isSet():
            # with open('matrixData', 'rb') as fp:
            # values = pickle.load(fp)
        user, weight, values = simulateMatrixData()
        self.lineEdit.setText(user)
        self.lineEdit_2.setText(weight)

        for row in range(29):
            for col in range(43):
                if values[row][col]:
                    self.matrix[row][col].setStyleSheet("QFrame { background-color: green }")
                else:
                    self.matrix[row][col].setStyleSheet("QFrame { background-color: rgb(236,236,236)}")

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


