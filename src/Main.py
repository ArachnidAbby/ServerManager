from PyQt5 import QtCore, QtGui, QtWidgets,uic
import re


# overview tab for main window tab bar
class BasicOverViewTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(f"{Settings.DIR}/UIFiles/OverViewTab.ui", self)
        self.show()

# Console tab for main window tab bar.
class BasicConsoleTab(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi(f"{Settings.DIR}/UIFiles/ConsoleTab.ui", self)
        self.show()

#login popup, handles connecting to remote.
class LoginPopup(QtWidgets.QDialog):
    def __init__(self, network):
        super().__init__()
        uic.loadUi(f"{Settings.DIR}/UIFiles/Login_PopUp.ui", self)
        self.RemoteName.addItems(list(Settings.config["Client"]["remotes"].keys()))
        


# Main window, lets the user interact with all other components.
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(f"{Settings.DIR}/UIFiles/mainWindow.ui",self)

        # connect close tab event
        self.Tabs.tabCloseRequested.connect(lambda index: self.Tabs.removeTab(index))
        # connect tree click event
        self.ServerTreeView.itemActivated.connect(lambda item,column: self.openServer(item,column))
    
    def openServer(self, item,column):
        '''opens a tab based on what tree item you press.'''
        if item.data(0,0)=="Overview":
            self.Tabs.addTab(BasicOverViewTab(),f"{self.getServerName(item.parent().data(0,0))}: Overview")
        elif item.data(0,0)=="Console":
            self.Tabs.addTab(BasicConsoleTab(),f"{self.getServerName(item.parent().data(0,0))}: Console")
    
    def getServerName(self,text):
        '''Gets the name of a server from its name on the tree.'''
        pattern = re.compile("(\[Online\] )|(\[Offline\] )")
        text = pattern.sub("",text)
        return text[0].upper()+text[1::]

class ServerManagerApplication(QtWidgets.QApplication):
    def __init__(self, *args):
        super().__init__(*args)
        self.popup = LoginPopup(None)
        self.popup.show()
        self.popup.finished.connect(lambda: self.openMain()) #opens the main window once popup is finished
    
    def openMain(self):
        self.main = MainWindow()
        self.main.show()
        self.thread = Client.connection("localhost:8088")
        self.thread.start()



if __name__ == "__main__":
    try:
        import sys
        import Settings
        import Client # must import settings first for error handling
        args = sys.argv
        if "--server" not in args:
            app = ServerManagerApplication(sys.argv)
            # HassiumServerManager = MainWindow()
            # HassiumServerManager.show()
            sys.exit(app.exec_())
        else:
            import Server
            s = Server.Server()
            s.run()
            Server.createNewLog() # archive log when server turns off.
    except Exception as ex:
        import Error
        Error.err(ex)