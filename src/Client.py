from PyQt5 import QtCore
import socket, json
import Server, datetime

class connection(QtCore.QThread):
    #slots
    recieve = QtCore.pyqtSignal(Server.Packets.recvPacket)

    def __init__(self,server):
        super().__init__()
        self.HOST,self.PORT = server.split(':')
        #self.run()
    
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.HOST,int(self.PORT)))
            content = json.dumps({
                "user" : "taustin",
                "sample" : "Handshake"
            })
            jj = Server.Packets.packet("GET",content.encode())
            jj.send(sock)
            p = Server.Packets.recvPacket(sock)
            self.recieve.emit(p)


    # def __del__(self):
    #     self.sock.close()