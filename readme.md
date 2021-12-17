# Hassium Server Manager

This is meant to be a tool for *mostly* internal use. I decided that I would make it open souce in case anyone wanted to use it.

# How do I run this app?

All you need to do is install python for your OS. After that you will need pyqt5... the installation for this heavily depends on what OS you use...

## installing pyqt5

On linux, you will need to install a few things from your package manager as well as the package from pip. Tutorials for this can be found online.

a guide can be found [here](https://pythonbasics.org/install-pyqt/)

## installing pyqt5 (Windows)

```shell
py -m pip install pyqt5
```
*`py` might not work on your system. Try `python`,`py3`, or whatever is the command for your system*

# License information

The code written by *me* is all under MIT. Unfortunately pyqt is licensed under GPL V3. This just means that any binary would likely need to be licensed under that GPL license. I do not know the proper law so I will not be releasing any binaries for the time being. Later on we might see some or at the very least a ``setup.py`` file to automatically build one for you