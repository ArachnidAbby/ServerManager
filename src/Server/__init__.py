from . import Console, Packets
import socket, threading, os, tarfile
import queue, datetime, traceback
import Settings

class Connection:
    def __init__(self, conn, addr, server):
        self.conn = conn
        self.addr = addr
        self.server = server

    def run(self):
        while True:
            try:
                data = Packets.recvPacket(self.conn)
                self.server.print(Console.INFO, data.content)
            except Exception:
                break
        self.__del__()

    
    def __del__(self):
        try:
            self.server.print(Console.INFO,f"Closing connection: {self.addr}")
            self.server.lockedConnectionClose(self.addr)
            self.conn.close()
        except Exception as ex:
            self.server.print(Console.WARNING,f"Error ocurred while closing connection: {self.addr} (1/2)")
            self.server.print(Console.ERROR,f"(2/2) {self.addr}'s Error: {traceback.format_exc()}")

class Server:
    def __init__(self):
        self.HOST = Settings.config["Server"]["host"]
        self.PORT = Settings.config["Server"]["port"]

        self.connections = {}

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.HOST, int(self.PORT)))
        self.queue = queue.Queue()

        self.conThread = threading.Thread(target=self.consoleThread,name="Console Thread", daemon=True)


    def run(self):
        self.connectionsLock = threading.Lock() # many threads will attempt to delete values when their connection closes
        self.conThread.start()
        self.print(Console.INFO,"Starting HSM Server")
        while True:
            try:
                self.sock.listen()
                conn, addr = self.sock.accept()
                conn.settimeout(60*60*2)
                client = Connection(conn, addr, self)
                thread = threading.Thread(target=client.run, name=f"client-{addr}", daemon=True)
                with self.connectionsLock:
                    self.connections[addr] = [client,thread]

                self.print(Console.INFO,f"Connection[{len(self.connections.keys())}] has been made, {addr}")
                thread.start()
            except KeyboardInterrupt:
                #del self.connections
                if self.sock:
                    self.sock.close()
                break

    def lockedConnectionClose(self, addr):
        with self.connectionsLock:
            if addr in self.connections.keys():
                del self.connections[addr]


    def consoleThread(self):
        while True:
            changes = []
            while not self.queue.empty():
                item = self.queue.get()
                changes.append(item)
                print(item)
            with open(f"{Settings.DIR}/logs/latest.log",'a+') as f:
                f.write(('\r\n'*(len(changes)>0))+'\r\n'.join(changes))
    
    def print(self, level, message):
        x = datetime.datetime.now()
        day = x.strftime('%Y-%m-%d %H:%M:%S')
        msg = f"{Console.Colors.GREEN}[{day}]{level} {message}"
        self.queue.put(msg)

def createNewLog():
    if not "latest.log" in os.listdir(f"{Settings.DIR}/logs"):
        return None
    count = len(os.listdir(f"{Settings.DIR}/logs"))
    with tarfile.open(f"{Settings.DIR}/logs/{count}.tar.gz",'w:gz') as tar:
        tar.add(f"{Settings.DIR}/logs/latest.log",arcname="latest.log")
    os.remove(f"{Settings.DIR}/logs/latest.log")