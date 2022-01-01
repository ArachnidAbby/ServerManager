from PyQt5 import QtCore, QtGui, QtWidgets,uic
import sys,os, traceback

# debug variable changes whether or not we use detailed error logging.
DEBUG = False # boolean (True/False)

class AppError(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(f"{os.path.dirname(os.path.realpath(__file__))}/UIFiles/Exception_PopUp.ui",self)
        self.finished.connect(lambda: quit())
        self.show()

def err(ex):
    app = QtWidgets.QApplication(sys.argv)
    e = AppError()
    if DEBUG:
        e.label.setText(traceback.format_exc())
    else:
        e.label.setText(str(ex))
    sys.exit(app.exec_())