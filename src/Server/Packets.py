import Settings

class recvPacket:
    def __init__(self,sock, encrypted = False):
        blocksize = Settings.config["General"]["HeaderSize"]
        pp = sock.recv(blocksize).decode()
        self.header = self.decodeHeader(pp)
        self.content = self.recvAll(sock, int(self.header["content-size"]), encrypted = encrypted)
        #print(self.content)
    
    def decodeHeader(self, header: str, encrypted = False) -> dict:
        if header == "":
            return {}
        lines = header.replace(' ','').split('\r\n') # sanitize header for later use
        output = {}
        for x in lines:
            key, value = x.split(':')
            output[key] = value
        return output

    def __getattr__(self, name: str) -> str:
        return self.header[name]
    
    
    def recvAll(self, sock, size: int, encrypted = False):
        remaining = size
        blocksize = Settings.config["General"]["BlockSize"]
        output = b''
        while remaining > 0:
            data = sock.recv(min(remaining,blocksize)) # pick the remaining size or blocksize
            output+=data
            remaining-=len(data)
        return output



class packet:
    def __init__(self, packtype: str, content: str, encrypted = False):
        self.header = {"request-type": packtype}
        self.content = content

    def headerToString(self):
        blocksize = Settings.config["General"]["HeaderSize"]
        output = []
        for key, value in self.header.items():
            output.append(f"{key}: {value}")
        output = '\r\n'.join(output)
        return output + (' ' * (blocksize-len(output)))
        
        
    def send(self,sock):
        self.header["content-size"] = str(len(self.content))
        sock.send(self.headerToString().encode())
        self.sendAll(sock, self.content)

    def sendAll(self, sock, data: str):
        remaining = data
        blocksize = Settings.config["General"]["BlockSize"]
        while len(remaining) > 0:
            sock.send(remaining[:min(len(remaining),blocksize)])
            remaining = remaining[min(len(remaining),blocksize):]