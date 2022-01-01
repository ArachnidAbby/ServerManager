from PyQt5 import QtCore, QtGui, QtWidgets,uic
import toml
import os

'''
Contains settings and other important globals
Anything done in this file can, and will, affect app functionality. Use src/data/config.toml instead!
'''

# Functions
def makeDefaultConfig():
    if "config.toml" in os.listdir(f"{DIR}/data"):
        return None
    default = """[General]
EncryptionSize = 512 # 512 recommended
HeaderSize = 1024 # 1024>=BlockSize<=3072
BlockSize = 2048 # 1024>=BlockSize<=1048576


[Client]
username = "default"

[Client.remotes]
localhost =  "127.0.0.1:8088"
other     =  "10.0.0.30:8088"


[Server]
adminUsername = "Root"
host = "localhost"
port = 8088
"""
    with open(f"{DIR}/data/config.toml",'w+') as f:
        f.write(default)
    raise RuntimeError("Please edit the config and restart the app!")

# Variables
DIR = os.path.dirname(os.path.realpath(__file__))
config = {}
serverKeys = {}


#Create files and folder that do not exist
os.makedirs(f"{DIR}/data",exist_ok=True)
os.makedirs(f"{DIR}/data/keys",exist_ok=True)
os.makedirs(f"{DIR}/data/serverKeys",exist_ok=True)
os.makedirs(f"{DIR}/logs",exist_ok=True)
makeDefaultConfig()

# open config
with open(f"{DIR}/data/config.toml") as f:
    config = toml.loads(f.read())

# open server keys
keyfiles = os.listdir(f"{DIR}/data/serverKeys")
for x in keyfiles:
    with open(f"{DIR}/data/serverKeys/{x}",'rb') as f:
        serverKeys[x.split(".")[0]] = f.read()

