from PyQt5 import QtCore, QtGui, QtWidgets,uic
import re


class basicOverViewTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/UIFiles/OverViewTab.ui",self)
        self.show()


class basicConsoleTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/UIFiles/ConsoleTab.ui",self)
        self.show()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("src/UIFiles/mainWindow.ui",self)

        # connect close tab event
        self.Tabs.tabCloseRequested.connect(lambda index: self.Tabs.removeTab(index))
        # connect tree click event
        self.ServerTreeView.itemActivated.connect(lambda item,column: self.openServer(item,column))
    
    def openServer(self, item,column):
        '''opens a tab based on what tree item you press.'''
        if item.data(0,0)=="Overview":
            self.Tabs.addTab(basicOverViewTab(),f"{self.getServerName(item.parent().data(0,0))}: Overview")
        elif item.data(0,0)=="Console":
            self.Tabs.addTab(basicConsoleTab(),f"{self.getServerName(item.parent().data(0,0))}: Console")
    
    def getServerName(self,text):
        '''Gets the name of a server from its name on the tree.'''
        pattern = re.compile("(\[Online\] )|(\[Offline\] )")
        text = pattern.sub("",text)
        return text[0].upper()+text[1::]



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    HassiumServerManager = MainWindow()
    HassiumServerManager.show()
    sys.exit(app.exec_())